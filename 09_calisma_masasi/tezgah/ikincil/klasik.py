"""İki klasik kök sözlüğü: İbn Fâris Mekâyîs ve Râgıb Müfredât — hipotez kaynağı, delil değil.

  ibnfaris  Mu'cemü Mekâyîsi'l-lüga (İbn Fâris, ö. 395/1004) — kökün "asl"ı
  ragib     el-Müfredât fî garîbi'l-Kur'ân (Râgıb, 5./11. yy.) — Kur'an kullanımı

Kurallar (CLAUDE.md §2.1, §2.4; protokol: 06_methodology/analiz_protokolu.md Aşama 7a):
- Zincir tek yönlüdür: sözlük hipotez üretir, korpus sınar, sonuç korpus bulgusuyla yazılır.
  Önce kör okuma, sonra sözlük.
- Birim cümle değil ANLAMDIR: bir anlam beyanı + o anlama getirilen tanık(lar). Her birim
  dayanağına göre etiketlenir ve statü alır (hadis, rivayet, şer'î, yorumcu nakli, dil-içi tanık).
  Etiketler biçimseldir; bir birimin içinde iki anlam kalmış olabilir. Örtük etki (tanık
  gösterilmeden tefsirden alınmış anlam) işaretle yakalanamaz.
- "Madde yok" anlam yok demek değildir; dijital metinde bazı kökler eksiktir ya da başka maddede
  anılır. Kapsam QAC v0.4'ün kökleriyle ölçülür (`klasik kapsam`).
- Zayıf kuralla eşleşen kök "<< DOĞRULA" ile işaretlenir ve elle denetlenir.
- Sözlüğün ayet atıfları korpusla denetlenir (`klasik ayet`): atıf yanlış ya da baskı hatası olabilir.
- Sunum: kök ve madde başlığı harf tablosuyla (harf.py) kayıpsız Latin yazılır. Sözlük
  cümleleri harekesizdir, kurallı okunuş üretilemez; özgün Arapça metin olarak, "hipotez" etiketiyle
  verilir ve analizde Türkçeye çevrilir (uzun birebir alıntı yapılmaz).

Veri: yerel/klasik/klasik.json (depoya işlenmez; OpenITI, CC BY-NC-SA 4.0).
Kurulum: python -m tezgah kur klasik
"""

from __future__ import annotations

import collections
import hashlib
import json
import re
import tempfile
from functools import lru_cache
from pathlib import Path

from .. import veri
from ..harf import HARF_LATIN
from . import etiketle as hipotez_etiketle
from . import indir, manifest_yaz
from .klasik_ayristir import TASH, anahtarlar, ayristir, eslestir, norm

MASA = Path(__file__).resolve().parents[2]
KLASIK_DIZINI = MASA / "yerel" / "klasik"
KLASIK_YOLU = KLASIK_DIZINI / "klasik.json"
KLASIK_MANIFEST = KLASIK_DIZINI / "manifest.json"
KAYNAK_ADI = "klasik"

# OpenITI — commit'e sabitlenmiş; dosya değişirse sağlama toplamı tutmaz.
OPENITI = "https://raw.githubusercontent.com/OpenITI/%s/%s/data/%s"
ESERLER = {
    "ibnfaris": dict(
        depo="0400AH", commit="5bb6966d8df2ed22b1bff5cdbe29bb9c24f3ca29",
        yol="0395IbnFarisQazwini/0395IbnFarisQazwini.MucjamMaqayis/"
            "0395IbnFarisQazwini.MucjamMaqayis.Shamela0021710-ara1",
        sha256="7f71af0dfe056cb84e7da24657fa13edc6e8061ca1980eed7f6c196bd18b5689"),
    "ragib": dict(
        depo="0525AH", commit="6290621b58e063ed1aa47ffd0a6fc1630191e7cb",
        yol="0502RaghibIsbahani/0502RaghibIsbahani.Mufradat/"
            "0502RaghibIsbahani.Mufradat.Shamela0023636-ara1",
        sha256="721da9e2168f8dcd6dd6876a73b4a304496656e57ba9b2e26a07d7f871a78e19"),
}
ESER_AD = {"ibnfaris": "İbn Fâris, Mekâyîs", "ragib": "Râgıb, Müfredât"}
BEKLENEN_MADDE = {"ibnfaris": 4649, "ragib": 1662}

