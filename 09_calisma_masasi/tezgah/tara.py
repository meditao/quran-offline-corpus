"""Kök / lemma / etiket / kalıp sorguları, sayım ve dağılım (QAC v0.4).

Birim kuralları (CLAUDE.md §4):
- Kök ve lemma sıklığında varsayılan birim kelime konumudur; aynı kelimede
  tekrar eden kök bir kez sayılır.
- Etiket, bab, iyelik eki ve kalıp sorguları segment düzeyindedir ve çıktıda
  "segment" diye işaretlenir.
- Etiket eşleşmesi tam eşleşmedir. Alt-dize eşleşmesi yalnız --alt-dize
  bayrağıyla yapılır ve çıktıya uyarı basılır.

Giriş kuralı (CLAUDE.md §2.8): kök Arapça harfle veya Buckwalter ile girilir.
Latin okunuş girişi (ör. "s-l-v") reddedilir; bilinmeyen kök boş sonuç değil,
hata üretir.
"""

from __future__ import annotations

import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass, field

from .veri import (
    ARAPCA_BW, KOK_HEMZE, KOK_LATIN, Korpus, Kelime, Segment, binlik, kok_latin,
)

BABLAR = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII")
LATIN_ISARETI = "Latin okunuş girişi kabul edilmez"


class GirdiHatasi(Exception):
    """Kullanıcı girdisi çözümlenemedi; sorgu çalıştırılmadı."""


@dataclass
class Sonuc:
    satirlar: list[str]
    birimler: list[str]
    veri: dict = field(default_factory=dict)
    basarili: bool = True


# ---------------------------------------------------------------- yardımcılar

def _arapca_mi(metin: str) -> bool:
    return any("؀" <= ch <= "ۿ" or "ݐ" <= ch <= "ݿ" for ch in metin)


def _sade_latin(metin: str) -> str:
    """Latin karşılaştırma anahtarı: küçük harf, ayırıcısız, işaretsiz."""
    ayrik = unicodedata.normalize("NFD", metin.lower())
    return "".join(
        ch for ch in ayrik
        if not unicodedata.combining(ch) and ch.isalpha() and ch != "ʿ"
    )


def _latin_adaylari(kor: Korpus, girdi: str) -> list[str]:
    anahtar = _sade_latin(girdi)
    if not anahtar:
        return []
    return sorted(k for k in kor.kok_kelimeleri if _sade_latin(kok_latin(k)) == anahtar)


def _aday_metni(adaylar: list[str]) -> str:
    return ", ".join(f"{k} ({kok_latin(k)})" for k in adaylar)


def ozet(kelimeler: list[Kelime]) -> dict[str, int]:
    return {
        "kelime konumu": len(kelimeler),
        "ayet": len({(k.sure, k.ayet) for k in kelimeler}),
        "sûre": len({k.sure for k in kelimeler}),
    }


def _ozet_satiri(o: dict[str, int]) -> str:
    return " | ".join(f"{ad}: {binlik(n)}" for ad, n in o.items())


def _tablo(basliklar: list[str], satirlar: list[list[object]], sag: set[int] | None = None) -> list[str]:
    """Basit hizalı metin tablosu. sag: sağa yaslanacak sütun indeksleri."""
    sag = sag or set()
    metin = [[str(x) for x in s] for s in satirlar]
    genislik = [len(b) for b in basliklar]
    for s in metin:
        for i, h in enumerate(s):
            genislik[i] = max(genislik[i], len(h))

    def bicimle(hucreler: list[str]) -> str:
        return "  ".join(
            h.rjust(genislik[i]) if i in sag else h.ljust(genislik[i])
            for i, h in enumerate(hucreler)
        ).rstrip()

    return [bicimle(basliklar), bicimle(["-" * g for g in genislik]), *map(bicimle, metin)]


# ------------------------------------------------------------ giriş çözümleme

@dataclass
class KokCozum:
    bw: str
    latin: str
    uyarilar: list[str]


