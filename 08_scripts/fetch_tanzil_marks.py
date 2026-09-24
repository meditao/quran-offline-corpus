#!/usr/bin/env python3
"""Tanzil Uthmani v1.1'in durak işaretli sürümünü AYRI bir ham dosya olarak indirir.

Kullanım:
    python 08_scripts/fetch_tanzil_marks.py --i-agree-to-tanzil-terms

- Mevcut 01_raw/tanzil/quran-uthmani.txt dosyasına dokunulmaz.
- Çıktı: 01_raw/tanzil/quran-uthmani-durak.txt (Tanzil'den geldiği gibi, değiştirilmeden).
- Kabul koşulu: durak işaretleri (U+06D6–06DC) ve fazladan boşluklar çıkarıldığında her ayet
  mevcut quran-uthmani.txt ile birebir aynı olmalıdır. Tutmazsa dosya yazılmaz.
- Kaynak adresi, bayt sayısı ve sha256 01_raw/tanzil/manifest.local.json'a eklenir.

Çalışma masasında bu dosya okunuşta yalnız sekte (U+06DC) için kullanılır. Diğer durak
işaretleri varsayılan olarak gösterilmez; gösterilirse "geleneksel — yorum içerebilir"
etiketi taşır.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "01_raw" / "tanzil"
BASE = RAW_DIR / "quran-uthmani.txt"
TARGET = RAW_DIR / "quran-uthmani-durak.txt"
MANIFEST = RAW_DIR / "manifest.local.json"
BASE_URL = "https://tanzil.net/pub/download/index.php"
PARAMS = {"quranType": "uthmani", "outType": "txt-2", "marks": "true", "agree": "true"}
DURAK = {chr(c) for c in range(0x06D6, 0x06DD)}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def ayetler(metin: str) -> dict[tuple[int, int], str]:
    sonuc = {}
    for satir in metin.splitlines():
        if not satir or satir.startswith("#"):
            continue
        s, a, t = satir.split("|", 2)
        sonuc[(int(s), int(a))] = t
    return sonuc


def durak_cikar(t: str) -> str:
    return " ".join("".join(c for c in t if c not in DURAK).split())


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--i-agree-to-tanzil-terms", action="store_true")
    p.add_argument("--dosyadan", type=Path, help="İndirmek yerine elle indirilmiş dosyayı kullan")
    p.add_argument("--kaynak-url", help="--dosyadan ile: dosyanın indirildiği tam adres")
    args = p.parse_args()
    if not args.i_agree_to_tanzil_terms:
        raise SystemExit("İndirme yapılmadı. Tanzil şartlarını okuyun: https://tanzil.net/download/")
    if TARGET.exists():
        raise SystemExit(f"{TARGET.relative_to(ROOT)} zaten var; üzerine yazılmaz.")

    if args.dosyadan:
        if not args.kaynak_url:
            raise SystemExit("--dosyadan için --kaynak-url zorunlu (manifest'e işlenir).")
        veri, url = args.dosyadan.read_bytes(), args.kaynak_url
    else:
        url = f"{BASE_URL}?{urlencode(PARAMS)}"
        istek = Request(url, headers={"User-Agent": "quran-offline-corpus/1.0"})
        with urlopen(istek, timeout=60) as yanit:
            veri = yanit.read()

    yeni = ayetler(veri.decode("utf-8-sig"))
    eski = ayetler(BASE.read_text(encoding="utf-8-sig"))
    if set(yeni) != set(eski):
        raise SystemExit(f"Ayet anahtarları farklı: {len(yeni)} ↔ {len(eski)}. Dosya yazılmadı.")
    farkli = [k for k in eski if durak_cikar(yeni[k]) != " ".join(eski[k].split())]
    if farkli:
        raise SystemExit(f"Durak işaretleri çıkarılınca {len(farkli)} ayet farklı (ilk: {farkli[:5]}). Dosya yazılmadı.")
    isaretli = sum(1 for k in yeni if any(c in DURAK for c in yeni[k]))

    TARGET.write_bytes(veri)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest["files"].append({
        "file": str(TARGET.relative_to(ROOT)),
        "source_url": url,
        "bytes": len(veri),
        "sha256": sha256_bytes(veri),
        "fetched": date.today().isoformat(),
        "note": "Durak işaretli sürüm. Okunuşta yalnız sekte (U+06DC) için kullanılır; "
                "diğer durak işaretleri geleneksel — yorum içerebilir.",
    })
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Yazıldı: {TARGET.relative_to(ROOT)} ({len(veri)} bayt, sha256 {sha256_bytes(veri)})")
    print(f"Durak işareti taşıyan ayet: {isaretli}; işaretler çıkarılınca 6236/6236 ayet aynı.")


if __name__ == "__main__":
    main()
