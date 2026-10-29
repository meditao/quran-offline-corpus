#!/usr/bin/env python3
"""Ankebût 29:43'teki *el-ʿâlimûn* için sabit QAC v0.4 üzerinde yeniden üretilebilir tarama.

Ham katmanlar salt okunur. Anlam hükmü üretilmez; lemma, kalıp, ayet birlikte
geçişi ve kişi/özne sınıflaması ayrı sorgularla raporlanır. Allah/insan ayrımı
ve "insan için ʿalîm" listesi elle yapılmış inceleme kararıdır; betik bu kararları
sabit küme olarak taşır ve korpusla tutarlılığını denetler.
Çalıştırma: python 08_scripts/analyze_alim_29_43.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

DEPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(DEPO / "09_calisma_masasi"))
from tezgah.okunus import TANZIL_YOLU, ayet_oku, tanzil  # noqa: E402
from tezgah.veri import QAC_YOLU, kok_latin, sha256, yukle  # noqa: E402

CIKTI = DEPO / "07_analyses" / "generated" / "alim_29_43"
KOMUT = "python 08_scripts/analyze_alim_29_43.py"
SURUM = "1.0.0"

ALIM = "Ea`lim"          # ʿâlim (ism-i fâil)
ALIM_COGUL_DISI = "Ea`lamiyn"  # ʿâlemîn — ayrı lemma, aynı ünsüz iskeleti
ALIYM = "Ealiym"         # ʿalîm; QAC ʿulemâʾ çoğulunu da bu lemmaya bağlar
ILM = "Eilom"
ALIMA = "Ealima"
ITTAHAZA = "{t~axa*a"

# Elle inceleme kararı: ʿâlim lemmasının insan için kullanıldığı ayetler.
# Diğer 15 kelime konumunun öznesi/nitelediği Allah'tır (ʿâlimu'l-ğayb… ; 21:51, 21:81 "kunnâ … ʿâlimîn").
ALIM_INSAN = {(12, 44), (29, 43), (30, 22)}
# Elle inceleme kararı: ʿalîm lemmasının açıkça insan için kullanıldığı ayetler
# (bilgin sihirbaz ×5, Yûsuf, oğul müjdesi ×2, ʿulemâʾ ×2). 12:76 tartışmalıdır, ayrı tutulur.
ALIYM_INSAN = {(7, 109), (7, 112), (10, 79), (26, 34), (26, 37), (12, 55), (15, 53), (51, 28), (26, 197), (35, 28)}
ALIYM_TARTISMALI = {(12, 76)}

SECILI = sorted({
    (29, 3), (29, 8), (29, 10), (29, 11), (29, 35), (29, 39), (29, 40), (29, 41), (29, 42), (29, 43),
    (29, 44), (29, 45), (29, 47), (29, 49), (29, 61), (29, 63), (29, 64),
    (12, 43), (12, 44), (12, 55), (12, 76), (30, 7), (30, 20), (30, 21), (30, 22), (30, 23), (30, 24),
    (35, 27), (35, 28), (26, 197), (39, 9), (2, 44), (2, 75), (2, 102), (2, 103), (16, 41), (39, 26),
    (68, 33), (28, 78), (28, 79), (28, 80), (59, 21), (22, 46), (22, 54), (45, 23), (40, 83), (53, 28),
    (16, 68), (7, 74), (9, 31), (16, 43), (21, 7), (47, 16), (17, 107), (34, 6), (58, 11), (16, 27),
    (30, 56), (7, 109), (26, 34), (15, 53), (51, 28), (45, 24), (6, 148), (4, 157),
})


def ref(anahtar):
    return ":".join(map(str, anahtar))


def sirala(kume):
    return [ref(x) for x in sorted(kume)]


def dogrula(kosul, mesaj):
    if not kosul:
        raise ValueError(mesaj)


def iskelet(bw):
    """Buckwalter biçiminden ünlü/işaretleri atarak ünsüz iskeleti üretir (yalnız karşılaştırma için)."""
    return re.sub(r"[aiuoFNK~`^@\[\]{}#:;,.'\"+]", "", bw)


def metin_yaz(ad, metin):
    with (CIKTI / ad).open("w", encoding="utf-8", newline="\n") as dosya:
        dosya.write(metin)


def csv_yaz(ad, satirlar):
    dogrula(bool(satirlar), f"Boş CSV beklenmiyordu: {ad}")
    with (CIKTI / ad).open("w", encoding="utf-8", newline="\n") as dosya:
        yazici = csv.DictWriter(dosya, fieldnames=list(satirlar[0]), lineterminator="\n")
        yazici.writeheader()
        yazici.writerows(satirlar)


def kaynak_kaydi(yol, ad, statu):
    return {"ad": ad, "yol": yol.relative_to(DEPO).as_posix(), "sha256": sha256(yol), "statü": statu}


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    kor = yukle()
    metinler = tanzil()
    temel = {"segment": len(kor.segmentler), "kelime_konumu": len(kor.kelimeler),
             "ayet": len(kor.ayet_segmentleri), "sure": len(kor.sureler), "benzersiz_kok": len(kor.kok_kelimeleri)}
    dogrula(temel == {"segment": 128219, "kelime_konumu": 77429, "ayet": 6236, "sure": 114, "benzersiz_kok": 1642},
            "Kanonik korpus sayımı değişti")
    dogrula(kor.telif_blogu, "QAC telif bloğu bulunamadı")

    ayet_kelimeleri = defaultdict(list)
    for k in kor.kelimeler:
        ayet_kelimeleri[k.anahtar[:2]].append(k)

    def lemma_kelimeleri(lemma):
        return [k for k in kor.kelimeler if lemma in k.lemmalar]

    def say(kelimeler):
        return {"kelime_konumu": len(kelimeler), "ayet": len({k.anahtar[:2] for k in kelimeler}),
                "sure": len({k.sure for k in kelimeler})}

    sonuc = {}
    # 1. Kök sayımları
    kokler = {}
    for kok in ("Elm", "Eql", "Ax*", "Enkb"):
        kk = kor.kok_kelimeleri.get(kok, [])
        kokler[kok] = {"kok_latin": kok_latin(kok), **say(kk)}
    dogrula((kokler["Elm"]["kelime_konumu"], kokler["Elm"]["ayet"], kokler["Elm"]["sure"]) == (854, 728, 85), "Elm sayımı değişti")
    dogrula((kokler["Eql"]["kelime_konumu"], kokler["Eql"]["ayet"], kokler["Eql"]["sure"]) == (49, 49, 30), "Eql sayımı değişti")

    # 2. ʿ-l-m lemma dağılımı
    lemma_say = defaultdict(set)
    for k in kor.kok_kelimeleri["Elm"]:
        for s in k.segmentler:
            if s.kok == "Elm":
                lemma_say[s.lemma].add(k.anahtar)
    lemma_dagilimi = {l: len(v) for l, v in sorted(lemma_say.items(), key=lambda x: -len(x[1]))}
    dogrula(lemma_dagilimi[ALIM] == 18 and lemma_dagilimi[ALIYM] == 163, "ʿâlim/ʿalîm lemma sayımı değişti")

    # 3. ʿâlim'in bütün geçişleri ve özne sınıfı
    alim_satir = []
    for k in lemma_kelimeleri(ALIM):
        s = next(x for x in k.segmentler if x.lemma == ALIM)
        sinif = "insan" if k.anahtar[:2] in ALIM_INSAN else "Allah"
        sonraki = [z for z in ayet_kelimeleri[k.anahtar[:2]] if z.kelime == k.kelime + 1]
        alim_satir.append({"kelime_konumu": k.konum, "bicim_bw": k.bicim, "ozellikler": "|".join(s.ozellikler),
                           "sonraki_kelime_bw": sonraki[0].bicim if sonraki else "", "atif": sinif})
    dogrula(len(alim_satir) == 18, "ʿâlim kelime konumu 18 değil")
    dogrula({tuple(map(int, r["kelime_konumu"].split(":")[:2])) for r in alim_satir if r["atif"] == "insan"} == ALIM_INSAN,
            "İnsan için ʿâlim kümesi korpusla uyuşmuyor")
    alim_sinif = {"Allah": sum(r["atif"] == "Allah" for r in alim_satir), "insan": sum(r["atif"] == "insan" for r in alim_satir)}

    # 4. ʿulemâʾ (ʿalîm, çoğul) ve insan için ʿalîm
    ulema = sorted({k.anahtar[:2] for k in lemma_kelimeleri(ALIYM)
                    if any(s.lemma == ALIYM and "MP" in s.ozellikler for s in k.segmentler)})
    dogrula(set(ulema) == {(26, 197), (35, 28)}, "ʿulemâʾ geçişleri değişti")
    aliym_ayetleri = {k.anahtar[:2] for k in lemma_kelimeleri(ALIYM)}
    dogrula(ALIYM_INSAN | ALIYM_TARTISMALI <= aliym_ayetleri, "İnsan için ʿalîm kümesinde ʿalîm geçmeyen ayet var")

    # 5. ʿâlim / ʿâlemîn ünsüz iskeleti
    iskeletler = defaultdict(set)
    for lemma in (ALIM, ALIM_COGUL_DISI):
        for k in lemma_kelimeleri(lemma):
            s = next(x for x in k.segmentler if x.lemma == lemma)
            if "MP" in s.ozellikler:
                iskeletler[iskelet(s.bicim)].add((lemma, k.konum))
    ortak_iskelet = {i: {"alim_konumlari": sorted(k for l, k in v if l == ALIM),
                         "alemin_kelime_konumu_sayisi": sum(1 for l, _ in v if l == ALIM_COGUL_DISI)}
                     for i, v in iskeletler.items() if len({l for l, _ in v}) > 1}
    dogrula(bool(ortak_iskelet), "ʿâlimîn/ʿâlemîn ortak iskeleti bulunamadı")

    # 6. ʿ-q-l: tür ve açık nesne zamiri
    aql_nesneli = []
    for k in kor.kok_kelimeleri["Eql"]:
        fiil = next(s for s in k.segmentler if s.kok == "Eql")
        kisi = next((o for o in fiil.ozellikler if re.fullmatch(r"[123][MF]?[SDP]", o)), None)
        nesne = [s.zamir for s in k.segmentler if s.zamir and s.zamir != kisi]
        if nesne:
            aql_nesneli.append({"kelime_konumu": k.konum, "bicim_bw": k.bicim, "fiil_kisi": kisi, "nesne_zamiri": ",".join(nesne)})
    dogrula({r["kelime_konumu"] for r in aql_nesneli} == {"2:75:17", "29:43:6"}, "Nesneli ʿ-q-l fiilleri değişti")
    aql_tur = defaultdict(int)
    for k in kor.kok_kelimeleri["Eql"]:
        s = next(x for x in k.segmentler if x.kok == "Eql")
        aql_tur[s.etiket] += 1
    dogrula(dict(aql_tur) == {"V": 49}, "ʿ-q-l kökünde fiil dışı biçim çıktı")

    # 7. lev kânû yaʿlemûn (ayet sonu, nesnesiz)
    lev = []
    for anahtar, kel in ayet_kelimeleri.items():
        for i in range(len(kel) - 2):
            a, b, c = kel[i], kel[i + 1], kel[i + 2]
            if ("law" in a.lemmalar and "kaAna" in b.lemmalar
                    and any(s.lemma == "kaAna" and "3MP" in s.ozellikler for s in b.segmentler)
                    and any(s.lemma == ALIMA and "IMPF" in s.ozellikler and "3MP" in s.ozellikler for s in c.segmentler)
                    and i + 2 == len(kel) - 1):
                lev.append(anahtar)
    dogrula(sirala(lev) == ["2:102", "2:103", "16:41", "29:41", "29:64", "39:26", "68:33"], "lev kânû yaʿlemûn kümesi değişti")

    # 8. ellezîne ûtû'l-ʿilm
    utu = set()
    for anahtar, kel in ayet_kelimeleri.items():
        for i in range(len(kel) - 1):
            if (any(s.kok == "Aty" and "PASS" in s.ozellikler and "3MP" in s.ozellikler for s in kel[i].segmentler)
                    and ILM in kel[i + 1].lemmalar):
                utu.add(anahtar)
    dogrula(sirala(utu) == ["16:27", "17:107", "22:54", "28:80", "29:49", "30:56", "34:6", "47:16", "58:11"],
            "ûtû'l-ʿilm kümesi değişti")

    # 9. mesel + ḍarb + nâs aynı ayette; tilke'l-emsâl
    mesel = sorted(a for a, segs in kor.ayet_segmentleri.items()
                   if any(s.lemma == "maval" for s in segs) and any(s.kok == "Drb" for s in segs)
                   and any(s.lemma == "n~aAs" for s in segs))
    tilke = sorted(a for a, kel in ayet_kelimeleri.items()
                   for i in range(len(kel) - 1)
                   if "*a`lik" in kel[i].lemmalar and any(s.bicim.startswith("tilo") for s in kel[i].segmentler)
                   and any(s.lemma == "maval" and "MP" in s.ozellikler for s in kel[i + 1].segmentler))
    dogrula(tilke == [(29, 43), (59, 21)], "tilke'l-emsâl kümesi değişti")

    # 10. Ankebût'ta mâ … illâ + belirli çoğul ism-i fâil (sınırlama kalıbı)
    hasr = []
    for (su, ay), kel in ayet_kelimeleri.items():
        if su != 29:
            continue
        for i, k in enumerate(kel[:-1]):
            if "<il~aA" in k.lemmalar and any(s.etiket == "NEG" for z in kel[:i] for s in z.segmentler):
                n = kel[i + 1].segmentler
                if any(s.etiket == "DET" for s in n) and any({"ACT", "PCPL", "MP"} <= set(s.ozellikler) for s in n):
                    hasr.append((su, ay))
    dogrula(sorted(set(hasr)) == [(29, 43), (29, 47), (29, 49)], "Ankebût sınırlama kalıbı kümesi değişti")
    dogrula(len(mesel) == 9, "mesel + ḍarb + nâs kümesi değişti")

    # 11. ittihâz: VIII. bab fiil ve birlikte geçtiği adlar
    itt = [k for k in kor.kok_kelimeleri["Ax*"] if ITTAHAZA in k.lemmalar]
    itt_ayet = {k.anahtar[:2] for k in itt}
    birlikte_itt = {}
    for ad, kosul in (("min_duni", lambda s: s.lemma == "duwn"), ("veli", lambda s: s.lemma == "waliY~"),
                      ("ilah", lambda s: s.lemma == "<ila`h"), ("veled", lambda s: s.lemma == "walad"),
                      ("beyt", lambda s: s.lemma == "bayot")):
        birlikte_itt[ad] = sirala({a for a in itt_ayet if any(kosul(s) for s in kor.ayet_segmentleri[a])})
    itt_disil = sirala({k.anahtar[:2] for k in itt for s in k.segmentler
                        if s.lemma == ITTAHAZA and ("3FS" in s.ozellikler or "2FS" in s.ozellikler)})

    # 12. ʿilm (isim) + ẓ-n-n aynı ayette
    ilm_zan = sirala({a for a, segs in kor.ayet_segmentleri.items()
                      if any(s.lemma == ILM for s in segs) and any(s.kok == "Znn" for s in segs)})

    sonuc = {
        "sema_surumu": 1, "betik_surumu": SURUM, "komut": KOMUT, "durum": "çalıştırıldı",
        "kaynaklar": [kaynak_kaydi(QAC_YOLU, "QAC v0.4", "kanonik morfoloji anotasyonu"),
                      kaynak_kaydi(TANZIL_YOLU, "Tanzil Uthmani v1.1", "ayet metni; Latin aktarımı delil değildir"),
                      kaynak_kaydi(Path(__file__).resolve(), Path(__file__).name, "üretim kodu")],
        "korpus_denetimi": temel,
        "kok_sayimlari": kokler,
        "Elm_lemma_dagilimi_kelime_konumu": lemma_dagilimi,
        "alim_atif_sinifi": alim_sinif,
        "ulema_ayetleri": sirala(ulema),
        "aliym_insan_ayetleri_elle": sirala(ALIYM_INSAN),
        "aliym_tartismali": sirala(ALIYM_TARTISMALI),
        "alim_alemin_ortak_iskelet": ortak_iskelet,
        "aql_tur": dict(aql_tur), "aql_nesneli": aql_nesneli,
        "lev_kanu_yalemun": sirala(lev), "utul_ilm": sirala(utu),
        "mesel_darb_nas": sirala(mesel), "tilkel_emsal": sirala(tilke),
        "ankebut_sinirlama_kalibi": sirala(set(hasr)),
        "ittihaz": {"kelime_konumu": len(itt), "ayet": len(itt_ayet), "birlikte_ayet": birlikte_itt, "disil_cekim_ayet": itt_disil},
        "ilm_zan_birlikte_ayet": ilm_zan,
        "sinirlar": [
            "Sayımlar kelime konumundadır; ayet sayıları ayrıca verilir. Beceri korpusunun (quran-morphology) segment sayıları bu tabloya katılmaz.",
            "Allah/insan ayrımı ve insan için ʿalîm listesi elle verilmiş inceleme kararıdır; korpus etiketi değildir.",
            "Kalıp sorguları yalnız aday bulur; anlam, nedensellik veya eşanlamlılık ispatlamaz.",
            "ʿâlimîn/ʿâlemîn iskelet eşliği yalnız yazım düzeyindedir; kıraat farkı bu veriden çıkmaz.",
            "Okunuş aktarımı yorum/delil değildir.",
        ],
    }

    gorunum = []
    for s, a in SECILI:
        aktarim = ayet_oku(s, a, metinler[(s, a)])
        gorunum.append({"ayet": ref((s, a)), "ayet_latin": aktarim.latin,
                        "okunus_belirsizlikleri": "; ".join(aktarim.belirsiz),
                        "tanzil_ayet_uthmani": metinler[(s, a)],
                        "qac_ayet_bw": " ".join(k.bicim for k in ayet_kelimeleri[(s, a)])})

    md = ["# Ankebût 29:43 — *el-ʿâlimûn*: mekanik QAC taraması", "",
          f"Betik sürümü: {SURUM}. Bu rapor `{KOMUT}` ile üretilir; elle düzenlenmez.", "",
          "Anlam değerlendirmesi: [Âlim kavram kartı](../../roots/Alim-concept-card.md). Sayım tek başına kavram tanımı değildir.", "",
          "## Kök sayımları (kelime konumu)", "", "| Kök | Kelime konumu | Ayet | Sûre |", "|---|---:|---:|---:|"]
    for kok, r in kokler.items():
        md.append(f"| {r['kok_latin']} (`{kok}`) | {r['kelime_konumu']} | {r['ayet']} | {r['sure']} |")
    md += ["", "## ʿ-l-m lemma dağılımı (kelime konumu)", "", "| Lemma (BW) | Kelime konumu |", "|---|---:|"]
    md += [f"| `{l}` | {n} |" for l, n in lemma_dagilimi.items()]
    md += ["", f"## ʿâlim (`{ALIM}`) — bütün geçişler", "",
           f"Atıf sınıfı (elle): Allah {alim_sinif['Allah']}, insan {alim_sinif['insan']}.", "",
           "| Kelime konumu | Biçim (BW) | Sonraki kelime | Atıf |", "|---|---|---|---|"]
    md += [f"| {r['kelime_konumu']} | `{r['bicim_bw']}` | `{r['sonraki_kelime_bw']}` | {r['atif']} |" for r in alim_satir]
    md += ["", "## Diğer sorgular (birim: ayet)", "",
           f"- ʿulemâʾ (`{ALIYM}`, MP): {', '.join(sirala(ulema))}",
           f"- İnsan için ʿalîm (elle): {', '.join(sirala(ALIYM_INSAN))}; tartışmalı: {', '.join(sirala(ALIYM_TARTISMALI))}",
           *[f"- ʿâlimîn/ʿâlemîn ortak ünsüz iskeleti `{i}`: ʿâlim konumları {', '.join(v['alim_konumlari'])}; "
             f"aynı iskeletli ʿâlemîn {v['alemin_kelime_konumu_sayisi']} kelime konumu" for i, v in ortak_iskelet.items()],
           f"- ʿ-q-l tür dağılımı: {dict(aql_tur)}; açık nesne zamirli: "
           + ", ".join(f"{r['kelime_konumu']} (`{r['bicim_bw']}`, nesne {r['nesne_zamiri']})" for r in aql_nesneli),
           f"- *lev kânû yaʿlemûn* (ayet sonu, nesnesiz): {len(lev)} ayet — {', '.join(sirala(lev))}",
           f"- *ellezîne ûtû'l-ʿilm*: {len(utu)} ayet — {', '.join(sirala(utu))}",
           f"- mesel + ḍ-r-b + nâs aynı ayette: {len(mesel)} ayet — {', '.join(sirala(mesel))}",
           f"- *tilke'l-emsâl*: {', '.join(sirala(tilke))}",
           f"- Ankebût'ta *mâ … illâ* + belirli çoğul ism-i fâil: {', '.join(sirala(set(hasr)))}",
           f"- *ittehaza* (VIII): {len(itt)} kelime konumu / {len(itt_ayet)} ayet; dişil çekim: {', '.join(itt_disil)}",
           ]
    md += [f"  - birlikte ({ad}): {len(v)} ayet" + (f" — {', '.join(v)}" if len(v) <= 10 else "") for ad, v in birlikte_itt.items()]
    md += [f"- ʿilm (isim) + ẓ-n-n aynı ayette: {len(ilm_zan)} ayet — {', '.join(ilm_zan)}",
           "", "## Seçilmiş ayetler (Latin aktarım)", ""]
    md += [f"- **{r['ayet']}**: {r['ayet_latin']}" for r in gorunum]
    md += ["", "## Sınırlar", "", *[f"- {x}" for x in sonuc["sinirlar"]], "",
           "## Kaynak ve yeniden üretim", "",
           "[Quranic Arabic Corpus](https://corpus.quran.com/download/), QAC v0.4, Copyright (C) 2011 Kais Dukes; özgün telif bloğu `source_notice.txt` içinde korunur.",
           "[Tanzil](https://tanzil.net/docs/download), Uthmani v1.1; kaynak metin değiştirilmez.", "",
           "Kaynak      : QAC v0.4 + Tanzil Uthmani v1.1 (yalnız aktarım)",
           "Sayım birimi: kelime konumu | ayet | sûre",
           f"Sorgu       : {KOMUT}", f"Veri izi    : {kor.sha256[:12]}", "Durum       : çalıştırıldı", ""]

    CIKTI.mkdir(parents=True, exist_ok=True)
    metin_yaz("summary.json", json.dumps(sonuc, ensure_ascii=False, indent=2) + "\n")
    csv_yaz("alim_occurrences.csv", alim_satir)
    csv_yaz("verse_lookup.csv", gorunum)
    metin_yaz("report.md", "\n".join(md))
    telif = QAC_YOLU.read_text(encoding="utf-8-sig").split("LOCATION\tFORM\tTAG\tFEATURES", 1)[0]
    telif += "\n" + "\n".join(x for x in TANZIL_YOLU.read_text(encoding="utf-8-sig").splitlines() if x.startswith("#")) + "\n"
    metin_yaz("source_notice.txt", telif)
    manifest = {"betik_surumu": SURUM, "dosyalar": {ad: hashlib.sha256((CIKTI / ad).read_bytes()).hexdigest()
                for ad in ("summary.json", "alim_occurrences.csv", "verse_lookup.csv", "report.md", "source_notice.txt")}}
    metin_yaz("manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: sonuc[k] for k in ("kok_sayimlari", "alim_atif_sinifi", "lev_kanu_yalemun", "utul_ilm",
                                             "mesel_darb_nas", "ankebut_sinirlama_kalibi", "ittihaz", "ilm_zan_birlikte_ayet",
                                             "alim_alemin_ortak_iskelet", "aql_nesneli")}, ensure_ascii=False, indent=1))
    print(f"Üretildi: {CIKTI.relative_to(DEPO).as_posix()}")


if __name__ == "__main__":
    main()
