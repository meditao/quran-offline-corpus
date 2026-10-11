#!/usr/bin/env python3
"""İman–tevekkül karşılaştırması için sabit QAC v0.4 üzerinde yeniden üretilebilir tarama.

Ham katmanlar salt okunur. Anlam ve tarih hükmü üretilmez; kök, lemma,
bap, kelime konumu ve ayet birlikte geçişi ayrı sorgularla raporlanır.
Çalıştırma: python 08_scripts/analyze_tawakkul_comparison.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

DEPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(DEPO / "09_calisma_masasi"))
from tezgah.okunus import TANZIL_YOLU, ayet_oku, lemma_okunusu, tanzil  # noqa: E402
from tezgah.veri import QAC_YOLU, kok_latin, sha256, yukle  # noqa: E402

CIKTI = DEPO / "07_analyses" / "generated" / "tawakkul_comparison"
KOMUT = "python 08_scripts/analyze_tawakkul_comparison.py"
SURUM = "1.0.0"
IMAN = "<iyma`n"
KOKLER = ("Amn", "wkl", "fwD")
# Bu ayetler yorum sonucu değil, karşılaştırmanın elle okunacak inceleme örneklemidir.
SECILI = (
    (3, 121), (3, 122), (3, 152), (3, 153), (3, 154), (3, 155), (3, 159), (3, 160), (3, 165),
    (3, 172), (3, 173), (5, 23), (6, 66), (6, 89), (6, 102), (6, 107), (8, 2), (10, 84), (10, 108),
    (12, 17), (12, 66), (12, 67), (12, 68), (14, 12), (17, 68),
    (17, 2), (17, 54), (25, 58), (32, 11), (33, 3), (39, 41), (39, 62),
    (40, 28), (40, 38), (40, 39), (40, 40), (40, 41), (40, 42), (40, 43), (40, 44), (40, 45),
    (64, 13), (65, 3), (67, 29), (73, 9), (106, 4),
)


def ref(anahtar):
    """Sıralama sayısal anahtarla yapılır; bu işlev yalnız gösterim içindir."""
    return ":".join(map(str, anahtar))


def say(segler):
    return {
        "kelime_konumu": len({s.kelime_anahtari for s in segler}),
        "segment": len(segler),
        "ayet": len({(s.sure, s.ayet) for s in segler}),
        "sure": len({s.sure for s in segler}),
    }


def ozet(segler):
    return {
        **say(segler),
        "kelime_konumlari": [ref(x) for x in sorted({s.kelime_anahtari for s in segler})],
        "ayetler": [ref(x) for x in sorted({(s.sure, s.ayet) for s in segler})],
    }


def bab(s):
    # QAC'ta I. bap yazılmaz. İsme kendiliğinden I. bap atanmaz.
    return s.bab or ("I" if s.etiket == "V" else "işaretsiz")


def dogrula(kosul, mesaj):
    # python -O altında da denetimler kapatılmaz.
    if not kosul:
        raise ValueError(mesaj)


def csv_yaz(ad, satirlar):
    dogrula(bool(satirlar), f"Boş CSV beklenmiyordu: {ad}")
    with (CIKTI / ad).open("w", encoding="utf-8", newline="\n") as dosya:
        yazici = csv.DictWriter(dosya, fieldnames=list(satirlar[0]), lineterminator="\n")
        yazici.writeheader()
        yazici.writerows(satirlar)


def metin_yaz(ad, metin):
    with (CIKTI / ad).open("w", encoding="utf-8", newline="\n") as dosya:
        dosya.write(metin)


def kaynak_kaydi(yol, ad, statü):
    return {"ad": ad, "yol": yol.relative_to(DEPO).as_posix(), "sha256": sha256(yol), "statü": statü}


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    kor = yukle()  # Kaynak hash'i ve ham satır yapısı mevcut kanonik ayrıştırıcıda denetlenir.
    metinler = tanzil()  # Tanzil hash'i de denetlenir; QAC kelime sırasına eşlenmez.
    temel = {
        "segment": len(kor.segmentler), "kelime_konumu": len(kor.kelimeler),
        "ayet": len(kor.ayet_segmentleri), "sure": len(kor.sureler),
        "benzersiz_kok": len(kor.kok_kelimeleri),
    }
    dogrula(temel == {"segment": 128219, "kelime_konumu": 77429,
                      "ayet": 6236, "sure": 114, "benzersiz_kok": 1642}, "Kanonik korpus sayımı değişti")
    dogrula(kor.telif_blogu, "QAC telif bloğu bulunamadı")
    dogrula(set(kor.ayet_segmentleri) == set(metinler), "QAC–Tanzil ayet anahtarları farklı")
    dogrula(len({s.konum for s in kor.segmentler}) == len(kor.segmentler), "Yinelenen segment konumu")

    kok_segleri = {k: [s for s in kor.segmentler if s.kok == k] for k in KOKLER}
    beklenen = {"Amn": (879, 723, 77), "wkl": (70, 61, 29), "fwD": (1, 1, 1)}
    for k, deger in beklenen.items():
        olcum = say(kok_segleri[k])
        dogrula(tuple(olcum[x] for x in ("kelime_konumu", "ayet", "sure")) == deger,
                 f"Kök sayımı değişti: {k}")

    sorgular = {
        "Amn_IV_fiil": [s for s in kok_segleri["Amn"] if s.etiket == "V" and s.bab == "IV"],
        "Amn_IV_tum_turler": [s for s in kok_segleri["Amn"] if s.bab == "IV"],
        "iman_isim_lemmasi": [s for s in kor.segmentler if s.lemma == IMAN and s.etiket == "N"],
        "wkl_V_fiil": [s for s in kok_segleri["wkl"] if s.etiket == "V" and s.bab == "V"],
        "wkl_V_isim": [s for s in kok_segleri["wkl"] if s.etiket == "N" and s.bab == "V"],
        "wakil_isim_lemmasi": [s for s in kok_segleri["wkl"] if s.lemma == "wakiyl" and s.etiket == "N"],
        "wkl_II_fiil": [s for s in kok_segleri["wkl"] if s.etiket == "V" and s.bab == "II"],
        "fwD_II_fiil": [s for s in kok_segleri["fwD"] if s.etiket == "V" and s.bab == "II"],
    }
    for ad, n in {"Amn_IV_fiil": 537, "Amn_IV_tum_turler": 812, "iman_isim_lemmasi": 45,
                  "wkl_V_fiil": 40, "wkl_V_isim": 4, "wakil_isim_lemmasi": 24,
                  "wkl_II_fiil": 2, "fwD_II_fiil": 1}.items():
        dogrula(say(sorgular[ad])["kelime_konumu"] == n, f"Alt sorgu sayımı değişti: {ad}")
    dogrula({s.kelime_anahtari for s in sorgular["wkl_II_fiil"]} == {(6, 89, 12), (32, 11, 6)},
             "wkl II. bap örnekleri değişti")
    dogrula({s.kelime_anahtari for s in sorgular["fwD_II_fiil"]} == {(40, 44, 5)},
             "fwD örneği değişti")
    dizin = {s.konum: s for s in kor.segmentler}
    a106 = dizin["106:4:5:2"]
    m12 = dizin["12:17:14:2"]
    dogrula((a106.kok, a106.lemma, a106.bab, a106.etiket) == ("Amn", "'aAmana", "IV", "V"),
             "106:4 IV. bap fiil anotasyonu değişti")
    dogrula((m12.kok, m12.lemma, m12.bab, m12.etiket) == ("Amn", "mu&omin", "IV", "N")
             and {"ACT", "PCPL"} <= m12.etiketler, "12:17 ism-i fâil anotasyonu değişti")

    def ayet_kumesi(segler):
        return {(s.sure, s.ayet) for s in segler}

    wkl_ayetleri = ayet_kumesi(kok_segleri["wkl"])
    birlikte = {}
    for ad, sol, sag in (
        ("Amn_koku_ve_wkl_koku", kok_segleri["Amn"], kok_segleri["wkl"]),
        ("iman_isim_lemmasi_ve_wkl_koku", sorgular["iman_isim_lemmasi"], kok_segleri["wkl"]),
        ("Amn_koku_ve_wkl_V_fiil", kok_segleri["Amn"], sorgular["wkl_V_fiil"]),
        ("iman_isim_lemmasi_ve_wkl_V_fiil", sorgular["iman_isim_lemmasi"], sorgular["wkl_V_fiil"]),
    ):
        ortak = ayet_kumesi(sol) & ayet_kumesi(sag)
        birlikte[ad] = {"birim": "ayet", "sayim": len(ortak), "ayetler": [ref(x) for x in sorted(ortak)]}
    dogrula(birlikte["Amn_koku_ve_wkl_koku"]["sayim"] == 17, "Kök birlikte geçişi değişti")
    dogrula(birlikte["iman_isim_lemmasi_ve_wkl_koku"]["ayetler"] == ["3:173", "8:2"],
             "İman isim lemması birlikte geçişi değişti")

    dagilim = []
    for k in KOKLER:
        gruplar = defaultdict(list)
        for s in kok_segleri[k]:
            gruplar[(s.lemma, s.etiket, bab(s))].append(s)
        for (lemma, tur, kalip), segler in sorted(gruplar.items()):
            dagilim.append({"kok_bw": k, "kok_latin": kok_latin(k), "lemma_bw": lemma,
                            "lemma_latin": lemma_okunusu(lemma).gosterim, "tur": tur,
                            "bap": kalip, **ozet(segler)})

    kaynaklar = [
        kaynak_kaydi(QAC_YOLU, "QAC v0.4", "kanonik morfoloji anotasyonu"),
        kaynak_kaydi(TANZIL_YOLU, "Tanzil Uthmani v1.1", "ayet metni; Latin aktarımı delil değildir"),
    ]
    kodlar = [Path(__file__).resolve(), *(DEPO / "09_calisma_masasi" / "tezgah" / x
                               for x in ("__init__.py", "veri.py", "harf.py", "okunus.py"))]
    kaynaklar += [kaynak_kaydi(p, p.name, "üretim kodu") for p in kodlar]
    sonuc = {
        "sema_surumu": 1, "betik_surumu": SURUM, "komut": KOMUT,
        "durum": "çalıştırıldı", "kaynaklar": kaynaklar, "korpus_denetimi": temel,
        "kok_sayimlari": {k: {"kok_latin": kok_latin(k), **ozet(kok_segleri[k])} for k in KOKLER},
        "sorgular": {ad: ozet(ss) for ad, ss in sorgular.items()}, "lemma_tur_bap_dagilimi": dagilim,
        "birlikte_gecis": birlikte,
        "sinirlar": [
            "Kök ve lemma sayımı kelime konumunda tekilleştirilir; segment sayısı ayrıca verilir.",
            "Bap etiketi fiil ile türemiş isimde ayrı değerlendirilir; etiketler tam eşleştirilir.",
            "Ayet içi birlikte geçiş yalnız aday bulur; anlam özdeşliği, zorunlu sıra veya nedensellik ispatlamaz.",
            "Amn kökü bütün geçişlerinde teknik iman terimi değildir; 17:68 kök kesişiminde güvenlik bağlamını içerir.",
            "106:4 IV. bap anotasyonunu, 12:17 IV. bap ism-i fâil anotasyonunu gösterir; anlam hükmü bağlam gerektirir.",
            "Tanzil ayetleri yalnız ayet anahtarıyla eşleştirilir; QAC kelime sırası Tanzil token sırası yerine kullanılmaz.",
            "Okunuş aktarımı yorum/delil değildir; belirsizlik alanları korunur.",
            "Bu tarama Uhud tarihini, Kur'an öncesi anlamı veya kavramsal yokluğu kanıtlamaz.",
        ],
    }

    kelimeler = {k.anahtar: k for k in kor.kelimeler}
    ayet_kelimeleri = defaultdict(list)
    for k in kor.kelimeler:
        ayet_kelimeleri[k.anahtar[:2]].append(k)
    gorunum = {}
    # Her wkl ayetinin aynı sûre içindeki önceki/sonraki ayeti; ayrıca 3:121–180 pasajı.
    incelenecek = wkl_ayetleri | set(SECILI) | {(3, a) for a in range(121, 181)}
    for s, a in list(incelenecek):
        incelenecek |= {(s, n) for n in (a - 1, a + 1) if (s, n) in metinler}
    for s, a in sorted(incelenecek):
        aktarim = ayet_oku(s, a, metinler[(s, a)])
        gorunum[(s, a)] = {
            "ayet": ref((s, a)), "qac_kaynak": f"https://corpus.quran.com/wordbyword.jsp?chapter={s}&verse={a}",
            "onceki_ayet": ref((s, a - 1)) if (s, a - 1) in metinler else "",
            "sonraki_ayet": ref((s, a + 1)) if (s, a + 1) in metinler else "",
            "ayet_latin": aktarim.latin, "okunus_belirsizlikleri": "; ".join(aktarim.belirsiz),
            "tanzil_ayet_uthmani": metinler[(s, a)],
            "qac_ayet_bw": " ".join(k.bicim for k in ayet_kelimeleri[(s, a)]),
        }
    satirlar = []
    for s in kor.segmentler:
        if s.kok not in KOKLER:
            continue
        k = kelimeler[s.kelime_anahtari]
        satirlar.append({
            "kok_bw": s.kok, "kok_latin": kok_latin(s.kok), "kelime_konumu": k.konum,
            "segment_konumu": s.konum, "ayet": ref((s.sure, s.ayet)), "kelime_bw": k.bicim,
            "govde_bw": s.bicim, "lemma_bw": s.lemma, "lemma_latin": lemma_okunusu(s.lemma).gosterim,
            "tur": s.etiket, "bap": bab(s), "ozellikler": "|".join(s.ozellikler),
            "kelimenin_tum_segmentleri": " ; ".join(f"{z.konum} {z.bicim} {z.etiket} {'|'.join(z.ozellikler)}" for z in k.segmentler),
            "kaynak": f"https://corpus.quran.com/wordmorphology.jsp?location=({s.sure}:{s.ayet}:{s.kelime})",
        })
    secili_segmentler = []
    for anahtar in sorted(SECILI):
        for s in kor.ayet_segmentleri[anahtar]:
            secili_segmentler.append({"ayet": ref(anahtar), "segment_konumu": s.konum,
                                      "bicim_bw": s.bicim, "tur": s.etiket,
                                      "ozellikler": "|".join(s.ozellikler)})

    md = ["# İman–tevekkül karşılaştırması: mekanik QAC taraması", "",
          f"Betik sürümü: {SURUM}. Bu rapor `{KOMUT}` ile üretilir; elle düzenlenmez.", "",
          "Anlam değerlendirmesi için [analiz dizinine](../../README.md) bakın. Sayım tek başına kavram tanımı değildir.", "",
          "## Kök sayımları", "", "| Kök | Kelime konumu | Segment | Ayet | Sûre |", "|---|---:|---:|---:|---:|"]
    for k in KOKLER:
        n = say(kok_segleri[k])
        md.append(f"| {kok_latin(k)} (`{k}`) | {n['kelime_konumu']} | {n['segment']} | {n['ayet']} | {n['sure']} |")
    md += ["", "## Tam eşleşen alt sorgular", "", "| Sorgu | Kelime konumu | Segment | Ayet | Sûre |", "|---|---:|---:|---:|---:|"]
    for ad, ss in sorgular.items():
        n = say(ss)
        md.append(f"| `{ad}` | {n['kelime_konumu']} | {n['segment']} | {n['ayet']} | {n['sure']} |")
    md += ["", "## Lemma, tür ve bap ayrımı", "", "| Kök | Lemma | Tür | Bap | Kelime konumu |", "|---|---|---|---|---:|"]
    for r in dagilim:
        md.append(f"| {r['kok_latin']} | {r['lemma_latin']} | {r['tur']} | {r['bap']} | {r['kelime_konumu']} |")
    md += ["", "## Aynı ayette birlikte geçiş", "",
           "Pencere tam ayettir. Bu çıktı sözdizimi bağı, eşanlamlılık, nedensellik veya zorunlu aşama sırası kurmaz.", ""]
    for ad, r in birlikte.items():
        md.append(f"- `{ad}`: **{r['sayim']} ayet** — {', '.join(r['ayetler'])}.")
    md += ["", "Kök düzeyindeki kesişimde 17:68 de vardır; bu yüzden bütün kesişimleri iman–tevekkül bağı diye saymak yanlıştır.", "",
           "## Kritik morfoloji denetimleri", "",
           "- **106:4:5:2**: `'aAmana`, `TAG:V`, `(IV)`, `ROOT:Amn`; 537 IV. bap fiil sayımına dahildir. IV. bap tek bir anlama eşitlenemez.",
           "- **12:17:14:2**: `mu&omin`, `TAG:N`, `ACT|PCPL|(IV)`, `ROOT:Amn`; fiil veya iman isim lemması değildir. 12:17:14:1 `bi` öneki, 12:17:15:1 `la` edatı ayrıca kayıttadır.",
           "- **6:89:12; 32:11:6**: w-k-l II. bap fiilleri; V. bap tevekkül fiilleriyle birleştirilmez.",
           "- **40:44:5:2**: `>ufaw~iDu`, `TAG:V`, `(II)`, `ROOT:fwD`; bu kök için taramada tek kelime konumu. Teknik tafvîż isim teriminin geçtiği sonucu çıkmaz.", "",
           "## Bütün w-k-l geçişleri", "",
           "Aşağıdaki liste tamdır. Ayetin tamamı, komşu ayet anahtarları ve aktarım belirsizlikleri `verse_lookup.csv` içindedir. Kelime biçimleri teknik Buckwalter verisidir; lemma okunuşu ayrıca gösterilir.", "",
           "| Kelime konumu | Lemma okunuşu | Kelime biçimi (BW) | Tür | Bap |", "|---|---|---|---|---|"]
    for r in satirlar:
        if r["kok_bw"] == "wkl":
            md.append(f"| [{r['kelime_konumu']}]({r['kaynak']}) | {r['lemma_latin']} | `{r['kelime_bw']}` | {r['tur']} | {r['bap']} |")
    md += ["", "## Seçilmiş ayet görünümü", "", "Latin aktarımı Tanzil ayetinden üretilir; bağımsız anlam delili değildir.", ""]
    for anahtar in sorted(SECILI):
        r = gorunum[anahtar]
        md.append(f"- **{r['ayet']}**: {r['ayet_latin']}")
        if r["okunus_belirsizlikleri"]:
            md.append(f"  Aktarım notu: {r['okunus_belirsizlikleri']}")
    md += ["", "## Sınırlar", "", *[f"- {x}" for x in sonuc["sinirlar"]], "",
           "## Kaynak ve yeniden üretim", "",
           "[Quranic Arabic Corpus](https://corpus.quran.com/download/), QAC v0.4, Copyright (C) 2011 Kais Dukes; özgün telif bloğu `source_notice.txt` içinde korunur.", "",
           "[Tanzil](https://tanzil.net/docs/download), Uthmani v1.1; bu dosyada ayet metninin kurallı Latin aktarımı kullanılır. Kaynak metin değiştirilmez.", "",
           "`summary.json`: kaynak ve üretim kodu hash'leri, tam sayımlar, her alt sorgunun bütün konumları.",
           "`occurrences.csv`: üç kökün bütün kök taşıyan segmentleri ve ait oldukları kelimenin segmentleri.",
           "`selected_segments.csv`: kritik ayetlerin tüm segmentleri; `verse_lookup.csv`: w-k-l ayetleri, komşuları ve 3:121–180 bağlamı.", "",
           f"Kaynak      : QAC v0.4 + Tanzil Uthmani v1.1 (yalnız aktarım)\n"
           f"Sayım birimi: kelime konumu | segment | ayet | sûre\nSorgu       : {KOMUT}\n"
           f"Veri izi    : {kor.sha256[:12]}\nDurum       : çalıştırıldı", ""]

    CIKTI.mkdir(parents=True, exist_ok=True)
    metin_yaz("summary.json", json.dumps(sonuc, ensure_ascii=False, indent=2) + "\n")
    csv_yaz("occurrences.csv", satirlar)
    csv_yaz("selected_segments.csv", secili_segmentler)
    csv_yaz("verse_lookup.csv", list(gorunum.values()))
    metin_yaz("report.md", "\n".join(md))
    # Ham dosyanın telif metni değiştirilmez; üretilmiş ek dosyaya kopyalanır.
    telif = QAC_YOLU.read_text(encoding="utf-8-sig").split("LOCATION\tFORM\tTAG\tFEATURES", 1)[0]
    telif += "\n" + "\n".join(x for x in TANZIL_YOLU.read_text(encoding="utf-8-sig").splitlines()
                               if x.startswith("#")) + "\n"
    metin_yaz("source_notice.txt", telif)
    manifest = {
        "betik_surumu": SURUM,
        "dosyalar": {ad: hashlib.sha256((CIKTI / ad).read_bytes()).hexdigest() for ad in
                     ("summary.json", "occurrences.csv", "selected_segments.csv", "verse_lookup.csv", "report.md", "source_notice.txt")},
    }
    metin_yaz("manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    for k in KOKLER:
        print(f"{k}: {say(kok_segleri[k])}")
    print(f"Birlikte geçiş (kök): {birlikte['Amn_koku_ve_wkl_koku']['sayim']} ayet")
    print(f"Üretildi: {CIKTI.relative_to(DEPO).as_posix()}")


if __name__ == "__main__":
    main()