def kok_coz(kor: Korpus, girdi: str) -> KokCozum:
    """Arapça veya Buckwalter kök girdisini envanterdeki köke çözer."""
    ham = girdi.strip()
    if not ham:
        raise GirdiHatasi("Kök boş.")

    if _arapca_mi(ham):
        bw = []
        for ch in ham:
            if ch in " -_ـ" or unicodedata.combining(ch):
                continue
            if ch in KOK_HEMZE:
                bw.append("A")
            elif ch == "ى":
                bw.append("y")
            elif ch in ARAPCA_BW and ARAPCA_BW[ch] in KOK_LATIN:
                bw.append(ARAPCA_BW[ch])
            else:
                raise GirdiHatasi(f"Arapça kök girdisinde kök harfi olmayan karakter: {ch!r}")
        aday = "".join(bw)
        if aday not in kor.kok_kelimeleri:
            raise GirdiHatasi(
                f"Kök envanterde yok: {ham} -> Buckwalter {aday!r}. "
                f"QAC v0.4 kök envanterinde bu kök bulunmadı; boş sonuç üretilmedi."
            )
        return KokCozum(aday, kok_latin(aday), [])

    gecersiz = sorted({ch for ch in ham if ch not in KOK_LATIN})
    if gecersiz:
        adaylar = _latin_adaylari(kor, ham)
        ek = f" Olası Buckwalter karşılıkları: {_aday_metni(adaylar)}." if adaylar else ""
        raise GirdiHatasi(
            f"{LATIN_ISARETI}: {ham!r} (Buckwalter kök alfabesinde olmayan karakter: "
            f"{' '.join(repr(c) for c in gecersiz)}). Kökü Arapça harfle veya Buckwalter "
            f"ile girin (ör. Slw, fTr, Amn).{ek}"
        )

    if ham not in kor.kok_kelimeleri:
        adaylar = sorted(set(_latin_adaylari(kor, ham)) | {
            k for k in kor.kok_kelimeleri if k.lower() == ham.lower()
        })
        ek = f" Olası karşılıklar: {_aday_metni(adaylar)}." if adaylar else ""
        raise GirdiHatasi(
            f"Kök envanterde yok: Buckwalter {ham!r} ({kok_latin(ham)}). Buckwalter büyük/küçük "
            f"harf duyarlıdır (S=ص, s=س). Boş sonuç üretilmedi.{ek}"
        )

    uyarilar = []
    ikizler = sorted(k for k in kor.kok_kelimeleri if k != ham and k.lower() == ham.lower())
    if ikizler:
        uyarilar.append(
            f"UYARI: Büyük/küçük harfle ayrışan başka kök var: {_aday_metni(ikizler)}. "
            f"Sorgulanan: {ham} ({kok_latin(ham)})."
        )
    return KokCozum(ham, kok_latin(ham), uyarilar)


_SESLI_IM = set("aiuo~`FNK")


def lemma_coz(kor: Korpus, girdi: str) -> str:
    ham = girdi.strip()
    if not ham:
        raise GirdiHatasi("Lemma boş.")
    bw = "".join(ARAPCA_BW.get(ch, ch) for ch in ham) if _arapca_mi(ham) else ham
    if bw in kor.lemma_kelimeleri:
        return bw
    iskelet = "".join(ch for ch in bw if ch not in _SESLI_IM)
    adaylar = sorted(
        l for l in kor.lemma_kelimeleri
        if "".join(ch for ch in l if ch not in _SESLI_IM) == iskelet
    )[:15]
    ek = f" Aynı ünsüz iskeletli lemmalar: {', '.join(adaylar)}." if adaylar else ""
    raise GirdiHatasi(f"Lemma envanterde yok: {bw!r}. Boş sonuç üretilmedi.{ek}")


def etiket_coz(kor: Korpus, etiket: str, alt_dize: bool = False) -> tuple[frozenset[str], list[str]]:
    """Etiketi envanterdeki tam etiket(ler)e çözer.

    Tam eşleşmede tek etiket döner. alt_dize=True ise etiketi içeren bütün
    envanter etiketleri döner ve uyarı üretilir.
    """
    uyarilar: list[str] = []
    if etiket.startswith("ROOT:"):
        cozum = kok_coz(kor, etiket[5:])
        uyarilar.extend(cozum.uyarilar)
        etiket = f"ROOT:{cozum.bw}"
    env = kor.etiket_envanteri
    if not alt_dize:
        if etiket in env:
            return frozenset({etiket}), uyarilar
        if etiket in {"(I)", "I"}:
            raise GirdiHatasi(
                "QAC I. babı etiketlemez; I. bab fiiller bab işareti taşımaz. "
                "Bab dağılımı için: dagilim --gore bab."
            )
        benzer = sorted(e for e in env if etiket and etiket in e)[:15]
        ek = f" Bu dizeyi içeren etiketler: {', '.join(benzer)}." if benzer else ""
        raise GirdiHatasi(
            f"Etiket envanterde yok (tam eşleşme): {etiket!r}.{ek} "
            f"Alt-dize eşleşmesi için --alt-dize bayrağını açıkça verin."
        )
    eslesen = frozenset(e for e in env if etiket in e)
    if not eslesen:
        raise GirdiHatasi(f"Alt-dize {etiket!r} hiçbir etikette geçmiyor.")
    uyarilar.append(
        f"UYARI: alt-dize eşleşmesi — {etiket!r} için {len(eslesen)} etiket birleştirildi: "
        f"{', '.join(sorted(eslesen))}"
    )
    return eslesen, uyarilar


