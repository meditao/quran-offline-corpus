#!/usr/bin/env python3
"""Sami kognat kanıt tablosunu Kur'an köküne göre sorgular."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "04_lexicons" / "semitic" / "cognates.tsv"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", help="QAC Buckwalter kökü, ör. Slw, Amn, wqy")
    args = parser.parse_args()

    if not TABLE.exists():
        raise SystemExit(f"Kognat tablosu bulunamadı: {TABLE}")

    with TABLE.open("r", encoding="utf-8", newline="") as f:
        rows = [r for r in csv.DictReader(f, delimiter="\t") if r["quran_root_bw"] == args.root]

    print(f"Root: {args.root}")
    print(f"Cognate records: {len(rows)}")
    for r in rows:
        print(
            f"- {r['language']} | {r['cognate_script']} ({r['cognate_translit']}) | "
            f"{r['gloss']} | confidence={r['confidence']} | source={r['source_name']} {r['source_locator']}"
        )
        if r.get("notes"):
            print(f"  note: {r['notes']}")


if __name__ == "__main__":
    main()
