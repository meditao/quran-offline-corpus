#!/usr/bin/env python3
"""QAC v0.4 ham morfoloji dosyasından yeniden üretilebilir indeksler üretir.

Ham dosyayı değiştirmez.

Girdi:
    02_morphology/qac/quranic-corpus-morphology-0.4.txt

Çıktılar:
    03_indices/generated/qac_word_annotations.csv
    03_indices/generated/root_index.csv
    03_indices/generated/lemma_index.csv
    03_indices/generated/pos_index.csv

Kök/lemma indekslerinde üç ayrı dağılım sayısı tutulur:
    word_occurrences  = kaç kelime konumu
    ayah_count        = kaç farklı ayet
    surah_count       = kaç farklı sûre
"""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QAC = ROOT / "02_morphology" / "qac" / "quranic-corpus-morphology-0.4.txt"
OUT = ROOT / "03_indices" / "generated"
LOCATION_RE = re.compile(r"^\((\d+):(\d+):(\d+):(\d+)\)$")

# Standard Buckwalter -> Arabic mapping. Kök/lemma alanlarını okunabilir yapmak için
# kullanılır; ana kimlik olarak Buckwalter biçimi de korunur.
BW = {
    "'": "ء", "|": "آ", ">": "أ", "&": "ؤ", "<": "إ", "}": "ئ",
    "A": "ا", "b": "ب", "p": "ة", "t": "ت", "v": "ث", "j": "ج",
    "H": "ح", "x": "خ", "d": "د", "*": "ذ", "r": "ر", "z": "ز",
    "s": "س", "$": "ش", "S": "ص", "D": "ض", "T": "ط", "Z": "ظ",
    "E": "ع", "g": "غ", "f": "ف", "q": "ق", "k": "ك", "l": "ل",
    "m": "م", "n": "ن", "h": "ه", "w": "و", "Y": "ى", "y": "ي",
    "F": "ً", "N": "ٌ", "K": "ٍ", "a": "َ", "u": "ُ", "i": "ِ",
    "~": "ّ", "o": "ْ", "`": "ٰ", "{": "ٱ", "_": "ـ",
}


def bw_to_arabic(text: str) -> str:
    return "".join(BW.get(ch, ch) for ch in text)


def feature_map(features: str) -> dict[str, list[str]]:
    out: dict[str, list[str]] = defaultdict(list)
    for item in features.split("|"):
        if ":" in item:
            key, value = item.split(":", 1)
            out[key].append(value)
        else:
            out[item].append("")
    return dict(out)


def new_stat() -> dict[str, object]:
    return {"words": 0, "ayat": set(), "surahs": set()}


def add_stat(stats: dict[str, dict[str, object]], key: str, surah: int, ayah: int) -> None:
    rec = stats.setdefault(key, new_stat())
    rec["words"] += 1
    rec["ayat"].add((surah, ayah))
    rec["surahs"].add(surah)


def write_index(path: Path, key_name: str, stats: dict[str, dict[str, object]], arabic=True) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        fields = [key_name]
        if arabic:
            fields.append(f"{key_name}_arabic")
        fields += ["word_occurrences", "ayah_count", "surah_count"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        ordered = sorted(
            stats.items(),
            key=lambda x: (-int(x[1]["words"]), x[0]),
        )
        for key, rec in ordered:
            row = {
                key_name: key,
                "word_occurrences": rec["words"],
                "ayah_count": len(rec["ayat"]),
                "surah_count": len(rec["surahs"]),
            }
            if arabic:
                row[f"{key_name}_arabic"] = bw_to_arabic(key)
            w.writerow(row)


def main() -> None:
    if not QAC.exists():
        raise SystemExit(f"QAC dosyası bulunamadı: {QAC}")

    # Her QAC kelime konumunda segmentleri birleştiriyoruz. Ham segmentler değişmez.
    words: dict[tuple[int, int, int], dict[str, object]] = {}

    with QAC.open("r", encoding="utf-8-sig", errors="strict") as f:
        for line_no, raw in enumerate(f, 1):
            line = raw.rstrip("\r\n")
            if not line.startswith("("):
                continue
            parts = line.split("\t")
            if len(parts) != 4:
                raise ValueError(f"Satır {line_no}: 4 TSV alanı bekleniyordu")
            location, form, tag, features = parts
            m = LOCATION_RE.match(location)
            if not m:
                raise ValueError(f"Satır {line_no}: geçersiz LOCATION {location!r}")
            surah, ayah, word, segment = map(int, m.groups())
            key = (surah, ayah, word)
            rec = words.setdefault(key, {
                "segments": [], "roots": set(), "lemmas": set(), "pos": set(),
            })
            rec["segments"].append((segment, form))
            fm = feature_map(features)
            for root in fm.get("ROOT", []):
                if root:
                    rec["roots"].add(root)
            for lemma in fm.get("LEM", []):
                if lemma:
                    rec["lemmas"].add(lemma)
            for pos in fm.get("POS", []):
                if pos:
                    rec["pos"].add(pos)
            # Prefix/suffix TAG'lerini kelime POS'u gibi saymıyoruz. POS alanı yoksa
            # yalnız STEM segmentinde TAG'i yedek olarak kullanıyoruz.
            if not fm.get("POS") and "STEM" in fm and tag:
                rec["pos"].add(tag)

    if len(words) != 77_429:
        raise SystemExit(f"Beklenen 77.429 kelime, bulundu {len(words):,}")

    OUT.mkdir(parents=True, exist_ok=True)

    root_stats: dict[str, dict[str, object]] = {}
    lemma_stats: dict[str, dict[str, object]] = {}
    pos_stats: dict[str, dict[str, object]] = {}

    word_path = OUT / "qac_word_annotations.csv"
    with word_path.open("w", encoding="utf-8", newline="") as f:
        fields = [
            "surah", "ayah", "word", "location", "form_bw", "form_arabic",
            "roots_bw", "roots_arabic", "lemmas_bw", "lemmas_arabic", "pos",
        ]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for (surah, ayah, word), rec in sorted(words.items()):
            segments = sorted(rec["segments"])
            form_bw = "".join(form for _, form in segments)
            roots = sorted(rec["roots"])
            lemmas = sorted(rec["lemmas"])
            poses = sorted(rec["pos"])
            for value in roots:
                add_stat(root_stats, value, surah, ayah)
            for value in lemmas:
                add_stat(lemma_stats, value, surah, ayah)
            for value in poses:
                add_stat(pos_stats, value, surah, ayah)
            w.writerow({
                "surah": surah,
                "ayah": ayah,
                "word": word,
                "location": f"{surah}:{ayah}:{word}",
                "form_bw": form_bw,
                "form_arabic": bw_to_arabic(form_bw),
                "roots_bw": ";".join(roots),
                "roots_arabic": ";".join(bw_to_arabic(x) for x in roots),
                "lemmas_bw": ";".join(lemmas),
                "lemmas_arabic": ";".join(bw_to_arabic(x) for x in lemmas),
                "pos": ";".join(poses),
            })

    write_index(OUT / "root_index.csv", "root_bw", root_stats)
    write_index(OUT / "lemma_index.csv", "lemma_bw", lemma_stats)
    write_index(OUT / "pos_index.csv", "pos", pos_stats, arabic=False)

    print(f"Words: {len(words):,}")
    print(f"Distinct roots: {len(root_stats):,}")
    print(f"Distinct lemmas: {len(lemma_stats):,}")
    print(f"Output: {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