# ------------------------------------------------------------- hedef seçimi

def _secim(kor: Korpus, kok: str | None, lemma: str | None) -> tuple[str, list[Kelime], list[str], dict]:
    """(başlık, kelimeler, uyarılar, kimlik) döner."""
    if kok is not None:
        c = kok_coz(kor, kok)
        return f"Kök: {c.bw} ({c.latin})", kor.kok_kelimeleri[c.bw], c.uyarilar, {"kok": c.bw}
    if lemma is not None:
        l = lemma_coz(kor, lemma)
        return f"Lemma: {l}", kor.lemma_kelimeleri[l], [], {"lemma": l}
    raise GirdiHatasi("--kok veya --lemma verilmeli.")


def _hedef_govdeler(kelime: Kelime, kimlik: dict) -> list[Segment]:
    if "kok" in kimlik:
        return [s for s in kelime.segmentler if s.kok == kimlik["kok"]]
    return [s for s in kelime.segmentler if s.lemma == kimlik["lemma"]]


def tur_etiketi(seg: Segment) -> str:
    parca = [seg.pos or seg.etiket]
    if seg.pos == "V":
        parca += [t for t in ("PERF", "IMPF", "IMPV") if t in seg.etiketler]
        if "PASS" in seg.etiketler:
            parca.append("PASS")
    else:
        if "PCPL" in seg.etiketler:
            parca.append("ACT PCPL" if "ACT" in seg.etiketler else "PASS PCPL")
        if "VN" in seg.etiketler:
            parca.append("VN")
    return " · ".join(parca)


def _sonraki_zamirler(kelime: Kelime, govde: Segment) -> list[str]:
    return [
        s.zamir for s in kelime.segmentler
        if s.no > govde.no and s.zamir is not None
    ]


# ----------------------------------------------------------------- komutlar

def kokler(kor: Korpus, limit: int = 0, siralama: str = "siklik") -> Sonuc:
    satirlar_veri = []
    for kok, kelimeler in kor.kok_kelimeleri.items():
        o = ozet(kelimeler)
        satirlar_veri.append((kok, o["kelime konumu"], o["ayet"], o["sûre"]))
    if siralama == "alfabe":
        satirlar_veri.sort(key=lambda r: r[0])
    else:
        satirlar_veri.sort(key=lambda r: (-r[1], r[0]))
    gosterilen = satirlar_veri if limit <= 0 else satirlar_veri[:limit]
    satirlar = [
        f"Benzersiz kök: {binlik(len(satirlar_veri))}",
        f"Gösterilen: {binlik(len(gosterilen))} / {binlik(len(satirlar_veri))}",
        "",
        *_tablo(
            ["kök (BW)", "Latin", "kelime konumu", "ayet", "sûre"],
            [[k, kok_latin(k), binlik(w), binlik(a), binlik(s)] for k, w, a, s in gosterilen],
            sag={2, 3, 4},
        ),
    ]
    return Sonuc(satirlar, ["kelime konumu", "ayet", "sûre"],
                 {"kokler": {k: (w, a, s) for k, w, a, s in satirlar_veri}})


