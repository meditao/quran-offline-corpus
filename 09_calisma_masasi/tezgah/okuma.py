"""Ayet görünümü (Aşama 2b): okunuş + kelime kelime QAC çözümlemesi + çalışma çevirisi + isteğe bağlı meal.

Katmanlar ve statüleri (CLAUDE.md §3):
    kelime çözümlemesi   QAC v0.4                  delil
    okunuş               Tanzil'den kurallı aktarım  aktarım, delil değil
    çalışma çevirisi     kullanıcı (kavramlar/)     kullanıcının yorumu
    meal                 yerel/ (varsayılan kapalı)  kurumsal okuma — sınanan, delil değil

Tanzil ↔ QAC kelime eşlemesi yalnız 03_indices/generated/tanzil_qac_alignment.csv üzerinden
yapılır: count_match (ofset 0) ve basmala_offset (besmele öneki okunuşta zaten ayrılır). Kalan
tokenization_difference ayetlerinde ardışık Tanzil tokenları, ünsüz iskeleti QAC kelimesiyle
birebir tutarsa birleştirilir; tutmazsa kelime "hizalanamadı" diye gösterilir.
"""

from __future__ import annotations

import csv
import json
import unicodedata
from dataclasses import dataclass
from datetime import date
from functools import lru_cache
from pathlib import Path
from urllib.request import Request, urlopen

from . import okunus, veri
from .veri import DEPO, Kelime, bw_arapca, kok_latin

MASA = Path(__file__).resolve().parents[1]
HIZALAMA_YOLU = DEPO / "03_indices" / "generated" / "tanzil_qac_alignment.csv"
CEVIRI_YOLU = MASA / "kavramlar" / "calisma_cevirisi.tsv"
MEAL_DIZINI = MASA / "yerel" / "meal"
MEAL_YOLU = MEAL_DIZINI / "tur-diyanetisleri.json"
MEAL_MANIFEST = MEAL_DIZINI / "manifest.json"
# fawazahmed0/quran-api deposunun kendisi (jsdelivr bu deponun önbelleğidir).
MEAL_URL = "https://raw.githubusercontent.com/fawazahmed0/quran-api/1/editions/tur-diyanetisleri.json"
MEAL_ETIKETI = "kurumsal okuma — sınanan, delil değil"
# Parmak izi: kurulan dosyanın gerçekten Diyanet İşleri meali olduğunu iki ayetin metniyle denetler
# (değerler 24.09.2026'da kurulan dosyadan okundu). Tutmazsa kurulum/yükleme reddedilir.
MEAL_PARMAK_IZI = {
    (1, 1): "Rahman ve Rahim olan Allah'ın adıyla",
    (107, 4): "Vay o namaz kılanların haline ki",
}
CEVIRI_ETIKETI = "kullanıcının yorumu"

_HEMZE = set("ءأإؤئٱآ")


def iskelet(arapca: str) -> str:
    """Ünsüz iskeleti: harekesiz; hemze/elif biçimleri, ى/ي ve ة/ت birleştirilir."""
    metin = arapca.replace("ـٔ", "ء")
    cikti = []
    for c in metin:
        if unicodedata.combining(c) or c == "ـ":
            continue
        if c in _HEMZE or c == "ا":
            c = "ا"
        elif c == "ى":
            c = "ي"
        elif c == "ة":
            c = "ت"
        if "ء" <= c <= "ي":
            cikti.append(c)
    return "".join(cikti)


def qac_iskeleti(kelime: Kelime) -> str:
    # QAC Buckwalter'ında tatvil üstü hemze "_#" / "#" ile yazılır.
    return iskelet(bw_arapca(kelime.bicim.replace("_#", "'").replace("#", "'")))


@dataclass
class Eslesme:
    kelime: Kelime
    tanzil: list[int]          # okunuş kelime sıraları (besmele öneki hariç, 0'dan)
    iskelet_ayni: bool
    not_: str = ""


@lru_cache(maxsize=1)
def hizalama_tablosu() -> dict[tuple[int, int], dict[str, str]]:
    with HIZALAMA_YOLU.open(encoding="utf-8", newline="") as f:
        return {(int(r["surah"]), int(r["ayah"])): r for r in csv.DictReader(f)}


