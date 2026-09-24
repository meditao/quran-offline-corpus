"""QAC v0.4 yükleme, dizinler ve kurulum denetimi.

Ham dosya salt okunur açılır; bu modül hiçbir veri katmanına yazmaz.

Birimler (06_methodology/counting_units.md):
    ayet          (sûre, ayet)
    kelime konumu (sûre, ayet, kelime)            — QAC ortografik kelime
    segment       (sûre, ayet, kelime, segment)   — ön ek / gövde / son ek
"""

from __future__ import annotations

import hashlib
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from .harf import HARF_LATIN

DEPO = Path(__file__).resolve().parents[2]
QAC_YOLU = DEPO / "02_morphology" / "qac" / "quranic-corpus-morphology-0.4.txt"
ROOT_INDEX_YOLU = DEPO / "03_indices" / "generated" / "root_index.csv"
LEMMA_INDEX_YOLU = DEPO / "03_indices" / "generated" / "lemma_index.csv"

KAYNAK_ADI = "QAC v0.4"
QAC_SHA256 = "a1d12923815341face765083805d2148ed2d9f5cc3f7d6665219d887675d8c46"

# Kurulum denetiminin beklenen değerleri (CLAUDE.md §6).
BEKLENEN = {
    "sure": 114,
    "ayet": 6_236,
    "kelime konumu": 77_429,
    "segment": 128_219,
    "benzersiz kök": 1_642,
}

KONUM_RE = re.compile(r"^\((\d+):(\d+):(\d+):(\d+)\)$")
BAB_ETIKETLERI = {f"({b})": b for b in ("II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII")}
TELIF_ISARETI = "Copyright (C) 2011 Kais Dukes"

# Standart Buckwalter -> Arapça harf eşlemesi (build_qac_indices.py ile aynı).
BW_ARAPCA = {
    "'": "ء", "|": "آ", ">": "أ", "&": "ؤ", "<": "إ", "}": "ئ",
    "A": "ا", "b": "ب", "p": "ة", "t": "ت", "v": "ث", "j": "ج",
    "H": "ح", "x": "خ", "d": "د", "*": "ذ", "r": "ر", "z": "ز",
    "s": "س", "$": "ش", "S": "ص", "D": "ض", "T": "ط", "Z": "ظ",
    "E": "ع", "g": "غ", "f": "ف", "q": "ق", "k": "ك", "l": "ل",
    "m": "م", "n": "ن", "h": "ه", "w": "و", "Y": "ى", "y": "ي",
    "F": "ً", "N": "ٌ", "K": "ٍ", "a": "َ", "u": "ُ", "i": "ِ",
    "~": "ّ", "o": "ْ", "`": "ٰ", "{": "ٱ", "_": "ـ",
}
ARAPCA_BW = {v: k for k, v in BW_ARAPCA.items()}

# QAC kök alanında hemze/elif tek harfle ("A") yazılır. Arapça kök girişinde
# bütün hemze taşıyıcıları bu harfe indirgenir.
KOK_HEMZE = {"ء", "أ", "إ", "آ", "ؤ", "ئ", "ا", "ٱ"}

# Kök harflerinin ayrık Latin gösterimi, okunuşla ortak harf tablosundan
# (harf.py) türetilir. QAC kök alanındaki "A" hemzedir (ء -> ʾ).
# Eşleme kayıpsızdır: ص/س, ط/ت, ح/ه/خ, ث/س, ذ/ز/ض/ظ ayrımı korunur.
KOK_BW_HARFLERI = "AbtvjHxd*rzs$SDTZEgfqklmnhwy"
KOK_LATIN = {
    bw: HARF_LATIN["ء" if bw == "A" else BW_ARAPCA[bw]] for bw in KOK_BW_HARFLERI
}


class VeriHatasi(Exception):
    """Veri dosyası eksik, bozuk veya sabitlenmiş sürümle uyuşmuyor."""


def sha256(yol: Path) -> str:
    h = hashlib.sha256()
    with yol.open("rb") as f:
        for parca in iter(lambda: f.read(1 << 20), b""):
            h.update(parca)
    return h.hexdigest()


def bw_arapca(metin: str) -> str:
    return "".join(BW_ARAPCA.get(ch, ch) for ch in metin)


def kok_latin(kok_bw: str) -> str:
    """Buckwalter kökü ayrık Latin biçime çevirir: Slw -> ṣ-l-v."""
    return "-".join(KOK_LATIN.get(ch, ch) for ch in kok_bw)


