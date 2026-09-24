"""Karşılaştırmalı Sâmî katmanı: İbranice + Süryanice — hipotez kaynağı, delil değil.

Kaynaklar:
- İbranice: depodaki 04_lexicons/generated/hebrew_lexical_index.tsv (Open Scriptures Hebrew Lexicon,
  CC BY 4.0) yerinde okunur, kopyalanmaz. Kök = `etym_root`, anlam = aynı köke bağlı `main` kayıtların
  `definition` alanı.
- Süryanice: SEDRA 3 (sedrajs deposundaki değiştirilmemiş ROOTS/LEXEMES/ENGLISH dosyaları) yerel/sedra/
  altında. Değiştirilmiş dosya dağıtılamaz; depoya işlenmez. Kurulum: python -m tezgah kur sedra
- İncelenmiş kognat kayıtları: 04_lexicons/semitic/cognates.tsv (yerinde okunur).

Kurallar (kök analizi becerisi §11; sayılar QAC v0.4'ün 1.642 köküne göre yeniden ölçülür):
- Kognat anlam değildir: ortak ünsüz dizisi yalnız ortak köken adayıdır.
- Tek dildeki vuruş tek başına raporlanmaz; gürültü tabanı `sami gurultu` ile ölçülür.
- "Aday yok" bulgu değildir: sözlükler eksiksiz değildir.
- İbranice ile Süryanice bağımsız iki tanık değildir (ikisi de Kuzeybatı Sâmî).
- Ödünçleme yönü bu yöntemle ayırt edilemez.
"""

from __future__ import annotations

import csv
import itertools
import random
from collections import Counter
from functools import lru_cache
from pathlib import Path

from .. import veri
from . import etiketle, indir, manifest_yaz

MASA = Path(__file__).resolve().parents[2]
IBRANICE_YOLU = veri.DEPO / "04_lexicons" / "generated" / "hebrew_lexical_index.tsv"
KOGNAT_YOLU = veri.DEPO / "04_lexicons" / "semitic" / "cognates.tsv"
SEDRA_DIZINI = MASA / "yerel" / "sedra"
SEDRA_MANIFEST = SEDRA_DIZINI / "manifest.json"
SEDRA_DEPO = "peshitta/sedrajs"
SEDRA_COMMIT = "ba6684a97e80cde14cc2b51903d8f802a1a19ab1"
SEDRA_DOSYALARI = {
    "ROOTS.TXT": "f90fbf51a3deb03ed94f86ddacaea341304180af00dd893d7d58507ae993169a",
    "LEXEMES.TXT": "30ee106f62237d5279f088c1c98c56460b9ae43db77b3752220b839d3813b5e4",
    "ENGLISH.TXT": "43ca8e0a0b3c66823cb9dbf2a6f029adf03384c02f69a00a0fcc9e9723df41d4",
    "SEDRA3.DOC": "f316c01596555d4c725a1ea819f18afc256e547bfc902955f4ad23d64b3cd4d6",
}
KAYNAK_ADI = "Sâmî"
SEDRA_ATIF = ("This work makes use of the Syriac Electronic Data Retrieval Archive (SEDRA) by George A. Kiraz, "
              "distributed by the Syriac Computing Institute. — G. Kiraz, 'Automatic Concordance Generation of "
              "Syriac Texts', VI Symposium Syriacum 1992, OCA 247, Roma 1994.")

