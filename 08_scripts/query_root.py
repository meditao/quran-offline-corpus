#!/usr/bin/env python3
"""Tek kök için QAC dağılımı + lemma/yüzey biçimleri + Sami kognat kayıtlarını birlikte gösterir."""
from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROOT_INDEX = ROOT / "03_indices" / "generated" / "root_index.csv"
WORDS = ROOT / "03_indices" / "generated" / "qac_word_annotations.csv"
COGNATES = ROOT / "04_lexicons" / "semitic" / "cognates.tsv"


def split_values(cell: str) -> set[str]:
    return {v for v in cell.split(";") if v}


def load_root(root_bw: str) -> dict[str, str] | None:
    with ROOT_INDEX.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            if row["root_bw"] == root_bw:
                return row
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", help="QAC Buckwalter ROOT, e.g. Slw, Amn, wqy, Hkm")
    parser.add_argument("--limit", type=int, default=20, help="Occurrence lines to show; 0 = none")
    args = parser.parse_args()

    meta = load_root(args.root)
    if meta is None:
        raise SystemExit(f"Unknown QAC root: {args.root}")

    forms: Counter[str] = Counter()
    lemmas: Counter[str] = Counter()
    occurrences: list[dict[str, str]] = []

    with WORDS.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if args.root not in split_values(row["roots_bw"]):
                continue
            occurrences.append(row)
            forms[row["form_arabic"]] += 1
            for lemma in split_values(row["lemmas_bw"]):
                lemmas[lemma] += 1

    cognates: list[dict[str, str]] = []
    if COGNATES.exists():
        with COGNATES.open("r", encoding="utf-8-sig", newline="") as f:
            cognates = [
                row for row in csv.DictReader(f, delimiter="\t")
                if (row.get("quran_root_bw") or "").strip() == args.root
            ]

    print(f"Root: {args.root} / {meta['root_bw_arabic']}")
    print(
        f"QAC distribution: {meta['word_occurrences']} word occurrences / "
        f"{meta['ayah_count']} ayat / {meta['surah_count']} surahs"
    )

    print("\nTop surface forms:")
    for form, count in forms.most_common(15):
        print(f"  {count:>4}  {form}")

    print("\nTop QAC lemmas (Buckwalter):")
    for lemma, count in lemmas.most_common(15):
        print(f"  {count:>4}  {lemma}")

    print(f"\nReviewed Semitic cognate records: {len(cognates)}")
    for row in cognates:
        print(
            f"  - {row['language']} [{row['dialect_period']}] "
            f"{row['cognate_script']} ({row['cognate_translit']}) — {row['gloss']}"
        )
        print(
            f"    source={row['source_name']} {row['source_locator']} | "
            f"phonology={row['phonological_fit']} | semantics={row['semantic_fit']} | "
            f"confidence={row['confidence']} | effect={row['effect_on_quran_analysis']}"
        )

    if args.limit > 0:
        shown = occurrences[:args.limit]
        print(f"\nFirst occurrences: {len(shown)} / {len(occurrences)}")
        for row in shown:
            print(
                f"  {row['location']:<12} {row['form_arabic']:<20} "
                f"lemma={row['lemmas_arabic'] or '-'} pos={row['pos'] or '-'}"
            )


if __name__ == "__main__":
    main()
