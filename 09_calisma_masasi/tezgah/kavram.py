"""Kavram dosyası işlemleri (Aşama 2b).

Dosya: kavramlar/<ad>/kavram.md  +  kavramlar/<ad>/oneriler.json

Düzen 07_analyses/README.md'deki standart analiz düzenidir. Kurallar:
- Sayım bölümleri elle yazılmaz: sorgu blokları `python -m tezgah` komutunu çalıştırıp çıktısını
  kayıt satırıyla birlikte gömer; `kavram yenile` blokları yeniden üretir, `kavram denetle`
  elle değişmiş ya da eskimiş blokları ve sorgu dışında yazılmış sayıları bildirir.
- Her bölüm kayıt bloğuyla biter (CLAUDE.md §8).
- Anlam önerisinde iç-tanım, falsifikasyon (+ fiilen bulunan ayetler), muhalif okumanın en güçlü
  hâli, dışarıda bırakılan örneklem ve iki eksenli sonuç zorunludur. Öneriler yalnız eklenir;
  düzeltme yeni öneri olarak açılır, eskisi silinmez.
- Meal kavram dosyasına gömülmez (delil değil; lisansı doğrulanmadı, depo herkese açık).
"""

from __future__ import annotations

import contextlib
import io
import json
import re
from datetime import date
from pathlib import Path

MASA = Path(__file__).resolve().parents[1]
KAVRAMLAR = MASA / "kavramlar"

BOLUMLER: tuple[tuple[str, str], ...] = (
    ("soru", "1. Kısa tanım ve araştırma sorusu"),
    ("asama1", "2. Aşama 1 — kök, morfoloji, biçimler ve sayımlar"),
    ("asama2", "3. Aşama 2 — sentaks ve kullanım kalıpları"),
    ("asama3", "4. Aşama 3 — Kur'an içi bağlam ağı ve dağılım"),
    ("kritik", "5. Kritik ayetler"),
    ("karsi", "6. Karşı örnekler / falsifikasyon"),
    ("sami", "7. Sâmî karşılaştırma (isteğe bağlı — hipotez / ikincil, delil değil)"),
    ("sentez", "8. Sentez ve anlam önerileri"),
    ("kart", "9. Kavram kartı"),
)
BOLUM_ADLARI = dict(BOLUMLER)

MANTIKSAL_DURUM = ("Destekleniyor", "Yalnız uyumlu", "Destek gösterilemedi", "Belirsiz", "Çelişiyor")
DELIL_DERECESI = ("Sağlam", "Muhtemel", "Spekülatif")

IZINLI_SORGULAR = {"sayim", "kok", "lemma", "kokler", "dagilim", "etiket", "birlikte", "kalip",
                   "okunus", "ayet", "denetim"}

SORGU_RE = re.compile(r"<!-- tezgah:sorgu (\[.*?\]) -->\n(.*?)<!-- /tezgah:sorgu -->\n?", re.S)
URETILEN_RE = re.compile(r"<!-- tezgah:(oneriler|kart-ozet|bolum-kaydi) -->\n(.*?)<!-- /tezgah:\1 -->\n?", re.S)
BOLUM_RE = re.compile(r"<!-- tezgah:bolum (\w+) -->\n")


class KavramHatasi(Exception):
    pass


def _tr_anahtar(metin: str) -> str:
    return " ".join(metin.translate(str.maketrans("ıİşŞçÇğĞöÖüÜ", "iissccggoouu")).lower().split())


def _secenek(deger: str, secenekler: tuple[str, ...], ad: str) -> str:
    for s in secenekler:
        if _tr_anahtar(s) == _tr_anahtar(deger):
            return s
    raise KavramHatasi(f"{ad} şunlardan biri olmalı: {' · '.join(secenekler)} (verilen: {deger!r})")


# --- dosya yolları ------------------------------------------------------------

def _dizin(ad: str) -> Path:
    if not re.fullmatch(r"[\w-]+", ad):
        raise KavramHatasi(f"Kavram adı yalnız harf, rakam, _ ve - içerebilir: {ad!r}")
    if ad == "tezler":
        raise KavramHatasi("'tezler' adı tez kayıtlarına ayrılmıştır (kavramlar/tezler/).")
    return KAVRAMLAR / ad