def _gecis_listesi(kelimeler: list[Kelime], kimlik: dict, limit: int) -> list[str]:
    gosterilen = kelimeler if limit <= 0 else kelimeler[:limit]
    satirlar = [f"Geçişler (kelime konumu) — gösterilen {binlik(len(gosterilen))} / {binlik(len(kelimeler))}:"]
    tablo = []
    for k in gosterilen:
        govdeler = _hedef_govdeler(k, kimlik)
        tablo.append([
            k.konum,
            k.bicim,
            ";".join(sorted({g.lemma or "-" for g in govdeler})),
            ";".join(sorted({tur_etiketi(g) for g in govdeler})),
            ";".join(sorted({g.bab or ("I" if g.pos == "V" else "-") for g in govdeler})),
        ])
    satirlar += _tablo(["konum", "biçim (Buckwalter)", "lemma", "tür", "bab"], tablo)
    return satirlar


def kok(kor: Korpus, girdi: str, limit: int = 50) -> Sonuc:
    baslik, kelimeler, uyarilar, kimlik = _secim(kor, girdi, None)
    o = ozet(kelimeler)
    satirlar = [*uyarilar, baslik, _ozet_satiri(o), "", *_gecis_listesi(kelimeler, kimlik, limit)]
    return Sonuc(satirlar, ["kelime konumu", "ayet", "sûre"], {**kimlik, **o})


def lemma(kor: Korpus, girdi: str, limit: int = 50) -> Sonuc:
    baslik, kelimeler, uyarilar, kimlik = _secim(kor, None, girdi)
    o = ozet(kelimeler)
    satirlar = [*uyarilar, baslik, _ozet_satiri(o), "", *_gecis_listesi(kelimeler, kimlik, limit)]
    return Sonuc(satirlar, ["kelime konumu", "ayet", "sûre"], {**kimlik, **o})


def _etiket_segmentleri(kor: Korpus, etiketler: list[str], alt_dize: bool) -> tuple[list[Segment], list[str], list[frozenset[str]]]:
    if not etiketler:
        raise GirdiHatasi("En az bir etiket verilmeli.")
    gruplar: list[frozenset[str]] = []
    uyarilar: list[str] = []
    for e in etiketler:
        grup, u = etiket_coz(kor, e, alt_dize)
        gruplar.append(grup)
        uyarilar.extend(u)
    eslesen = [s for s in kor.segmentler if all(s.etiketler & g for g in gruplar)]
    return eslesen, uyarilar, gruplar


def _segment_ozeti(segmentler: list[Segment]) -> dict[str, int]:
    return {
        "segment": len(segmentler),
        "kelime konumu": len({s.kelime_anahtari for s in segmentler}),
        "ayet": len({(s.sure, s.ayet) for s in segmentler}),
        "sûre": len({s.sure for s in segmentler}),
    }


def etiket(kor: Korpus, etiketler: list[str], alt_dize: bool = False, limit: int = 50) -> Sonuc:
    segmentler, uyarilar, gruplar = _etiket_segmentleri(kor, etiketler, alt_dize)
    o = _segment_ozeti(segmentler)
    gosterilen = segmentler if limit <= 0 else segmentler[:limit]
    satirlar = [
        *uyarilar,
        f"Etiket ({'alt-dize' if alt_dize else 'tam eşleşme'}, aynı segmentte hepsi): "
        + " & ".join(etiketler),
        _ozet_satiri(o),
        "",
        f"Segmentler — gösterilen {binlik(len(gosterilen))} / {binlik(len(segmentler))}:",
        *_tablo(
            ["konum", "biçim (Buckwalter)", "TAG", "özellikler"],
            [[s.konum, s.bicim, s.etiket, "|".join(s.ozellikler)] for s in gosterilen],
        ),
    ]
    return Sonuc(satirlar, ["segment", "kelime konumu", "ayet", "sûre"],
                 {**o, "etiket_gruplari": [sorted(g) for g in gruplar], "alt_dize": alt_dize})


