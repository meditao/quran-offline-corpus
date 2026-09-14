#!/usr/bin/env python3
"""Tanzil ham dosyalarının temel yapısal doğrulamasını yapar.

Beklenen kanonik yapı:
- 114 sûre
- 6236 numaralı ayet
- her ayet için benzersiz sûre:ayet anahtarı

Script Arapça metni değiştirmez; yalnızca okur ve rapor üretir.
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
                # Tanzil dosyasının sonundaki lisans/yorum bloklarını yok say.
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

    errors: list[str] = []
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
        "sha256": sha256(path),
        "verse_count": len(verses),
        "surah_count": len(surahs),
        "first_key": f"{keys[0][0]}:{keys[0][1]}" if keys else None,
        "last_key": f"{keys[-1][0]}:{keys[-1][1]}" if keys else None,
        "duplicate_key_count": len(duplicates),
        "valid": not errors,
        "errors": errors,
    }


def main() -> None:
    targets = [RAW_DIR / "quran-uthmani.txt", RAW_DIR / "quran-simple-clean.txt"]
    missing = [str(p.relative_to(ROOT)) for p in targets if not p.exists()]
    if missing:
        raise SystemExit(
            "Eksik ham kaynak: " + ", ".join(missing) +
            ". Önce fetch_tanzil.py çalıştırılmalı."
        )

    report = {
        "expected_surah_count": EXPECTED_SURAH_COUNT,
        "expected_verse_count": EXPECTED_VERSE_COUNT,
        "files": [validate_one(path) for path in targets],
    }
    report["valid"] = all(item["valid"] for item in report["files"])

    out = RAW_DIR / "validation.local.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))

    if not report["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
