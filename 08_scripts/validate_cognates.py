#!/usr/bin/env python3
"""Sami kognat tablosunu sabit QAC kök evrenine karşı doğrular.

Varsayılan davranışta sıfır veri satırı FAIL'dir. Yalnız altyapı/şema testi yapmak
isteyen CI veya geliştirici açıkça `--allow-empty` vermelidir.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROOT_INDEX = ROOT / "03_indices" / "generated" / "root_index.csv"
COGNATES = ROOT / "04_lexicons" / "semitic" / "cognates.tsv"

EXPECTED_COLUMNS = [
    "quran_root_bw", "quran_root_ar", "arabic_lemma", "language", "dialect_period",
    "cognate_script", "cognate_translit", "lexical_root", "gloss", "source_name",
    "source_locator", "source_url", "phonological_fit", "semantic_fit", "confidence",
    "effect_on_quran_analysis", "notes", "reviewed_date",
]
ALLOWED_CONFIDENCE = {"güçlü", "orta", "zayıf", "strong", "medium", "weak"}
ALLOWED_EFFECT = {"destekliyor", "nötr", "zorlaştırıyor", "supports", "neutral", "challenges"}


def load_roots() -> dict[str, dict[str, str]]:
    with ROOT_INDEX.open("r", encoding="utf-8-sig", newline="") as f:
        return {row["root_bw"]: row for row in csv.DictReader(f)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--allow-empty", action="store_true", help="Only validate schema/infrastructure when the cognate table has no data rows")
    args = parser.parse_args()

    if not ROOT_INDEX.exists():
        raise SystemExit(f"Root index missing: {ROOT_INDEX}")
    if not COGNATES.exists():
        raise SystemExit(f"Cognate table missing: {COGNATES}")

    roots = load_roots()
    if len(roots) != 1642:
        raise SystemExit(f"Expected 1,642 QAC roots; found {len(roots):,}")

    errors: list[str] = []
    rows = 0
    represented_roots: set[str] = set()
    with COGNATES.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        if reader.fieldnames != EXPECTED_COLUMNS:
            errors.append(f"Header mismatch: {reader.fieldnames!r}")
        else:
            for line_no, row in enumerate(reader, 2):
                if not any((v or "").strip() for v in row.values()):
                    continue
                rows += 1
                bw = (row["quran_root_bw"] or "").strip()
                ar = (row["quran_root_ar"] or "").strip()
                if bw not in roots:
                    errors.append(f"line {line_no}: quran_root_bw {bw!r} is not in QAC root index")
                    continue
                represented_roots.add(bw)
                expected_ar = roots[bw]["root_bw_arabic"].strip()
                if ar and ar != expected_ar:
                    errors.append(f"line {line_no}: Arabic root {ar!r} != generated QAC mapping {expected_ar!r} for {bw}")
                if not (row["language"] or "").strip():
                    errors.append(f"line {line_no}: language is required")
                if not (row["cognate_script"] or "").strip():
                    errors.append(f"line {line_no}: cognate_script is required")
                if not (row["source_name"] or "").strip():
                    errors.append(f"line {line_no}: source_name is required")
                confidence = (row["confidence"] or "").strip().lower()
                if confidence and confidence not in ALLOWED_CONFIDENCE:
                    errors.append(f"line {line_no}: unsupported confidence {confidence!r}")
                effect = (row["effect_on_quran_analysis"] or "").strip().lower()
                if effect and effect not in ALLOWED_EFFECT:
                    errors.append(f"line {line_no}: unsupported analysis effect {effect!r}")

    print(f"QAC root registry: {len(roots):,}")
    print(f"Cognate records: {rows:,}")
    print(f"QAC roots represented in cognate table: {len(represented_roots):,}")

    if rows == 0 and not args.allow_empty:
        errors.append("cognates.tsv has zero data rows; semantic cognate layer is not populated")

    if errors:
        print("\nErrors:")
        for error in errors:
            print("-", error)
        raise SystemExit(1)

    if rows == 0:
        print("Validation: SCHEMA-ONLY PASS (--allow-empty); no cognate evidence validated")
    else:
        print("Validation: PASS")


if __name__ == "__main__":
    main()