def _goreli(yol: Path) -> str:
    try:
        return str(yol.relative_to(MASA))
    except ValueError:
        return str(yol)


def _dosya(ad: str) -> Path:
    return _dizin(ad) / "kavram.md"


def _oneriler_yolu(ad: str) -> Path:
    return _dizin(ad) / "oneriler.json"


# --- sorgu çalıştırma -----------------------------------------------------------

def sorgu_calistir(argv: list[str]) -> str:
    """tezgah komutunu süreç içinde çalıştırır; çıktıyı (kayıt bloğu dahil) döndürür."""
    if not argv or argv[0] not in IZINLI_SORGULAR:
        raise KavramHatasi(f"Kavram dosyasına gömülebilen sorgular: {', '.join(sorted(IZINLI_SORGULAR))}")
    if "--meal" in argv:
        raise KavramHatasi("Meal kavram dosyasına gömülmez (delil değil; lisansı doğrulanmadı, depo açık).")
    if "--arapca" in argv:
        raise KavramHatasi("Gömülü sorguda --arapca kullanılmaz (sunum: Latin harfli okunuş, §2.8).")
    from .__main__ import main
    tampon = io.StringIO()
    try:
        with contextlib.redirect_stdout(tampon), contextlib.redirect_stderr(tampon):
            kod = main(list(argv))
    except SystemExit as e:
        raise KavramHatasi(f"Geçersiz sorgu: {' '.join(argv)}\n{tampon.getvalue()}") from e
    if kod == 2:
        raise KavramHatasi("Sorgu çalıştırılmadı:\n" + tampon.getvalue())
    return tampon.getvalue()


def _sorgu_blogu(argv: list[str], cikti: str) -> str:
    return (f"<!-- tezgah:sorgu {json.dumps(argv, ensure_ascii=False)} -->\n"
            f"```text\n{cikti.rstrip()}\n```\n<!-- /tezgah:sorgu -->\n")


def _kayit_alanlari(cikti: str) -> dict[str, str]:
    alanlar = {}
    for satir in cikti.splitlines():
        for ad in ("Kaynak", "Sayım birimi", "Veri izi", "Durum"):
            if satir.startswith(ad) and ":" in satir:
                alanlar[ad] = satir.split(":", 1)[1].strip()
    return alanlar


# --- üretilen bloklar -------------------------------------------------------------

def _uretilen(ad: str, govde: str) -> str:
    return f"<!-- tezgah:{ad} -->\n{govde.rstrip()}\n<!-- /tezgah:{ad} -->\n"


def _bolum_kaydi(sorgu_ciktilari: list[str], oneri_var: bool = False) -> str:
    if not sorgu_ciktilari:
        durum = "çalıştırılmadı (bu bölümde sorgu yok; sayı elle yazılmaz)"
        kaynak = "oneriler.json (kullanıcı önerileri)" if oneri_var else "—"
        satirlar = [f"Kaynak      : {kaynak}", "Sayım birimi: —", "Sorgu       : —",
                    "Veri izi    : —", f"Durum       : {durum}"]
    else:
        def birlesim(ad: str) -> str:
            degerler: list[str] = []
            for c in sorgu_ciktilari:
                for d in _kayit_alanlari(c).get(ad, "—").split(" | "):
                    if d not in degerler:
                        degerler.append(d)
            return " | ".join(degerler)
        durumlar = {_kayit_alanlari(c).get("Durum", "") for c in sorgu_ciktilari}
        satirlar = [f"Kaynak      : {birlesim('Kaynak')}", f"Sayım birimi: {birlesim('Sayım birimi')}",
                    f"Sorgu       : {len(sorgu_ciktilari)} sorgu (yukarıda, her biri kendi kaydıyla)",
                    f"Veri izi    : {birlesim('Veri izi')}",
                    f"Durum       : {'çalıştırıldı' if durumlar == {'çalıştırıldı'} else 'kısmen çalıştırıldı'}"]
    return _uretilen("bolum-kaydi", "Bölüm kaydı:\n```text\n" + "\n".join(satirlar) + "\n```")


