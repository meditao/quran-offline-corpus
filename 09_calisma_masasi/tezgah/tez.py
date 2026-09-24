"""Tez sınama kaydı (Aşama 3).

Dosyalar: kavramlar/tezler/<ad>/
    surum-001.json   dondurulmuş sürüm (salt okunur; sha256 defterde)
    defter.json      zincirli kayıt defteri: sürüm, tarama, bulgu, sonuç (yalnız eklenir)
    tez.md           defterden üretilen rapor (elle değiştirilmez)

Kurallar (CLAUDE.md §7, §2.6):
- Tez tek cümleyle dondurulur ve olduğu gibi saklanır; araç tez ifadesini değiştirmez, güçlendirmez.
- Tanımlar, eksenler ve karşı örnek havuzu `tez ac` anında, taramadan önce kaydedilir. Havuz
  sorgu tanımıdır; `tez tara` ile çalıştırılır. Değişiklik yalnız yeni sürümle olur; eski sürüm
  silinmez ve yeni sürümün kaç bulgudan sonra açıldığı kayda geçer.
- Her bulgu eksen etiketi taşır ve bir sorguya dayanır; bulgudaki ayetler o sorgunun çıktısında
  geçmek zorundadır. Eksenleri tezinkinden farklı olan bulgu yalnız "farklı eksen" rafına konur
  (çelişen rafına konamaz; simetri için destekleyen / yalnız uyumlu rafına da konamaz).
- "Farklı eksen" rafındaki her bulgu gerekçe taşır; rapor bu rafı ayrı bir bölümde listeler.
- Bulgunun rafı silinmeden, gerekçeli "yeniden değerlendirme" kaydıyla değiştirilir; eski
  değerlendirme raporda görünür, defter zinciri korunur (kayıt yalnız eklenir).
- Sonuç iki eksende yazılır (mantıksal durum + delil derecesi) ve bulgularla tutarlı olmalıdır:
  "Yalnız uyumlu" bulgulardan "Destekleniyor" sonucu çıkmaz. "Destekleniyor" sonucunda
  desteklenen kapsam zorunludur.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shlex
from datetime import date
from pathlib import Path

from .kavram import (DELIL_DERECESI, MANTIKSAL_DURUM, KavramHatasi, _bolum_kaydi, _secenek,
                     _tr_anahtar, sorgu_calistir)

MASA = Path(__file__).resolve().parents[1]
TEZLER = MASA / "kavramlar" / "tezler"

EKSEN_BOYUTLARI: dict[str, tuple[str, ...]] = {
    "kip": ("tanımlayıcı", "normatif"),
    "düzlem": ("oluşum", "sorumluluk"),
}
RAFLAR = ("destekleyen", "yalnız uyumlu", "çelişen", "belirsiz", "farklı eksen")
AYET_RE = r"(?<![\d:]){s}:{a}(?!\d)"


class TezHatasi(Exception):
    pass


def _sec(deger: str, secenekler: tuple[str, ...], ad: str) -> str:
    try:
        return _secenek(deger, secenekler, ad)
    except KavramHatasi as e:
        raise TezHatasi(str(e)) from e


# --- yardımcılar ------------------------------------------------------------

def _json(veri: object) -> str:
    return json.dumps(veri, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha(metin: str | bytes) -> str:
    return hashlib.sha256(metin.encode("utf-8") if isinstance(metin, str) else metin).hexdigest()


def _dizin(ad: str) -> Path:
    if not re.fullmatch(r"[\w-]+", ad):
        raise TezHatasi(f"Tez adı yalnız harf, rakam, _ ve - içerebilir: {ad!r}")
    return TEZLER / ad


def _sorgu(argv: list[str]) -> str:
    try:
        return sorgu_calistir(argv)
    except KavramHatasi as e:
        raise TezHatasi(str(e)) from e


def _komut_ayristir(metin: str) -> list[str]:
    """Havuz sorgusunu çalıştırmadan doğrular (taramadan önce kayıt)."""
    from .__main__ import parser_kur
    from .kavram import IZINLI_SORGULAR
    argv = shlex.split(metin)
    if not argv or argv[0] not in IZINLI_SORGULAR:
        raise TezHatasi(f"Havuz sorgusu şunlardan biri olmalı: {', '.join(sorted(IZINLI_SORGULAR))} ({metin!r})")
    if "--meal" in argv or "--arapca" in argv:
        raise TezHatasi("Havuz sorgusunda --meal ve --arapca kullanılmaz.")
    try:
        parser_kur().parse_args(argv)
    except SystemExit as e:
        raise TezHatasi(f"Geçersiz havuz sorgusu: {metin!r}") from e
    return argv


def tek_cumle(tez: str) -> str:
    """Tezi olduğu gibi döndürür (yalnız baş/son boşluk kırpılır); tek cümle değilse hata."""
    t = tez.strip()
    if not t:
        raise TezHatasi("Tez boş olamaz.")
    if "\n" in t:
        raise TezHatasi("Tez tek satır, tek cümle olmalı.")
    ic = re.sub(r"(?<=\d)[.:](?=\d)", "", t).rstrip().rstrip(".!?…").rstrip()
    if re.search(r"[.!?…]", ic):
        raise TezHatasi("Tez tek cümle olmalı (cümle içinde . ! ? … bulundu).")
    return t


def _tanimlar(ham: list[str]) -> list[dict[str, str]]:
    sonuc = []
    for h in ham:
        if "=" not in h:
            raise TezHatasi(f"Tanım 'terim=tanım' biçiminde olmalı: {h!r}")
        terim, tanim = (x.strip() for x in h.split("=", 1))
        if not terim or not re.search(r"\w", tanim):
            raise TezHatasi(f"Tanımda terim ve tanım boş olamaz: {h!r}")
        sonuc.append({"terim": terim, "tanim": " ".join(tanim.split())})
    if not sonuc:
        raise TezHatasi("En az bir tanım gerekli (taramadan önce kaydedilir).")
    return sonuc


def eksenler(ham: list[str]) -> dict[str, str]:
    """boyut=değer. Bilinen boyutlarda değer sözlükten; diğer boyutlar serbest (vb.)."""
    sonuc: dict[str, str] = {}
    for h in ham:
        if "=" not in h:
            raise TezHatasi(f"Eksen 'boyut=değer' biçiminde olmalı: {h!r}")
        boyut, deger = (x.strip() for x in h.split("=", 1))
        if not boyut or not deger:
            raise TezHatasi(f"Eksende boyut ve değer boş olamaz: {h!r}")
        bilinen = next((b for b in EKSEN_BOYUTLARI if _tr_anahtar(b) == _tr_anahtar(boyut)), None)
        if bilinen:
            boyut, deger = bilinen, _sec(deger, EKSEN_BOYUTLARI[bilinen], f"'{bilinen}' ekseni")
        else:
            boyut, deger = _tr_anahtar(boyut), " ".join(deger.split())
        if boyut in sonuc:
            raise TezHatasi(f"Eksen iki kez verildi: {boyut}")
        sonuc[boyut] = deger
    if not sonuc:
        raise TezHatasi("En az bir eksen gerekli (ör. kip=tanımlayıcı, düzlem=oluşum).")
    return sonuc


# --- defter -----------------------------------------------------------------

class Tez:
    def __init__(self, ad: str):
        self.ad = ad
        self.dizin = _dizin(ad)
        self.defter_yolu = self.dizin / "defter.json"
        if not self.defter_yolu.exists():
            raise TezHatasi(f"Tez yok: {ad} (önce: python -m tezgah tez ac {ad} ...)")
        self.kayitlar: list[dict] = json.loads(self.defter_yolu.read_text(encoding="utf-8"))
        self.butunluk_denetle()

    # bütünlük
    @staticmethod
    def _zincir(onceki: str, kayit: dict) -> str:
        govde = {k: v for k, v in kayit.items() if k != "zincir"}
        return _sha(onceki + _json(govde))

    def butunluk_denetle(self) -> None:
        onceki = ""
        for i, k in enumerate(self.kayitlar, 1):
            if k.get("zincir") != self._zincir(onceki, k):
                raise TezHatasi(f"Defter zinciri bozuk: kayıt {i} ({k.get('tur')}) sonradan değiştirilmiş.")
            onceki = k["zincir"]
            if k["tur"] == "surum":
                yol = self.dizin / k["dosya"]
                if not yol.exists() or _sha(yol.read_bytes()) != k["sha256"]:
                    raise TezHatasi(f"Dondurulmuş sürüm değiştirilmiş ya da eksik: {k['dosya']}")

    def _ekle(self, kayit: dict) -> dict:
        onceki = self.kayitlar[-1]["zincir"] if self.kayitlar else ""
        kayit = {**kayit, "tarih": date.today().isoformat()}
        kayit["zincir"] = self._zincir(onceki, kayit)
        self.kayitlar.append(kayit)
        self.defter_yolu.write_text(json.dumps(self.kayitlar, ensure_ascii=False, indent=2) + "\n",
                                    encoding="utf-8")
        return kayit

    # okuma
    def turler(self, tur: str, surum: int | None = None) -> list[dict]:
        return [k for k in self.kayitlar if k["tur"] == tur and (surum is None or k.get("surum") == surum)]

    def surum(self, no: int | None = None) -> dict:
        kayitlar = self.turler("surum")
        k = kayitlar[-1] if no is None else next(x for x in kayitlar if x["surum"] == no)
        return json.loads((self.dizin / k["dosya"]).read_text(encoding="utf-8"))

    @property
    def guncel_no(self) -> int:
        return self.turler("surum")[-1]["surum"]

    def degerlendirmeler(self, no: int) -> list[dict]:
        return [k for k in self.kayitlar if k["tur"] == "degerlendirme" and k["bulgu"] == no]

    def etkin(self, b: dict) -> dict:
        """Bulgunun son değerlendirmeye göre etkin rafı, eksenleri ve (farklı eksen) gerekçesi."""
        durum = {"raf": b["raf"], "eksenler": b["eksenler"], "gerekce": b.get("gerekce", "")}
        for d in self.degerlendirmeler(b["no"]):
            durum = {"raf": d["yeni_raf"], "eksenler": d["yeni_eksenler"], "gerekce": d["gerekce"]}
        return durum

    def raf_sayilari(self, surum: int) -> dict[str, int]:
        sayim = {r: 0 for r in RAFLAR}
        for b in self.turler("bulgu", surum):
            sayim[self.etkin(b)["raf"]] += 1
        return sayim

    # yazma
    def _surum_yaz(self, icerik: dict) -> None:
        no = icerik["surum"]
        dosya = f"surum-{no:03d}.json"
        yol = self.dizin / dosya
        if yol.exists():
            raise TezHatasi(f"Sürüm dosyası zaten var: {dosya}")
        ham = json.dumps(icerik, ensure_ascii=False, indent=2) + "\n"
        yol.write_text(ham, encoding="utf-8")
        os.chmod(yol, 0o444)
        self._ekle({"tur": "surum", "surum": no, "dosya": dosya, "sha256": _sha(ham.encode("utf-8"))})


def ac(ad: str, tez: str, tanim: list[str], eksen: list[str], karsi: list[str], havuz_notu: str = "") -> Tez:
    dizin = _dizin(ad)
    if dizin.exists():
        raise TezHatasi(f"Tez zaten var: {ad} (değişiklik için: tez yeni-surum)")
    icerik = {
        "surum": 1,
        "tez": tek_cumle(tez),
        "tanimlar": _tanimlar(tanim),
        "eksenler": eksenler(eksen),
        "karsi_ornek_havuzu": [_komut_ayristir(k) for k in karsi],
        "havuz_notu": " ".join(havuz_notu.split()),
        "donduruldu": date.today().isoformat(),
        "onceki_surum": None,
        "gerekce": None,
    }
    if not icerik["karsi_ornek_havuzu"]:
        raise TezHatasi("Karşı örnek havuzu taramadan önce kaydedilmeli: en az bir --karsi sorgusu.")
    dizin.mkdir(parents=True)
    (dizin / "defter.json").write_text("[]\n", encoding="utf-8")
    t = Tez(ad)
    t._surum_yaz(icerik)
    rapor_yaz(t)
    return t


def yeni_surum(ad: str, gerekce: str, tez: str | None = None, tanim: list[str] | None = None,
               eksen: list[str] | None = None, karsi: list[str] | None = None) -> dict:
    t = Tez(ad)
    if not gerekce or not re.search(r"\w", gerekce):
        raise TezHatasi("Yeni sürüm için gerekçe zorunlu.")
    eski = t.surum()
    yeni = dict(eski)
    if tez is not None:
        yeni["tez"] = tek_cumle(tez)
    if tanim:
        yeni["tanimlar"] = _tanimlar(tanim)
    if eksen:
        yeni["eksenler"] = eksenler(eksen)
    if karsi:
        yeni["karsi_ornek_havuzu"] = [_komut_ayristir(k) for k in karsi]
    alanlar = ("tez", "tanimlar", "eksenler", "karsi_ornek_havuzu")
    if all(yeni[a] == eski[a] for a in alanlar):
        raise TezHatasi("Yeni sürümde değişiklik yok (tez, tanım, eksen ya da havuz değişmeli).")
    no = eski["surum"] + 1
    yeni.update({
        "surum": no,
        "donduruldu": date.today().isoformat(),
        "onceki_surum": eski["surum"],
        "gerekce": " ".join(gerekce.split()),
        "degisen_alanlar": [a for a in alanlar if yeni[a] != eski[a]],
        "onceki_surumdeki_bulgu": len(t.turler("bulgu", eski["surum"])),
        "onceki_surum_tarandi": bool(t.turler("tarama", eski["surum"])),
        "onceki_surumdeki_sonuc": len(t.turler("sonuc", eski["surum"])),
    })
    t._surum_yaz(yeni)
    rapor_yaz(t)
    return yeni


def tara(ad: str) -> dict:
    t = Tez(ad)
    s = t.surum()
    sorgular = [{"argv": argv, "cikti": _sorgu(argv)} for argv in s["karsi_ornek_havuzu"]]
    k = t._ekle({"tur": "tarama", "surum": s["surum"], "sorgular": sorgular})
    rapor_yaz(t)
    return k


def _dolu(metin: str | None) -> bool:
    return bool(metin) and bool(re.search(r"\w", metin))


def eksen_farki(b_eksen: dict[str, str], t_eksen: dict[str, str]) -> dict[str, tuple[str, str]]:
    return {b: (b_eksen[b], t_eksen[b]) for b in b_eksen if b_eksen[b] != t_eksen[b]}


def _raf_denetle(b_eksen: dict[str, str], t_eksen: dict[str, str], raf: str, gerekce: str | None) -> str:
    """Eksen/raf kuralı; geçerli raf adını döndürür."""
    if set(b_eksen) != set(t_eksen):
        raise TezHatasi(f"Bulgu tezin bütün eksen boyutlarını etiketlemeli: {', '.join(t_eksen)}")
    raf = _sec(raf, RAFLAR, "Raf")
    farkli = eksen_farki(b_eksen, t_eksen)
    if farkli and raf != "farklı eksen":
        ayrinti = ", ".join(f"{b}: bulgu {x} ↔ tez {y}" for b, (x, y) in farkli.items())
        raise TezHatasi(f"Farklı eksendeki bulgu '{raf}' rafına konamaz ({ayrinti}); raf: farklı eksen.")
    if not farkli and raf == "farklı eksen":
        raise TezHatasi("Eksenleri tezle aynı olan bulgu 'farklı eksen' rafına konamaz.")
    if raf == "farklı eksen" and not _dolu(gerekce):
        raise TezHatasi("'Farklı eksen' rafına konan bulgu için gerekçe zorunlu (--gerekce): "
                        "bulgunun neden tezin ekseninde olmadığını yazın.")
    return raf


def bulgu(ad: str, eksen: list[str], raf: str, aciklama: str, argv: list[str],
          ayetler: list[str] | None = None, gerekce: str | None = None) -> dict:
    from . import okunus
    t = Tez(ad)
    s = t.surum()
    if not _dolu(aciklama):
        raise TezHatasi("Bulgu açıklaması boş olamaz.")
    b_eksen = eksenler(eksen)
    raf = _raf_denetle(b_eksen, s["eksenler"], raf, gerekce)
    if not argv:
        raise TezHatasi("Bulgu bir sorguya dayanmalı (-- ile tezgah komutu).")
    if "--arapca" in argv:
        raise TezHatasi("Bulgu sorgusunda --arapca kullanılmaz.")
    cikti = _sorgu(argv)
    bulunan = []
    for ref in ayetler or []:
        sa = okunus._ayet_ayristir(ref)
        if not re.search(AYET_RE.format(s=sa[0], a=sa[1]), cikti):
            raise TezHatasi(f"Ayet {sa[0]}:{sa[1]} bulgunun sorgu çıktısında yok; ayet referansı sorgudan gelmeli.")
        bulunan.append(f"{sa[0]}:{sa[1]}")
    k = t._ekle({"tur": "bulgu", "surum": s["surum"], "no": len(t.turler("bulgu")) + 1,
                 "eksenler": b_eksen, "raf": raf, "aciklama": " ".join(aciklama.split()),
                 "gerekce": " ".join((gerekce or "").split()),
                 "ayetler": bulunan, "argv": argv, "cikti": cikti})
    rapor_yaz(t)
    return k


def degerlendir(ad: str, no: int, raf: str, gerekce: str, eksen: list[str] | None = None) -> dict:
    """Bulgunun rafını (ve gerekirse eksen etiketini) silmeden değiştirir: yeni kayıt eklenir."""
    t = Tez(ad)
    s = t.surum()
    b = next((x for x in t.turler("bulgu") if x["no"] == no), None)
    if b is None:
        raise TezHatasi(f"Bulgu yok: {no}")
    if b["surum"] != s["surum"]:
        raise TezHatasi(f"Bulgu {no} sürüm {b['surum']}'e ait; yalnız güncel sürümün ({s['surum']}) bulguları "
                        "yeniden değerlendirilir.")
    if not _dolu(gerekce):
        raise TezHatasi("Yeniden değerlendirme için gerekçe zorunlu.")
    once = t.etkin(b)
    yeni_eksen = eksenler(eksen) if eksen else once["eksenler"]
    yeni_raf = _raf_denetle(yeni_eksen, s["eksenler"], raf, gerekce)
    if yeni_raf == once["raf"] and yeni_eksen == once["eksenler"]:
        raise TezHatasi("Değişiklik yok: raf ve eksen aynı.")
    k = t._ekle({"tur": "degerlendirme", "surum": s["surum"], "bulgu": no,
                 "eski_raf": once["raf"], "yeni_raf": yeni_raf,
                 "eski_eksenler": once["eksenler"], "yeni_eksenler": yeni_eksen,
                 "gerekce": " ".join(gerekce.split())})
    rapor_yaz(t)
    return k


def sonuc_tutarliligi(durum: str, sayim: dict[str, int], tarandi: bool) -> str | None:
    """Tutarsızlık varsa açıklaması, yoksa None."""
    if not tarandi:
        return "karşı örnek havuzu bu sürüm için taranmadı (önce: tez tara)"
    if durum == "Destekleniyor":
        if sayim["çelişen"]:
            return "çelişen bulgu varken 'Destekleniyor' yazılamaz"
        if not sayim["destekleyen"]:
            return ("'Destekleniyor' için en az bir 'destekleyen' bulgu gerekir; "
                    "'yalnız uyumlu' bulgu destek sayılmaz")
    if durum == "Yalnız uyumlu":
        if sayim["çelişen"]:
            return "çelişen bulgu varken 'Yalnız uyumlu' yazılamaz"
        if not (sayim["destekleyen"] or sayim["yalnız uyumlu"]):
            return "'Yalnız uyumlu' için en az bir destekleyen ya da yalnız uyumlu bulgu gerekir"
    if durum == "Çelişiyor" and not sayim["çelişen"]:
        return "'Çelişiyor' için en az bir çelişen bulgu gerekir"
    return None


def sonuc(ad: str, mantiksal_durum: str, delil_derecesi: str, gerekce: str, kapsam: str | None = None) -> dict:
    t = Tez(ad)
    no = t.guncel_no
    durum = _sec(mantiksal_durum, MANTIKSAL_DURUM, "Mantıksal durum")
    derece = _sec(delil_derecesi, DELIL_DERECESI, "Delil derecesi")
    if not _dolu(gerekce):
        raise TezHatasi("Sonuç gerekçesi boş olamaz.")
    if durum == "Destekleniyor" and not _dolu(kapsam):
        raise TezHatasi("'Destekleniyor' sonucunda desteklenen kapsam zorunlu (--kapsam): tezin hangi "
                        "kullanımlar / ayet kümesi için desteklendiğini yazın.")
    sayim = t.raf_sayilari(no)
    sorun = sonuc_tutarliligi(durum, sayim, bool(t.turler("tarama", no)))
    if sorun:
        raise TezHatasi(f"Sonuç bulgularla tutarsız: {sorun}.")
    k = t._ekle({"tur": "sonuc", "surum": no, "mantiksal_durum": durum, "delil_derecesi": derece,
                 "gerekce": " ".join(gerekce.split()), "kapsam": " ".join((kapsam or "").split()),
                 "raf_sayilari": sayim})
    rapor_yaz(t)
    return k


# --- rapor ------------------------------------------------------------------

def _blok(argv: list[str], cikti: str) -> str:
    return f"`python -m tezgah {shlex.join(argv)}`\n\n```text\n{cikti.rstrip()}\n```\n"


def _kayit(ciktilar: list[str], kaynak: str = "—") -> str:
    ic = _bolum_kaydi(ciktilar, oneri_var=False)
    if not ciktilar and kaynak != "—":
        ic = ic.replace("Kaynak      : —", f"Kaynak      : {kaynak}")
    return re.sub(r"<!-- /?tezgah:bolum-kaydi -->\n?", "", ic)


def rapor(t: Tez) -> str:
    s = t.surum()
    no = s["surum"]
    p = [f"# Tez: {t.ad}\n",
         "_Bu dosya defter.json'dan üretilir; elle değiştirilmez (python -m tezgah tez goster)._\n"]

    p.append(f"## 1. Tez (sürüm {no}, donduruldu {s['donduruldu']})\n\n> {s['tez']}\n")
    p.append(_kayit([], f"surum-{no:03d}.json (sha256 {t.turler('surum')[-1]['sha256'][:12]})"))

    p.append("## 2. Tanımlar (taramadan önce kaydedildi)\n")
    p += [f"- **{d['terim']}**: {d['tanim']}" for d in s["tanimlar"]]
    p.append("")
    p.append(_kayit([], f"surum-{no:03d}.json"))

    p.append("## 3. Eksenler\n")
    p += [f"- {b}: **{d}**" for b, d in s["eksenler"].items()]
    p.append("\nFarklı eksendeki bulgu çelişen (ve destekleyen) rafına konamaz; 'farklı eksen' rafında ayrı tutulur.\n")
    p.append(_kayit([], f"surum-{no:03d}.json"))

    p.append("## 4. Karşı örnek havuzu (taramadan önce kaydedildi)\n")
    p += [f"- `python -m tezgah {shlex.join(a)}`" for a in s["karsi_ornek_havuzu"]]
    if s.get("havuz_notu"):
        p.append(f"\nNot: {s['havuz_notu']}")
    taramalar = t.turler("tarama", no)
    ciktilar = []
    if not taramalar:
        p.append("\n_Havuz bu sürüm için henüz taranmadı (python -m tezgah tez tara)._\n")
    else:
        son = taramalar[-1]
        p.append(f"\nTarama ({son['tarih']}; bu sürümde {len(taramalar)} tarama):\n")
        for q in son["sorgular"]:
            p.append(_blok(q["argv"], q["cikti"]))
            ciktilar.append(q["cikti"])
    p.append(_kayit(ciktilar))

    p.append("## 5. Bulgular\n")
    sayim = t.raf_sayilari(no)
    p.append(" · ".join(f"{r}: {n}" for r, n in sayim.items()) + " (bulgu sayısı, etkin raf, bu sürüm)\n")
    ciktilar = []

    def bulgu_md(b: dict) -> None:
        e = t.etkin(b)
        eks = ", ".join(f"{k}={v}" for k, v in e["eksenler"].items())
        p.append(f"#### Bulgu {b['no']} — {b['tarih']} — eksen: {eks}\n\n{b['aciklama']}\n")
        if e["raf"] == "farklı eksen":
            fark = eksen_farki(e["eksenler"], s["eksenler"])
            p.append("Eksen farkı: " + ", ".join(f"{k}: bulgu **{x}** ↔ tez **{y}**" for k, (x, y) in fark.items()))
            p.append(f"\nGerekçe (farklı eksen): {e['gerekce']}\n")
        gecmis = t.degerlendirmeler(b["no"])
        if gecmis:
            p.append(f"Değerlendirme geçmişi (ilk kayıt: {b['raf']}; eski değerlendirmeler silinmez):")
            for d in gecmis:
                ek = "" if d["eski_eksenler"] == d["yeni_eksenler"] else " (eksen etiketi değişti)"
                p.append(f"- {d['tarih']}: {d['eski_raf']} → **{d['yeni_raf']}**{ek} — {d['gerekce']}")
            p.append("")
        if b["ayetler"]:
            p.append(f"Ayetler (sorgu çıktısında doğrulandı): {', '.join(b['ayetler'])}\n")
        p.append(_blok(b["argv"], b["cikti"]))
        ciktilar.append(b["cikti"])

    for raf in RAFLAR[:-1]:
        bulgular = [b for b in t.turler("bulgu", no) if t.etkin(b)["raf"] == raf]
        if bulgular:
            p.append(f"### Raf: {raf}\n")
            for b in bulgular:
                bulgu_md(b)
    p.append(_kayit(ciktilar))

    farkli = [b for b in t.turler("bulgu", no) if t.etkin(b)["raf"] == "farklı eksen"]
    p.append(f"## 5b. Farklı eksen rafı ({len(farkli)} bulgu — sonuç hesabına girmez, çelişen/destekleyen sayılmaz)\n")
    ciktilar = []
    if not farkli:
        p.append("_Bu sürümde farklı eksen rafında bulgu yok._\n")
    for b in farkli:
        bulgu_md(b)
    p.append(_kayit(ciktilar))

    p.append("## 6. Sonuç (iki eksen)\n")
    sonuclar = t.turler("sonuc", no)
    if not sonuclar:
        p.append("_Bu sürüm için sonuç yazılmadı._\n")
    for k in sonuclar:
        kapsam = f" · **Desteklenen kapsam:** {k['kapsam']}" if k.get("kapsam") else ""
        p.append(f"- {k['tarih']}: **Mantıksal durum:** {k['mantiksal_durum']} · "
                 f"**Delil derecesi:** {k['delil_derecesi']}{kapsam} — {k['gerekce']} "
                 f"(raflar: {', '.join(f'{r} {n}' for r, n in k['raf_sayilari'].items())})")
    p.append("")
    p.append(_kayit([], "defter.json" if sonuclar else "—"))

    p.append("## 7. Sürüm geçmişi (eski sürümler silinmez)\n")
    for k in t.turler("surum"):
        v = t.surum(k["surum"])
        satir = f"- Sürüm {v['surum']} ({v['donduruldu']}, sha256 {k['sha256'][:12]}): {v['tez']}"
        if v.get("onceki_surum"):
            satir += (f"\n  - Gerekçe: {v['gerekce']} · değişen: {', '.join(v['degisen_alanlar'])} · "
                      f"önceki sürümdeki bulgu: {v['onceki_surumdeki_bulgu']} · önceki sürüm tarandı: "
                      f"{'evet' if v['onceki_surum_tarandi'] else 'hayır'} · önceki sürümdeki sonuç: "
                      f"{v['onceki_surumdeki_sonuc']}")
        sayim = t.raf_sayilari(v["surum"])
        satir += (f"\n  - Bulgular: {', '.join(f'{r} {n}' for r, n in sayim.items())} · "
                  f"tarandı: {'evet' if t.turler('tarama', v['surum']) else 'hayır'}")
        for k2 in t.turler("sonuc", v["surum"]):
            satir += f"\n  - Sonuç ({k2['tarih']}): {k2['mantiksal_durum']} · {k2['delil_derecesi']} — {k2['gerekce']}"
        p.append(satir)
    p.append("")
    p.append(_kayit([], "defter.json"))
    return "\n".join(p)


def rapor_yaz(t: Tez) -> Path:
    yol = t.dizin / "tez.md"
    yol.write_text(rapor(t), encoding="utf-8")
    return yol


def denetle(ad: str) -> tuple[list[str], list[str]]:
    """(hatalar, uyarılar). Defter zinciri ve sürüm sha256'ları Tez() açılışında denetlenir."""
    try:
        t = Tez(ad)
    except TezHatasi as e:
        return [str(e)], []
    hatalar, uyarilar = [], []
    for k in t.kayitlar:
        sorgular = k.get("sorgular", []) if k["tur"] == "tarama" else (
            [{"argv": k["argv"], "cikti": k["cikti"]}] if k["tur"] == "bulgu" else [])
        for q in sorgular:
            if _sorgu(q["argv"]) != q["cikti"]:
                hatalar.append(f"{k['tur']} (sürüm {k['surum']}): sorgu çıktısı değişti — "
                               f"python -m tezgah {shlex.join(q['argv'])}")
    for b in t.turler("bulgu"):
        e = t.etkin(b)
        if e["raf"] == "farklı eksen" and not _dolu(e["gerekce"]):
            hatalar.append(f"bulgu {b['no']}: farklı eksen rafında gerekçesiz")
    for k in t.turler("sonuc"):
        if k["mantiksal_durum"] == "Destekleniyor" and not _dolu(k.get("kapsam")):
            hatalar.append(f"sonuç (sürüm {k['surum']}): 'Destekleniyor' için desteklenen kapsam yok")
        sorun = sonuc_tutarliligi(k["mantiksal_durum"], k["raf_sayilari"], True)
        if sorun:
            hatalar.append(f"sonuç (sürüm {k['surum']}): {sorun}")
        if k["raf_sayilari"] != t.raf_sayilari(k["surum"]):
            uyarilar.append(f"sonuç (sürüm {k['surum']}) yazıldıktan sonra bulgu eklendi ya da yeniden "
                            f"değerlendirildi; sonuç yeniden gözden geçirilmeli")
    rapor_yolu = t.dizin / "tez.md"
    if not rapor_yolu.exists() or rapor_yolu.read_text(encoding="utf-8") != rapor(t):
        hatalar.append("tez.md defterle uyuşmuyor (elle değiştirilmiş; yeniden üretmek için: tez goster)")
    return hatalar, uyarilar