# Ünsüz denklik tablosu (karşılaştırmalı Sâmî dilbiliminin yerleşik denklikleri; hipotez düzeyinde).
# Arapça harf -> İbranice harfler (sonu-harfleri normalleştirilmiş, noktasız ש) / SEDRA harf kodları.
IBRANICE_DENKLIK = {
    "ء": "א", "ب": "ב", "ت": "ת", "ث": "ש", "ج": "ג", "ح": "ח", "خ": "ח", "د": "ד", "ذ": "ז", "ر": "ר",
    "ز": "ז", "س": "שס", "ش": "ש", "ص": "צ", "ض": "צ", "ط": "ט", "ظ": "צט", "ع": "ע", "غ": "ע", "ف": "פ",
    "ق": "ק", "ك": "כ", "ل": "ל", "م": "מ", "ن": "נ", "ه": "ה", "و": "וי", "ي": "יו",
}
# SEDRA kodu: A B G D H O Z K Y ; C L M N S E I / X R W T = ʾ b g d h w z ḥ ṭ y k l m n s ʿ p ṣ q r š t
SURYANICE_DENKLIK = {
    "ء": "A", "ب": "B", "ت": "T", "ث": "T", "ج": "G", "ح": "K", "خ": "K", "د": "D", "ذ": "D", "ر": "R",
    "ز": "Z", "س": "SW", "ش": "W", "ص": "/", "ض": "E/", "ط": "Y", "ظ": "Y", "ع": "E", "غ": "E", "ف": "I",
    "ق": "X", "ك": "C", "ل": "L", "م": "M", "ن": "N", "ه": "H", "و": "O;", "ي": ";O",
}
SEDRA_LATIN = dict(zip("ABGDHOZKY;CLMNSEI/XRWT",
                       ["ʾ", "b", "g", "d", "h", "w", "z", "ḥ", "ṭ", "y", "k", "l", "m", "n", "s", "ʿ", "p", "ṣ", "q", "r", "š", "t"]))
IBRANICE_LATIN = {"א": "ʾ", "ב": "b", "ג": "g", "ד": "d", "ה": "h", "ו": "w", "ז": "z", "ח": "ḥ", "ט": "ṭ",
                  "י": "y", "כ": "k", "ל": "l", "מ": "m", "נ": "n", "ס": "s", "ע": "ʿ", "פ": "p", "צ": "ṣ",
                  "ק": "q", "ר": "r", "ש": "š/ś", "ת": "t"}
SONU_HARFLERI = str.maketrans("ךםןףץ", "כמנפצ")


def ibranice_normal(metin: str) -> str:
    """Harekeleri (U+0591–05C7) atar, sonu-harflerini normalleştirir."""
    return "".join(c for c in metin if not ("֑" <= c <= "ׇ")).translate(SONU_HARFLERI)


def qac_harfleri(kok_bw: str) -> str:
    return "".join("ء" if c == "A" else veri.BW_ARAPCA[c] for c in kok_bw)


# --- veri yükleme ---------------------------------------------------------------