def _oneri_md(n: int, o: dict) -> str:
    bulunan = ", ".join(o["bulunan_ayetler"]) if o["bulunan_ayetler"] else f"yok — tarama: {o['bulunan_sorgu']}"
    return "\n".join([
        f"#### Öneri {n} — {o['tarih']}",
        f"- **Anlam önerisi:** {o['anlam']}",
        f"- **Mantıksal durum:** {o['mantiksal_durum']} · **Delil derecesi:** {o['delil_derecesi']}",
        f"- **İç-tanım (metin terimi kendi içinde açıyor mu):** {o['ic_tanim']}",
        f"- **Falsifikasyon (hangi ayet çürütürdü):** {o['falsifikasyon']}",
        f"  - Fiilen bulunan ayetler: {bulunan}",
        f"- **Muhalif okumanın en güçlü hâli:** {o['muhalif']}",
        f"- **Örneklem — kurulduğu kullanımlar:** {o['kurulan_orneklem']}",
        f"- **Örneklem — sonradan uygulandığı kullanımlar:** {o['uygulanan_orneklem']}",
    ])


def _oneriler_blogu(oneriler: list[dict]) -> str:
    if not oneriler:
        govde = "_Henüz anlam önerisi yok (python -m tezgah kavram oneri ...)._"
    else:
        govde = "### Anlam önerileri (oneriler.json'dan üretilir; eski öneriler silinmez)\n\n" + \
                "\n\n".join(_oneri_md(i, o) for i, o in enumerate(oneriler, 1))
    return _uretilen("oneriler", govde)


def _kart_ozeti(oneriler: list[dict]) -> str:
    if not oneriler:
        return _uretilen("kart-ozet", "_Kart özeti son anlam önerisinden üretilir; henüz öneri yok._")
    o = oneriler[-1]
    return _uretilen("kart-ozet", "\n".join([
        f"**Son öneri (Öneri {len(oneriler)}):** {o['anlam']}",
        f"**Mantıksal durum:** {o['mantiksal_durum']} · **Delil derecesi:** {o['delil_derecesi']}",
    ]))


# --- dosya kurma / yenileme ----------------------------------------------------

def _oneriler(ad: str) -> list[dict]:
    yol = _oneriler_yolu(ad)
    return json.loads(yol.read_text(encoding="utf-8")) if yol.exists() else []


def _bolumlere_ayir(metin: str) -> tuple[str, list[tuple[str, str]]]:
    parcalar = BOLUM_RE.split(metin)
    bas, geri = parcalar[0], parcalar[1:]
    return bas, [(geri[i], geri[i + 1]) for i in range(0, len(geri), 2)]


def _bolum_yenile(anahtar: str, govde: str, oneriler: list[dict], calistir: bool) -> str:
    ciktilar: list[str] = []

    def sorgu(m: re.Match) -> str:
        argv = json.loads(m.group(1))
        cikti = sorgu_calistir(argv) if calistir else m.group(2).split("```text\n", 1)[1].rsplit("\n```", 1)[0]
        ciktilar.append(cikti)
        return _sorgu_blogu(argv, cikti)

    govde = SORGU_RE.sub(sorgu, govde)

    def uretilen(m: re.Match) -> str:
        if m.group(1) == "oneriler":
            return _oneriler_blogu(oneriler)
        if m.group(1) == "kart-ozet":
            return _kart_ozeti(oneriler)
        return ""  # bölüm kaydı sona yeniden eklenir

    govde = URETILEN_RE.sub(uretilen, govde).rstrip() + "\n\n"
    return govde + _bolum_kaydi(ciktilar, oneri_var=anahtar == "sentez" and bool(oneriler)) + "\n"