def liste() -> list[str]:
    """Dondurulmuş tez kayıtları (kavramlar/tezler/<ad>/surum-001.json)."""
    if not TEZLER.exists():
        return []
    return sorted(d.name for d in TEZLER.iterdir() if d.is_dir() and (d / "surum-001.json").exists())


# --- komut satırı -----------------------------------------------------------

def _komut(n):
    from .tara import GirdiHatasi, Sonuc
    try:
        if n.tez_komut == "liste":
            adlar = liste()
            satirlar = [f"Tez kayıtları (kavramlar/tezler/): {len(adlar)}", *[f"  {a}" for a in adlar]]
            return Sonuc(satirlar, [], {"tezler": adlar}, kaynak="tez kaydı", veri_izi="—")
        if n.tez_komut == "ac":
            t = ac(n.ad, n.tez, n.tanim, n.eksen, n.karsi, n.havuz_notu)
            s = t.surum()
            satirlar = [f"Tez donduruldu: sürüm 1 ({t.dizin.name}/surum-001.json)",
                        f"  Tez: {s['tez']}",
                        f"  Tanım: {len(s['tanimlar'])} · eksen: {len(s['eksenler'])} · "
                        f"karşı örnek havuzu: {len(s['karsi_ornek_havuzu'])} sorgu (henüz taranmadı)"]
        elif n.tez_komut == "yeni-surum":
            v = yeni_surum(n.ad, n.gerekce, n.tez, n.tanim, n.eksen, n.karsi)
            satirlar = [f"Yeni sürüm donduruldu: {v['surum']} (değişen: {', '.join(v['degisen_alanlar'])}; "
                        f"önceki sürümdeki bulgu: {v['onceki_surumdeki_bulgu']})"]
        elif n.tez_komut == "tara":
            k = tara(n.ad)
            satirlar = [f"Karşı örnek havuzu tarandı (sürüm {k['surum']}): {len(k['sorgular'])} sorgu"]
        elif n.tez_komut == "bulgu":
            argv = n.argv[1:] if n.argv[:1] == ["--"] else n.argv
            k = bulgu(n.ad, n.eksen, n.raf, n.aciklama, argv, n.ayet, n.gerekce)
            satirlar = [f"Bulgu {k['no']} kaydedildi (sürüm {k['surum']}, raf: {k['raf']})"]
        elif n.tez_komut == "degerlendir":
            k = degerlendir(n.ad, n.no, n.raf, n.gerekce, n.eksen)
            satirlar = [f"Bulgu {k['bulgu']} yeniden değerlendirildi: {k['eski_raf']} → {k['yeni_raf']} "
                        "(eski kayıt korunur)"]
        elif n.tez_komut == "sonuc":
            k = sonuc(n.ad, n.mantiksal_durum, n.delil_derecesi, n.gerekce, n.kapsam)
            satirlar = [f"Sonuç kaydedildi (sürüm {k['surum']}): {k['mantiksal_durum']} · {k['delil_derecesi']}"]
        elif n.tez_komut == "goster":
            t = Tez(n.ad)
            yol = rapor_yaz(t)
            satirlar = [rapor(t), "", f"(rapor: {yol})"]
        else:
            hatalar, uyarilar = denetle(n.ad)
            satirlar = [f"Tez denetimi: {n.ad} — {len(hatalar)} hata, {len(uyarilar)} uyarı",
                        *[f"  HATA: {h}" for h in hatalar], *[f"  UYARI: {u}" for u in uyarilar]]
            return Sonuc(satirlar, [], {"hata": len(hatalar), "uyari": len(uyarilar)},
                         basarili=not hatalar, kaynak="tez kaydı", veri_izi="—")
    except (TezHatasi, KavramHatasi) as e:
        raise GirdiHatasi(str(e)) from e
    return Sonuc(satirlar, [], {}, kaynak="tez kaydı", veri_izi="—")