SURELER = """الفاتحة البقرة آل_عمران النساء المائدة الأنعام الأعراف الأنفال التوبة يونس هود
يوسف الرعد إبراهيم الحجر النحل الإسراء الكهف مريم طه الأنبياء الحج المؤمنون النور
الفرقان الشعراء النمل القصص العنكبوت الروم لقمان السجدة الأحزاب سبأ فاطر يس الصافات ص
الزمر غافر فصلت الشورى الزخرف الدخان الجاثية الأحقاف محمد الفتح الحجرات ق الذاريات
الطور النجم القمر الرحمن الواقعة الحديد المجادلة الحشر الممتحنة الصف الجمعة المنافقون
التغابن الطلاق التحريم الملك القلم الحاقة المعارج نوح الجن المزمل المدثر القيامة
الإنسان المرسلات النبأ النازعات عبس التكوير الانفطار المطففين الانشقاق البروج الطارق
الأعلى الغاشية الفجر البلد الشمس الليل الضحى الشرح التين العلق القدر البينة الزلزلة
العاديات القارعة التكاثر العصر الهمزة الفيل قريش الماعون الكوثر الكافرون النصر المسد
الإخلاص الفلق الناس""".split()
SURE_NO = {norm(a.replace("_", " ")): i + 1 for i, a in enumerate(SURELER)}
SURE_NO.update({norm(k): v for k, v in (
    ("الدهر", 76), ("عم", 78), ("المؤمن", 40), ("حم السجدة", 41), ("بني إسرائيل", 17),
    ("الانشراح", 94), ("اللهب", 111), ("تبت", 111), ("براءة", 9), ("المعارج", 70))})

# ---------------------------------------------------------------------------
# İşaret etiketleri. Sıra önemlidir: bir birim birden çok etiket alabilir.
# ---------------------------------------------------------------------------
ETIKET = collections.OrderedDict([
    ("KUR", ("Kur'an atfı (ayet alıntısı veya 'kâle teâlâ')",
             r"\{[^}]+\}|\[[^\]\[]{2,30}?[/:]\s*\d+|قال\s+(الله\s+)?تعالى|قوله\s+تعالى|"
             r"قال\s+الله|جل\s+ثناؤه|عز\s+وجل|قال\s+عز")),
    ("HADİS", ("Peygamber'e açıkça nisbet edilen söz",
               r"رسول\s+الله|قال\s+النبي|عن\s+النبي|النبي\s+صلى|عليه\s+السلام|"
               r"عليه\s+الصلاة\s+والسلام|صلى\s+الله\s+عليه")),
    ("RİVAYET", ("sahibi yazılmamış rivayet: 'el-hadîs', 'el-haber', 'ruviye', 'câe fî'",
                 r"الحديث|في\s+حديث|الخبر|\bروي\b|\bوروي\b|\bيروى\b|\bويروى\b|جاء\s+في\s+ذكر")),
    ("ŞER", ("şer'î / ıstılâhî anlam (fıkıh, kelâm, 'şeriatın getirdiği')",
             r"الشرع|شرعا|الشريعة|الفقهاء|الفقه|المتكلم|المخصوصة|اصطلاح|في\s+عرف")),
    ("NAKİL", ("sahabe, tâbiûn, müfessir görüşü ya da adsız 'kîle'",
               r"ابن\s+عباس|\bمجاهد\b|\bقتادة\b|\bعكرمة\b|\bالضحاك\b|\bالسدي\b|\bالحسن\b|المفسر|أهل\s+التفسير|"
               r"رضي\s+الله\s+عنه|\bقيل\b|\bوقيل\b|قال\s+بعضهم|وقال\s+بعضهم|بعض\s+الناس|قول\s+من\s+قال|\bزعم")),
    ("ŞİİR", ("şiir tanığı (mısra ayıracı '...' ya da 'enşede')",
              r"\s\.\.\.(\s|$)|\*\*|أنشد|ينشد|قال\s+الشاعر|قال\s+الراجز|الأعشى|لبيد|امرؤ\s+القيس|"
              r"النابغة|زهير|جرير|الفرزدق|ذو\s+الرمة|الأخطل|حسان|طرفة|عنترة")),
    ("DİLCİ", ("dilci otoritesi (Halîl, Asmaî, Ferrâ…)",
               r"الخليل|الأصمعي|الفراء|ابن\s+دريد|أبو\s+عبيد|الكسائي|سيبويه|ابن\s+الأعرابي|"
               r"أبو\s+زيد|الشيباني|اللحياني|ثعلب|الزجاج|أبو\s+عمرو|ابن\s+السكيت|الليث")),
    ("KULLANIM", ("Arapların gündelik kullanımı ('yukâlu', 'kavlühüm')",
                  r"\bيقال\b|\bويقال\b|تقول\s+العرب|العرب\s+تقول|\bقولهم\b|ويقولون|يقولون|"
                  r"تقول:|وتقول")),
    ("ASL", ("kök anlamı beyanı ('asl', 'kıyâs')",
             r"\bأصل|أصلان|أصول|الأصل|أصله|كلمة\s+واحدة|القياس|قياس")),
])
ETIKET_RE = {k: re.compile(v[1]) for k, v in ETIKET.items()}
DIL_ICI = ("KULLANIM", "ŞİİR", "DİLCİ")