@lru_cache(maxsize=1)
def ibranice() -> dict[str, list[tuple[str, str]]]:
    """İbranice kök -> [(transliterasyon, anlam)] (main kayıtlar)."""
    d: dict[str, list[tuple[str, str]]] = {}
    with IBRANICE_YOLU.open(encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            kok = ibranice_normal(r["etym_root"])
            if not kok:
                continue
            d.setdefault(kok, [])
            if r["etym_type"] == "main" and r["definition"]:
                d[kok].append((r["translit"], r["definition"]))
    return d


def sedra_kurulu() -> bool:
    return all((SEDRA_DIZINI / ad).exists() for ad in SEDRA_DOSYALARI)


def _sedra_satirlari(ad: str) -> list[list[str]]:
    yol = SEDRA_DIZINI / ad
    satirlar = []
    with yol.open(encoding="latin-1", newline="") as f:
        for ham in f:
            satir = ham.rstrip("\r\n")          # SEDRA dosyaları CRLF'dir
            if satir:
                satirlar.append(next(csv.reader([satir])))
    return satirlar


@lru_cache(maxsize=1)
def suryanice() -> dict[str, list[str]] | None:
    """SEDRA kök kodu -> İngilizce anlamlar (kök -> sözcük -> anlam zinciri)."""
    if not sedra_kurulu():
        return None
    for ad, sha in SEDRA_DOSYALARI.items():
        if veri.sha256(SEDRA_DIZINI / ad) != sha:
            raise veri.VeriHatasi(f"SEDRA dosyası değişmiş: {ad} (değiştirilmiş SEDRA kullanılmaz/dağıtılmaz)")
    # Bağlantısız kayıtlar (adres alanı NULL) atlanır ve sayılır: sedra_bagsiz().
    kokler = {s[0].split(":")[1]: s[1] for s in _sedra_satirlari("ROOTS.TXT")}
    sozcuk_kok = {s[0].split(":")[1]: s[1].split(":")[1] for s in _sedra_satirlari("LEXEMES.TXT") if s[1] != "NULL"}
    d: dict[str, list[str]] = {k: [] for k in kokler.values()}
    for s in _sedra_satirlari("ENGLISH.TXT"):
        if s[1] == "NULL":
            continue
        kok_no = sozcuk_kok.get(s[1].split(":")[1])
        if kok_no in kokler and s[2]:
            d[kokler[kok_no]].append(s[2])
    return d


@lru_cache(maxsize=1)
def sedra_bagsiz() -> dict[str, int]:
    return {ad: sum(1 for s in _sedra_satirlari(ad) if s[1] == "NULL") for ad in ("LEXEMES.TXT", "ENGLISH.TXT")}


@lru_cache(maxsize=1)
def incelenmis() -> dict[str, list[dict]]:
    if not KOGNAT_YOLU.exists():
        return {}
    d: dict[str, list[dict]] = {}
    with KOGNAT_YOLU.open(encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            d.setdefault(r["quran_root_bw"], []).append(r)
    return d


def kur() -> dict:
    if sedra_kurulu():
        raise FileExistsError(f"SEDRA zaten kurulu: {SEDRA_DIZINI}")
    SEDRA_DIZINI.mkdir(parents=True, exist_ok=True)
    for ad, sha in SEDRA_DOSYALARI.items():
        url = f"https://raw.githubusercontent.com/{SEDRA_DEPO}/{SEDRA_COMMIT}/sedra/{ad}"
        (SEDRA_DIZINI / ad).write_bytes(indir(url, sha))
    bilgi = {"depo": SEDRA_DEPO, "commit": SEDRA_COMMIT, "dosyalar": SEDRA_DOSYALARI,
             "lisans": "SEDRA 3: kişisel/akademik kullanım; değiştirilmiş dosya dağıtılamaz, ticari kullanılamaz, "
                       "yayında atıf zorunlu — depoya işlenmez",
             "atif": SEDRA_ATIF, "statu": "hipotez kaynağı, delil değil"}
    manifest_yaz(SEDRA_MANIFEST, bilgi)
    return bilgi


# --- eşleştirme -----------------------------------------------------------------

# Son harfi zayıf (و/ي) kökler: İbranice sözlük geleneği ה ile (lamed-he: בנה), SEDRA Alef ile yazar.
# Varsayılan KAPALI: aynı kök ve sahte kök kümesinde ölçüldü, kural gerçek/rastgele oranını üç
# ölçümde de düşürüyor (gerçek vuruşu artırıyor ama gürültüyü daha çok artırıyor). --zayif-son ile açılır.
SON_ZAYIF = {"ibranice": "ה", "suryanice": "A"}


def adaylar(harfler: str, denklik: dict[str, str], envanter, son_zayif: str = "") -> list[str]:
    secenek = [denklik.get(c, "") for c in harfler]
    if harfler and harfler[-1] in "وي" and son_zayif:
        secenek[-1] += son_zayif
    if not all(secenek):
        return []
    return sorted({"".join(p) for p in itertools.product(*secenek) if "".join(p) in envanter})


def vurus(harfler: str, zayif_son: bool = False) -> tuple[list[str], list[str]]:
    sur = suryanice() or {}
    ek_h, ek_s = (SON_ZAYIF["ibranice"], SON_ZAYIF["suryanice"]) if zayif_son else ("", "")
    return (adaylar(harfler, IBRANICE_DENKLIK, ibranice(), ek_h),
            adaylar(harfler, SURYANICE_DENKLIK, sur, ek_s))


def _oranlar(kokler: list[str], zayif_son: bool = False) -> dict[str, float]:
    n = len(kokler)
    h = s = iki = 0
    for k in kokler:
        a, b = vurus(k, zayif_son)
        h += bool(a)
        s += bool(b)
        iki += bool(a and b)
    return {"ibranice": h / n, "suryanice": s / n, "ikisi": iki / n}


@lru_cache(maxsize=4)
def gurultu(tekrar: int = 10, tohum: int = 20260924, zayif_son: bool = False) -> dict:
    """Gerçek QAC kökleri ile aynı harf ve uzunluk dağılımından üretilmiş sahte köklerin vuruş oranı."""
    kor = veri.korpus()
    gercek = [qac_harfleri(k) for k in kor.kok_kelimeleri]
    gercek_kume = set(gercek)
    harf_dagilimi = Counter(c for k in gercek for c in k)
    harfler, agirlik = zip(*sorted(harf_dagilimi.items()))
    uzunluk = [len(k) for k in gercek]
    rng = random.Random(tohum)
    rastgele_oranlar = []
    for _ in range(tekrar):
        sahte = []
        for u in uzunluk:
            while True:
                aday = "".join(rng.choices(harfler, agirlik, k=u))
                if aday not in gercek_kume:
                    break
            sahte.append(aday)
        rastgele_oranlar.append(_oranlar(sahte, zayif_son))
    g = _oranlar(gercek, zayif_son)
    sonuc = {"kok": len(gercek), "tekrar": tekrar, "tohum": tohum, "gercek": g, "rastgele": {}, "gurultu_payi": {}}
    for dil in ("ibranice", "suryanice", "ikisi"):
        degerler = [r[dil] for r in rastgele_oranlar]
        ort = sum(degerler) / len(degerler)
        sonuc["rastgele"][dil] = {"ortalama": ort, "en_az": min(degerler), "en_cok": max(degerler)}
        sonuc["gurultu_payi"][dil] = ort / g[dil] if g[dil] else None
    return sonuc


def _yuzde(x: float) -> str:
    return f"%{100 * x:.1f}".replace(".", ",")


# --- komutlar ---------------------------------------------------------------------

def kok_komutu(kor: veri.Korpus, girdi: str, tek_dil: bool = False, tam: bool = False, zayif_son: bool = False):
    from ..tara import Sonuc, kok_coz
    c = kok_coz(kor, girdi)
    harfler = qac_harfleri(c.bw)
    heb, sur = vurus(harfler, zayif_son)
    sur_kurulu = suryanice() is not None
    g = gurultu(zayif_son=zayif_son)
    satirlar = [
        "Karşılaştırmalı Sâmî katmanı (İbranice: Open Scriptures Hebrew Lexicon dizini; Süryanice: SEDRA 3) — "
        "hipotez kaynağı, delil değil.",
        "Kognat anlam değildir: ortak ünsüz dizisi yalnız ortak köken adayıdır. İbranice ve Süryanice bağımsız "
        "iki tanık değildir; ödünçleme yönü bu yöntemle ayırt edilemez.",
        f"QAC kökü: {c.bw} ({c.latin})",
        "Son-harf-zayıf kuralı: " + ("AÇIK (--zayif-son; ölçümde gerçek/rastgele oranını düşürüyor, gürültü payı yüksek)"
                                     if zayif_son else "kapalı (açmak için --zayif-son)"),
    ]
    for r in incelenmis().get(c.bw, []):
        satirlar.append(f"İncelenmiş kayıt (04_lexicons/semitic/cognates.tsv): {r['language']} {r['cognate_translit']} — "
                        f"{r['gloss']} · ses uyumu: {r['phonological_fit'].split(':')[0]} · anlam uyumu: "
                        f"{r['semantic_fit'].split(':')[0]} · güven: {r['confidence']}")
    if not sur_kurulu:
        satirlar.append("SEDRA kurulu değil (python -m tezgah kur sedra): Süryanice taranmadı; 'ikisi birden' ölçülemez.")

    def goster(dil: str, kokler: list[str], anlam, latin) -> None:
        for k in kokler:
            anlamlar = anlam(k)
            metin = "; ".join(anlamlar if tam else anlamlar[:4]) or "(anlam kaydı yok)"
            satirlar.append(f"  {dil} {latin(k)}: {metin}")

    heb_latin = lambda k: "-".join(IBRANICE_LATIN.get(x, x) for x in k)
    sur_latin = lambda k: "-".join(SEDRA_LATIN.get(x, x) for x in k)
    heb_anlam = lambda k: [f"{t} '{d}'" for t, d in ibranice()[k]]
    sur_anlam = lambda k: suryanice()[k]

    if heb and sur:
        satirlar.append(f"İki dilde aday var (ikisi birden; ölçülen gürültü payı ≈ {_yuzde(g['gurultu_payi']['ikisi'])}):")
        goster("İbranice", heb, heb_anlam, heb_latin)
        goster("Süryanice", sur, sur_anlam, sur_latin)
    elif heb or sur:
        dil, kokler = ("İbranice", heb) if heb else ("Süryanice", sur)
        pay = g["gurultu_payi"]["ibranice" if heb else "suryanice"]
        satirlar.append(f"Yalnız {dil}'de {len(kokler)} aday — tek dil vuruşu tek başına raporlanmaz "
                        f"(ölçülen gürültü payı ≈ {_yuzde(pay)}).")
        if tek_dil:
            satirlar.append("  --tek-dil: adaylar gösteriliyor; anlam yakınlığı ayrıca gerekçelendirilmedikçe kullanılmaz.")
            goster(dil, kokler, heb_anlam if heb else sur_anlam, heb_latin if heb else sur_latin)
    else:
        satirlar.append("Aday yok — bu bir bulgu değildir (sözlükler eksiksiz değildir).")
    if not zayif_son:
        h2, s2 = vurus(harfler, True)
        if (h2, s2) != (heb, sur):
            satirlar.append(f"Not: --zayif-son ile aday kümesi değişir (İbranice {len(h2)}, Süryanice {len(s2)}); kural "
                            "ölçümde gerçek/rastgele oranını düşürdüğü için varsayılan kapalı (sami gurultu).")
    satirlar.append("Kural: hipotez korpusta sınanır; sonuç korpus bulgusuyla yazılır. SEDRA yayında atıf ister: sami atif")
    iz = f"{kor.veri_izi} | {veri.sha256(IBRANICE_YOLU)[:12]}" + (
        f" | {SEDRA_DOSYALARI['ROOTS.TXT'][:12]}" if sur_kurulu else "")
    return Sonuc(etiketle(satirlar), [], {"ibranice": heb, "suryanice": sur},
                 kaynak=f"QAC v0.4 | + {KAYNAK_ADI}", veri_izi=iz)


DIL_ADI = {"ibranice": "İbranice", "suryanice": "Süryanice", "ikisi": "ikisi birden"}


def gurultu_karsilastirma(tekrar: int = 10, tohum: int = 20260924) -> dict:
    """Aynı gerçek kök ve aynı sahte kök kümesinde son-harf-zayıf kuralı kapalı ↔ açık."""
    sonuc = {}
    for ad, z in (("kapali", False), ("acik", True)):
        g = dict(gurultu(tekrar, tohum, z))   # önbellekteki sözlük değiştirilmez
        g["gercek_rastgele_orani"] = {d: (g["gercek"][d] / g["rastgele"][d]["ortalama"]
                                          if g["rastgele"][d]["ortalama"] else None) for d in g["gercek"]}
        sonuc[ad] = g
    sonuc["kural_iyilestiriyor"] = {d: sonuc["acik"]["gercek_rastgele_orani"][d] > sonuc["kapali"]["gercek_rastgele_orani"][d]
                                    for d in sonuc["kapali"]["gercek"]}
    return sonuc


def gurultu_komutu(kor: veri.Korpus, tekrar: int, tohum: int):
    from ..tara import GirdiHatasi, Sonuc, _tablo
    if suryanice() is None:
        raise GirdiHatasi("SEDRA kurulu değil (python -m tezgah kur sedra); gürültü ölçümü iki dili ister.")
    k = gurultu_karsilastirma(tekrar, tohum)
    g0 = k["kapali"]
    tablo = []
    for ad_k, etiket in (("kapali", "kapalı (varsayılan)"), ("acik", "açık (--zayif-son)")):
        g = k[ad_k]
        for dil, ad in (("ibranice", "İbranice"), ("suryanice", "Süryanice"), ("ikisi", "ikisi birden")):
            r = g["rastgele"][dil]
            tablo.append([etiket, ad, _yuzde(g["gercek"][dil]),
                          f"{_yuzde(r['ortalama'])} ({_yuzde(r['en_az'])}–{_yuzde(r['en_cok'])})",
                          f"{g['gercek_rastgele_orani'][dil]:.2f}".replace(".", ","), _yuzde(g["gurultu_payi"][dil])])
    iyi = k["kural_iyilestiriyor"]
    satirlar = [
        f"Sâmî gürültü tabanı — QAC v0.4'ün {g0['kok']} gerçek kökü ↔ aynı harf ve uzunluk dağılımından "
        f"{g0['tekrar']} kez {g0['kok']} sahte kök (tohum {g0['tohum']}; gerçek köklerle çakışanlar atıldı). Birim: kök.",
        "Son-harf-zayıf kuralı kapalı ve açık, aynı gerçek ve aynı sahte kök kümesinde ölçüldü:",
        *_tablo(["kural", "dil", "gerçek vuruş", "rastgele vuruş (ort., en az–en çok)", "gerçek/rastgele", "gürültü payı"],
                tablo, sag={2, 3, 4, 5}),
        "Gürültü payı = rastgele ortalama / gerçek oran. Gerçek/rastgele oranı yüksek olan ayrım gücü yüksek olandır.",
        "Kural oranı iyileştiriyor mu: " + ", ".join(f"{DIL_ADI[d]}: {'evet' if v else 'hayır'}" for d, v in iyi.items())
        + (" → varsayılan kapalı." if not any(iyi.values()) else " → karışık sonuç; varsayılan kapalı."),
        f"İbranice kök envanteri: {len(ibranice())}; SEDRA kök envanteri: {len(suryanice())} (farklı kök yazımı; "
        f"köke bağlanmamış SEDRA kaydı atlandı: sözcük {sedra_bagsiz()['LEXEMES.TXT']}, anlam {sedra_bagsiz()['ENGLISH.TXT']}).",
    ]
    return Sonuc(etiketle(satirlar), ["kök"], k, kaynak=f"QAC v0.4 | + {KAYNAK_ADI}",
                 veri_izi=f"{kor.veri_izi} | {veri.sha256(IBRANICE_YOLU)[:12]} | {SEDRA_DOSYALARI['ROOTS.TXT'][:12]}")


def denklik_komutu():
    from ..harf import HARF_LATIN
    from ..tara import Sonuc, _tablo
    tablo = [[HARF_LATIN.get(a, a), " / ".join(IBRANICE_LATIN[h] for h in IBRANICE_DENKLIK[a]),
              " / ".join(SEDRA_LATIN[s] for s in SURYANICE_DENKLIK[a])] for a in IBRANICE_DENKLIK]
    satirlar = ["Ünsüz denklik tablosu (Arapça → İbranice / Süryanice; karşılaştırmalı Sâmî dilbiliminin yerleşik "
                "denklikleri — hipotez düzeyinde, ses yasası istisnaları kapsanmaz):",
                *_tablo(["Arapça", "İbranice", "Süryanice"], tablo),
                "Son harfi zayıf kök (و/ي): --zayif-son ile İbranice ayrıca ה (lamed-he yazımı), Süryanice ayrıca ʾ (Alef) "
                "ile eşlenir; varsayılan kapalı (sami gurultu: kural gerçek/rastgele oranını düşürüyor)."]
    return Sonuc(etiketle(satirlar), [], {}, kaynak=KAYNAK_ADI, veri_izi="—")


def atif_komutu():
    from ..tara import Sonuc
    return Sonuc(etiketle(["SEDRA atıf metni (sonuç yayımlanırsa zorunlu):", SEDRA_ATIF,
                           "BDB/Open Scriptures Hebrew Lexicon: CC BY 4.0 — atıf: Open Scriptures Hebrew Lexicon."]),
                 [], {}, kaynak=KAYNAK_ADI, veri_izi="—")
