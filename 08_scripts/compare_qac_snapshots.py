#!/usr/bin/env python3
"""QAC kök sayımı denetimi: 1,651 iddiası ile sağlam 1,642 parse sonucunu yeniden üretir.

İki kontrol yapar:
1) 2019'da yayımlanan türetilmiş CSV ile mevcut sabit QAC indeksini karşılaştırır.
2) 2019 yazısındaki shell pipeline'ını QAC ham baytları üzerinde mümkün olduğunca aynen
   taklit ederek görünmeyen satır-sonu/ayraç artefaktlarını ölçer.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
from collections import Counter
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / "03_indices" / "generated" / "root_index.csv"
QAC_RAW = ROOT / "02_morphology" / "qac" / "quranic-corpus-morphology-0.4.txt"
OUT_DIR = ROOT / "03_indices" / "audits"
OLD_COMMIT = "86611929fd5a35220bc46e1944acc69c619aa57b"
OLD_URL = (
    "https://raw.githubusercontent.com/abdulbaqi/quranic_roots/"
    f"{OLD_COMMIT}/quran-morphology-final.csv"
)
ROOT_RE_BYTES = re.compile(br"ROOT:([^|]*)")


def download(url: str) -> bytes:
    req = Request(url, headers={"User-Agent": "quran-offline-corpus/1.0"})
    with urlopen(req, timeout=120) as response:
        return response.read()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_old(data: bytes) -> Counter[str]:
    text = data.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    if "Root" not in (reader.fieldnames or []):
        raise RuntimeError(f"Old CSV has no Root column: {reader.fieldnames}")
    counts: Counter[str] = Counter()
    for row in reader:
        root = (row.get("Root") or "").strip()
        if root and root.lower() not in {"nan", "none", "null"}:
            counts[root] += 1
    return counts


def load_current(path: Path) -> Counter[str]:
    counts: Counter[str] = Counter()
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            root = (row.get("root_bw") or "").strip()
            if root:
                counts[root] = int(row["word_occurrences"])
    return counts


def emulate_2019_shell(path: Path) -> tuple[Counter[bytes], Counter[str], list[dict]]:
    """2019 yazısındaki şu mantığı bayt düzeyinde taklit eder:

    sed 's/\\t/,/g' | cut -d',' -f4 | grep -oE 'ROOT:[^|]*' | cut -d':' -f2

    split(b'\\n') bilinçli olarak CR baytını korur; GNU grep'in CRLF satırlarında
    regex eşleşmesine CR dahil etmesi ihtimalini görünür kılar.
    """
    raw_counts: Counter[bytes] = Counter()
    for line in path.read_bytes().split(b"\n"):
        comma_line = line.replace(b"\t", b",")
        fields = comma_line.split(b",")
        if len(fields) < 4:
            continue
        fourth = fields[3]
        for match in ROOT_RE_BYTES.finditer(fourth):
            root = match.group(1)
            raw_counts[root] += 1

    cleaned_counts: Counter[str] = Counter()
    suspicious: list[dict] = []
    for raw_root, count in sorted(raw_counts.items()):
        cleaned_bytes = raw_root.rstrip(b"\r")
        cleaned = cleaned_bytes.decode("ascii", errors="backslashreplace")
        cleaned_counts[cleaned] += count
        if raw_root != cleaned_bytes:
            suspicious.append({
                "raw_repr": repr(raw_root),
                "cleaned_root": cleaned,
                "count": count,
                "also_exists_without_cr": cleaned_bytes in raw_counts,
            })
    return raw_counts, cleaned_counts, suspicious


def main() -> None:
    if not CURRENT.exists():
        raise SystemExit(f"Current root index missing: {CURRENT}")
    if not QAC_RAW.exists():
        raise SystemExit(f"Raw QAC missing: {QAC_RAW}")

    old_bytes = download(OLD_URL)
    old_counts = load_old(old_bytes)
    current_counts = load_current(CURRENT)
    legacy_raw, legacy_clean, cr_variants = emulate_2019_shell(QAC_RAW)

    old_roots = set(old_counts)
    current_roots = set(current_counts)
    old_only = sorted(old_roots - current_roots)
    current_only = sorted(current_roots - old_roots)
    common = old_roots & current_roots

    changed = [
        {
            "root": root,
            "old": old_counts[root],
            "current": current_counts[root],
            "delta": current_counts[root] - old_counts[root],
        }
        for root in common
        if old_counts[root] != current_counts[root]
    ]
    changed.sort(key=lambda x: (-abs(x["delta"]), x["root"]))

    legacy_clean_roots = set(legacy_clean)
    legacy_missing_vs_current = sorted(current_roots - legacy_clean_roots)
    legacy_extra_vs_current = sorted(legacy_clean_roots - current_roots)

    report = {
        "old_source": {
            "repository": "abdulbaqi/quranic_roots",
            "commit": OLD_COMMIT,
            "path": "quran-morphology-final.csv",
            "url": OLD_URL,
            "sha256": sha256_bytes(old_bytes),
        },
        "current_source": {
            "path": str(CURRENT.relative_to(ROOT)),
            "raw_qac_path": str(QAC_RAW.relative_to(ROOT)),
            "raw_qac_sha256": sha256_bytes(QAC_RAW.read_bytes()),
        },
        "counts": {
            "old_derived_csv_distinct_roots": len(old_roots),
            "current_robust_distinct_roots": len(current_roots),
            "common_roots": len(common),
            "old_only_count": len(old_only),
            "current_only_count": len(current_only),
            "roots_with_frequency_change": len(changed),
            "legacy_shell_distinct_raw_byte_values": len(legacy_raw),
            "legacy_shell_distinct_after_cr_strip": len(legacy_clean_roots),
            "legacy_shell_cr_suffixed_variants": len(cr_variants),
        },
        "old_only": old_only,
        "current_only": current_only,
        "frequency_changes": changed,
        "legacy_shell": {
            "cr_suffixed_variants": cr_variants,
            "missing_vs_current_after_cr_strip": legacy_missing_vs_current,
            "extra_vs_current_after_cr_strip": legacy_extra_vs_current,
        },
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = OUT_DIR / "qac_1651_vs_1642.json"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md: list[str] = []
    md.append("# QAC 1,651 ↔ 1,642 Root Audit\n")
    md.append("This audit separates the actual root set from legacy shell-count artefacts.\n")
    md.append("## Sources\n")
    md.append(f"- 2019 derived CSV: `abdulbaqi/quranic_roots@{OLD_COMMIT}` / `quran-morphology-final.csv`")
    md.append(f"- Old CSV SHA-256: `{report['old_source']['sha256']}`")
    md.append(f"- Current raw QAC SHA-256: `{report['current_source']['raw_qac_sha256']}`\n")
    md.append("## Counts\n")
    for k, v in report["counts"].items():
        md.append(f"- `{k}`: **{v}**")

    md.append("\n## Set comparison: 2019 derived CSV vs current robust parser\n")
    md.append("- Old-only: " + ("`" + "`, `".join(old_only) + "`" if old_only else "(none)"))
    md.append("- Current-only: " + ("`" + "`, `".join(current_only) + "`" if current_only else "(none)"))
    md.append(f"- Common roots with frequency changes: **{len(changed)}**")

    md.append("\n## Legacy shell pipeline artefacts\n")
    if cr_variants:
        md.append("The following values contain a trailing carriage-return byte (`\\r`) and can be counted as distinct by a raw `sort | uniq` pipeline:")
        md.append("| raw representation | cleaned root | count | clean variant also exists? |")
        md.append("|---|---|---:|---|")
        for item in cr_variants:
            md.append(
                f"| `{item['raw_repr']}` | `{item['cleaned_root']}` | {item['count']} | {item['also_exists_without_cr']} |"
            )
    else:
        md.append("No CR-suffixed ROOT values were produced by the emulated pipeline.")

    md.append("\nAfter stripping CR, roots missing from the legacy comma/cut pipeline:\n")
    md.append("`" + "`, `".join(legacy_missing_vs_current) + "`" if legacy_missing_vs_current else "(none)")
    md.append("\nAfter stripping CR, roots extra in the legacy comma/cut pipeline:\n")
    md.append("`" + "`, `".join(legacy_extra_vs_current) + "`" if legacy_extra_vs_current else "(none)")

    md.append("\n## Largest frequency changes: old derived CSV vs current\n")
    md.append("| root | 2019 CSV | current | delta |")
    md.append("|---|---:|---:|---:|")
    for item in changed[:100]:
        md.append(f"| `{item['root']}` | {item['old']} | {item['current']} | {item['delta']:+d} |")

    md.append("\n## Interpretation rule\n")
    md.append("A root-count claim must specify corpus/hash, parser and normalization. Shell pipelines that do not normalize CRLF or that replace TSV delimiters with a character that may occur in Buckwalter data are not authoritative root counters.")

    md_path = OUT_DIR / "qac_1651_vs_1642.md"
    md_path.write_text("\n".join(md) + "\n", encoding="utf-8")

    print(json.dumps(report["counts"], indent=2))
    print("CR variants:", cr_variants)
    print("legacy missing vs current:", legacy_missing_vs_current)
    print("legacy extra vs current:", legacy_extra_vs_current)
    print("wrote", md_path.relative_to(ROOT), "and", json_path.relative_to(ROOT))


if __name__ == "__main__":
    main()