# ---------------------------------------------------------------------------
# Anlam birimi: bir anlam beyanı + o anlama getirilen tanık(lar). Cümle birimi yetmez: Râgıb bir
# cümlede üç anlam ve üç tanık birleştirir, o zaman hangi tanığın hangi anlama ait olduğu kaybolur.
# ---------------------------------------------------------------------------
_KORU = re.compile(r"«[^»]*»|\{[^}]*\}|\[[^\]]*\]|\([^)]{0,200}\)")
# Yeni anlam başlatan kalıplar: "والنفس:", "النفس:", "ويقال", "يقال", "والثاني"
_YENI = re.compile(
    r"(?<=[،؛:\]»)\x00])\s(?=(?:و|ف)?ال[ء-ي]{2,12}\s?:)"  # "، والنفس:" — yalnız
    # noktalamadan sonra: "وفي الحديث:", "قال الشاعر:", "عليه الصلاة والسلام:" bölünmez
    r"|\s(?=(?:و)?يقال\b)"                               # ويقال ...
    r"|\s(?=(?:و|ف)أما\b)"                               # فأما / وأما
    r"|(?<=[^.]\.)\s+|(?<=[؟!])\s+"                       # cümle sonu ('...' mısra ayıracıdır, sonu değil)
    r"|\s*\x01\s*")                                        # tam beyit satırının sonu

# Kendi başına anlam vermeyen, ÖNCEKİ anlama tanık getiren açılışlar
_TANIK_BASI = re.compile(
    r"^(\[|«|،|\{"
    r"|(?:و|ف)?قال\s*:"                                          # "قال:" + beyit
    r"|(?:و|ف)?قال\s+(?:رسول|النبي|الشاعر|الراجز|تعالى|الله|عز|عليه|صلى|"
    r"الأعشى|لبيد|امرؤ|النابغة|زهير|جرير|الفرزدق|ذو\s+الرمة|الأخطل|حسان|طرفة|عنترة)"
    r"|(?:و|ف)?قال\s+(?:في|آخر)\b|(?:و)?أنشد|(?:و)?ينشد"
    r"|(?:و|ف)?قوله\s+(?:تعالى|عليه|صلى)"
    r"|(?:و|ف)?(?:في|ومنه|منه)\s+(?:ال)?(?:حديث|خبر)"
    r"|ومنه\s+ما\s+روي|(?:و)?روي\b|(?:و)?يروى\b|وجاء\s+في)")


def anlam_birimleri(metin: str) -> list[str]:
    """Metni ANLAM BİRİMLERİNE böler. Tırnak, ayet ve köşeli parantez içindeki metin bölünmez;
    tanık getiren ifadeler ("ومنه ما روي", "قال تعالى", "قال الشاعر") kendinden önceki anlama
    bağlı kalır."""
    # İki yarısı tek satırda duran beyit (' ... ' satır ortasında) satır sonunda biter: oradan
    # böl. Satır SONU '...' ise ikinci yarı alt satırdadır: bölme.
    satirlar = metin.split("\n")
    t = ""
    for i, sat in enumerate(satirlar):
        t += sat
        if i + 1 < len(satirlar):
            tam_beyit = " ... " in sat and not sat.rstrip().endswith("...")
            t += " \x01 " if tam_beyit else " "
    korunan: list[str] = []

    def sakla(m: re.Match) -> str:
        korunan.append(m.group(0))
        return "\x00%d\x00" % (len(korunan) - 1)

    t = _KORU.sub(sakla, t)
    parca = [x.strip() for x in _YENI.split(t) if x and x.strip()]
    geri = lambda x: re.sub(r"\x00(\d+)\x00", lambda m: korunan[int(m.group(1))], x)
    out: list[str] = []
    for x in parca:
        x = geri(x)
        # yalnız tanık/atıf parçası ("[البقرة/ 43] ،", "قال:") öncekine aittir
        tanik_basi = _TANIK_BASI.match(TASH.sub("", x))
        harf_sayisi = len(re.sub("[^ء-ي]", "", x))
        siir_devami = bool(out) and (out[-1].rstrip().endswith("...")   # mısranın ikinci yarısı
                                     or (" ... " in x and ":" not in x.split(" ... ")[0]))  # yalnız beyit
        if out and (harf_sayisi < 8 or tanik_basi or siir_devami):
            out[-1] += " " + x
        else:
            out.append(x)
    return out