def sayim(kor: Korpus, kok: str | None = None, lemma: str | None = None,
          etiketler: list[str] | None = None, alt_dize: bool = False) -> Sonuc:
    if etiketler:
        segmentler, uyarilar, _ = _etiket_segmentleri(kor, etiketler, alt_dize)
        o = _segment_ozeti(segmentler)
        satirlar = [*uyarilar, "Etiket: " + " & ".join(etiketler), _ozet_satiri(o)]
        return Sonuc(satirlar, ["segment", "kelime konumu", "ayet", "sûre"], o)
    if kok is None and lemma is None:
        o = {
            "sûre": len(kor.sureler),
            "ayet": len(kor.ayet_segmentleri),
            "kelime konumu": len(kor.kelimeler),
            "segment": len(kor.segmentler),
        }
        satirlar = [
            "Korpus toplamları (her satır ayrı birim; toplanmaz):",
            *[f"  {ad:<14}: {binlik(n)}" for ad, n in o.items()],
            f"  {'benzersiz kök':<14}: {binlik(len(kor.kok_kelimeleri))}",
            f"  {'benzersiz lemma':<14}: {binlik(len(kor.lemma_kelimeleri))}",
        ]
        o = {**o, "benzersiz kök": len(kor.kok_kelimeleri), "benzersiz lemma": len(kor.lemma_kelimeleri)}
        return Sonuc(satirlar, ["sûre", "ayet", "kelime konumu", "segment"], o)
    baslik, kelimeler, uyarilar, kimlik = _secim(kor, kok, lemma)
    o = ozet(kelimeler)
    return Sonuc([*uyarilar, baslik, _ozet_satiri(o)], ["kelime konumu", "ayet", "sûre"], {**kimlik, **o})


def dagilim(kor: Korpus, gore: str, kok: str | None = None, lemma: str | None = None) -> Sonuc:
    baslik, kelimeler, uyarilar, kimlik = _secim(kor, kok, lemma)
    o = ozet(kelimeler)
    satirlar = [*uyarilar, baslik, _ozet_satiri(o), ""]

    if gore == "sure":
        sayac: dict[int, list[Kelime]] = defaultdict(list)
        for k in kelimeler:
            sayac[k.sure].append(k)
        tablo = [[s, binlik(len(ks)), binlik(len({k.ayet for k in ks}))] for s, ks in sorted(sayac.items())]
        satirlar += ["Sûre dağılımı (sûre numarası; geleneksel sınıflandırma kullanılmadı):",
                     *_tablo(["sûre", "kelime konumu", "ayet"], tablo, sag={0, 1, 2})]
        veri = {s: (len(ks), len({k.ayet for k in ks})) for s, ks in sayac.items()}
        return Sonuc(satirlar, ["kelime konumu", "ayet"], {**kimlik, **o, "dagilim": veri})

    if gore in {"tur", "lemma"}:
        sayac_c: Counter = Counter()
        for k in kelimeler:
            govdeler = _hedef_govdeler(k, kimlik)
            if gore == "tur":
                degerler = {tur_etiketi(g) for g in govdeler}
            else:
                degerler = {g.lemma or "-" for g in govdeler}
            sayac_c.update(degerler)
        ad = "tür" if gore == "tur" else "lemma"
        toplam = sum(sayac_c.values())
        satirlar += [f"{ad.capitalize()} dağılımı (kelime konumu):",
                     *_tablo([ad, "kelime konumu"],
                             [[d, binlik(n)] for d, n in sorted(sayac_c.items(), key=lambda x: (-x[1], x[0]))],
                             sag={1})]
        if toplam != o["kelime konumu"]:
            satirlar.append(
                f"Not: satır toplamı {binlik(toplam)} ≠ {binlik(o['kelime konumu'])} kelime konumu; "
                f"bazı kelimelerde hedef birden fazla {ad} değeriyle geçiyor."
            )
        return Sonuc(satirlar, ["kelime konumu"], {**kimlik, **o, "dagilim": dict(sayac_c)})

    if gore == "bab":
        fiil: Counter = Counter()
        isim: Counter = Counter()
        for k in kelimeler:
            for g in _hedef_govdeler(k, kimlik):
                if g.pos == "V":
                    fiil[g.bab or "I"] += 1
                else:
                    isim[g.bab or "I"] += 1
        tablo = []
        for b in BABLAR:
            if fiil[b] or isim[b]:
                ad = "I / işaretsiz" if b == "I" else b
                tablo.append([ad, binlik(fiil[b]), binlik(isim[b])])
        tablo.append(["toplam", binlik(sum(fiil.values())), binlik(sum(isim.values()))])
        satirlar += [
            "Bab dağılımı (segment: hedefi taşıyan gövde segmenti):",
            *_tablo(["bab", "fiil", "isim"], tablo, sag={1, 2}),
            "Not: QAC I. babı işaretlemez. 'fiil' sütununda işaretsiz = I. bab; 'isim' sütununda",
            "     işaretsiz = bab işareti taşımayan isim (I. bab türevi mi, türemiş olmayan isim mi",
            "     ayrımı bu veriden yapılmaz).",
        ]
        return Sonuc(satirlar, ["segment"], {**kimlik, **o, "fiil": dict(fiil), "isim": dict(isim)})

    if gore == "iyelik":
        isim_c: Counter = Counter()
        fiil_c: Counter = Counter()
        for k in kelimeler:
            for g in _hedef_govdeler(k, kimlik):
                zamirler = _sonraki_zamirler(k, g)
                anahtar = " + ".join(zamirler) if zamirler else "— (ek zamir yok)"
                (fiil_c if g.pos == "V" else isim_c)[anahtar] += 1
        satirlar += [
            "İsim gövdesi + sonraki ek zamir segmenti (iyelik eki; segment):",
            *_tablo(["iyelik eki", "segment"],
                    [[d, binlik(n)] for d, n in sorted(isim_c.items(), key=lambda x: (-x[1], x[0]))],
                    sag={1}),
            f"toplam isim gövdesi: {binlik(sum(isim_c.values()))}",
            "",
            "Fiil gövdesi + sonraki ek zamir segmentleri (segment):",
            *_tablo(["ek zamir(ler)", "segment"],
                    [[d, binlik(n)] for d, n in sorted(fiil_c.items(), key=lambda x: (-x[1], x[0]))],
                    sag={1}),
            f"toplam fiil gövdesi: {binlik(sum(fiil_c.values()))}",
            "Not: fiildeki ek zamir özne de nesne de olabilir; QAC morfoloji dosyası bu ayrımı",
            "     etiketlemez. İsmin kendi etiketlerinde zamir aranmadı; sonraki segmente bakıldı.",
        ]
        return Sonuc(satirlar, ["segment"], {**kimlik, **o, "isim": dict(isim_c), "fiil": dict(fiil_c)})

    raise GirdiHatasi(f"Bilinmeyen dağılım türü: {gore!r} (tur | lemma | bab | iyelik | sure)")