def _yaz(ad: str, metin: str, calistir: bool = True) -> str:
    oneriler = _oneriler(ad)
    bas, bolumler = _bolumlere_ayir(metin)
    anahtarlar = [a for a, _ in bolumler]
    eksik = [a for a, _ in BOLUMLER if a not in anahtarlar]
    if eksik:
        raise KavramHatasi(f"Kavram dosyasında eksik bölüm işaretleri: {', '.join(eksik)}")
    yeni = bas + "".join(f"<!-- tezgah:bolum {a} -->\n" + _bolum_yenile(a, g, oneriler, calistir)
                         for a, g in bolumler)
    _dosya(ad).write_text(yeni, encoding="utf-8")
    return yeni


def ac(ad: str, soru: str, kokler: list[str]) -> Path:
    from .tara import kok_coz
    from . import veri
    dizin = _dizin(ad)
    if dizin.exists():
        raise KavramHatasi(f"Kavram zaten var: {_goreli(dizin)}")
    if not soru.strip():
        raise KavramHatasi("Araştırma sorusu boş olamaz.")
    if not kokler:
        raise KavramHatasi("En az bir --kok verilmeli.")
    kor = veri.korpus()
    cozumler = [kok_coz(kor, k) for k in kokler]   # Latin giriş burada reddedilir
    dizin.mkdir(parents=True)
    _oneriler_yolu(ad).write_text("[]\n", encoding="utf-8")
    parca = [f"# Kavram: {ad}\n\n",
             "_Çalışma dosyası (kavramlar/). Sorgu blokları `python -m tezgah kavram yenile` ile yeniden "
             "üretilir; elle değiştirilmez. Bölüm kayıtları otomatiktir._\n\n"]
    for anahtar, baslik in BOLUMLER:
        parca.append(f"<!-- tezgah:bolum {anahtar} -->\n## {baslik}\n\n")
        if anahtar == "soru":
            parca.append(f"**Araştırma sorusu:** {' '.join(soru.split())}\n\n"
                         f"**Kökler:** {', '.join(f'{c.bw} ({c.latin})' for c in cozumler)}\n\n")
        elif anahtar == "asama1":
            for c in cozumler:
                for argv in (["sayim", "--kok", c.bw], ["dagilim", "--kok", c.bw, "--gore", "tur"],
                             ["dagilim", "--kok", c.bw, "--gore", "bab"],
                             ["dagilim", "--kok", c.bw, "--gore", "sure"]):
                    parca.append(_sorgu_blogu(argv, "") + "\n")
        elif anahtar == "sami":
            parca.append("_Bu bölümdeki her bilgi hipotezdir; korpus bulgusunun yerine geçmez._\n\n")
        elif anahtar == "sentez":
            parca.append(_oneriler_blogu([]) + "\n")
        elif anahtar == "kart":
            parca.append(_kart_ozeti([]) + "\n")
        parca.append(_bolum_kaydi([]))
    _yaz(ad, "".join(parca))
    return _dosya(ad)


def _metin(ad: str) -> str:
    yol = _dosya(ad)
    if not yol.exists():
        raise KavramHatasi(f"Kavram yok: {ad} (önce: python -m tezgah kavram ac {ad} ...)")
    return yol.read_text(encoding="utf-8")


def sorgu_ekle(ad: str, bolum: str, argv: list[str]) -> None:
    if bolum not in BOLUM_ADLARI:
        raise KavramHatasi(f"Bölüm şunlardan biri olmalı: {', '.join(BOLUM_ADLARI)}")
    cikti = sorgu_calistir(argv)
    metin = _metin(ad)
    bas, bolumler = _bolumlere_ayir(metin)
    yeni = []
    for a, g in bolumler:
        if a == bolum:
            g = URETILEN_RE.sub(lambda m: "" if m.group(1) == "bolum-kaydi" else m.group(0), g).rstrip()
            g += "\n\n" + _sorgu_blogu(argv, cikti) + "\n"
        yeni.append(f"<!-- tezgah:bolum {a} -->\n" + g)
    _yaz(ad, bas + "".join(yeni), calistir=False)