def birim_etiketle(birim: str, eser: str) -> list[str]:
    t = TASH.sub("", birim)
    et = [k for k, r in ETIKET_RE.items() if r.search(t)]
    # İbn Fâris hadisi «...» içinde verir; Râgıb'da «2» dipnot numarasıdır.
    if eser == "ibnfaris" and re.search(r"«[^»\d]{6,}»", t) \
            and not ({"HADİS", "RİVAYET"} & set(et)):
        et.append("RİVAYET")
    return et


def statu(et: list[str]) -> str:
    """Anlam biriminin dayanağına göre statüsü."""
    e = set(et)
    if "ŞER" in e:
        return "şer'î / ıstılâhî"
    dil = bool(e & set(DIL_ICI))
    riv = bool(e & {"HADİS", "RİVAYET"})
    if dil and riv:
        return "dil-içi tanıklı (+ rivayet)"
    if dil:
        return "dil-içi tanıklı"
    if riv:
        return "YALNIZ rivayetle tanıklı"
    if "NAKİL" in e:
        return "yalnız yorumcu nakli"
    if "KUR" in e:
        return "sözlükçünün ayet okuması"
    return "tanıksız: sözlükçünün açıklaması"


# ---------------------------------------------------------------------------
# Kurulum ve yükleme
# ---------------------------------------------------------------------------

def kur() -> dict:
    if KLASIK_YOLU.exists():
        raise FileExistsError(f"Klasik sözlükler zaten kurulu: {KLASIK_YOLU}")
    maddeler: list[dict] = []
    kaynaklar: dict[str, dict] = {}
    with tempfile.TemporaryDirectory() as tmp:
        for eser, e in ESERLER.items():
            url = OPENITI % (e["depo"], e["commit"], e["yol"])
            ham = indir(url, e["sha256"])
            dosya = Path(tmp) / f"{eser}.txt"
            dosya.write_bytes(ham)
            parcalar = ayristir(dosya, eser)
            if len(parcalar) != BEKLENEN_MADDE[eser]:
                raise veri.VeriHatasi(f"{ESER_AD[eser]}: {len(parcalar)} madde ayrıştırıldı, "
                                      f"beklenen {BEKLENEN_MADDE[eser]}")
            for m in parcalar:
                m["eser"] = eser
                m["anahtar"] = sorted(anahtarlar(m["baslik"], eser))
                maddeler.append(m)
            kaynaklar[eser] = dict(url=url, depo=e["depo"], commit=e["commit"], sha256=e["sha256"],
                                   madde=len(parcalar))
    icerik = json.dumps(dict(kaynaklar=kaynaklar, maddeler=maddeler), ensure_ascii=False).encode("utf-8")
    KLASIK_DIZINI.mkdir(parents=True, exist_ok=True)
    KLASIK_YOLU.write_bytes(icerik)
    bilgi = {"kaynak": "OpenITI (Zenodo 10007820)", "klasik_sha256": hashlib.sha256(icerik).hexdigest(),
             "bytes": len(icerik), "madde": {e: kaynaklar[e]["madde"] for e in ESERLER},
             "eserler": kaynaklar,
             "lisans": "OpenITI metni CC BY-NC-SA 4.0 — depo herkese açık olduğu için depoya işlenmez",
             "statu": "hipotez kaynağı, delil değil"}
    manifest_yaz(KLASIK_MANIFEST, bilgi)
    return bilgi