def kok_arapca_ayrik(kok_bw: str) -> str:
    return " ".join(BW_ARAPCA.get(ch, ch) for ch in kok_bw)


def binlik(n: int) -> str:
    """Türkçe binlik ayırıcıyla sayı: 77429 -> 77.429"""
    return f"{n:,}".replace(",", ".")


@dataclass(slots=True, eq=False)
class Segment:
    sure: int
    ayet: int
    kelime: int
    no: int
    bicim: str                 # FORM sütunu (Buckwalter, ham)
    etiket: str                # TAG sütunu
    ozellikler: tuple[str, ...]  # FEATURES sütunu, '|' ile bölünmüş, ham
    tur: str                   # PREFIX | STEM | SUFFIX
    pos: str | None
    lemma: str | None
    kok: str | None
    bab: str | None            # "II".."XII"; QAC I. babı işaretlemez -> None
    etiketler: frozenset[str]  # ozellikler + "TAG:<etiket>" (tam eşleşme kümesi)

    @property
    def konum(self) -> str:
        return f"{self.sure}:{self.ayet}:{self.kelime}:{self.no}"

    @property
    def kelime_anahtari(self) -> tuple[int, int, int]:
        return (self.sure, self.ayet, self.kelime)

    @property
    def zamir(self) -> str | None:
        """Son ek zamir segmentiyse zamir kişisi (ör. '3MS'), değilse None."""
        if self.tur != "SUFFIX":
            return None
        for oz in self.ozellikler:
            if oz.startswith("PRON:"):
                return oz.split(":", 1)[1]
        return None


@dataclass
class Kelime:
    sure: int
    ayet: int
    kelime: int
    segmentler: list[Segment] = field(default_factory=list)

    @property
    def anahtar(self) -> tuple[int, int, int]:
        return (self.sure, self.ayet, self.kelime)

    @property
    def konum(self) -> str:
        return f"{self.sure}:{self.ayet}:{self.kelime}"

    @property
    def bicim(self) -> str:
        return "".join(s.bicim for s in self.segmentler)

    @property
    def kokler(self) -> frozenset[str]:
        return frozenset(s.kok for s in self.segmentler if s.kok)

    @property
    def lemmalar(self) -> frozenset[str]:
        return frozenset(s.lemma for s in self.segmentler if s.lemma)


@dataclass
class Korpus:
    segmentler: list[Segment]
    kelimeler: list[Kelime]
    sha256: str
    telif_blogu: bool
    kok_kelimeleri: dict[str, list[Kelime]]
    lemma_kelimeleri: dict[str, list[Kelime]]
    ayet_segmentleri: dict[tuple[int, int], list[Segment]]
    etiket_envanteri: Counter  # etiket -> segment sayısı

    @property
    def veri_izi(self) -> str:
        return self.sha256[:12]

    @property
    def ayetler(self) -> list[tuple[int, int]]:
        return list(self.ayet_segmentleri)

    @property
    def sureler(self) -> set[int]:
        return {s for s, _ in self.ayet_segmentleri}


def _segment_ayristir(satir_no: int, satir: str) -> Segment:
    parcalar = satir.split("\t")
    if len(parcalar) != 4:
        raise VeriHatasi(f"Satır {satir_no}: 4 TSV alanı bekleniyordu, {len(parcalar)} bulundu")
    konum, bicim, etiket, ozellik_metni = parcalar
    m = KONUM_RE.match(konum)
    if not m:
        raise VeriHatasi(f"Satır {satir_no}: geçersiz konum {konum!r}")
    sure, ayet, kelime, no = map(int, m.groups())
    ozellikler = tuple(ozellik_metni.split("|"))
    tur = ozellikler[0]
    pos = lemma = kok = bab = None
    for oz in ozellikler:
        if oz.startswith("POS:"):
            pos = oz[4:]
        elif oz.startswith("LEM:"):
            lemma = oz[4:]
        elif oz.startswith("ROOT:"):
            kok = oz[5:]
        elif oz in BAB_ETIKETLERI:
            bab = BAB_ETIKETLERI[oz]
    return Segment(
        sure=sure, ayet=ayet, kelime=kelime, no=no,
        bicim=bicim, etiket=etiket, ozellikler=ozellikler, tur=tur,
        pos=pos, lemma=lemma, kok=kok, bab=bab,
        etiketler=frozenset(ozellikler) | {f"TAG:{etiket}"},
    )