def birlikte(kor: Korpus, kok_a: str, kok_b: str, pencere: int | None = None, limit: int = 50) -> Sonuc:
    ca, cb = kok_coz(kor, kok_a), kok_coz(kor, kok_b)
    ka, kb = kor.kok_kelimeleri[ca.bw], kor.kok_kelimeleri[cb.bw]
    ayet_a: dict[tuple[int, int], list[Kelime]] = defaultdict(list)
    ayet_b: dict[tuple[int, int], list[Kelime]] = defaultdict(list)
    for k in ka:
        ayet_a[(k.sure, k.ayet)].append(k)
    for k in kb:
        ayet_b[(k.sure, k.ayet)].append(k)
    ortak = sorted(set(ayet_a) & set(ayet_b))

    ciftler: dict[tuple[int, int], list[tuple[Kelime, Kelime]]] = {}
    if pencere is not None:
        if pencere < 1:
            raise GirdiHatasi("--pencere en az 1 olmalı.")
        for ay in ortak:
            c = [(x, y) for x in ayet_a[ay] for y in ayet_b[ay]
                 if x.kelime != y.kelime and abs(x.kelime - y.kelime) <= pencere]
            if c:
                ciftler[ay] = c
        hedef = sorted(ciftler)
    else:
        hedef = ortak

    satirlar = [*ca.uyarilar, *cb.uyarilar,
                f"Kök A: {ca.bw} ({ca.latin}) — {binlik(len(ayet_a))} ayet",
                f"Kök B: {cb.bw} ({cb.latin}) — {binlik(len(ayet_b))} ayet",
                f"Aynı ayette birlikte: {binlik(len(ortak))} ayet | {binlik(len({s for s, _ in ortak}))} sûre"]
    veri = {"a": ca.bw, "b": cb.bw, "ayet_a": len(ayet_a), "ayet_b": len(ayet_b),
            "ortak_ayet": len(ortak), "ortak_sure": len({s for s, _ in ortak})}
    birimler = ["ayet", "sûre"]
    if pencere is not None:
        cift_sayisi = sum(len(c) for c in ciftler.values())
        satirlar.append(
            f"±{pencere} kelime konumu penceresinde: {binlik(len(hedef))} ayet | "
            f"{binlik(cift_sayisi)} kelime konumu çifti (farklı kelime konumları)"
        )
        veri.update({"pencere": pencere, "pencere_ayet": len(hedef), "pencere_cift": cift_sayisi})
        birimler = ["ayet", "sûre", "kelime konumu"]
    gosterilen = hedef if limit <= 0 else hedef[:limit]
    satirlar += ["", f"Ayetler — gösterilen {binlik(len(gosterilen))} / {binlik(len(hedef))}:"]
    tablo = []
    for ay in gosterilen:
        tablo.append([f"{ay[0]}:{ay[1]}",
                      ",".join(str(k.kelime) for k in ayet_a[ay]),
                      ",".join(str(k.kelime) for k in ayet_b[ay])])
    satirlar += _tablo(["ayet", f"{ca.bw} kelime no", f"{cb.bw} kelime no"], tablo)
    return Sonuc(satirlar, birimler, veri)