def oneri_ekle(ad: str, **alan: str) -> dict:
    from . import okunus
    _metin(ad)
    zorunlu = {
        "anlam": "anlam önerisi", "ic_tanim": "iç-tanım", "falsifikasyon": "falsifikasyon",
        "muhalif": "muhalif okumanın en güçlü hâli", "kurulan_orneklem": "kurulduğu örneklem",
        "uygulanan_orneklem": "sonradan uygulandığı örneklem",
        "mantiksal_durum": "mantıksal durum", "delil_derecesi": "delil derecesi",
    }
    for k, ad_ in zorunlu.items():
        if not (alan.get(k) or "").strip() or not re.search(r"\w", alan[k]):
            raise KavramHatasi(f"Boş bırakılamaz: {ad_} (--{k.replace('_', '-')})")
    bulunan_ham = (alan.get("bulunan_ayetler") or "").strip()
    if not bulunan_ham:
        raise KavramHatasi("Boş bırakılamaz: fiilen bulunan ayetler (--bulunan-ayetler; bulunamadıysa 'yok')")
    bulunan: list[str] = []
    if _tr_anahtar(bulunan_ham) == "yok":
        if not (alan.get("bulunan_sorgu") or "").strip():
            raise KavramHatasi("Bulunan ayet 'yok' ise hangi taramayla bulunamadığını yazın: "
                               "--bulunan-sorgu (boş çıktı yokluk delili değildir)")
    else:
        for ref in re.split(r"[,\s]+", bulunan_ham):
            anahtar = okunus._ayet_ayristir(ref)
            bulunan.append(f"{anahtar[0]}:{anahtar[1]}")
    kayit = {
        "tarih": date.today().isoformat(),
        "anlam": " ".join(alan["anlam"].split()),
        "mantiksal_durum": _secenek(alan["mantiksal_durum"], MANTIKSAL_DURUM, "Mantıksal durum"),
        "delil_derecesi": _secenek(alan["delil_derecesi"], DELIL_DERECESI, "Delil derecesi"),
        "ic_tanim": " ".join(alan["ic_tanim"].split()),
        "falsifikasyon": " ".join(alan["falsifikasyon"].split()),
        "bulunan_ayetler": bulunan,
        "bulunan_sorgu": " ".join((alan.get("bulunan_sorgu") or "").split()),
        "muhalif": " ".join(alan["muhalif"].split()),
        "kurulan_orneklem": " ".join(alan["kurulan_orneklem"].split()),
        "uygulanan_orneklem": " ".join(alan["uygulanan_orneklem"].split()),
    }
    oneriler = _oneriler(ad) + [kayit]
    _oneriler_yolu(ad).write_text(json.dumps(oneriler, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _yaz(ad, _metin(ad), calistir=False)
    return kayit


def yenile(ad: str) -> None:
    _yaz(ad, _metin(ad), calistir=True)


SAYI_RE = re.compile(r"(?<![\w:.\-/])\d{1,3}(?:\.\d{3})+(?![\w:])|(?<![\w:.\-/])\d{2,}(?![\w:.])")


def denetle(ad: str) -> tuple[list[str], list[str]]:
    """(hatalar, uyarılar). Hata: eskimiş/elle değişmiş blok, eksik bölüm, geçersiz öneri."""
    metin = _metin(ad)
    hatalar: list[str] = []
    uyarilar: list[str] = []
    bas, bolumler = _bolumlere_ayir(metin)
    anahtarlar = [a for a, _ in bolumler]
    for a, _ in BOLUMLER:
        if a not in anahtarlar:
            hatalar.append(f"eksik bölüm: {a}")
    oneriler = _oneriler(ad)
    for a, govde in bolumler:
        for m in SORGU_RE.finditer(govde):
            argv = json.loads(m.group(1))
            kayitli = m.group(2)
            taze = _sorgu_blogu(argv, sorgu_calistir(argv)).split("\n", 1)[1].rsplit("<!-- /tezgah:sorgu -->", 1)[0]
            if kayitli != taze:
                hatalar.append(f"[{a}] sorgu bloğu güncel çıktıyla aynı değil (elle değişmiş ya da veri değişmiş): "
                               f"python -m tezgah {' '.join(argv)}")
        for m in URETILEN_RE.finditer(govde):
            taze = {"oneriler": _oneriler_blogu(oneriler), "kart-ozet": _kart_ozeti(oneriler)}.get(m.group(1))
            if taze is not None and m.group(0).rstrip("\n") != taze.rstrip("\n"):
                hatalar.append(f"[{a}] üretilen blok ({m.group(1)}) oneriler.json ile uyuşmuyor")
        if "<!-- tezgah:bolum-kaydi -->" not in govde:
            hatalar.append(f"[{a}] bölüm kaydı yok")
        elle = URETILEN_RE.sub("", SORGU_RE.sub("", govde))
        elle = re.sub(r"^#+ .*$", "", elle, flags=re.M)                  # başlık numaraları
        elle = re.sub(r"\b\d+:\d+(?::\d+)*\b", "", elle)                 # ayet/konum referansları
        for s in SAYI_RE.findall(elle):
            uyarilar.append(f"[{a}] sorgu dışında sayı: {s} (sayımlar sorgudan gömülmeli)")
        if a in {"sentez", "kart"} and any(o["mantiksal_durum"] == "Yalnız uyumlu" for o in oneriler):
            if re.search(r"desteklen", elle, re.I):
                uyarilar.append(f"[{a}] 'Yalnız uyumlu' öneri varken metinde 'destekleniyor' geçiyor")
    for i, o in enumerate(oneriler, 1):
        if o.get("mantiksal_durum") not in MANTIKSAL_DURUM or o.get("delil_derecesi") not in DELIL_DERECESI:
            hatalar.append(f"öneri {i}: geçersiz sonuç ekseni")
    return hatalar, uyarilar


def liste() -> list[str]:
    """Kavram dosyası olan adlar (kavramlar/<ad>/kavram.md)."""
    if not KAVRAMLAR.exists():
        return []
    return sorted(d.name for d in KAVRAMLAR.iterdir() if d.is_dir() and d.name != "tezler" and (d / "kavram.md").exists())


# --- komut satırı -----------------------------------------------------------------

def _komut(n):
    from . import veri
    from .tara import GirdiHatasi, Sonuc
    try:
        if n.kavram_komut == "liste":
            adlar = liste()
            satirlar = [f"Kavram dosyaları ({_goreli(KAVRAMLAR)}): {len(adlar)}", *[f"  {a}" for a in adlar]]
            return Sonuc(satirlar, [], {"kavramlar": adlar}, kaynak="kavram dosyası", veri_izi="—")
        if n.kavram_komut == "goster":
            metin = _metin(n.ad)
            satirlar = [f"Kavram dosyası: {_goreli(_dosya(n.ad))} (olduğu gibi; gömülü sorgular kendi kayıt "
                        "bloklarıyla)", "", *metin.splitlines()]
            return Sonuc(satirlar, [], {"ad": n.ad}, kaynak="kavram dosyası",
                         veri_izi=veri.sha256(_dosya(n.ad))[:12])
        if n.kavram_komut == "ac":
            yol = ac(n.ad, n.soru, n.kok)
            satirlar = [f"Kavram dosyası açıldı: {_goreli(yol)}",
                        "Aşama 1 sorguları gömüldü (sayim, dagilim tur/bab/sure)."]
        elif n.kavram_komut == "sorgu":
            argv = n.argv[1:] if n.argv[:1] == ["--"] else n.argv
            sorgu_ekle(n.ad, n.bolum, argv)
            satirlar = [f"Sorgu gömüldü [{n.bolum}]: python -m tezgah {' '.join(argv)}"]
        elif n.kavram_komut == "ayet":
            sorgu_ekle(n.ad, n.bolum, ["ayet", n.ayet])
            satirlar = [f"Ayet görünümü gömüldü [{n.bolum}]: {n.ayet} "
                        "(çalışma çevirisi: python -m tezgah ceviri; sonra kavram yenile)"]
        elif n.kavram_komut == "oneri":
            k = oneri_ekle(n.ad, anlam=n.anlam, ic_tanim=n.ic_tanim, falsifikasyon=n.falsifikasyon,
                           bulunan_ayetler=n.bulunan_ayetler, bulunan_sorgu=n.bulunan_sorgu,
                           muhalif=n.muhalif, kurulan_orneklem=n.kurulan_orneklem,
                           uygulanan_orneklem=n.uygulanan_orneklem,
                           mantiksal_durum=n.mantiksal_durum, delil_derecesi=n.delil_derecesi)
            satirlar = [f"Öneri eklendi ({k['mantiksal_durum']} · {k['delil_derecesi']})."]
        elif n.kavram_komut == "yenile":
            yenile(n.ad)
            satirlar = [f"Yenilendi: {_goreli(_dosya(n.ad))}"]
        else:
            hatalar, uyarilar = denetle(n.ad)
            satirlar = [f"Kavram denetimi: {n.ad} — {len(hatalar)} hata, {len(uyarilar)} uyarı",
                        *[f"  HATA: {h}" for h in hatalar], *[f"  UYARI: {u}" for u in uyarilar]]
            return Sonuc(satirlar, [], {"hata": len(hatalar), "uyari": len(uyarilar)},
                         basarili=not hatalar, kaynak="kavram dosyası", veri_izi="—")
    except KavramHatasi as e:
        raise GirdiHatasi(str(e)) from e
    return Sonuc(satirlar, [], {}, kaynak="kavram dosyası", veri_izi="—")


def parser_ekle(alt) -> None:
    p = alt.add_parser("kavram", help="kavram dosyası: liste / goster / ac / sorgu / ayet / oneri / yenile / denetle")
    k = p.add_subparsers(dest="kavram_komut", required=True, metavar="işlem")

    k.add_parser("liste", help="kavram dosyalarını listele")
    s = k.add_parser("goster", help="kavram dosyasını olduğu gibi göster")
    s.add_argument("ad")

    s = k.add_parser("ac", help="yeni kavram dosyası (Aşama 1 sorguları gömülür)")
    s.add_argument("ad")
    s.add_argument("--soru", required=True, help="araştırma sorusu")
    s.add_argument("--kok", action="append", required=True, help="Arapça veya Buckwalter; birden çok verilebilir")

    s = k.add_parser("sorgu", help="bir bölüme sorgu göm: kavram sorgu AD --bolum asama2 -- kalip \"...\"")
    s.add_argument("ad")
    s.add_argument("--bolum", required=True, choices=list(BOLUM_ADLARI))
    s.add_argument("argv", nargs="+", help="tezgah komutu (-- ile ayırın)")

    s = k.add_parser("ayet", help="ayet görünümünü göm (meal gömülmez)")
    s.add_argument("ad")
    s.add_argument("ayet")
    s.add_argument("--bolum", default="kritik", choices=list(BOLUM_ADLARI))

    s = k.add_parser("oneri", help="anlam önerisi ekle (bütün alanlar zorunlu)")
    s.add_argument("ad")
    s.add_argument("--anlam", required=True)
    s.add_argument("--ic-tanim", required=True, help="metin terimi kendi içinde açıyor mu")
    s.add_argument("--falsifikasyon", required=True, help="bu öneri doğru olsaydı hangi ayet onu çürütürdü")
    s.add_argument("--bulunan-ayetler", required=True, help="fiilen bulunan ayetler (ör. 2:3,5:6) ya da 'yok'")
    s.add_argument("--bulunan-sorgu", default="", help="'yok' ise hangi taramayla bulunamadığı")
    s.add_argument("--muhalif", required=True, help="muhalif okumanın en güçlü hâli")
    s.add_argument("--kurulan-orneklem", required=True, help="öneri hangi kullanımlardan kuruldu")
    s.add_argument("--uygulanan-orneklem", required=True, help="hangilerine sonradan uygulandı")
    s.add_argument("--mantiksal-durum", required=True, help=" · ".join(MANTIKSAL_DURUM))
    s.add_argument("--delil-derecesi", required=True, help=" · ".join(DELIL_DERECESI))

    s = k.add_parser("yenile", help="gömülü sorguları yeniden çalıştır, üretilen blokları yenile")
    s.add_argument("ad")
    s = k.add_parser("denetle", help="eskimiş/elle değişmiş blokları ve sorgu dışı sayıları bildir")
    s.add_argument("ad")

    p.set_defaults(islev=lambda kor, n: _komut(n), korpus_gerekmez=True)