def yukle(yol: Path = QAC_YOLU, sha_denetle: bool = True) -> Korpus:
    """QAC dosyasını okur. Sabitlenmiş sha256 tutmazsa VeriHatasi fırlatır."""
    if not yol.exists():
        raise VeriHatasi(f"QAC dosyası bulunamadı: {yol}")
    gercek_sha = sha256(yol)
    if sha_denetle and gercek_sha != QAC_SHA256:
        raise VeriHatasi(
            f"QAC sha256 uyuşmuyor.\n  beklenen: {QAC_SHA256}\n  bulunan : {gercek_sha}"
        )

    segmentler: list[Segment] = []
    telif = False
    # utf-8-sig: olası BOM; satır sonları CRLF olduğundan \r ayrıca soyulur.
    with yol.open("r", encoding="utf-8-sig", errors="strict", newline="") as f:
        for satir_no, ham in enumerate(f, 1):
            satir = ham.rstrip("\r\n")
            if TELIF_ISARETI in satir:
                telif = True
            if not satir.startswith("("):
                continue
            segmentler.append(_segment_ayristir(satir_no, satir))

    kelimeler: list[Kelime] = []
    kelime_dizini: dict[tuple[int, int, int], Kelime] = {}
    ayet_segmentleri: dict[tuple[int, int], list[Segment]] = {}
    etiket_envanteri: Counter = Counter()
    for seg in segmentler:
        k = kelime_dizini.get(seg.kelime_anahtari)
        if k is None:
            k = Kelime(seg.sure, seg.ayet, seg.kelime)
            kelime_dizini[seg.kelime_anahtari] = k
            kelimeler.append(k)
        k.segmentler.append(seg)
        ayet_segmentleri.setdefault((seg.sure, seg.ayet), []).append(seg)
        etiket_envanteri.update(seg.etiketler)

    kok_kelimeleri: dict[str, list[Kelime]] = defaultdict(list)
    lemma_kelimeleri: dict[str, list[Kelime]] = defaultdict(list)
    for k in kelimeler:
        # Aynı kelime konumunda tekrar eden kök/lemma bir kez sayılır.
        for kok in k.kokler:
            kok_kelimeleri[kok].append(k)
        for lemma in k.lemmalar:
            lemma_kelimeleri[lemma].append(k)

    return Korpus(
        segmentler=segmentler,
        kelimeler=kelimeler,
        sha256=gercek_sha,
        telif_blogu=telif,
        kok_kelimeleri=dict(kok_kelimeleri),
        lemma_kelimeleri=dict(lemma_kelimeleri),
        ayet_segmentleri=ayet_segmentleri,
        etiket_envanteri=etiket_envanteri,
    )


@lru_cache(maxsize=1)
def korpus() -> Korpus:
    """Süreç başına bir kez yüklenen kanonik korpus."""
    return yukle()


@dataclass(frozen=True)
class Denetim:
    ad: str
    beklenen: str
    bulunan: str
    gecti: bool


def kurulum_denetimi() -> list[Denetim]:
    """Dosya varlığı, sha256, telif bloğu ve temel sayımları denetler."""
    sonuc: list[Denetim] = []
    if not QAC_YOLU.exists():
        return [Denetim("QAC dosyası", str(QAC_YOLU.relative_to(DEPO)), "yok", False)]
    try:
        kor = korpus()
    except VeriHatasi:
        kor = yukle(sha_denetle=False)
    sonuc.append(Denetim("QAC sha256", QAC_SHA256, kor.sha256, kor.sha256 == QAC_SHA256))
    sonuc.append(Denetim("QAC telif bloğu", "var", "var" if kor.telif_blogu else "yok", kor.telif_blogu))
    olculen = {
        "sure": len(kor.sureler),
        "ayet": len(kor.ayet_segmentleri),
        "kelime konumu": len(kor.kelimeler),
        "segment": len(kor.segmentler),
        "benzersiz kök": len(kor.kok_kelimeleri),
    }
    for ad, beklenen in BEKLENEN.items():
        sonuc.append(Denetim(ad, binlik(beklenen), binlik(olculen[ad]), olculen[ad] == beklenen))
    for yol in (ROOT_INDEX_YOLU, LEMMA_INDEX_YOLU):
        var = yol.exists()
        sonuc.append(Denetim(str(yol.relative_to(DEPO)), "var", "var" if var else "yok", var))
    return sonuc