class Klasik:
    def __init__(self, d: dict, sha: str):
        self.kaynak = d["kaynaklar"]
        self.maddeler = d["maddeler"]
        self.sha = sha
        self.idx: dict[str, dict[str, list[dict]]] = {e: {} for e in ESER_AD}
        for m in self.maddeler:
            for a in m["anahtar"]:
                self.idx[m["eser"]].setdefault(a, []).append(m)

    @property
    def veri_izi(self) -> str:
        return self.sha[:12]

    def coz(self, kok_ar: str, eser: str) -> list[tuple[str, list[dict]]]:
        return [(kural, self.idx[eser][a]) for kural, a in eslestir(self.idx[eser], kok_ar)]


@lru_cache(maxsize=1)
def yukle() -> Klasik | None:
    """Kuruluysa Klasik; değilse None. Dosya manifestteki sha256 ile uyuşmazsa VeriHatasi."""
    if not KLASIK_YOLU.exists():
        return None
    if not KLASIK_MANIFEST.exists():
        raise veri.VeriHatasi(f"{KLASIK_MANIFEST} yok; yeniden kurun (python -m tezgah kur klasik)")
    ham = KLASIK_YOLU.read_bytes()
    sha = hashlib.sha256(ham).hexdigest()
    beklenen = json.loads(KLASIK_MANIFEST.read_text(encoding="utf-8"))["klasik_sha256"]
    if sha != beklenen:
        raise veri.VeriHatasi("klasik.json sha256 manifestle uyuşmuyor; yeniden kurun")
    return Klasik(json.loads(ham.decode("utf-8")), sha)


def _kurulu() -> Klasik:
    from ..tara import GirdiHatasi
    k = yukle()
    if k is None:
        raise GirdiHatasi("Klasik sözlükler kurulu değil (python -m tezgah kur klasik).")
    return k


# ---------------------------------------------------------------------------
# Gösterim yardımcıları
# ---------------------------------------------------------------------------

def baslik_latin(baslik: str) -> str:
    """Madde başlığı -> ayrık Latin (harf.py tablosu). Yalın elif ilk harfse hemzedir (ʾ), sonrasında
    illetli harf / uzun ünlüdür (â): "صلا" ṣ-l-â, "أمن" ʾ-m-n. Başlıktaki elif'i hemze yazmak, illetli
    kökü hemzeli köke benzetirdi."""
    s = TASH.sub("", baslik)
    return "-".join(("ʾ" if i == 0 else "â") if c == "ا" else HARF_LATIN.get(c, c) for i, c in enumerate(s))


def _kirp(s: str, n: int) -> str:
    s = s.replace("\n", " ")
    return s if len(s) <= n else s[:n - 1].rstrip() + "…"


def _eserler(eser: str | None) -> list[str]:
    return [eser] if eser else list(ESER_AD)


def _baslik(m: dict, kural: str) -> str:
    uyar = "   << DOĞRULA" if kural.startswith("ZAYIF") else ""
    kayma = f"  [başlık {m['kayma']} paragraf kaymıştı]" if m.get("kayma") else ""
    return (f"{ESER_AD[m['eser']]} · madde {baslik_latin(m['baslik'])} · c./s. {m['sayfa'] or '?'} · "
            f"eşleşme: {kural}{uyar}{kayma}")


def _sonuc(kor: veri.Korpus | None, k: Klasik, satirlar: list[str], birimler: list[str], veri_: dict):
    from ..tara import Sonuc
    kaynak = f"QAC v0.4 | + {KAYNAK_ADI}" if kor is not None else KAYNAK_ADI
    iz = f"{kor.veri_izi} | {k.veri_izi}" if kor is not None else k.veri_izi
    return Sonuc(hipotez_etiketle(satirlar, KAYNAK_ADI), birimler, veri_, kaynak=kaynak, veri_izi=iz)


def _cozumle(kor: veri.Korpus, girdiler: list[str]):
    """Girdiyi QAC envanterine karşı çözer (Latin okunuş reddedilir) -> [(KokCozum, Arapça kök)]."""
    from ..tara import kok_coz
    return [(c, veri.bw_arapca(c.bw)) for c in (kok_coz(kor, g) for g in girdiler)]


ZINCIR = ("Zincir: sözlük hipotez üretir, korpus sınar (CLAUDE.md §2.1). Birim cümle değil ANLAMDIR; "
          "statü birimin TANIĞINA göredir, doğruluğuna değil.")


