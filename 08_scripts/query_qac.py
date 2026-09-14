#!/usr/bin/env python3
"""Üretilmiş QAC kelime indeksinde kök veya lemma sorgusu yapar.

Örnekler:
    python 08_scripts/query_qac.py --root Slw
    python 08_scripts/query_qac.py --lemma Salaw`p
    python 08_scripts/query_qac.py --root Amn --limit 20
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORDS = ROOT / "03_indices" / "generated" / "qac_word_annotations.csv"


def values(cell: str) -> set[str]:
    return {x for x in cell.split(";") if x}


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--root", help="QAC Buckwalter kökü, ör. Slw, Amn, wqy")
    group.add_argument("--lemma", help="QAC Buckwalter lemma biçimi")
    parser.add_argument("--limit", type=int, default=50, help="Gösterilecek ilk occurrence sayısı; 0=tümü")
    args = parser.parse_args()

    if not WORDS.exists():
        raise SystemExit(
            f"İndeks bulunamadı: {WORDS}\n"
            "Önce python 08_scripts/build_qac_indices.py çalıştırın."
        )

    target = args.root if args.root is not None else args.lemma
    field = "roots_bw" if args.root is not None else "lemmas_bw"

    rows: list[dict[str, str]] = []
    ayat: set[tuple[int, int]] = set()
    surahs: set[int] = set()
    forms: dict[str, int] = {}

    with WORDS.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if target not in values(row[field]):
                continue
            rows.append(row)
            s, a = int(row["surah"]), int(row["ayah"])
            ayat.add((s, a))
            surahs.add(s)
            form = row["form_arabic"]
            forms[form] = forms.get(form, 0) + 1

    print(f"Query: {field}={target}")
    print(f"Word occurrences: {len(rows):,}")
    print(f"Ayat: {len(ayat):,}")
    print(f"Surahs: {len(surahs):,}")

    print("\nMost frequent surface forms:")
    for form, count in sorted(forms.items(), key=lambda x: (-x[1], x[0]))[:20]:
        print(f"  {count:>4}  {form}")

    shown = rows if args.limit == 0 else rows[: max(args.limit, 0)]
    print(f"\nOccurrences shown: {len(shown):,} / {len(rows):,}")
    for row in shown:
        print(
            f"  {row['location']:<12} {row['form_arabic']:<20} "
            f"root={row['roots_arabic'] or '-'} lemma={row['lemmas_arabic'] or '-'} pos={row['pos'] or '-'}"
        )


if __name__ == "__main__":
    main()
