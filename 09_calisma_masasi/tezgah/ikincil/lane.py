"""Lane, An Arabic-English Lexicon (LexiconDatabase v1.0.9) — hipotez kaynağı, delil değil.

Kurallar (kök analizi becerisi §10; sayılar QAC v0.4'ün 1.642 köküne göre yeniden ölçülür):
- Lane birincil kaynak değildir: Kur'an ← klasik sözlükler ← Lane. Anlam çoğu zaman hadis, şiir
  ya da tefsir kaynaklıdır.
- Dairesellik: Lane bir Kur'an kelimesini çoğu zaman yerleşik Kur'anî anlamıyla açıklar; "Lane de
  böyle diyor" bağımsız doğrulama değildir. Kur'an atfı taşıyan madde ayrıca işaretlenir.
- ك sonrası seyrelme: Lane'in ك-ي bölgesi ölümünden sonra derlendi ve seyrektir; bu bölgede
  "Lane'de yok" argümanı üretilmez. Yoğunluk `lane kapsam` ile ölçülür.
- Tefsir, hadis ("trad." ve hadis kısaltmaları) ve şiir satırları işaretlenir; kısaltma kategorileri ve
  dayanakları: 09_calisma_masasi/lane_kisaltmalari.tsv (`lane sigla` ölçer).
- Zayıf kuralla eşleşen kök "<< DOĞRULA" ile işaretlenir ve elle denetlenir.

Veri: yerel/lane/lexicon.sqlite (depoya işlenmez; 265 MB). Kurulum: python -m tezgah kur lane
"""

from __future__ import annotations

import io
import re
import sqlite3
import zipfile
from collections import Counter
from functools import lru_cache
from pathlib import Path

from .. import veri
from . import arapca_latin_metin, etiketle, indir, manifest_yaz

MASA = Path(__file__).resolve().parents[2]
LANE_DIZINI = MASA / "yerel" / "lane"
LANE_YOLU = LANE_DIZINI / "lexicon.sqlite"
LANE_MANIFEST = LANE_DIZINI / "manifest.json"
LANE_DEPO = "laneslexicon/LexiconDatabase"
LANE_COMMIT = "b371ab16b963def3085674a516e5f45d9c787b1d"   # etiket v1.0.9
ZIP_URL = f"https://raw.githubusercontent.com/{LANE_DEPO}/{LANE_COMMIT}/lexicon.sqlite.zip"
ZIP_SHA256 = "eff9e0528572a1d2d4bc7097da78d938d6db444b0e99e8f1ef4f010c8ab15463"
SQLITE_SHA256 = "a16651d5381bbeccf5e26a58a3be77f36e5225374404117835abef90b791ef49"
KAYNAK_ADI = "Lane"

# Arap alfabesi sırası; ك ve sonrası Lane-Poole'un derlediği seyrek bölge.
ALFABE = "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"
SEYREK_BOLGE = set("كلمنهوي")
HEMZE = set("ءأإآؤئٱا")

# Lane kaynak kısaltmaları: kategori ve dayanak ayrı tablo dosyasındadır (lane_kisaltmalari.tsv).
KISALTMA_YOLU = MASA / "lane_kisaltmalari.tsv"
KISALTMA_SUTUNLARI = ["kisaltma", "kategori", "kaynak", "kimlik_dayanagi", "veri_deseni", "kategori_dayanagi"]
KATEGORILER = {"sözlük", "tefsir", "hadis", "dil bilgisi"}
YAKINLIK = 300     # atfın iki yanında bakılan karakter sayısı (olcum:kur / olcum:trad)
KAT_ESIGI = 3.0    # ölçülen oran, sözlük kategorisi ortancasının en az bu katı olmalı


