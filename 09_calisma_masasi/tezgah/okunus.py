"""Tanzil Uthmani metninden Latin harfli okunuş (Aşama 2a).

Ünsüzler kök gösterimiyle aynı tablodan gelir (harf.py). Kurallar ve
uygulanmayan kurallar: 09_calisma_masasi/okunus_kurallari.md

Okunuş bir aktarımdır, delil değildir. Kelime sınırları Tanzil'in boşluk
tokenlarıdır; QAC kelime konumlarıyla doğrudan eşlenmez
(03_indices/generated/tanzil_qac_alignment.csv).

Bilinmeyen karakter sessizce atlanmaz: BilinmeyenKarakter fırlatılır.
Kuralın öngörmediği bir dizilim "belirsiz" listesine yazılır ve çıktıda görünür.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from .harf import HARF_LATIN, UNLU_LATIN, UZUN
from .veri import VeriHatasi, sha256

DEPO = Path(__file__).resolve().parents[2]
TANZIL_YOLU = DEPO / "01_raw" / "tanzil" / "quran-uthmani.txt"
TANZIL_SHA256 = "bf4f57b968d03f4131c070b1e285da9be0e0a108a21c910e872801ca273312c8"
KAYNAK_ADI = "Tanzil Uthmani v1.1"

# --- karakter sınıfları ---------------------------------------------------
FETHA, KESRE, DAMME = "َ", "ِ", "ُ"
TENVINLER = {"ً", "ٌ", "ٍ"}
KISA_UNLULER = {FETHA, KESRE, DAMME} | TENVINLER
SEDDE = "ّ"
SUKUN = "ْ"
MEDDE = "ٓ"              # uzatma işareti; okunuşta ayrıca gösterilmez
HEMZE_UST = "ٔ"          # tatvil üzerinde hemze
UST_ELIF = "ٰ"           # hançerî elif -> â
VASL_ELIF = "ٱ"
TATVIL = "ـ"
SESSIZ_ISARETLER = {"۟", "۠"}  # ۟ daima okunmaz, ۠ vaslda okunmaz
IKLAB = {"ۢ", "ۭ"}             # ۢ ۭ küçük mim: n -> m
KUCUK_SIN_UST = "ۜ"                 # ۜ ص sin okunur
KUCUK_SIN_ALT = "ۣ"                 # ۣ ص okunur (sin ikinci vecih); gösterilmez
KUCUK_YA_UST = "ۧ"                  # ۧ -> î
KUCUK_NUN_UST = "ۨ"                 # ۨ -> n
IMALE = "۪"                         # ۪ sonraki â -> ê
ISMAM = "۫"                         # ۫ işmam; duyulmaz, gösterilmez
TESHIL = "۬"                        # ۬ teshil hemzesi
KUCUK_VAV, KUCUK_YA = "ۥ", "ۦ"  # ۥ ۦ sıla: û / î

ISARETLER = (
    KISA_UNLULER | {SEDDE, SUKUN, MEDDE, HEMZE_UST, UST_ELIF, KUCUK_SIN_UST, KUCUK_SIN_ALT,
                    KUCUK_YA_UST, KUCUK_NUN_UST, IMALE, ISMAM, TESHIL}
    | SESSIZ_ISARETLER | IKLAB
)
HAREKELER = KISA_UNLULER | {SEDDE, SUKUN, UST_ELIF}
UZATMA_HARFLERI = {"ا", "و", "ي", "ى"}
TABAN = set(HARF_LATIN) | {"ا", "ى", "ة", VASL_ELIF, TATVIL, KUCUK_VAV, KUCUK_YA}

# Hurûf-ı mukattaa harf adları (ortak tablodan kurulur).
MUKATTAA_ADLARI = {
    "ا": "ʾalif", "ل": "lâm", "م": "mîm", "ر": "râ", "ص": "ṣâd", "ك": "kâf",
    "ه": "hâ", "ي": "yâ", "ع": "ʿayn", "ط": "ṭâ", "س": "sîn", "ح": "ḥâ",
    "ق": "qâf", "ن": "nûn",
}


# Lafzatullah: Tanzil Uthmani "ٱللَّه" adında hançerî elifi yazmaz; okunuştaki
# uzun â yazıdan çıkmaz. Tek sözlüksel istisna budur. Desen: iki lam (ikincisi
# şeddeli-fethalı) + he + son hareke (+ ٱللَّهُمَّ). ٱللَّهْو, ٱللَّهَب, لَّهُم eşleşmez.
ALLAH_RE = re.compile("ل[\u0651\u0650]*ل\u0651\u064E\u0647[\u064E\u064F\u0650](?:\u0645\u0651\u064E)?$")


class BilinmeyenKarakter(Exception):
    pass


@dataclass
class Birim:
    """Bir taban harf ve işaretleri; okunuşta (ünsüz, ünlü) çiftine dönüşür."""
    taban: str
    isaretler: list[str] = field(default_factory=list)
    unsuz: str = ""
    unlu: str = ""
    sila: bool = False       # ۥ/ۦ kaynaklı uzun ünlü (vakfta düşer)
    marbuta: bool = False
    acik: bool = False       # harekesiz ve sükûnsuz ünsüz (idgam/ihfa adayı)
    vakfta_uzun: bool = False  # sonraki elif ۠ ile işaretli: vakfta okunur (أَنَا۠)

    def sedde(self) -> bool:
        return SEDDE in self.isaretler


@dataclass
class KelimeOkunus:
    arapca: str
    latin: str
    belirsiz: list[str] = field(default_factory=list)


@dataclass
class AyetOkunus:
    sure: int
    ayet: int
    kelimeler: list[KelimeOkunus]
    besmele: list[KelimeOkunus] = field(default_factory=list)

    @property
    def latin(self) -> str:
        return " ".join(k.latin for k in self.kelimeler)

    @property
    def belirsiz(self) -> list[str]:
        return [b for k in self.besmele + self.kelimeler for b in k.belirsiz]


# --- ayrıştırma -------------------------------------------------------------

def _birimlere_ayir(kelime: str) -> list[Birim]:
    birimler: list[Birim] = []
    for ch in kelime:
        if ch in TABAN:
            birimler.append(Birim(ch))
        elif ch in ISARETLER:
            if not birimler:
                raise BilinmeyenKarakter(f"işaret tabansız: U+{ord(ch):04X} {kelime!r}")
            birimler[-1].isaretler.append(ch)
        else:
            raise BilinmeyenKarakter(f"U+{ord(ch):04X} {ch!r} ({kelime!r})")
    return birimler


def _mukattaa_mi(kelime: str) -> bool:
    return not any(ch in HAREKELER for ch in kelime)


def _mukattaa(kelime: str) -> str:
    adlar = []
    for ch in kelime:
        if ch == MEDDE:
            continue
        if ch not in MUKATTAA_ADLARI:
            raise BilinmeyenKarakter(f"mukattaa harfi tabloda yok: {ch!r} ({kelime!r})")
        adlar.append(MUKATTAA_ADLARI[ch])
    return " ".join(adlar)


def _unlu(b: Birim) -> str:
    for i in b.isaretler:
        if i in UNLU_LATIN:
            u = UNLU_LATIN[i]
            if UST_ELIF in b.isaretler and u == "a":
                return "â"
            return u
    if UST_ELIF in b.isaretler:
        return "â"
    return ""


def _onceki_sesli(birimler: list[Birim], i: int) -> Birim | None:
    for j in range(i - 1, -1, -1):
        if birimler[j].unsuz or birimler[j].unlu:
            return birimler[j]
    return None


def _uzat(onceki: Birim | None, kisa: str, belirsiz: list[str], baglam: str) -> None:
    """Uzatma harfi/işareti: önceki kısa ünlüyü uzun yapar."""
    if onceki is None:
        belirsiz.append(f"uzatma harfinden önce harf yok: {baglam}")
        return
    if onceki.unlu in {kisa, ""}:
        onceki.unlu, onceki.acik = UZUN[kisa], False
    elif onceki.unlu != UZUN[kisa]:
        belirsiz.append(f"uzatma '{UZUN[kisa]}' ama önceki ünlü '{onceki.unlu}': {baglam}")


def kelime_oku(kelime: str, ayet_basi: bool) -> tuple[list[Birim], list[str]]:
    """Kelimeyi birimlere çözer ve her birime ünsüz/ünlü atar (vasl ve vakf hariç)."""
    birimler = _birimlere_ayir(kelime)
    belirsiz: list[str] = []
    imale = False
    allah_lami = None
    if ALLAH_RE.search(kelime):
        he = max(i for i, b in enumerate(birimler) if b.taban == "ه")
        allah_lami = he - 1
    for i, b in enumerate(birimler):
        sonraki = birimler[i + 1] if i + 1 < len(birimler) else None
        onceki = _onceki_sesli(birimler, i)
        t, isr = b.taban, b.isaretler

        if any(s in isr for s in SESSIZ_ISARETLER):
            if "\u06E0" in isr and onceki is not None:
                onceki.vakfta_uzun = True
            continue                                            # okunmayan harf

        if t == VASL_ELIF:
            if i == 0 and ayet_basi:                            # ibtidâ
                if sonraki is not None and sonraki.taban == "ل":
                    b.unlu = "a"
                else:
                    ucuncu = birimler[2] if len(birimler) > 2 else None
                    b.unlu = "u" if ucuncu is not None and DAMME in ucuncu.isaretler else "i"
            continue                                            # vaslda okunmaz

        if t == "ا":
            if TESHIL in isr:
                b.unsuz, b.unlu = HARF_LATIN["ء"], "a"
            elif onceki is not None and onceki.unlu in {"an", "am"}:
                pass                                            # tenvin elifi
            else:
                _uzat(onceki, "a", belirsiz, kelime)
            continue

        if t in {KUCUK_VAV, KUCUK_YA}:
            _uzat(onceki, "u" if t == KUCUK_VAV else "i", belirsiz, kelime)
            if onceki is not None:
                onceki.sila = True
            continue

        if t == TATVIL:
            if HEMZE_UST in isr:
                b.unsuz, b.unlu = HARF_LATIN["ء"], _unlu(b)
            elif KUCUK_NUN_UST in isr:
                b.unsuz, b.unlu = "n", _unlu(b)
            elif KUCUK_YA_UST in isr:
                _uzat(onceki, "i", belirsiz, kelime)
            elif UST_ELIF in isr:
                _uzat(onceki, "a", belirsiz, kelime)
            continue

        harekeli = any(x in isr for x in KISA_UNLULER | {SUKUN, SEDDE})
        if t in {"و", "ي", "ى"} and not harekeli:
            if UST_ELIF in isr:                                 # صَلَوٰة, عَلَىٰ
                _uzat(onceki, "a", belirsiz, kelime)
                if imale and onceki is not None and onceki.unlu == "â":
                    onceki.unlu, imale = "ê", False
            elif t in {"و", "ي"} and onceki is not None and onceki.unlu == "a":
                b.unsuz, b.acik = HARF_LATIN[t], True             # عَصَوا۟ وَّ: diftong, idgam adayı
            elif t == "و":
                _uzat(onceki, "u", belirsiz, kelime)
            elif onceki is not None and onceki.unlu in {"a", "an"} and t == "ى":
                if onceki.unlu == "a":
                    onceki.unlu = "â"                           # هُدًى: tenvin, ى okunmaz
            else:
                _uzat(onceki, "i", belirsiz, kelime)
            continue

        # ünsüz
        unsuz = HARF_LATIN.get(t)
        if unsuz is None:
            raise BilinmeyenKarakter(f"harf tabloda yok: {t!r} ({kelime!r})")
        if t == "ص" and KUCUK_SIN_UST in isr:
            unsuz = HARF_LATIN["س"]
        b.marbuta = t == "ة"
        b.unsuz = unsuz * 2 if SEDDE in isr else unsuz
        b.unlu = _unlu(b)
        if i == allah_lami:
            b.unlu = "â"
        if IMALE in isr:
            imale = True
        if any(x in isr for x in IKLAB):
            if b.unlu.endswith("n"):
                b.unlu = b.unlu[:-1] + "m"                      # tenvin iklabı
            elif t == "ن" and not b.unlu:
                b.unsuz = "m"
        if not b.unlu and SUKUN not in isr and not any(x in isr for x in IKLAB):
            if sonraki is not None and sonraki.sedde() and sonraki.taban in HARF_LATIN:
                b.unsuz = ""                                    # kelime içi idgam: ٱلرَّ, دتّ
            else:
                b.acik = True
    return birimler, belirsiz


def _metin(birimler: list[Birim]) -> str:
    return "".join(b.unsuz + b.unlu for b in birimler)


def _vakf(birimler: list[Birim]) -> None:
    """Ayet sonu durak: son kısa ünlü ve tenvin düşer, fetha tenvini â olur, ة -> h."""
    for b in reversed(birimler):
        if not (b.unsuz or b.unlu):
            continue
        if b.sila:
            b.unlu = ""
        if b.vakfta_uzun and b.unlu in UZUN:
            b.unlu = UZUN[b.unlu]
            return
        if b.marbuta:
            b.unsuz, b.unlu = "h" * len(b.unsuz), ""
        elif b.unlu in {"a", "i", "u", "un", "in", "um", "im"}:
            b.unlu = ""
        elif b.unlu in {"an", "am"}:
            b.unlu = "â"
        return


def ayet_oku(sure: int, ayet: int, metin: str) -> AyetOkunus:
    kelimeler = metin.split(" ")
    besmele: list[KelimeOkunus] = []
    if ayet == 1 and sure not in (1, 9):
        # Sûre başı besmelesi Tanzil'de ilk ayete önek olarak yazılır; QAC'ta yoktur.
        # 95:1 ve 97:1'de önekin ilk harfi şeddelidir (بِّسْمِ); karşılaştırmada şedde yok sayılır.
        bsm = besmele_metni().split(" ")
        aday = kelimeler[:len(bsm)]
        if aday and [aday[0].replace(SEDDE, "", 1), *aday[1:]] == bsm:
            besmele = ayet_oku(1, 1, besmele_metni()).kelimeler
            kelimeler = kelimeler[len(bsm):]

    cozulen: list[tuple[str, list[Birim] | None, str, list[str]]] = []
    for i, k in enumerate(kelimeler):
        if _mukattaa_mi(k):
            cozulen.append((k, None, _mukattaa(k), []))
        else:
            birimler, belirsiz = kelime_oku(k, ayet_basi=(i == 0))
            cozulen.append((k, birimler, "", belirsiz))

    # Ayet başında kelime sedde'li harfle başlıyorsa (önceki ayetle vasl yazımı) tek yazılır.
    if cozulen and cozulen[0][1]:
        ilk = cozulen[0][1][0]
        if ilk.unsuz and ilk.sedde():
            ilk.unsuz = ilk.unsuz[: len(ilk.unsuz) // 2]

    # Kelimeler arası idgam: kelime sedde'li harfle başlıyorsa, önceki kelimenin
    # sonundaki açık ünsüz ya da tenvin n'si bu harfe dönüşür; baştaki harf tek yazılır.
    for i in range(1, len(cozulen)):
        _, birimler, _, belirsiz = cozulen[i]
        _, onceki, _, onceki_belirsiz = cozulen[i - 1]
        if birimler is None or onceki is None:
            continue
        ilk = birimler[0]
        if not (ilk.unsuz and ilk.sedde()):
            continue
        tek = ilk.unsuz[: len(ilk.unsuz) // 2]
        son = next((b for b in reversed(onceki) if b.unsuz or b.unlu), None)
        if son is not None and son.unlu.endswith(("n", "m")) and son.unlu[:-1] in {"a", "i", "u"}:
            son.unlu = son.unlu[:-1] + tek
        elif son is not None and son.acik:
            son.unsuz = tek
        else:
            belirsiz.append(f"kelime başı sedde, önceki kelime açık ünsüzle bitmiyor: {kelimeler[i]}")
            continue
        ilk.unsuz = tek

    son_i = len(cozulen) - 1
    if cozulen and cozulen[son_i][1] is not None:
        _vakf(cozulen[son_i][1])

    sonuc = [
        KelimeOkunus(k, muk if b is None else _metin(b), bel)
        for k, b, muk, bel in cozulen
    ]
    return AyetOkunus(sure, ayet, sonuc, besmele)


# --- Tanzil -----------------------------------------------------------------

@lru_cache(maxsize=1)
def tanzil() -> dict[tuple[int, int], str]:
    """Tanzil Uthmani v1.1 ayetleri. Sabitlenmiş sha256 tutmazsa VeriHatasi."""
    if not TANZIL_YOLU.exists():
        raise VeriHatasi(f"Tanzil dosyası bulunamadı: {TANZIL_YOLU}")
    gercek = sha256(TANZIL_YOLU)
    if gercek != TANZIL_SHA256:
        raise VeriHatasi(f"Tanzil sha256 uyuşmuyor.\n  beklenen: {TANZIL_SHA256}\n  bulunan : {gercek}")
    ayetler: dict[tuple[int, int], str] = {}
    with TANZIL_YOLU.open("r", encoding="utf-8-sig", newline="") as f:
        for ham in f:
            satir = ham.rstrip("\r\n")
            if not satir or satir.startswith("#"):
                continue
            s, a, metin = satir.split("|", 2)
            ayetler[(int(s), int(a))] = metin
    return ayetler


def besmele_metni() -> str:
    return tanzil()[(1, 1)]


def oku(sure: int, ayet: int) -> AyetOkunus:
    metin = tanzil().get((sure, ayet))
    if metin is None:
        raise KeyError(f"Tanzil'de ayet yok: {sure}:{ayet}")
    return ayet_oku(sure, ayet, metin)


# --- komut ------------------------------------------------------------------

def _ayet_ayristir(ref: str) -> tuple[int, int]:
    from .tara import GirdiHatasi
    parca = ref.split(":")
    if len(parca) != 2 or not all(p.isdigit() for p in parca):
        raise GirdiHatasi(f"Ayet referansı sûre:ayet biçiminde olmalı: {ref!r}")
    anahtar = (int(parca[0]), int(parca[1]))
    if anahtar not in tanzil():
        raise GirdiHatasi(f"Tanzil'de böyle bir ayet yok: {ref}")
    return anahtar


def okunus_komutu(refler: list[str], arapca: bool = False):
    from .tara import Sonuc, _tablo
    anahtarlar = [_ayet_ayristir(r) for r in refler]
    satirlar = ["Okunuş — Tanzil Uthmani metninden kurallı aktarım (delil değil; kurallar: okunus_kurallari.md)"]
    veri = {}
    for s, a in anahtarlar:
        o = oku(s, a)
        veri[f"{s}:{a}"] = o.latin
        satirlar += ["", f"Ayet {s}:{a}"]
        if o.besmele:
            satirlar.append("  [sûre başı besmelesi — Tanzil öneki, QAC'ta bu ayete dahil değil] "
                            + " ".join(k.latin for k in o.besmele))
        satirlar.append("  " + o.latin)
        basliklar = ["no", "okunuş"] + (["Tanzil (denetim için)"] if arapca else [])
        tablo = [[i, k.latin] + ([k.arapca] if arapca else []) for i, k in enumerate(o.kelimeler, 1)]
        satirlar += ["", "  Kelime kelime (Tanzil boşluk tokenı; QAC kelime konumu değildir):"]
        satirlar += ["  " + x for x in _tablo(basliklar, tablo, sag={0})]
        for b in o.belirsiz:
            satirlar.append(f"  BELİRSİZ: {b}")
    return Sonuc(satirlar, [], veri, kaynak=KAYNAK_ADI, veri_izi=TANZIL_SHA256[:12])
