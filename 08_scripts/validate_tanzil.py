#!/usr/bin/env python3
"""Tanzil ham dosyalarının yapı ve sabit kaynak hash doğrulamasını yapar.

Beklenen kanonik yapı:
- 114 sûre
- 6236 numaralı ayet
- her ayet için benzersiz sûre:ayet anahtarı

Ham Arapça metin değiştirilmez; yalnız okunur ve doğrulanır.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "01_raw" / "tanzil"
EXPECTED_SURAH_COUNT = 114
EXPECTED_VERSE_COUNT = 6236
EXPECTED_SHA256 = {
    "quran-uthmani.txt": "bf4f57b968d03f4131c070b1e285da9be0e0a108a21c910e872801ca273312c8",
    "quran-simple-clean.txt": "228df2a717671aeb9d2ff573002bd28d6b3f973f4bc7153554e3a81663d67610",
    "quran-data.xml": "8867c1d88191472adec9db694b3cd9f135b1a2ef580574d32cf888dcb22c5c7a",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_txt2(path: Path) -> list[tuple[int, int, str]]:
    verses: list[tuple[int, int, str]] = []
    with path.open("r", encoding="utf-8-sig") as f:
        for line_no, raw in enumerate(f, start=1):
            line = raw.rstrip("\n\r")
            if not line or line.startswith("#"):
                continue
            parts = line.split("|", 2)
            if len(parts) != 3:
                continue
            s, a, text = parts
            try:
                surah = int(s)
                ayah = int(a)
            except ValueError:
                continue
            if not text:
                raise ValueError(f"Empty ayah text at line {line_no}: {surah}:{ayah}")
            verses.append((surah, ayah, text))
    return verses


def validate_one(path: Path) -> dict[str, object]:
    verses = parse_txt2(path)
    keys = [(s, a) for s, a, _ in verses]
    key_counts = Counter(keys)
    duplicates = [f"{s}:{a}" for (s, a), n in key_counts.items() if n > 1]
    surahs = sorted({s for s, _, _ in verses})
    actual_sha = sha256(path)
    expected_sha = EXPECTED_SHA256[path.name]

    errors: list[str] = []
    if actual_sha != expected_sha:
        errors.append(f"sha256={actual_sha} expected={expected_sha}")
    if len(verses) != EXPECTED_VERSE_COUNT:
        errors.append(f"verse_count={len(verses)} expected={EXPECTED_VERSE_COUNT}")
    if len(surahs) != EXPECTED_SURAH_COUNT:
        errors.append(f"surah_count={len(surahs)} expected={EXPECTED_SURAH_COUNT}")
    if surahs and (surahs[0] != 1 or surahs[-1] != 114):
        errors.append(f"surah_range={surahs[0]}..{surahs[-1]} expected=1..114")
    if duplicates:
        errors.append(f"duplicate_keys={duplicates[:20]}")

    return {
        "file": str(path.relative_to(ROOT)),
        "sha256": actual_sha,
        "expected_sha256": expected_sha,
        "hash_match": actual_sha == expected_sha,
        "verse_count": len(verses),
        "surah_count": len(surahs),
        "first_key": f"{keys[0][0]}:{keys[0][1]}" if keys else None,
        "last_key": f"{keys[-1][0]}:{keys[-1][1]}" if keys else None,
        "duplicate_key_count": len(duplicates),
        "valid": not errors,
        "errors": errors,
    }


def main() -> None:
    text_targets = [RAW_DIR / "quran-uthmani.txt", RAW_DIR / "quran-simple-clean.txt"]
    all_targets = text_targets + [RAW_DIR / "quran-data.xml"]
    missing = [str(p.relative_to(ROOT)) for p in all_targets if not p.exists()]
    if missing:
        raise SystemExit("Eksik ham kaynak: " + ", ".join(missing))

    files = [validate_one(path) for path in text_targets]
    metadata = RAW_DIR / "quran-data.xml"
    metadata_sha = sha256(metadata)
    metadata_ok = metadata_sha == EXPECTED_SHA256[metadata.name]

    report = {
        "expected_surah_count": EXPECTED_SURAH_COUNT,
        "expected_verse_count": EXPECTED_VERSE_COUNT,
        "files": files,
        "metadata": {
            "file": str(metadata.relative_to(ROOT)),
            "sha256": metadata_sha,
            "expected_sha256": EXPECTED_SHA256[metadata.name],
            "hash_match": metadata_ok,
        },
    }
    report["valid"] = all(item["valid"] for item in files) and metadata_ok

    out = RAW_DIR / "validation.local.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))

    if not report["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