@lru_cache(maxsize=1)
def kisaltmalar() -> dict[str, dict[str, str]]:
    """lane_kisaltmalari.tsv → {kısaltma: satır}. '#' ile başlayan satırlar açıklamadır."""
    satirlar = [s for s in KISALTMA_YOLU.read_text(encoding="utf-8").splitlines() if s.strip() and not s.startswith("#")]
    baslik = satirlar[0].split("\t")
    if baslik != KISALTMA_SUTUNLARI:
        raise veri.VeriHatasi(f"{KISALTMA_YOLU.name}: sütunlar {KISALTMA_SUTUNLARI} olmalı, bulunan {baslik}")
    tablo = {}
    for s in satirlar[1:]:
        r = dict(zip(baslik, s.split("\t")))
        if len(r) != len(baslik) or r["kategori"] not in KATEGORILER or r["kisaltma"] in tablo:
            raise veri.VeriHatasi(f"{KISALTMA_YOLU.name}: geçersiz satır: {s!r}")
        if r["kategori_dayanagi"] not in {"elle", "olcum:kur", "olcum:trad"}:
            raise veri.VeriHatasi(f"{KISALTMA_YOLU.name}: bilinmeyen kategori dayanağı: {r['kategori_dayanagi']}")
        tablo[r["kisaltma"]] = r
    return tablo


def _kategori_re(kategori: str) -> str:
    return "|".join(re.escape(k) for k, r in kisaltmalar().items() if r["kategori"] == kategori)


TEFSIR_RE = re.compile(rf"\b({_kategori_re('tefsir')})\b")
HADIS_RE = re.compile(rf"\btrads?\.|\b(?:{_kategori_re('hadis')})\b")
SIIR_RE = re.compile(r"\b(verse|poet|hemistich|rejez|rajaz)\b", re.I)
KURAN_RE = re.compile(r"\bKur\b")


def notr(kok: str) -> str:
    """Hemze ve ى nötrlenir, harekeler silinir (kök tablosunda harekeli yazılmış kökler var: جَهِلَ)."""
    import unicodedata
    return "".join("ء" if c in HEMZE else ("ي" if c == "ى" else c)
                   for c in kok if not unicodedata.combining(c) and c != "\u0640")


def kur() -> dict:
    if LANE_YOLU.exists():
        raise FileExistsError(f"Lane zaten kurulu: {LANE_YOLU}")
    ham = indir(ZIP_URL, ZIP_SHA256)
    with zipfile.ZipFile(io.BytesIO(ham)) as z:
        veri_ = z.read("lexicon.sqlite")
    import hashlib
    if hashlib.sha256(veri_).hexdigest() != SQLITE_SHA256:
        raise veri.VeriHatasi("lexicon.sqlite sha256 beklenenden farklı")
    LANE_DIZINI.mkdir(parents=True, exist_ok=True)
    LANE_YOLU.write_bytes(veri_)
    bilgi = {"depo": LANE_DEPO, "commit": LANE_COMMIT, "etiket": "v1.0.9", "source_url": ZIP_URL,
             "zip_sha256": ZIP_SHA256, "sqlite_sha256": SQLITE_SHA256, "bytes": len(veri_),
             "lisans": "veritabanı GPLv3; Lane metni (1863-93) kamu malı — boyut nedeniyle depoya işlenmez",
             "statu": "hipotez kaynağı, delil değil"}
    manifest_yaz(LANE_MANIFEST, bilgi)
    return bilgi


@lru_cache(maxsize=1)
def baglanti() -> sqlite3.Connection | None:
    if not LANE_YOLU.exists():
        return None
    if veri.sha256(LANE_YOLU) != SQLITE_SHA256:
        raise veri.VeriHatasi("Lane lexicon.sqlite sha256 uyuşmuyor")
    return sqlite3.connect(f"file:{LANE_YOLU}?mode=ro", uri=True, check_same_thread=False)


@lru_cache(maxsize=1)
def lane_kokleri() -> dict[str, list[tuple[str, int, int]]]:
    """nötr kök -> [(Lane kök yazımı, sayfa, ek cilt bayrağı)]"""
    c = baglanti()
    d: dict[str, list[tuple[str, int, int]]] = {}
    for word, page, supp in c.execute("select word, page, supplement from root"):
        d.setdefault(notr(word), []).append((word, page, supp))
    return d


