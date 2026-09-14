#!/usr/bin/env python3
"""QuranMorph CSV dosyasını yapısal olarak doğrular ve varsa QAC ile konum hizasını sınar."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QM = ROOT / "02_morphology" / "quranmorph" / "quran-dataset.csv"
QAC_WORDS = ROOT / "03_indices" / "generated" / "qac_word_annotations.csv"

EXPECTED_ROWS = 77_429
EXPECTED_SURAHS = 114
EXPECTED_VERSE_KEYS = 6_236
REQUIRED = {
    "surah_number", "verse_number", "word_position", "word", "POS", "qabas_lemma"
}


def main() -> None:
    if not QM.exists():
        raise SystemExit(f"QuranMorph dosyası bulunamadı: {QM}")

    locations: set[tuple[int, int, int]] = set()
    verses: set[tuple[int, int]] = set()
    surahs: set[int] = set()
    rows = 0
    empty_word = 0
    empty_lemma = 0

    with QM.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fields = set(reader.fieldnames or [])
        missing = REQUIRED - fields
        if missing:
            raise SystemExit(f"Eksik zorunlu kolonlar: {sorted(missing)}; bulunan: {reader.fieldnames}")

        for line_no, row in enumerate(reader, 2):
            try:
                s = int(row["surah_number"])
                a = int(row["verse_number"])
                w = int(row["word_position"])
            except Exception as exc:
                raise ValueError(f"Satır {line_no}: geçersiz konum") from exc
            loc = (s, a, w)
            if loc in locations:
                raise ValueError(f"Tekrarlanan kelime konumu: {loc}")
            locations.add(loc)
            verses.add((s, a))
            surahs.add(s)
            rows += 1
            if not (row.get("word") or "").strip():
                empty_word += 1
            if not (row.get("qabas_lemma") or "").strip():
                empty_lemma += 1

    checks = {
        "rows_77429": rows == EXPECTED_ROWS,
        "unique_locations_77429": len(locations) == EXPECTED_ROWS,
        "surahs_114": len(surahs) == EXPECTED_SURAHS,
        "verse_keys_6236": len(verses) == EXPECTED_VERSE_KEYS,
        "no_empty_word": empty_word == 0,
        "no_empty_lemma": empty_lemma == 0,
    }

    print(f"Rows: {rows:,}")
    print(f"Unique locations: {len(locations):,}")
    print(f"Verse keys: {len(verses):,}")
    print(f"Surahs: {len(surahs):,}")
    print("\nChecks:")
    for name, ok in checks.items():
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")

    if QAC_WORDS.exists():
        qac_locations: set[tuple[int, int, int]] = set()
        with QAC_WORDS.open("r", encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                qac_locations.add((int(row["surah"]), int(row["ayah"]), int(row["word"])))
        only_qm = locations - qac_locations
        only_qac = qac_locations - locations
        aligned = not only_qm and not only_qac
        checks["location_set_matches_qac"] = aligned
        print(f"\nQAC location alignment: {'PASS' if aligned else 'FAIL'}")
        print(f"  only QuranMorph: {len(only_qm):,}")
        print(f"  only QAC: {len(only_qac):,}")
        for label, items in (("only QuranMorph", only_qm), ("only QAC", only_qac)):
            if items:
                print(f"  first {label}: {sorted(items)[:10]}")
    else:
        print("\nQAC word index bulunmadı; çapraz konum kontrolü atlandı.")

    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