def parser_ekle(alt) -> None:
    p = alt.add_parser("tez", help="tez sınama: liste / ac / tara / bulgu / degerlendir / sonuc / yeni-surum / goster / denetle")
    k = p.add_subparsers(dest="tez_komut", required=True, metavar="işlem")

    k.add_parser("liste", help="tez kayıtlarını listele")

    s = k.add_parser("ac", help="tezi dondur: tek cümle + tanımlar + eksenler + karşı örnek havuzu")
    s.add_argument("ad")
    s.add_argument("--tez", required=True, help="tek cümle; olduğu gibi saklanır")
    s.add_argument("--tanim", action="append", required=True, help="terim=tanım (birden çok)")
    s.add_argument("--eksen", action="append", required=True,
                   help="boyut=değer, ör. kip=tanımlayıcı, düzlem=oluşum (birden çok)")
    s.add_argument("--karsi", action="append", required=True,
                   help='karşı örnek havuzu sorgusu, ör. "kalip ROOT:Slw&POS:V" (birden çok)')
    s.add_argument("--havuz-notu", default="")

    s = k.add_parser("yeni-surum", help="değişiklik için yeni sürüm (eskisi silinmez)")
    s.add_argument("ad")
    s.add_argument("--gerekce", required=True)
    s.add_argument("--tez")
    s.add_argument("--tanim", action="append")
    s.add_argument("--eksen", action="append")
    s.add_argument("--karsi", action="append")

    s = k.add_parser("tara", help="karşı örnek havuzunu tara (güncel sürüm)")
    s.add_argument("ad")

    s = k.add_parser("bulgu", help="bulgu ekle: tez bulgu AD --eksen ... --raf ... --aciklama ... -- komut")
    s.add_argument("ad")
    s.add_argument("--eksen", action="append", required=True)
    s.add_argument("--raf", required=True, help=" · ".join(RAFLAR))
    s.add_argument("--aciklama", required=True)
    s.add_argument("--ayet", action="append", help="sorgu çıktısında geçmesi gereken ayet (birden çok)")
    s.add_argument("--gerekce", help="'farklı eksen' rafı için zorunlu")
    s.add_argument("argv", nargs="+", help="-- ile ayrılmış tezgah komutu")

    s = k.add_parser("degerlendir", help="bulgunun rafını silmeden değiştir (gerekçeli yeni kayıt)")
    s.add_argument("ad")
    s.add_argument("no", type=int, help="bulgu numarası")
    s.add_argument("--raf", required=True, help=" · ".join(RAFLAR))
    s.add_argument("--gerekce", required=True)
    s.add_argument("--eksen", action="append", help="eksen etiketi de değişiyorsa (boyut=değer)")

    s = k.add_parser("sonuc", help="iki eksenli sonuç (bulgularla tutarlı olmalı)")
    s.add_argument("ad")
    s.add_argument("--mantiksal-durum", required=True, help=" · ".join(MANTIKSAL_DURUM))
    s.add_argument("--delil-derecesi", required=True, help=" · ".join(DELIL_DERECESI))
    s.add_argument("--gerekce", required=True)
    s.add_argument("--kapsam", help="'Destekleniyor' için zorunlu: desteklenen kapsam")

    s = k.add_parser("goster", help="raporu üret ve göster")
    s.add_argument("ad")
    s = k.add_parser("denetle", help="zincir, sürüm sha256, sorgu çıktıları ve sonuç tutarlılığı")
    s.add_argument("ad")

    p.set_defaults(islev=lambda kor, n: _komut(n), korpus_gerekmez=True)