@lru_cache(maxsize=1)
def baslik_kokleri() -> dict[str, set[str]]:
    """Harekesiz madde başlığı (nötr) -> altında durduğu Lane kök(ler)i.

    LexiconDatabase'in kök tablosunda bazı kökler yoktur; maddeleri komşu bir kökün altına
    kaydedilmiştir (ör. جَهِلَ maddeleri جهض altında). Bu dizin o durumu yakalar.
    """
    d: dict[str, set[str]] = {}
    for root, bare in baglanti().execute("select root, bareword from entry"):
        if bare:
            d.setdefault(notr(bare), set()).add(root)
    return d


def eslestir(kok_bw: str) -> tuple[str | None, str]:
    """QAC kökü -> (Lane nötr kökü, kural). Kurallar sırayla denenir; zayıf olanlar 'zayıf:' ile başlar."""
    lk = lane_kokleri()
    q = notr(veri.bw_arapca(kok_bw).replace("ا", "ء"))
    if q in lk:
        return q, "tam"
    if len(q) == 3 and q[1] == q[2] and q[:2] in lk:
        return q[:2], "ikiz: C1C2C2 -> C1C2 (Lane ikiz kökleri iki harfle yazar)"
    if len(q) == 4 and q[:2] == q[2:] and q[:2] in lk:
        return q[:2], "yineleme: C1C2C1C2 -> C1C2"
    degis = {"و": "ي", "ي": "و"}
    if q[-1] in degis and q[:-1] + degis[q[-1]] in lk:
        return q[:-1] + degis[q[-1]], "zayıf: son harf و↔ي"
    if len(q) == 3 and q[1] in degis and q[0] + degis[q[1]] + q[2] in lk:
        return q[0] + degis[q[1]] + q[2], "zayıf: orta harf و↔ي"
    if q.endswith("ء") and q[:-1] in lk:
        return q[:-1], "zayıf: son hemze düşürüldü"
    baslik = baslik_kokleri().get(q)
    if baslik:
        hedef = sorted(baslik)[0]
        return notr(hedef), f"zayıf: kök tablosunda yok, maddeleri {arapca_latin_kok(hedef)} kökü altında"
    return None, "eşleşme yok"


def arapca_latin_kok(kok_ar: str) -> str:
    from ..harf import HARF_LATIN
    return "-".join(HARF_LATIN["ء"] if c in HEMZE else HARF_LATIN.get(c, c) for c in kok_ar)


def bolge(kok_ar: str) -> str:
    return "ك-ي (seyrek)" if kok_ar[:1] in SEYREK_BOLGE else "ا-ق"


def _duz_metin(xml: str) -> str:
    """XML'i düz metne çevirir; Arapça parçalar Latin okunuşa (ya da bw:) çevrilir."""
    def arapca(m: re.Match) -> str:
        return " ".join(arapca_latin_metin(w) for w in m.group(1).split())
    metin = re.sub(r"<(?:foreign|orth)[^>]*lang=\"ar\"[^>]*>(.*?)</(?:foreign|orth)>", arapca, xml, flags=re.S)
    metin = re.sub(r"<[^>]+>", "", metin)
    metin = re.sub(r"[؀-ۿ]+", lambda m: arapca_latin_metin(m.group(0)), metin)
    metin = metin.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    return " ".join(metin.split())


def isaretler(metin: str) -> list[str]:
    e = []
    if TEFSIR_RE.search(metin):
        e.append("tefsir: " + ",".join(sorted(set(TEFSIR_RE.findall(metin)))))
    if HADIS_RE.search(metin):
        e.append("hadis")
    if SIIR_RE.search(metin):
        e.append("şiir")
    if KURAN_RE.search(metin):
        e.append("Kur'an atfı — dairesellik riski")
    return e