# ---------------------------------------------------------------------------
# Komutlar
# ---------------------------------------------------------------------------

def kok_komutu(kor: veri.Korpus, girdiler: list[str], eser: str | None = None, tam: bool = False):
    k = _kurulu()
    satirlar = [ZINCIR]
    n_madde = n_birim = 0
    for c, ar in _cozumle(kor, girdiler):
        satirlar += ["", f"KÖK: {c.bw} ({c.latin})", *c.uyarilar]
        for e in _eserler(eser):
            cozum = k.coz(ar, e)
            if not cozum:
                satirlar.append(f"{ESER_AD[e]}: madde yok. Bu 'anlam yok' DEĞİLDİR "
                                f"(CLAUDE.md §2.4; kapsam için: klasik kapsam).")
                continue
            for kural, mad in cozum:
                for m in mad:
                    n_madde += 1
                    satirlar += ["", _baslik(m, kural)]
                    for b in anlam_birimleri(m["metin"]):
                        n_birim += 1
                        et = birim_etiketle(b, e)
                        isaret = " ".join(f"[{x}]" for x in et) or "[—]"
                        satirlar.append(f"  {isaret:<24} {b if tam else _kirp(b, 150)}")
    satirlar += ["", "Hangi anlamın neye dayandığı için: klasik isaret <kök>. Anlamı korpusa döndürmeden yazma."]
    return _sonuc(kor, k, satirlar, ["madde", "anlam birimi"], {"madde": n_madde, "anlam_birimi": n_birim})


def _asl_birimleri(m: dict) -> list[str]:
    cs = anlam_birimleri(m["metin"])
    if m["eser"] == "ibnfaris":
        return cs[:1] + [c for c in cs[1:3] if ETIKET_RE["ASL"].search(TASH.sub("", c))]
    return [c for c in cs if re.search(r"^أصل|\bأصل\s|أصله|في\s+الأصل", TASH.sub("", c))][:3] or cs[:1]


def asl_komutu(kor: veri.Korpus, girdiler: list[str], eser: str | None = None):
    k = _kurulu()
    satirlar = [ZINCIR]
    n_madde = n_birim = 0
    for c, ar in _cozumle(kor, girdiler):
        satirlar += ["", f"KÖK: {c.bw} ({c.latin})", *c.uyarilar]
        for e in _eserler(eser):
            cozum = k.coz(ar, e)
            if not cozum:
                satirlar.append(f"  {ESER_AD[e]}: madde yok.")
                continue
            for kural, mad in cozum:
                for m in mad:
                    n_madde += 1
                    satirlar.append("  " + _baslik(m, kural))
                    for b in _asl_birimleri(m):
                        n_birim += 1
                        satirlar.append("     › " + _kirp(b, 260))
    return _sonuc(kor, k, satirlar, ["madde", "anlam birimi"], {"madde": n_madde, "anlam_birimi": n_birim})


def isaret_komutu(kor: veri.Korpus, girdiler: list[str], eser: str | None = None, tam: bool = False):
    k = _kurulu()
    satirlar = [ZINCIR]
    n_madde = n_birim = 0
    statuler: collections.Counter = collections.Counter()
    for c, ar in _cozumle(kor, girdiler):
        satirlar += ["", f"ANLAM → DAYANAK: {c.bw} ({c.latin})", *c.uyarilar]
        for e in _eserler(eser):
            for kural, mad in k.coz(ar, e):
                for m in mad:
                    n_madde += 1
                    bs = [(b, birim_etiketle(b, e)) for b in anlam_birimleri(m["metin"])]
                    say = collections.Counter(statu(et) for _, et in bs)
                    statuler.update(say)
                    n_birim += len(bs)
                    satirlar += ["", _baslik(m, kural),
                                 f"  {len(bs)} anlam birimi · " + " · ".join(f"{s} {v}" for s, v in say.most_common())]
                    for i, (b, et) in enumerate(bs, 1):
                        satirlar += ["", f"  {i:>2}. {statu(et)}   " + " ".join(f"[{x}]" for x in et),
                                     "      " + (b if tam else _kirp(b, 230))]
    satirlar += ["",
                 "Statü birimin TANIĞINA göredir, doğruluğuna değil. 'YALNIZ rivayetle tanıklı' ve 'şer'î' "
                 "birimler dil anlamı diye aktarılmaz (analiz_protokolu.md Aşama 7a).",
                 "Etiket biçimseldir: bir birimin içinde iki anlam kalmışsa elle ayır."]
    return _sonuc(kor, k, satirlar, ["madde", "anlam birimi"],
                  {"madde": n_madde, "anlam_birimi": n_birim, "statu": dict(statuler)})


