#!/usr/bin/env python3
"""Quranic Arabic Corpus v0.4 morphology dosyasını yapı ve hash düzeyinde doğrular."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QAC = ROOT / "02_morphology" / "qac" / "quranic-corpus-morphology-0.4.txt"
LOCATION_RE = re.compile(r"^\((\d+):(\d+):(\d+):(\d+)\)$")

EXPECTED_SHA256 = "a1d12923815341face765083805d2148ed2d9f5cc3f7d6665219d887675d8c46"
EXPECTED_SEGMENTS = 128_219
EXPECTED_WORDS = 77_429
EXPECTED_SURAHS = 114
EXPECTED_AYAT = 6_236


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    if not QAC.exists():
        raise SystemExit(f"Dosya bulunamadı: {QAC}")

    actual_sha = sha256(QAC)
    segments = 0
    words: set[tuple[int, int, int]] = set()
    ayat: set[tuple[int, int]] = set()
    surahs: set[int] = set()
    bad_rows: list[tuple[int, str]] = []
    empty_forms = 0
    copyright_seen = False
    version_seen = False

    with QAC.open("r", encoding="utf-8-sig", errors="strict") as f:
        for line_no, raw in enumerate(f, 1):
            line = raw.rstrip("\n\r")
            if "Quranic Arabic Corpus" in line and "version 0.4" in line.lower():
                version_seen = True
            if "Copyright (C) 2011 Kais Dukes" in line:
                copyright_seen = True
            if not line.startswith("("):
                continue
            parts = line.split("\t")
            if len(parts) != 4:
                bad_rows.append((line_no, line[:160]))
                continue
            location, form, tag, features = parts
            m = LOCATION_RE.match(location)
            if not m:
                bad_rows.append((line_no, line[:160]))
                continue
            surah, ayah, word, segment = map(int, m.groups())
            segments += 1
            surahs.add(surah)
            ayat.add((surah, ayah))
            words.add((surah, ayah, word))
            if not form:
                empty_forms += 1
            if not tag or not features:
                bad_rows.append((line_no, line[:160]))

    checks = {
        "sha256_pinned": actual_sha == EXPECTED_SHA256,
        "version_header": version_seen,
        "copyright_header": copyright_seen,
        "segments_128219": segments == EXPECTED_SEGMENTS,
        "words_77429": len(words) == EXPECTED_WORDS,
        "surahs_114": len(surahs) == EXPECTED_SURAHS,
        "ayat_6236": len(ayat) == EXPECTED_AYAT,
        "no_structurally_bad_rows": not bad_rows,
    }

    print(f"File: {QAC.relative_to(ROOT)}")
    print(f"SHA-256: {actual_sha}")
    print(f"Expected SHA-256: {EXPECTED_SHA256}")
    print(f"Segments: {segments:,}")
    print(f"Unique word positions: {len(words):,}")
    print(f"Ayat: {len(ayat):,}")
    print(f"Surahs: {len(surahs):,}")
    print(f"Zero-form annotated segments: {empty_forms:,}")
    print("\nChecks:")
    for name, ok in checks.items():
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")

    if bad_rows:
        print("\nFirst structurally malformed rows:")
        for row in bad_rows[:10]:
            print(f"  line {row[0]}: {row[1]}")

    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