def kok_komutu(kor: veri.Korpus, girdi: str, tam: bool = False, madde: int | None = None):
    from ..tara import GirdiHatasi, Sonuc, kok_coz
    if baglanti() is None:
        raise GirdiHatasi("Lane kurulu değil (python -m tezgah kur lane).")
    c = kok_coz(kor, girdi)
    anahtar, kural = eslestir(c.bw)
    satirlar = [
        "Lane, An Arabic-English Lexicon (LexiconDatabase v1.0.9) — hipotez kaynağı, delil değil.",
        "Zincir: Kur'an ← klasik sözlükler ← Lane. Anlamlar çoğu zaman hadis, şiir ya da tefsir kaynaklıdır.",
        "Dairesellik: Lane'in Kur'an kelimesine verdiği anlam tefsirden gelebilir; 'Lane de böyle diyor' "
        "bağımsız doğrulama değildir. Hipotez korpusta sınanır, sonuç korpus bulgusuyla yazılır.",
        f"QAC kökü: {c.bw} ({c.latin}) · Lane eşleşmesi: {kural}",
    ]
    if anahtar is None:
        satirlar.append("Lane'de bu kökün maddesi bulunamadı — bu bir bulgu değildir"
                        + (" (ك-ي bölgesi seyrek: yokluk argümanı kurulamaz)." if bolge(veri.bw_arapca(c.bw)) != "ا-ق" else "."))
        return Sonuc(etiketle(satirlar), [], {"kural": kural, "madde": 0}, kaynak=f"QAC v0.4 | + {KAYNAK_ADI}",
                     veri_izi=f"{kor.veri_izi} | {SQLITE_SHA256[:12]}")
    if kural.startswith("zayıf"):
        satirlar.append("<< DOĞRULA: zayıf kuralla eşleşti; maddenin gerçekten bu köke ait olduğunu elle denetleyin.")
    kok_yazimlari = lane_kokleri().get(anahtar) or [(r, 0, 0) for r in sorted(baslik_kokleri().get(notr(veri.bw_arapca(c.bw)), []))]
    if bolge(kok_yazimlari[0][0]) != "ا-ق":
        satirlar.append("ك-ي bölgesi: Lane burada seyrektir (ölçüm: lane kapsam); eksik anlam yokluk delili değildir.")
    maddeler = []
    q = notr(veri.bw_arapca(c.bw))
    for kok_yazimi, _, _ in kok_yazimlari:
        for bas, sayfa, xml, ek, bare in baglanti().execute(
                "select word, page, xml, supplement, bareword from entry where root=? order by nodenum", (kok_yazimi,)):
            if "maddeleri" in kural and not notr(bare or "").startswith(q):
                continue   # komşu kökün kendi maddeleri
            maddeler.append((bas, sayfa, xml, ek))
    satirlar.append(f"Madde sayısı: {len(maddeler)} (Lane sayfaları: "
                    f"{', '.join(sorted({str(p) for _, p, _ in kok_yazimlari}))})")
    for i, (bas, sayfa, xml, ek) in enumerate(maddeler, 1):
        if madde is not None and i != madde:
            continue
        metin = _duz_metin(xml)
        isr = isaretler(metin)
        satirlar.append(f"Madde {i}/{len(maddeler)} — {arapca_latin_metin(bas)} (s. {sayfa}{', ek cilt' if ek else ''})"
                        + (f" [{'; '.join(isr)}]" if isr else ""))
        satirlar.append("  " + (metin if tam or madde else metin[:300] + ("…" if len(metin) > 300 else "")))
    satirlar.append("Sunum: İngilizce tanım burada özgün hâliyle kısaltılarak verilir; analizde Türkçeye çevrilir, "
                    "uzun birebir alıntı yapılmaz. Arapça parçalar Latin okunuşla (çözülemeyenler bw:) gösterilir.")
    return Sonuc(etiketle(satirlar), [], {"kural": kural, "madde": len(maddeler)},
                 kaynak=f"QAC v0.4 | + {KAYNAK_ADI}", veri_izi=f"{kor.veri_izi} | {SQLITE_SHA256[:12]}")