def hizala(sure: int, ayet: int, o: okunus.AyetOkunus) -> tuple[list[Eslesme], str]:
    qac = _ayet_kelimeleri(sure, ayet)
    durum = hizalama_tablosu()[(sure, ayet)]["status"]
    tz = [iskelet(k.arapca) for k in o.kelimeler]
    sonuc: list[Eslesme] = []
    if durum in {"count_match", "basmala_offset"}:
        if len(qac) != len(tz):
            raise veri.VeriHatasi(f"{sure}:{ayet} hizalama tablosu {durum} diyor ama sayılar farklı")
        for i, k in enumerate(qac):
            ayni = qac_iskeleti(k) == tz[i]
            sonuc.append(Eslesme(k, [i], ayni, "" if ayni else "yazım farkı (Tanzil v1.1 ↔ QAC)"))
        return sonuc, durum
    j = 0
    for k in qac:
        hedef = qac_iskeleti(k)
        if j < len(tz) and tz[j] == hedef:
            sonuc.append(Eslesme(k, [j], True))
            j += 1
            continue
        birlesik = next((n for n in (2, 3) if j + n <= len(tz) and "".join(tz[j:j + n]) == hedef), None)
        if birlesik:
            sonuc.append(Eslesme(k, list(range(j, j + birlesik)), True,
                                 f"{birlesik} Tanzil tokenı tek QAC kelimesi (iskelet birebir)"))
            j += birlesik
        else:
            sonuc.append(Eslesme(k, [], False, "hizalanamadı"))
    return sonuc, durum


@lru_cache(maxsize=1)
def _ayet_dizini() -> dict[tuple[int, int], list[Kelime]]:
    d: dict[tuple[int, int], list[Kelime]] = {}
    for k in veri.korpus().kelimeler:
        d.setdefault((k.sure, k.ayet), []).append(k)
    return d


def _ayet_kelimeleri(sure: int, ayet: int) -> list[Kelime]:
    return _ayet_dizini().get((sure, ayet), [])


# --- çalışma çevirisi -------------------------------------------------------