@dataclass
class _Desen:
    joker: bool
    gerekli: list[frozenset[str]]
    yasak: list[frozenset[str]]

    def uyar(self, seg: Segment) -> bool:
        if self.joker:
            return True
        return all(seg.etiketler & g for g in self.gerekli) and not any(seg.etiketler & y for y in self.yasak)


def _desen_ayristir(kor: Korpus, desen: str, alt_dize: bool) -> tuple[list[_Desen], list[str]]:
    ogeler = desen.split()
    if not ogeler:
        raise GirdiHatasi("Kalıp boş.")
    sonuc: list[_Desen] = []
    uyarilar: list[str] = []
    for oge in ogeler:
        if oge == "*":
            sonuc.append(_Desen(True, [], []))
            continue
        gerekli, yasak = [], []
        for parca in oge.split("&"):
            if not parca:
                raise GirdiHatasi(f"Kalıp öğesinde boş parça: {oge!r}")
            olumsuz = parca.startswith("!")
            grup, u = etiket_coz(kor, parca[1:] if olumsuz else parca, alt_dize)
            uyarilar.extend(u)
            (yasak if olumsuz else gerekli).append(grup)
        if not gerekli:
            raise GirdiHatasi(f"Kalıp öğesi yalnız olumsuz etiketten oluşamaz: {oge!r}")
        sonuc.append(_Desen(False, gerekli, yasak))
    return sonuc, uyarilar


def kalip(kor: Korpus, desen: str, kelime_ici: bool = False, alt_dize: bool = False, limit: int = 50) -> Sonuc:
    ogeler, uyarilar = _desen_ayristir(kor, desen, alt_dize)
    n = len(ogeler)
    diziler = ([k.segmentler for k in kor.kelimeler] if kelime_ici
               else list(kor.ayet_segmentleri.values()))
    eslesmeler: list[list[Segment]] = []
    for dizi in diziler:
        for i in range(len(dizi) - n + 1):
            if all(ogeler[j].uyar(dizi[i + j]) for j in range(n)):
                eslesmeler.append(dizi[i:i + n])
    o = {
        "eşleşme": len(eslesmeler),
        "kelime konumu": len({e[0].kelime_anahtari for e in eslesmeler}),
        "ayet": len({(e[0].sure, e[0].ayet) for e in eslesmeler}),
        "sûre": len({e[0].sure for e in eslesmeler}),
    }
    gosterilen = eslesmeler if limit <= 0 else eslesmeler[:limit]
    kapsam = "aynı kelime konumu içinde" if kelime_ici else "aynı ayet içinde, kelime sınırı geçilebilir"
    satirlar = [
        *uyarilar,
        f"Kalıp ({'alt-dize' if alt_dize else 'tam eşleşme'}; ardışık {n} segment; {kapsam}): {desen}",
        f"eşleşme (segment dizisi): {binlik(o['eşleşme'])} | ilk segmentin kelime konumu: "
        f"{binlik(o['kelime konumu'])} | ayet: {binlik(o['ayet'])} | sûre: {binlik(o['sûre'])}",
        "",
        f"Eşleşmeler — gösterilen {binlik(len(gosterilen))} / {binlik(len(eslesmeler))}:",
        *_tablo(["başlangıç", "segmentler (biçim/TAG)"],
                [[e[0].konum, "  ".join(f"{s.bicim}/{s.etiket}" for s in e)] for e in gosterilen]),
    ]
    return Sonuc(satirlar, ["segment", "kelime konumu", "ayet", "sûre"], o)