def _ayet_atiflari(m: dict):
    t = TASH.sub("", m["metin"])
    desen = r"\[([^\]\[]{2,30}?)[/:]\s*(\d+)(?:\s*-\s*(\d+))?\s*\]"
    for ad, b, s in re.findall(desen, t):
        ad = re.sub(r"^سورة\s+", "", ad.replace("\n", " ").strip())
        yield ad, SURE_NO.get(norm(ad)), int(b), int(s) if s else int(b)


def _kok_ayetleri(kor: veri.Korpus, bw: str) -> set[str]:
    return {f"{w.sure}:{w.ayet}" for w in kor.kok_kelimeleri.get(bw, [])}


def ayet_komutu(kor: veri.Korpus, girdiler: list[str], eser: str | None = None):
    k = _kurulu()
    satirlar = [ZINCIR]
    n_atif = 0
    ayetler: set[str] = set()
    for c, ar in _cozumle(kor, girdiler):
        satirlar += ["", f"AYET ATIFLARI: {c.bw} ({c.latin})", *c.uyarilar]
        for e in _eserler(eser):
            for kural, mad in k.coz(ar, e):
                for m in mad:
                    satirlar += ["", _baslik(m, kural)]
                    # bu maddeye düşen BÜTÜN QAC kökleri (ör. ṣ-l-v ve ṣ-l-y aynı maddede)
                    kardes = [c.bw] + sorted(
                        r for r in kor.kok_kelimeleri if r != c.bw and any(
                            x[1] in m["anahtar"] for x in eslestir(k.idx[e], veri.bw_arapca(r))))
                    atif = list(_ayet_atiflari(m))
                    if not atif:
                        satirlar.append("  ayet numaralı atıf yok (İbn Fâris çoğu yerde numara vermez)")
                        continue
                    if len(kardes) > 1:
                        satirlar.append("  bu madde birden çok QAC kökünü kapsar: "
                                        + ", ".join(f"{r} ({veri.kok_latin(r)})" for r in kardes))
                    icinde: set[str] = set()
                    gor: set[str] = set()
                    for ad, no, b, s_ in atif:
                        if not no:
                            satirlar.append(f"  ?  sûre adı çözülemedi: {ad} / {b}")
                            continue
                        refs = [f"{no}:{x}" for x in range(b, s_ + 1)]
                        etiket = refs[0] if len(refs) == 1 else f"{refs[0]}-{s_}"
                        if etiket in gor:
                            continue
                        gor.add(etiket)
                        n_atif += 1
                        ayetler.update(refs)
                        var = [r for r in kardes if _kok_ayetleri(kor, r) & set(refs)]
                        if c.bw in var:
                            icinde.update(_kok_ayetleri(kor, c.bw) & set(refs))
                        durum = ("kök VAR: " + ", ".join(var)) if var else "maddenin hiçbir kökü YOK — elle bak"
                        satirlar.append(f"  {etiket:<11} {durum}")
                    tum = _kok_ayetleri(kor, c.bw)
                    satirlar.append(f"  → madde, {c.latin} kökünün QAC'taki {len(tum)} ayetinden {len(icinde)} "
                                    f"tanesini anıyor (%{100.0 * len(icinde) / max(1, len(tum)):.0f}). "
                                    f"Kalanı maddede anılmayan kullanımlardır (birim: ayet).")
    satirlar += ["", "'YOK' satırı ya yanlış atıftır ya da baskı hatası; elle bak (korpus sınavı)."]
    return _sonuc(kor, k, satirlar, ["atıf geçişi", "ayet"], {"atif": n_atif, "ayet": len(ayetler)})