def ceviriler() -> dict[str, list[tuple[str, str]]]:
    """ayet -> [(tarih, çeviri), ...] (eskiden yeniye). Dosya ekleme yapılarak tutulur."""
    if not CEVIRI_YOLU.exists():
        return {}
    sonuc: dict[str, list[tuple[str, str]]] = {}
    with CEVIRI_YOLU.open(encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            sonuc.setdefault(r["ayet"], []).append((r["tarih"], r["ceviri"]))
    return sonuc


def ceviri_ekle(ref: str, metin: str) -> None:
    metin = " ".join(metin.split())
    if not metin:
        raise ValueError("Çeviri boş olamaz.")
    CEVIRI_YOLU.parent.mkdir(parents=True, exist_ok=True)
    yeni = not CEVIRI_YOLU.exists()
    with CEVIRI_YOLU.open("a", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        if yeni:
            w.writerow(["ayet", "tarih", "ceviri"])
        w.writerow([ref, date.today().isoformat(), metin])


# --- meal (yerel/, depoya işlenmez) ----------------------------------------

def meal_dogrula(json_verisi: dict) -> dict[tuple[int, int], str]:
    """Ayet kümesi Tanzil ile aynı ve parmak izi ayetleri birebir tutmalı; yoksa VeriHatasi."""
    metinler = {(int(r["chapter"]), int(r["verse"])): r["text"] for r in json_verisi["quran"]}
    if set(metinler) != set(okunus.tanzil()):
        raise veri.VeriHatasi(f"Meal ayet kümesi Tanzil ile aynı değil ({len(metinler)} ayet)")
    for (s, a), beklenen in MEAL_PARMAK_IZI.items():
        if metinler[(s, a)] != beklenen:
            raise veri.VeriHatasi(f"Meal parmak izi tutmadı: {s}:{a}\n  beklenen: {beklenen!r}\n"
                                  f"  bulunan : {metinler[(s, a)]!r}")
    return metinler


def meal_kur() -> dict[str, object]:
    if MEAL_YOLU.exists():
        raise FileExistsError(f"Meal zaten kurulu: {MEAL_YOLU}")
    istek = Request(MEAL_URL, headers={"User-Agent": "quran-offline-corpus/1.0"})
    with urlopen(istek, timeout=60) as yanit:
        ham = yanit.read()
    metinler = meal_dogrula(json.loads(ham))
    anahtarlar = set(metinler)
    MEAL_DIZINI.mkdir(parents=True, exist_ok=True)
    MEAL_YOLU.write_bytes(ham)
    bilgi = {
        "file": MEAL_YOLU.name, "source_url": MEAL_URL, "bytes": len(ham),
        "sha256": veri.sha256(MEAL_YOLU), "fetched": date.today().isoformat(),
        "ayet": len(anahtarlar), "parmak_izi": {f"{s}:{a}": m for (s, a), m in MEAL_PARMAK_IZI.items()},
        "lisans": "doğrulanmadı — depoya işlenmez (CLAUDE.md §9)",
        "statu": MEAL_ETIKETI,
    }
    MEAL_MANIFEST.write_text(json.dumps(bilgi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return bilgi


@lru_cache(maxsize=1)
def meal() -> dict[tuple[int, int], str] | None:
    if not MEAL_YOLU.exists():
        return None
    bilgi = json.loads(MEAL_MANIFEST.read_text(encoding="utf-8"))
    if veri.sha256(MEAL_YOLU) != bilgi["sha256"]:
        raise veri.VeriHatasi("Meal dosyasının sha256'sı yerel manifest ile uyuşmuyor.")
    return meal_dogrula(json.loads(MEAL_YOLU.read_text(encoding="utf-8")))


# --- görünüm ----------------------------------------------------------------

def _kelime_satiri(e: Eslesme, o: okunus.AyetOkunus) -> list[str]:
    k = e.kelime
    govdeler = [s for s in k.segmentler if s.tur == "STEM"]
    kokler = sorted(k.kokler)
    from .tara import tur_etiketi
    return [
        k.konum,
        " ".join(o.kelimeler[i].latin for i in e.tanzil) if e.tanzil else "—",
        ";".join(f"{x} ({kok_latin(x)})" for x in kokler) or "—",
        ";".join(sorted(k.lemmalar)) or "—",
        ";".join(dict.fromkeys(tur_etiketi(g) for g in govdeler)) or "—",
        ";".join(dict.fromkeys(g.bab or ("I" if g.pos == "V" else "") for g in govdeler if g.kok)) or "",
        " + ".join(f"{s.bicim}/{'PRON:' + s.zamir if s.zamir else s.etiket}" for s in k.segmentler),
    ]


def ayet_komutu(ref: str, meal_goster: bool = False, arapca: bool = False):
    from .tara import GirdiHatasi, Sonuc, _tablo
    s, a = okunus._ayet_ayristir(ref)
    qac = _ayet_kelimeleri(s, a)
    if not qac:
        raise GirdiHatasi(f"QAC'ta ayet yok: {ref}")
    o = okunus.oku(s, a)
    eslesmeler, durum = hizala(s, a, o)
    satirlar = [f"Ayet {s}:{a} — QAC: {len(qac)} kelime konumu · Tanzil: {len(o.kelimeler)} token"
                f"{' (+ besmele öneki)' if o.besmele else ''} · hizalama: {durum}"]
    if o.besmele:
        satirlar.append("  [sûre başı besmelesi — Tanzil öneki, QAC'ta bu ayete dahil değil] "
                        + " ".join(k.latin for k in o.besmele))
    satirlar += ["", "Okunuş (aktarım, delil değil):", "  " + o.latin_isaretli, "",
                 "Kelime çözümlemesi (QAC v0.4; birim: kelime konumu):"]
    basliklar = ["konum", "okunuş", "kök", "lemma", "tür", "bab", "segmentler (Buckwalter/TAG)"]
    tablo = [_kelime_satiri(e, o) for e in eslesmeler]
    if arapca:
        basliklar.append("Tanzil (denetim için)")
        for satir, e in zip(tablo, eslesmeler):
            satir.append(" ".join(o.kelimeler[i].arapca for i in e.tanzil))
    satirlar += ["  " + x for x in _tablo(basliklar, tablo)]
    notlar = [f"  {e.kelime.konum}: {e.not_}" for e in eslesmeler if e.not_]
    if notlar:
        satirlar += ["", "Hizalama notları:", *notlar]

    cv = ceviriler().get(f"{s}:{a}")
    satirlar += ["", f"Çalışma çevirisi ({CEVIRI_ETIKETI}):"]
    if cv:
        tarih, metin = cv[-1]
        satirlar.append(f"  {metin}   [{tarih}{f'; {len(cv) - 1} önceki sürüm' if len(cv) > 1 else ''}]")
    else:
        satirlar.append(f'  — (yok; eklemek için: python -m tezgah ceviri {s}:{a} "...")')

    kaynak = f"QAC v0.4 | + {okunus.KAYNAK_ADI}"
    iz = f"{veri.korpus().veri_izi} | {okunus.TANZIL_SHA256[:12]}"
    if meal_goster:
        m = meal()
        satirlar += ["", f"Meal — {MEAL_ETIKETI} (Diyanet İşleri, fawazahmed0/quran-api; yerel/):"]
        if m is None:
            satirlar.append("  — meal kurulu değil (python -m tezgah kur meal)")
        else:
            satirlar.append(f"  {m[(s, a)]}")
            kaynak += " | + meal (kurumsal okuma — sınanan, delil değil)"
            iz += f" | {veri.sha256(MEAL_YOLU)[:12]}"
    veri_ = {"ayet": f"{s}:{a}", "qac": len(qac), "tanzil": len(o.kelimeler), "durum": durum,
             "hizalanamayan": sum(1 for e in eslesmeler if not e.tanzil)}
    return Sonuc(satirlar, ["kelime konumu"], veri_, kaynak=kaynak, veri_izi=iz)


def ceviri_komutu(ref: str, metin: str | None):
    from .tara import GirdiHatasi, Sonuc
    s, a = okunus._ayet_ayristir(ref)
    anahtar = f"{s}:{a}"
    if metin is not None:
        try:
            ceviri_ekle(anahtar, metin)
        except ValueError as e:
            raise GirdiHatasi(str(e)) from e
    gecmis = ceviriler().get(anahtar, [])
    satirlar = [f"Çalışma çevirisi {anahtar} ({CEVIRI_ETIKETI}; dosya: kavramlar/calisma_cevirisi.tsv)"]
    satirlar += [f"  {t}  {m}" for t, m in gecmis] or ["  — yok"]
    return Sonuc(satirlar, [], {"surum": len(gecmis)}, kaynak="çalışma çevirisi (kullanıcı)", veri_izi="—")


def kur_komutu(ne: str):
    from .tara import GirdiHatasi, Sonuc
    from . import qm
    from .ikincil import lane, sami
    kurucular = {"meal": meal_kur, "quran-morphology": qm.kur, "lane": lane.kur, "sedra": sami.kur}
    if ne not in kurucular:
        raise GirdiHatasi("Kurulabilecek katman: " + ", ".join(kurucular))
    try:
        bilgi = kurucular[ne]()
    except FileExistsError as e:
        raise GirdiHatasi(str(e)) from e
    if ne in {"lane", "sedra"}:
        return Sonuc([f"{ne} kuruldu (yerel/, depoya işlenmez):", *[f"  {k}: {v}" for k, v in bilgi.items()]], [],
                     bilgi, kaynak=ne, veri_izi="—")
    if ne == "quran-morphology":
        return Sonuc(["quran-morphology kuruldu (yerel/, depoya işlenmez):",
                      *[f"  {k}: {v}" for k, v in bilgi.items()]], [], bilgi,
                     kaynak=qm.KAYNAK_ADI, veri_izi=str(bilgi["sha256"])[:12])
    satirlar = ["Meal kuruldu (yerel/, depoya işlenmez):", *[f"  {k}: {v}" for k, v in bilgi.items()]]
    return Sonuc(satirlar, ["ayet"], bilgi, kaynak="fawazahmed0/quran-api tur-diyanetisleri",
                 veri_izi=str(bilgi["sha256"])[:12])