def kapsam(kor: veri.Korpus) -> dict:
    """QAC 1.642 kökünün Lane eşleşmesi ve bölge yoğunluğu (ölçüm)."""
    c = baglanti()
    kurallar = Counter()
    eslesmeyen, zayif = [], []
    for kok in sorted(kor.kok_kelimeleri):
        anahtar, kural = eslestir(kok)
        tur = "tam" if kural == "tam" else ("kural" if anahtar and not kural.startswith("zayıf") else
                                            ("zayıf" if anahtar else "yok"))
        kurallar[tur] += 1
        if tur == "yok":
            eslesmeyen.append(kok)
        elif tur == "zayıf":
            zayif.append((kok, kural))
    madde_sayisi = Counter()
    kok_sayisi = Counter()
    for word, in c.execute("select word from root"):
        kok_sayisi[bolge(word)] += 1
    for root, in c.execute("select root from entry"):
        madde_sayisi[bolge(root)] += 1
    yogunluk = {b: round(madde_sayisi[b] / kok_sayisi[b], 2) for b in kok_sayisi}
    return {
        "qac_kok": len(kor.kok_kelimeleri), "eslesme": dict(kurallar),
        "eslesmeyen": eslesmeyen, "zayif": zayif,
        "eslesmeyen_bolge": dict(Counter(bolge(veri.bw_arapca(k)) for k in eslesmeyen)),
        "lane_kok": sum(kok_sayisi.values()), "lane_madde": sum(madde_sayisi.values()),
        "bolge_kok": dict(kok_sayisi), "bolge_madde": dict(madde_sayisi), "bolge_yogunluk": yogunluk,
    }


def kapsam_komutu(kor: veri.Korpus):
    from ..tara import GirdiHatasi, Sonuc, _tablo
    if baglanti() is None:
        raise GirdiHatasi("Lane kurulu değil (python -m tezgah kur lane).")
    k = kapsam(kor)
    e = k["eslesme"]
    satirlar = [
        f"Lane kapsamı — QAC v0.4'ün {k['qac_kok']} kökü (birim: kök; ölçüm bu çalıştırmada yapıldı):",
        *_tablo(["eşleşme", "kök", "oran"], [[ad, e.get(ad, 0), f"%{100 * e.get(ad, 0) / k['qac_kok']:.1f}"]
                                             for ad in ("tam", "kural", "zayıf", "yok")], sag={1, 2}),
        "kural = ikiz/yineleme yazım farkı; zayıf = elle doğrulanmalı (<< DOĞRULA).",
        "Zayıf eşleşmeler: " + (", ".join(a + " (" + kr.split(": ", 1)[1] + ")" for a, kr in k["zayif"]) or "—"),
        f"Eşleşmeyen kökler: {', '.join(f'{x} ({veri.kok_latin(x)})' for x in k['eslesmeyen'])}",
        f"Eşleşmeyenlerin bölgesi: {k['eslesmeyen_bolge']}",
        "",
        f"Lane geneli: {k['lane_kok']} kök, {k['lane_madde']} madde. Bölge yoğunluğu (madde / kök):",
        *_tablo(["bölge", "kök", "madde", "madde/kök"],
                [[b, k["bolge_kok"][b], k["bolge_madde"][b], k["bolge_yogunluk"][b]] for b in sorted(k["bolge_kok"])],
                sag={1, 2, 3}),
        "ك-ي bölgesinde 'Lane'de yok' argümanı kurulamaz.",
    ]
    return Sonuc(etiketle(satirlar), ["kök"], k, kaynak=f"QAC v0.4 | + {KAYNAK_ADI}",
                 veri_izi=f"{kor.veri_izi} | {SQLITE_SHA256[:12]}")


ATIF_GRUBU = re.compile(r"\(([A-Z][A-Za-z]{0,6}(?:,?\s*\*?\s*[A-Z][A-Za-z]{0,6}\.?)*),?\s*\*?\)")
KUR_YAKIN = re.compile(r"\bKur\b")
TRAD_YAKIN = re.compile(r"\btrads?\.")