def ara_komutu(ifade: str, eser: str | None = None, limit: int = 30):
    """--limit 0 = tümü (paketin ortak kuralı)."""
    from ..tara import GirdiHatasi
    if not any("؀" <= ch <= "ۿ" for ch in ifade):
        raise GirdiHatasi("Arama ifadesi Arapça olmalı (harekesiz, hemze-normal eşleşir).")
    k = _kurulu()
    n = norm(ifade)
    satirlar = [ZINCIR]
    say = 0
    for m in k.maddeler:
        if eser and m["eser"] != eser:
            continue
        for b in anlam_birimleri(m["metin"]):
            if n in norm(b):
                say += 1
                if not limit or say <= limit:
                    satirlar.append(f"[{ESER_AD[m['eser']]} · madde {baslik_latin(m['baslik'])}] {_kirp(b, 220)}")
    satirlar += ["", f"{say} anlam birimi bulundu" + ("" if not limit or say <= limit else f" (ilk {limit} gösterildi; --limit 0 = tümü)")
                 + ". Bulunmaması yokluk delili değildir."]
    return _sonuc(None, k, satirlar, ["anlam birimi"], {"bulunan": say})


def kapsam(kor: veri.Korpus, k: Klasik) -> dict:
    """QAC kökleri sözlük maddeleriyle ne kadar karşılanır (ölçüm)."""
    sonuc = {}
    for e in ESER_AD:
        kesin, zayif, yok = [], [], []
        for r in sorted(kor.kok_kelimeleri):
            s = eslestir(k.idx[e], veri.bw_arapca(r))
            if not s:
                yok.append(r)
            elif s[0][0].startswith("ZAYIF"):
                zayif.append((r, s[0][1]))
            else:
                kesin.append(r)
        sonuc[e] = {"madde": sum(1 for m in k.maddeler if m["eser"] == e), "kesin": len(kesin),
                    "zayif": zayif, "yok": yok,
                    "yok_kelime_konumu": sum(len(kor.kok_kelimeleri[r]) for r in yok)}
    return sonuc


def kapsam_komutu(kor: veri.Korpus, liste: bool = False):
    from ..tara import _tablo
    k = _kurulu()
    o = kapsam(kor, k)
    toplam = len(kor.kok_kelimeleri)
    satirlar = [f"Klasik sözlük kapsamı — QAC v0.4'ün {toplam} kökü (birim: kök; ölçüm bu çalıştırmada yapıldı). "
                "Sayılar beceri envanterinin (1.651 kök) sayılarıyla toplanmaz.",
                *_tablo(["eser", "madde", "kesin", "zayıf", "yok", "yok olanların kelime konumu"],
                        [[ESER_AD[e], v["madde"], v["kesin"], len(v["zayif"]), len(v["yok"]),
                          v["yok_kelime_konumu"]] for e, v in o.items()], sag={1, 2, 3, 4, 5}),
                "kesin = birebir/mudâaf/illetli yazım; zayıf = elle doğrulanmalı (<< DOĞRULA); "
                "yok = bu sorguyla bulunmadı (anlam yok demek değildir)."]
    if liste:
        for e, v in o.items():
            satirlar += ["", f"{ESER_AD[e]} — yok: " + (", ".join(
                f"{r} ({veri.kok_latin(r)})" for r in sorted(v["yok"], key=lambda r: -len(kor.kok_kelimeleri[r]))) or "—"),
                f"{ESER_AD[e]} — zayıf: " + (", ".join(
                    f"{r} ({veri.kok_latin(r)}) → {kural}" for r, kural in v["zayif"]) or "—")]
    return _sonuc(kor, k, satirlar, ["madde", "kök", "kelime konumu"], o)


def etiketler_komutu():
    from ..tara import Sonuc
    satirlar = ["İşaret etiketleri (klasik kok / isaret çıktısında):", ""]
    satirlar += [f"  [{ad:<8}] {acik}" for ad, (acik, _) in ETIKET.items()]
    satirlar += ["  [—]        hiçbir işaret yok: sözlükçünün tanıksız beyanı", "",
                 "Statüler (isaret komutu): dil-içi tanıklı · dil-içi tanıklı (+ rivayet) · YALNIZ rivayetle "
                 "tanıklı · şer'î / ıstılâhî · yalnız yorumcu nakli · sözlükçünün ayet okuması · tanıksız. "
                 "Birim cümle değil ANLAMDIR.", "",
                 "İşaretler biçimsel ipucudur, kaynağın kendisi değildir. Bir birim birden çok etiket alabilir. "
                 "Örtük etki (tanık gösterilmeden tefsirden alınmış anlam) işaretle yakalanamaz; "
                 "analiz_protokolu.md Aşama 7a'daki üç sınav onun içindir."]
    return Sonuc(hipotez_etiketle(satirlar, KAYNAK_ADI), [], {}, kaynak=KAYNAK_ADI, veri_izi="—")
