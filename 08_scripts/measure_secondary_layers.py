#!/usr/bin/env python3
"""İkincil katman ölçümleri (Aşama 5): Lane kapsamı ve Sâmî gürültü tabanı, QAC v0.4'ün kökleri üzerinden.

Önkoşul (veriler depoya işlenmez):
    cd 09_calisma_masasi && python -m tezgah kur lane && python -m tezgah kur sedra

Çıktılar: 03_indices/audits/ikincil_katmanlar.{md,json}

Ölçümler bu depodaki QAC köklerine göre yapılır; başka korpus ya da araçtan aktarılmış sayı yoktur.
Her iki katman da hipotez kaynağıdır, delil değildir.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "09_calisma_masasi"))
from tezgah import veri  # noqa: E402
from tezgah.ikincil import lane, sami  # noqa: E402

OUT = ROOT / "03_indices" / "audits"


def yuzde(x: float) -> str:
    return f"%{100 * x:.1f}".replace(".", ",")


def binlik(n: int) -> str:
    return f"{n:,}".replace(",", ".")


def hesapla() -> dict:
    if lane.baglanti() is None or sami.suryanice() is None:
        raise SystemExit("Lane ve SEDRA kurulu olmalı: python -m tezgah kur lane / kur sedra")
    kor = veri.korpus()
    k = lane.kapsam(kor)
    g = sami.gurultu(10, 20260924)
    ozet = {
        "qac_sha256": kor.sha256, "lane_sqlite_sha256": lane.SQLITE_SHA256, "lane_commit": lane.LANE_COMMIT,
        "ibranice_dizin_sha256": veri.sha256(sami.IBRANICE_YOLU), "sedra_commit": sami.SEDRA_COMMIT,
        "lane_kapsam": {**k, "zayif": [list(z) for z in k["zayif"]]},
        "sami_gurultu": g,
        "envanter": {"ibranice_kok": len(sami.ibranice()), "sedra_kok": len(sami.suryanice()),
                     "sedra_bagsiz": sami.sedra_bagsiz()},
    }
    e = k["eslesme"]
    md = [
        "# İkincil katmanlar — Lane kapsamı ve Sâmî gürültü tabanı",
        "",
        "Üretici: `08_scripts/measure_secondary_layers.py`. Her iki katman da **hipotez kaynağıdır, delil değildir**. "
        f"Ölçümler QAC v0.4'ün {binlik(k['qac_kok'])} kökü üzerinden bu depoda yapıldı (birim: kök).",
        "",
        "## Lane (LexiconDatabase v1.0.9)",
        "",
        f"Lane geneli: {binlik(k['lane_kok'])} kök, {binlik(k['lane_madde'])} madde.",
        "",
        "| eşleşme | kök | oran |",
        "|---|---:|---:|",
        *[f"| {ad} | {binlik(e.get(ad, 0))} | {yuzde(e.get(ad, 0) / k['qac_kok'])} |" for ad in ("tam", "kural", "zayıf", "yok")],
        "",
        "- **tam**: hemze yazımı ve harekeler nötrlenince aynı kök.",
        "- **kural**: Lane'in yazım geleneği — ikiz kök iki harfle (C1C2C2 → C1C2), yinelemeli dörtlü kısaltılmış (C1C2C1C2 → C1C2).",
        "- **zayıf** (`<< DOĞRULA`, elle denetlenir): " + ", ".join(f"`{a}` ({kr.split(': ', 1)[1]})" for a, kr in k["zayif"]),
        f"- **yok**: {', '.join(f'`{x}`' for x in k['eslesmeyen'])}. Bölge: {k['eslesmeyen_bolge']}.",
        "",
        "Bölge yoğunluğu (madde / kök). ك-ي bölgesi Lane'in ölümünden sonra derlendi; bu bölgede \"Lane'de yok\" argümanı kurulamaz:",
        "",
        "| bölge | kök | madde | madde/kök |",
        "|---|---:|---:|---:|",
        *[f"| {b} | {binlik(k['bolge_kok'][b])} | {binlik(k['bolge_madde'][b])} | {str(k['bolge_yogunluk'][b]).replace('.', ',')} |"
          for b in sorted(k["bolge_kok"])],
        "",
        "Veri notu: LexiconDatabase kök tablosunda harekeli yazılmış kökler vardır (ör. `جَهِلَ`); eşleştirme harekeleri siler.",
        "",
        "## Sâmî gürültü tabanı",
        "",
        f"İbranice: depodaki `04_lexicons/generated/hebrew_lexical_index.tsv` ({binlik(ozet['envanter']['ibranice_kok'])} kök, "
        f"sonu-harfleri ve harekeler normalleştirilmiş). Süryanice: SEDRA 3 ({binlik(ozet['envanter']['sedra_kok'])} kök yazımı; "
        f"köke bağlanmamış kayıt atlandı: sözcük {ozet['envanter']['sedra_bagsiz']['LEXEMES.TXT']}, anlam "
        f"{ozet['envanter']['sedra_bagsiz']['ENGLISH.TXT']}). Denklik tablosu: `python -m tezgah sami denklik`.",
        "",
        f"Yöntem: {binlik(g['kok'])} gerçek QAC kökü ile aynı harf ve uzunluk dağılımından üretilmiş {g['tekrar']} × "
        f"{binlik(g['kok'])} sahte kök (tohum {g['tohum']}; gerçek köklerle çakışanlar atıldı) aynı işlemden geçirildi.",
        "",
        "| dil | gerçek vuruş | rastgele vuruş (ort.; en az–en çok) | gürültü payı |",
        "|---|---:|---:|---:|",
        *[f"| {ad} | {yuzde(g['gercek'][d])} | {yuzde(g['rastgele'][d]['ortalama'])} ({yuzde(g['rastgele'][d]['en_az'])}–"
          f"{yuzde(g['rastgele'][d]['en_cok'])}) | {yuzde(g['gurultu_payi'][d])} |"
          for d, ad in (("ibranice", "İbranice"), ("suryanice", "Süryanice"), ("ikisi", "ikisi birden"))],
        "",
        "Kurallar: kognat anlam değildir; tek dildeki vuruş tek başına raporlanmaz; \"aday yok\" bulgu değildir; İbranice ve "
        "Süryanice bağımsız iki tanık değildir. SEDRA verisi değiştirilmiş hâliyle dağıtılamaz ve depoya işlenmez; sonuç "
        "yayımlanırsa atıf zorunludur (`python -m tezgah sami atif`).",
        "",
    ]
    return {"ozet": ozet, "md": md}


def main() -> int:
    h = hesapla()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "ikincil_katmanlar.json").write_text(json.dumps(h["ozet"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "ikincil_katmanlar.md").write_text("\n".join(h["md"]), encoding="utf-8")
    print("\n".join(h["md"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