@lru_cache(maxsize=1)
def sigla_olcumu() -> dict:
    """Parantez içi atıf kısaltmalarını sayar; her geçişin ±YAKINLIK karakterinde Kur / trad. oranını ölçer."""
    c = baglanti()
    say, kur, trad, desen = Counter(), Counter(), Counter(), Counter()
    tablo = kisaltmalar()
    desenler = {k: re.compile(r["veri_deseni"]) for k, r in tablo.items() if r["veri_deseni"] != "-"}
    for xml, in c.execute("select xml from entry"):
        m = re.sub(r"<[^>]+>", "", xml)
        for k, d in desenler.items():
            if d.search(m):
                desen[k] += 1
        for g in ATIF_GRUBU.finditer(m):
            pencere = m[max(0, g.start() - YAKINLIK):g.end() + YAKINLIK]
            k_var, t_var = bool(KUR_YAKIN.search(pencere)), bool(TRAD_YAKIN.search(pencere))
            for x in re.split(r"[,\s*]+", g.group(1)):
                x = x.strip(". ")
                if x:
                    say[x] += 1
                    kur[x] += k_var
                    trad[x] += t_var
    oran = lambda sayac, k: sayac[k] / say[k] if say[k] else 0.0

    def ortanca(xs):
        xs = sorted(xs)
        return (xs[(len(xs) - 1) // 2] + xs[len(xs) // 2]) / 2 if xs else 0.0
    sozluk = [k for k, r in tablo.items() if r["kategori"] == "sözlük"]
    taban = {"kur": ortanca([oran(kur, k) for k in sozluk]), "trad": ortanca([oran(trad, k) for k in sozluk])}
    satir = {}
    for k, r in tablo.items():
        o = {"gecis": say[k], "kur": oran(kur, k), "trad": oran(trad, k),
             "veri_deseni_madde": desen[k] if k in desenler else None}
        if r["kategori_dayanagi"].startswith("olcum:"):
            tur = r["kategori_dayanagi"].split(":")[1]
            o["olcum_tutuyor"] = say[k] > 0 and taban[tur] > 0 and o[tur] >= KAT_ESIGI * taban[tur]
        satir[k] = o
    return {"satir": satir, "taban": taban, "diger": dict((k, n) for k, n in say.most_common() if k not in tablo)}


def sigla_komutu():
    """Kısaltma tablosunu (lane_kisaltmalari.tsv) veride ölçülen dayanakla birlikte gösterir."""
    from ..tara import GirdiHatasi, Sonuc, _tablo
    if baglanti() is None:
        raise GirdiHatasi("Lane kurulu değil (python -m tezgah kur lane).")
    o = sigla_olcumu()
    yz = lambda x: f"%{100 * x:.1f}".replace(".", ",")
    tablo = []
    for k, r in kisaltmalar().items():
        s = o["satir"][k]
        if r["kategori_dayanagi"] == "elle":
            kd = "elle"
        else:
            kd = f"{r['kategori_dayanagi']} — {'tutuyor' if s['olcum_tutuyor'] else 'TUTMUYOR'}"
        tablo.append([k, s["gecis"], r["kategori"], r["kaynak"], yz(s["kur"]), yz(s["trad"]), kd,
                      "—" if s["veri_deseni_madde"] is None else f"{r['veri_deseni']} → {s['veri_deseni_madde']} madde"])
    diger = list(o["diger"].items())[:15]
    satirlar = [
        f"Lane kaynak kısaltmaları — tablo: {KISALTMA_YOLU.name}; sayımlar ve oranlar bu çalıştırmada ölçüldü.",
        "Kimlik (kısaltma → eser): Lane önsözündeki liste; LexiconDatabase'de önsöz yok, eşleme bu depoda veriyle "
        "doğrulanmadı (elle atandı). Veri deseni yalnız dolaylı destektir.",
        f"Kategori ölçümü: atfın ±{YAKINLIK} karakterinde 'Kur' / 'trad.' geçme oranı (birim: atıf geçişi). Sözlük "
        f"ortancası: Kur {yz(o['taban']['kur'])}, trad {yz(o['taban']['trad'])}; eşik ortancanın {KAT_ESIGI:g} katı.",
        *_tablo(["kısaltma", "geçiş", "kategori", "kaynak", "Kur yakın", "trad yakın", "kategori dayanağı", "veri deseni"],
                tablo, sag={1, 4, 5}),
        "Tabloda olmayan en sık kısaltmalar (kategori atanmadı): " + ", ".join(f"{k} {n}" for k, n in diger),
        "tefsir ve hadis kategorisindeki atıflar delil değildir; aktarılırsa kaynağı açıkça yazılır.",
    ]
    veri_ = {"satir": o["satir"], "taban": o["taban"]}
    return Sonuc(etiketle(satirlar), ["atıf geçişi"], veri_, kaynak=KAYNAK_ADI,
                 veri_izi=f"{SQLITE_SHA256[:12]} | {veri.sha256(KISALTMA_YOLU)[:12]}")
