#!/usr/bin/env python3
"""2019'da 1,651 kök üreten QAC-türev snapshot ile sabitlenmiş mevcut QAC v0.4 indeksini karşılaştırır.

Eski veri kaynağı commit'e sabitlenmiştir:
  abdulbaqi/quranic_roots@86611929fd5a35220bc46e1944acc69c619aa57b
  quran-morphology-final.csv

Amaç "kaç kök var?" sorusunu sayı tartışması olmaktan çıkarıp iki somut annotation
snapshot'ı arasındaki set ve frekans farkına dönüştürmektir.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
from collections import Counter
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / "03_indices" / "generated" / "root_index.csv"
OUT_DIR = ROOT / "03_indices" / "audits"
OLD_COMMIT = "86611929fd5a35220bc46e1944acc69c619aa57b"
OLD_URL = (
    "https://raw.githubusercontent.com/abdulbaqi/quranic_roots/"
    f"{OLD_COMMIT}/quran-morphology-final.csv"
)


def download(url: str) -> bytes:
    req = Request(url, headers={"User-Agent": "quran-offline-corpus/1.0"})
    with urlopen(req, timeout=120) as response:
        return response.read()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_old(data: bytes) -> Counter[str]:
    # utf-8-sig tolerates a possible BOM.
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


def main() -> None:
    if not CURRENT.exists():
        raise SystemExit(f"Current root index missing: {CURRENT}")

    old_bytes = download(OLD_URL)
    old_counts = load_old(old_bytes)
    current_counts = load_current(CURRENT)

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
            "provenance": "QAC v0.4 pinned public copy; see SOURCES.md and qac/source_manifest.json",
        },
        "counts": {
            "old_distinct_roots": len(old_roots),
            "current_distinct_roots": len(current_roots),
            "common_roots": len(common),
            "old_only_count": len(old_only),
            "current_only_count": len(current_only),
            "roots_with_frequency_change": len(changed),
        },
        "old_only": old_only,
        "current_only": current_only,
        "frequency_changes": changed,
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = OUT_DIR / "qac_1651_vs_1642.json"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = []
    md.append("# QAC 1,651 ↔ 1,642 Root Audit\n")
    md.append("This report compares two concrete annotation snapshots; it does not assume either count is a universal linguistic truth.\n")
    md.append("## Sources\n")
    md.append(f"- Old derived snapshot: `abdulbaqi/quranic_roots@{OLD_COMMIT}` / `quran-morphology-final.csv`")
    md.append(f"- Old file SHA-256: `{report['old_source']['sha256']}`")
    md.append("- Current snapshot: repository-pinned QAC v0.4 root index generated from the verified morphology file.\n")
    md.append("## Counts\n")
    for k, v in report["counts"].items():
        md.append(f"- `{k}`: **{v}**")
    md.append("\n## Roots only in the 2019 snapshot\n")
    md.append("`" + "`, `".join(old_only) + "`" if old_only else "(none)")
    md.append("\n## Roots only in the current snapshot\n")
    md.append("`" + "`, `".join(current_only) + "`" if current_only else "(none)")
    md.append("\n## Largest frequency changes among common roots\n")
    md.append("| root | 2019 | current | delta |")
    md.append("|---|---:|---:|---:|")
    for item in changed[:100]:
        md.append(f"| `{item['root']}` | {item['old']} | {item['current']} | {item['delta']:+d} |")
    md.append("\n## Interpretation rule\n")
    md.append("A root-count claim must name the annotation snapshot/hash and counting unit. The bare statement ‘the Quran has exactly N roots’ is not reproducible without those qualifiers.")

    md_path = OUT_DIR / "qac_1651_vs_1642.md"
    md_path.write_text("\n".join(md) + "\n", encoding="utf-8")

    print(json.dumps(report["counts"], indent=2))
    print("old_only:", old_only)
    print("current_only:", current_only)
    print("largest changes:", changed[:20])
    print("wrote", md_path.relative_to(ROOT), "and", json_path.relative_to(ROOT))


if __name__ == "__main__":
    main()
