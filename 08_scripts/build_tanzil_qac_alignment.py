#!/usr/bin/env python3
"""Tanzil Uthmani v1.1 ile QAC kelime konumlarını ayet düzeyinde hizalar.

Amaç: `(sûre,ayet,kelime)` anahtarının iki kaynak arasında otomatik olarak aynı
olduğu varsayımını engellemek. QAC kelime indeksleri QAC içinde güvenlidir; Tanzil
ile kelime düzeyinde join yapılacaksa bu rapor dikkate alınmalıdır.
"""
from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TANZIL = ROOT / "01_raw" / "tanzil" / "quran-uthmani.txt"
QAC_WORDS = ROOT / "03_indices" / "generated" / "qac_word_annotations.csv"
OUT = ROOT / "03_indices" / "generated" / "tanzil_qac_alignment.csv"
AUDIT = ROOT / "03_indices" / "audits" / "tanzil_qac_alignment.md"


def load_tanzil() -> dict[tuple[int, int], list[str]]:
    out: dict[tuple[int, int], list[str]] = {}
    with TANZIL.open("r", encoding="utf-8-sig") as f:
        for raw in f:
            line = raw.rstrip("\r\n")
            if not line or line.startswith("#"):
                continue
            parts = line.split("|", 2)
            if len(parts) != 3:
                continue
            try:
                s, a = int(parts[0]), int(parts[1])
            except ValueError:
                continue
            out[(s, a)] = parts[2].split()
    return out


def load_qac() -> dict[tuple[int, int], list[tuple[int, str]]]:
    out: dict[tuple[int, int], list[tuple[int, str]]] = defaultdict(list)
    with QAC_WORDS.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            key = (int(row["surah"]), int(row["ayah"]))
            out[key].append((int(row["word"]), row["form_arabic"]))
    for key in out:
        out[key].sort()
    return dict(out)


def classify(s: int, a: int, t_count: int, q_count: int) -> tuple[str, str]:
    delta = t_count - q_count
    # Tanzil txt-2 includes the opening basmala in the first numbered verse of
    # most surahs; QAC does not place those four words in the same verse-word
    # sequence. In those cases QAC word n maps to Tanzil word n+4.
    if a == 1 and s not in {1, 9} and delta == 4:
        return "basmala_offset", "4"
    if delta == 0:
        return "count_match", "0"
    return "tokenization_difference", ""


def main() -> None:
    for path in (TANZIL, QAC_WORDS):
        if not path.exists():
            raise SystemExit(f"Missing prerequisite: {path.relative_to(ROOT)}")

    tanzil = load_tanzil()
    qac = load_qac()
    if set(tanzil) != set(qac):
        missing_t = sorted(set(qac) - set(tanzil))
        missing_q = sorted(set(tanzil) - set(qac))
        raise SystemExit(f"Verse-key mismatch; missing Tanzil={missing_t[:10]} missing QAC={missing_q[:10]}")

    rows: list[dict[str, object]] = []
    status_counts: Counter[str] = Counter()
    for s, a in sorted(tanzil):
        t_count = len(tanzil[(s, a)])
        q_count = len(qac[(s, a)])
        status, offset = classify(s, a, t_count, q_count)
        status_counts[status] += 1
        rows.append({
            "surah": s,
            "ayah": a,
            "tanzil_word_count": t_count,
            "qac_word_count": q_count,
            "delta_tanzil_minus_qac": t_count - q_count,
            "status": status,
            "qac_to_tanzil_word_offset": offset,
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    t_total = sum(len(v) for v in tanzil.values())
    q_total = sum(len(v) for v in qac.values())
    mismatches = [r for r in rows if r["status"] != "count_match"]
    token_diffs = [r for r in rows if r["status"] == "tokenization_difference"]

    lines = [
        "# Tanzil Uthmani v1.1 ↔ QAC v0.4 alignment audit",
        "",
        "Bu rapor otomatik üretilir. `(sûre,ayet)` anahtarı ortaktır; `(sûre,ayet,kelime)` doğrudan ortak anahtar kabul edilmez.",
        "",
        f"- Tanzil Uthmani whitespace-token total: **{t_total:,}**",
        f"- QAC orthographic word-position total: **{q_total:,}**",
        f"- Difference: **{t_total - q_total:+,}**",
        f"- Exact count-match ayat: **{status_counts['count_match']:,}**",
        f"- Basmala-offset ayat: **{status_counts['basmala_offset']:,}**",
        f"- Other tokenization-difference ayat: **{status_counts['tokenization_difference']:,}**",
        "",
        "## Non-basmala tokenization differences",
        "",
        "| ayah | Tanzil words | QAC words | delta |",
        "|---|---:|---:|---:|",
    ]
    for r in token_diffs:
        lines.append(
            f"| {r['surah']}:{r['ayah']} | {r['tanzil_word_count']} | {r['qac_word_count']} | {int(r['delta_tanzil_minus_qac']):+d} |"
        )
    lines += [
        "",
        "## Join rule",
        "",
        "- QAC içi morfoloji/kök/lemma sorgularında QAC `(sûre,ayet,kelime)` anahtarı kullanılabilir.",
        "- Tanzil ile kelime düzeyinde birleştirme yapılırken bu alignment tablosu kullanılmalıdır.",
        "- `basmala_offset` satırlarında QAC word `n`, Tanzil whitespace word `n+4` konumuna karşılık gelir.",
        "- `tokenization_difference` satırlarında otomatik pozisyon eşitlemesi yapılmaz; ayrı split/merge eşlemesi gerekir.",
        "",
        f"Total non-count-match ayat: **{len(mismatches):,}**",
    ]
    AUDIT.parent.mkdir(parents=True, exist_ok=True)
    AUDIT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Tanzil words: {t_total:,}")
    print(f"QAC words: {q_total:,}")
    print(f"Status counts: {dict(status_counts)}")
    print("Tokenization differences:", [f"{r['surah']}:{r['ayah']}" for r in token_diffs])


if __name__ == "__main__":
    main()
