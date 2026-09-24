#!/usr/bin/env python3
"""Tanzil Uthmani v1.1'in durak işaretli sürümünü AYRI bir ham dosya olarak indirir.

Kullanım:
    python 08_scripts/fetch_tanzil_marks.py --i-agree-to-tanzil-terms

- Mevcut 01_raw/tanzil/quran-uthmani.txt dosyasına dokunulmaz.
- Çıktı: 01_raw/tanzil/quran-uthmani-durak.txt (Tanzil'den geldiği gibi, değiştirilmeden).
- Kabul koşulu (tezgah.okunus.denklik_tokenlari): tek başına duran işaret tokenları (U+06D6–06DC,
  U+06DE rubʿ, U+06E9 secde) ve tokenlardaki U+06D6–06DB, U+06DE, U+06E9, tatvil U+0640 çıkarılınca
  6.236 ayetin hepsi mevcut quran-uthmani.txt ile birebir aynı olmalıdır. Tutmazsa dosya yazılmaz.
  (Bu sürüm, sajdah/rub/tatweel parametreleri kapalı olsa da rubʿ, secde ve tatvil ekler.)
- Kaynak adresi, bayt sayısı, sha256 ve beklenen sha256 karşılaştırması manifest.local.json'a eklenir.
  Sha256 beklenenden farklıysa (dinamik üretim olabilir) rapor edilir, iş durmaz.

Çalışma masasında bu dosya okunuşta yalnız sekte (U+06DC) için kullanılır. Diğer durak
işaretleri varsayılan olarak gösterilmez; gösterilirse "geleneksel — yorum içerebilir"
etiketi taşır.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "01_raw" / "tanzil"
BASE = RAW_DIR / "quran-uthmani.txt"
TARGET = RAW_DIR / "quran-uthmani-durak.txt"
MANIFEST = RAW_DIR / "manifest.local.json"
URL = ("https://tanzil.net/pub/download/index.php?marks=true&sajdah=false&rub=false&tatweel=false"
       "&quranType=uthmani&outType=txt-2&agree=true")
# Kullanıcının kendi ölçümü (24.09.2026). Tanzil dosyayı dinamik üretiyor olabilir.
BEKLENEN_SHA256 = "7f30c647331a61100ebf24a80507dc0fcdd9f2df97f1312b5b2dfcb982a7f326"

sys.path.insert(0, str(ROOT / "09_calisma_masasi"))
from tezgah.okunus import DURAK_KARAKTERLERI, EK_ISARETLER, SEKTE, _isaret_tokeni, denklik_tokenlari  # noqa: E402


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
        url = URL
        istek = Request(url, headers={"User-Agent": "quran-offline-corpus/1.0"})
        with urlopen(istek, timeout=60) as yanit:
            veri = yanit.read()

    yeni = ayetler(veri.decode("utf-8-sig"))
    eski = ayetler(BASE.read_text(encoding="utf-8-sig"))
    if set(yeni) != set(eski):
        raise SystemExit(f"Ayet anahtarları farklı: {len(yeni)} ↔ {len(eski)}. Dosya yazılmadı.")
    farkli = [k for k in eski if denklik_tokenlari(yeni[k]) != denklik_tokenlari(eski[k])]
    if farkli:
        raise SystemExit(f"İşaretler ve tatvil çıkarılınca {len(farkli)} ayet farklı (ilk: {farkli[:5]}). "
                         "Dosya yazılmadı.")
    sayim = Counter(c for k in yeni for c in yeni[k] if c in DURAK_KARAKTERLERI | set(EK_ISARETLER))
    tatvil_farki = sum(yeni[k].count("\u0640") for k in yeni) - sum(eski[k].count("\u0640") for k in eski)
    sekte = sorted(k for k in yeni for tok in yeni[k].split() if _isaret_tokeni(tok) and SEKTE in tok)
    sha = sha256_bytes(veri)

    TARGET.write_bytes(veri)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest["files"].append({
        "file": str(TARGET.relative_to(ROOT)),
        "source_url": url,
        "bytes": len(veri),
        "sha256": sha,
        "sha256_beklenen": BEKLENEN_SHA256,
        "sha256_beklenenle_ayni": sha == BEKLENEN_SHA256,
        "fetched": date.today().isoformat(),
        "denklik": "6236/6236 (tezgah.okunus.denklik_tokenlari)",
        "isaret_sayilari": {f"U+{ord(c):04X}": n for c, n in sorted(sayim.items())},
        "eklenen_tatvil": tatvil_farki,
        "tek_basina_sekte": [f"{s}:{a}" for s, a in sekte],
        **({"edinim": "kullanıcı tarafından yüklendi (--dosyadan); source_url kullanıcı beyanı"}
           if args.dosyadan else {"edinim": "betik tarafından indirildi"}),
        "note": "Durak işaretli sürüm. Okunuşta yalnız sekte (U+06DC) için kullanılır; "
                "diğer durak işaretleri geleneksel — yorum içerebilir.",
    })
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Yazıldı: {TARGET.relative_to(ROOT)} ({len(veri)} bayt)")
    print(f"sha256: {sha}")
    print("sha256 beklenenle " + ("AYNI" if sha == BEKLENEN_SHA256 else f"FARKLI (beklenen {BEKLENEN_SHA256})"))
    print("Denklik: 6236/6236 ayet aynı (işaretler ve tatvil çıkarılınca).")
    print("İşaret sayıları:", {f"U+{ord(c):04X}": n for c, n in sorted(sayim.items())}, "| eklenen tatvil:", tatvil_farki)
    print("Tek başına sekte:", ", ".join(f"{s}:{a}" for s, a in sekte))


if __name__ == "__main__":
    from tezgah import utf8_akislar
    utf8_akislar()
    main()
