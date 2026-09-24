"""Yerel web arayüzü (Aşama 6): python -m tezgah arayuz

Yalnız Python standart kütüphanesi (http.server). Arayüzün kendi sorgu mantığı yoktur. Her form bir
`python -m tezgah ...` komut satırına çevrilir ve aynı paketin `main(argv)` işleviyle çalıştırılır.
Çıktı süzülmeden gösterilir: uyarılar (ikiz kök, iki korpus farkı), "[hipotez]" etiketleri ve kayıt
bloğu gizlenmez. Kayıt bloğu sonuç panelinin altında sabit durur. Meal kutusu varsayılan olarak
kapalıdır.

Güvenlik: yalnız 127.0.0.1'e bağlanır; Host başlığı denetlenir (DNS yeniden bağlama); her POST
oturum belirteci ister (başka sitenin formu yerel dosyalara yazamaz). Tek iş parçacıklıdır, çünkü
çıktı sys.stdout yönlendirmesiyle yakalanır.
"""

from __future__ import annotations

import contextlib
import html
import io
import secrets
import shlex
import sys
import traceback
import webbrowser
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlsplit

from . import kavram, okuma, tez
from .kayit import CALISTIRILMADI, Kayit, komut_metni

AYRAC = "-" * 60
VARSAYILAN_PORT = 8765
# Arayüzden çalıştırılabilen üst komutlar. test ve kur burada yok: komut satırından çalıştırılır.
IZINLI = {"denetim", "kokler", "kok", "lemma", "sayim", "dagilim", "etiket", "birlikte", "kalip",
          "okunus", "ayet", "ceviri", "lane", "sami", "kavram", "tez"}


# --- form tanımları (yalnız argv kurmak için; anlam denetimi paketin kendisindedir) --------------

@dataclass
class Alan:
    ad: str                 # konumsal argüman adı ya da --bayrak
    tur: str                # poz | poz_coklu | deger | coklu | tekrar | bayrak | secim | komut
    etiket: str
    varsayilan: str = ""
    zorunlu: bool = False
    secenekler: tuple[str, ...] = ()
    uzun: bool = False      # çok satırlı metin kutusu


@dataclass
class Form:
    kimlik: str
    baslik: str
    onek: list[str]
    alanlar: list[Alan] = field(default_factory=list)
    aciklama: str = ""


def _k(ad="kok", etiket="Kök (Arapça ya da Buckwalter; ör. Slw)"):
    return Alan(ad, "poz", etiket, zorunlu=True)


def _limit(v="50"):
    return Alan("--limit", "deger", "Limit (0 = tümü)", v)


def _ad(etiket="Ad"):
    return Alan("ad", "poz", etiket, zorunlu=True)


def ekranlar() -> dict[str, tuple[str, list[Form]]]:
    bolumler = tuple(kavram.BOLUM_ADLARI)
    md, dd = kavram.MANTIKSAL_DURUM, kavram.DELIL_DERECESI
    return {
        "tarama": ("Tarama", [
            Form("kok", "Kök geçişleri", ["kok"], [_k(), _limit(),
                 Alan("--capraz", "bayrak", "İki korpus yan yana (--capraz; quran-morphology, çapraz kontrol)")],
                 "Birim: kelime konumu."),
            Form("sayim", "Sayım", ["sayim"], [
                Alan("--kok", "deger", "Kök"), Alan("--lemma", "deger", "Lemma"),
                Alan("--etiket", "coklu", "Etiket(ler) — boşlukla, tam eşleşme (ör. (IV) PRON:3MP)"),
                Alan("--alt-dize", "bayrak", "Alt-dize eşleşmesi (uyarı basılır)"),
                Alan("--capraz", "bayrak", "--kok ile iki korpus yan yana (--capraz)")],
                "Hepsi boşsa korpus toplamı."),
            Form("dagilim", "Dağılım", ["dagilim"], [
                Alan("--kok", "deger", "Kök"), Alan("--lemma", "deger", "Lemma (kök yerine)"),
                Alan("--gore", "secim", "Göre", "tur", True, ("tur", "lemma", "bab", "iyelik", "sure"))]),
            Form("lemma", "Lemma geçişleri", ["lemma"], [Alan("lemma", "poz", "Lemma (QAC)", zorunlu=True), _limit()]),
            Form("etiket", "Etiket (segment)", ["etiket"], [
                Alan("etiketler", "poz_coklu", "Etiket(ler) — boşlukla, aynı segmentte", zorunlu=True),
                Alan("--alt-dize", "bayrak", "Alt-dize eşleşmesi (uyarı basılır)"), _limit()]),
            Form("birlikte", "Ortak geçiş", ["birlikte"], [
                _k("kok_a", "Kök A"), _k("kok_b", "Kök B"),
                Alan("--pencere", "deger", "± kelime konumu penceresi (boş = aynı ayet)"), _limit()]),
            Form("kalip", "Kalıp (ardışık segment)", ["kalip"], [
                Alan("desen", "poz", "Desen (ör. ROOT:Amn&POS:V PRON:3MP)", zorunlu=True),
                Alan("--kelime-ici", "bayrak", "Yalnız aynı kelime konumu içinde"),
                Alan("--alt-dize", "bayrak", "Alt-dize eşleşmesi (uyarı basılır)"), _limit()]),
            Form("kokler", "Kök envanteri", ["kokler"], [
                _limit("30"), Alan("--siralama", "secim", "Sıralama", "siklik", False, ("siklik", "alfabe"))]),
            Form("denetim", "Kurulum denetimi", ["denetim"], []),
        ]),
        "ayet": ("Ayet okuma", [
            Form("ayet", "Ayet görünümü", ["ayet"], [
                Alan("ayet", "poz", "Sûre:ayet (ör. 2:3)", zorunlu=True),
                Alan("--meal", "bayrak", f"Meal göster ({okuma.MEAL_ETIKETI}) — varsayılan kapalı"),
                Alan("--arapca", "bayrak", "Denetim için Tanzil kelimesi")],
                "Okunuş + kelime çözümlemesi (QAC) + çalışma çevirisi."),
            Form("okunus", "Okunuş", ["okunus"], [
                Alan("ayetler", "poz_coklu", "Ayetler (boşlukla; ör. 2:3 30:30)"),
                Alan("--arapca", "bayrak", "Denetim için Tanzil kelimesi"),
                Alan("--durak", "bayrak", "Sekte dışı durak işaretleri (geleneksel — yorum içerebilir)"),
                Alan("--mukattaa", "bayrak", "Hurûf-ı mukattaa taraması (ayet listesi yok sayılır)")]),
            Form("ceviri_goster", "Çalışma çevirisi — göster", ["ceviri"], [Alan("ayet", "poz", "Sûre:ayet", zorunlu=True)]),
            Form("ceviri_ekle", "Çalışma çevirisi — yeni sürüm ekle", ["ceviri"], [
                Alan("ayet", "poz", "Sûre:ayet", zorunlu=True),
                Alan("metin", "poz", "Çeviri (kullanıcının yorumu)", zorunlu=True, uzun=True)]),
        ]),
        "kavram": ("Kavram dosyası", [
            Form("kavram_liste", "Kavram dosyaları", ["kavram", "liste"], []),
            Form("kavram_goster", "Göster", ["kavram", "goster"], [_ad()]),
            Form("kavram_denetle", "Denetle", ["kavram", "denetle"], [_ad()]),
            Form("kavram_yenile", "Gömülü sorguları yenile", ["kavram", "yenile"], [_ad()]),
            Form("kavram_ac", "Yeni kavram dosyası", ["kavram", "ac"], [
                _ad(), Alan("--soru", "deger", "Araştırma sorusu", zorunlu=True, uzun=True),
                Alan("--kok", "tekrar", "Kök(ler) — her satıra bir kök", zorunlu=True, uzun=True)]),
            Form("kavram_sorgu", "Bölüme sorgu göm", ["kavram", "sorgu"], [
                _ad(), Alan("--bolum", "secim", "Bölüm", bolumler[0], True, bolumler),
                Alan("argv", "komut", "tezgah komutu (ör. kalip \"ROOT:Slw&POS:V\")", zorunlu=True)]),
            Form("kavram_ayet", "Ayet göm", ["kavram", "ayet"], [
                _ad(), Alan("ayet", "poz", "Sûre:ayet", zorunlu=True),
                Alan("--bolum", "secim", "Bölüm", "kritik", False, bolumler)]),
            Form("kavram_oneri", "Anlam önerisi (bütün alanlar zorunlu)", ["kavram", "oneri"], [
                _ad(), Alan("--anlam", "deger", "Anlam önerisi", zorunlu=True, uzun=True),
                Alan("--ic-tanim", "deger", "İç-tanım var mı (metin terimi kendi içinde açıyor mu)", zorunlu=True, uzun=True),
                Alan("--falsifikasyon", "deger", "Falsifikasyon: hangi ayet çürütürdü", zorunlu=True, uzun=True),
                Alan("--bulunan-ayetler", "deger", "Fiilen bulunan ayetler (ör. 2:3,5:6) ya da 'yok'", zorunlu=True),
                Alan("--bulunan-sorgu", "deger", "'yok' ise hangi taramayla bulunamadığı"),
                Alan("--muhalif", "deger", "Muhalif okumanın en güçlü hâli", zorunlu=True, uzun=True),
                Alan("--kurulan-orneklem", "deger", "Öneri hangi kullanımlardan kuruldu", zorunlu=True, uzun=True),
                Alan("--uygulanan-orneklem", "deger", "Hangilerine sonradan uygulandı", zorunlu=True, uzun=True),
                Alan("--mantiksal-durum", "secim", "Mantıksal durum", md[0], True, md),
                Alan("--delil-derecesi", "secim", "Delil derecesi", dd[0], True, dd)]),
        ]),
        "tez": ("Tez sınama", [
            Form("tez_liste", "Tez kayıtları", ["tez", "liste"], []),
            Form("tez_goster", "Raporu üret ve göster", ["tez", "goster"], [_ad()]),
            Form("tez_denetle", "Denetle", ["tez", "denetle"], [_ad()]),
            Form("tez_tara", "Karşı örnek havuzunu tara", ["tez", "tara"], [_ad()]),
            Form("tez_ac", "Tezi dondur (taramadan önce)", ["tez", "ac"], [
                _ad(), Alan("--tez", "deger", "Tez — tek cümle, olduğu gibi saklanır", zorunlu=True, uzun=True),
                Alan("--tanim", "tekrar", "Tanımlar — her satıra terim=tanım", zorunlu=True, uzun=True),
                Alan("--eksen", "tekrar", "Eksenler — her satıra boyut=değer", zorunlu=True, uzun=True),
                Alan("--karsi", "tekrar", "Karşı örnek havuzu — her satıra bir tezgah komutu", zorunlu=True, uzun=True),
                Alan("--havuz-notu", "deger", "Havuz notu")]),
            Form("tez_bulgu", "Bulgu ekle", ["tez", "bulgu"], [
                _ad(), Alan("--eksen", "tekrar", "Eksen — her satıra boyut=değer", zorunlu=True, uzun=True),
                Alan("--raf", "secim", "Raf", tez.RAFLAR[0], True, tez.RAFLAR),
                Alan("--aciklama", "deger", "Açıklama", zorunlu=True, uzun=True),
                Alan("--ayet", "tekrar", "Çıktıda geçmesi gereken ayet(ler) — her satıra bir", uzun=True),
                Alan("--gerekce", "deger", "Gerekçe ('farklı eksen' rafı için zorunlu)", uzun=True),
                Alan("argv", "komut", "tezgah komutu", zorunlu=True)]),
            Form("tez_degerlendir", "Bulguyu yeniden değerlendir", ["tez", "degerlendir"], [
                _ad(), Alan("no", "poz", "Bulgu no", zorunlu=True),
                Alan("--raf", "secim", "Yeni raf", tez.RAFLAR[0], True, tez.RAFLAR),
                Alan("--gerekce", "deger", "Gerekçe", zorunlu=True, uzun=True),
                Alan("--eksen", "tekrar", "Eksen de değişiyorsa — her satıra boyut=değer", uzun=True)]),
            Form("tez_sonuc", "Sonuç (iki eksen)", ["tez", "sonuc"], [
                _ad(), Alan("--mantiksal-durum", "secim", "Mantıksal durum", md[0], True, md),
                Alan("--delil-derecesi", "secim", "Delil derecesi", dd[0], True, dd),
                Alan("--gerekce", "deger", "Gerekçe", zorunlu=True, uzun=True),
                Alan("--kapsam", "deger", "Kapsam ('Destekleniyor' için zorunlu)", uzun=True)]),
            Form("tez_yeni_surum", "Yeni sürüm (eskisi silinmez)", ["tez", "yeni-surum"], [
                _ad(), Alan("--gerekce", "deger", "Gerekçe", zorunlu=True, uzun=True),
                Alan("--tez", "deger", "Yeni tez cümlesi", uzun=True),
                Alan("--tanim", "tekrar", "Tanımlar — her satıra terim=tanım", uzun=True),
                Alan("--eksen", "tekrar", "Eksenler — her satıra boyut=değer", uzun=True),
                Alan("--karsi", "tekrar", "Karşı örnek havuzu — her satıra bir komut", uzun=True)]),
        ]),
        "ikincil": ("İkincil katmanlar (hipotez)", [
            Form("lane_kok", "Lane — kök maddeleri", ["lane", "kok"], [
                _k(), Alan("--madde", "deger", "Yalnız şu madde no"), Alan("--tam", "bayrak", "Tam metin")],
                "Hipotez kaynağı, delil değil. Dairesellik ve ك-ي seyrekliği çıktıda belirtilir."),
            Form("lane_kapsam", "Lane — kapsam ölçümü", ["lane", "kapsam"], []),
            Form("lane_sigla", "Lane — kaynak kısaltmaları", ["lane", "sigla"], []),
            Form("sami_kok", "Sâmî — kognat adayları", ["sami", "kok"], [
                _k(), Alan("--tek-dil", "bayrak", "Tek dil vuruşlarını da göster (etiketli)"),
                Alan("--zayif-son", "bayrak", "Son-harf-zayıf kuralı (ölçümde gürültüyü artırıyor; varsayılan kapalı)"),
                Alan("--tam", "bayrak", "Bütün anlamlar")],
                "Kognat anlam değildir; tek dil vuruşu tek başına raporlanmaz."),
            Form("sami_gurultu", "Sâmî — gürültü tabanı", ["sami", "gurultu"], []),
            Form("sami_denklik", "Sâmî — denklik tablosu", ["sami", "denklik"], []),
            Form("sami_atif", "SEDRA atıf metni", ["sami", "atif"], []),
        ]),
    }


def form_bul(kimlik: str) -> tuple[str, Form] | None:
    for ekran, (_, formlar) in ekranlar().items():
        for f in formlar:
            if f.kimlik == kimlik:
                return ekran, f
    return None


class FormHatasi(ValueError):
    pass


def argv_kur(form: Form, degerler: dict[str, str]) -> list[str]:
    """Form değerlerinden tezgah argv'si. Yalnız sözdizimi: boş alan atlanır, zorunlu boşsa hata."""
    argv = list(form.onek)
    son: list[str] = []
    for a in form.alanlar:
        v = (degerler.get(a.ad) or "").strip()
        if a.tur == "bayrak":
            if v:
                argv.append(a.ad)
            continue
        if not v:
            if a.zorunlu:
                raise FormHatasi(f"Zorunlu alan boş: {a.etiket}")
            continue
        if a.tur == "poz":
            argv.append(v)
        elif a.tur == "poz_coklu":
            argv += v.split()
        elif a.tur in ("deger", "secim"):
            argv += [f"{a.ad}={v}"] if v.startswith("-") else [a.ad, v]   # '-' ile başlayan değer bayrak sanılmasın
        elif a.tur == "coklu":
            argv += [a.ad, *v.split()]
        elif a.tur == "tekrar":
            for satir in v.splitlines():
                if satir.strip():
                    x = satir.strip()
                    argv += [f"{a.ad}={x}"] if x.startswith("-") else [a.ad, x]
        elif a.tur == "komut":
            try:
                son = ["--", *shlex.split(v)]
            except ValueError as e:
                raise FormHatasi(f"Komut ayrıştırılamadı ({a.etiket}): {e}") from e
    return argv + son


# --- çalıştırma ----------------------------------------------------------------------

@dataclass
class Calisma:
    argv: list[str]
    kod: int
    cikti: str


def calistir(argv: list[str]) -> Calisma:
    """argv'yi paketin main() işleviyle çalıştırır; stdout ve stderr olduğu gibi döner."""
    from .__main__ import main
    if not argv or argv[0] not in IZINLI:
        return _calistirilmadi(argv, f"arayüzden çalıştırılamayan komut: {argv[:1]}")
    out, err = io.StringIO(), io.StringIO()
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            kod = main(argv)
    except SystemExit as e:        # argparse hatası: mesaj stderr'de
        kod = e.code if isinstance(e.code, int) else 2
        metin = out.getvalue() + err.getvalue()
        if AYRAC not in metin:
            return _calistirilmadi(argv, metin.strip() or "argüman hatası", kod)
        return Calisma(argv, kod, metin)
    except Exception:              # noqa: BLE001 — beklenmeyen hata da görünür kalır
        return _calistirilmadi(argv, "beklenmeyen hata:\n" + traceback.format_exc(), 2,
                               onceki=out.getvalue())
    return Calisma(argv, kod, out.getvalue() + err.getvalue())


def _calistirilmadi(argv: list[str], sebep: str, kod: int = 2, onceki: str = "") -> Calisma:
    kayit = Kayit(komut_metni(argv), kaynaklar=["—"], veri_izi="—", durum=CALISTIRILMADI, sebep="girdi hatası").metin()
    return Calisma(argv, kod, f"{onceki}HATA: {sebep}\n{kayit}\n")


def ayir(cikti: str) -> tuple[str, str]:
    """(içerik, kayıt bloğu). Komutun kendi kayıt bloğu son ayraçtan sonradır; gömülü bloklar içerikte kalır."""
    if AYRAC not in cikti:
        return cikti, ""
    icerik, _, kayit = cikti.rpartition(AYRAC)
    return icerik, AYRAC + kayit


# --- HTML ------------------------------------------------------------------------------

CSS = """
:root{--zemin:#fbfaf7;--yuzey:#fff;--metin:#1f2328;--soluk:#5b6470;--cizgi:#d9d4c7;--vurgu:#1d5f8a;
--uyari-z:#fff4d6;--uyari-c:#b7791f;--hip-z:#efe9fb;--hip-c:#6b46c1;--hata-z:#fde8e8;--hata-c:#c53030;
--kayit-z:#eef4f8;--meal-z:#f3f3f3}
@media (prefers-color-scheme:dark){:root{--zemin:#16181c;--yuzey:#1e2127;--metin:#e6e6e6;--soluk:#a0a7b1;
--cizgi:#343a44;--vurgu:#6cb2e0;--uyari-z:#3a3016;--uyari-c:#e0b050;--hip-z:#2b2540;--hip-c:#b39cf0;
--hata-z:#3d1e1e;--hata-c:#f08080;--kayit-z:#1c2a35;--meal-z:#2a2a2a}}
*{box-sizing:border-box}body{margin:0;background:var(--zemin);color:var(--metin);
font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
header{background:var(--yuzey);border-bottom:1px solid var(--cizgi);padding:10px 16px}
header h1{font-size:18px;margin:0 0 4px}.ilke{font-size:13px;color:var(--soluk);margin:0}
nav{display:flex;flex-wrap:wrap;gap:4px;padding:8px 16px;background:var(--yuzey);border-bottom:1px solid var(--cizgi)}
nav a{padding:6px 12px;border-radius:6px;text-decoration:none;color:var(--metin)}
nav a.secili{background:var(--vurgu);color:#fff}
main{display:grid;grid-template-columns:minmax(280px,420px) 1fr;gap:16px;padding:16px}
@media (max-width:860px){main{grid-template-columns:1fr}}
details{background:var(--yuzey);border:1px solid var(--cizgi);border-radius:8px;margin-bottom:8px}
summary{cursor:pointer;padding:8px 12px;font-weight:600}
form{padding:0 12px 12px}label{display:block;font-size:13px;color:var(--soluk);margin-top:8px}
label.kutu{display:flex;gap:6px;align-items:flex-start;color:var(--metin)}
input[type=text],textarea,select{width:100%;padding:6px 8px;border:1px solid var(--cizgi);border-radius:6px;
background:var(--zemin);color:var(--metin);font:inherit}textarea{min-height:56px}
button{margin-top:10px;padding:6px 14px;border:0;border-radius:6px;background:var(--vurgu);color:#fff;font:inherit;cursor:pointer}
.not{font-size:12px;color:var(--soluk);margin:6px 0 0}
.sonuc{background:var(--yuzey);border:1px solid var(--cizgi);border-radius:8px;display:flex;flex-direction:column;
max-height:calc(100vh - 150px);min-height:200px}
.sonuc h2{font-size:14px;margin:0;padding:8px 12px;border-bottom:1px solid var(--cizgi)}
.sonuc h2 code{font-weight:400}
.icerik{overflow:auto;padding:8px 0;flex:1}
main>div{min-width:0}
pre{margin:0;font:13px/1.45 ui-monospace,"SFMono-Regular",Consolas,monospace;white-space:pre-wrap;overflow-wrap:anywhere}
.s{display:block;padding:0 12px 0 24px;text-indent:-12px}.s.uyari{background:var(--uyari-z);border-left:4px solid var(--uyari-c)}
.s.hipotez{background:var(--hip-z);border-left:4px solid var(--hip-c)}
.s.hata{background:var(--hata-z);border-left:4px solid var(--hata-c)}
.s.meal{background:var(--meal-z);border-left:4px solid var(--soluk)}
.kayit{position:sticky;bottom:0;background:var(--kayit-z);border-top:2px solid var(--vurgu);padding:8px 12px}
.kayit b{font-size:12px;color:var(--soluk)}
.bos{padding:12px;color:var(--soluk)}
"""


def _e(x: str) -> str:
    return html.escape(x, quote=True)


def satir_siniflari(satirlar: list[str]) -> list[str]:
    """Yalnız görsel vurgu; metin değişmez, satır atılmaz. Uyarı ve meal başlığının altındaki girintili
    satırlar aynı vurguyu taşır (ör. çapraz kontrol uyarısının ayrıntı satırları, meal metni)."""
    siniflar, blok = [], ""
    for s in satirlar:
        girintili = s.startswith(" ")
        if "UYARI" in s:
            k = "uyari"
        elif s.startswith("HATA") or s.lstrip().startswith("HATA:"):
            k = "hata"
        elif s.startswith("[hipotez"):
            k = "hipotez"
        elif okuma.MEAL_ETIKETI in s and not girintili:
            k = "meal"
        elif girintili and blok in ("uyari", "meal"):
            k = blok
        else:
            k = ""
        if not girintili:
            blok = k
        siniflar.append(k)
    return siniflar


def cikti_html(c: Calisma) -> str:
    icerik, kayit = ayir(c.cikti)
    ham = icerik.rstrip("\n").split("\n")
    satirlar = "".join(f'<span class="s {k}">{_e(s) or " "}</span>' for s, k in zip(ham, satir_siniflari(ham)))
    kayit_html = (f'<div class="kayit" id="kayit"><b>Kayıt satırı (§8) — gizlenmez</b><pre>{_e(kayit.strip(chr(10)))}</pre></div>'
                  if kayit else '<div class="kayit" id="kayit"><b>Kayıt satırı yok — çıktı eksik</b></div>')
    return (f'<section class="sonuc"><h2>Sonuç · çıkış kodu {c.kod} · <code>{_e(komut_metni(c.argv))}</code></h2>'
            f'<div class="icerik"><pre>{satirlar}</pre></div>{kayit_html}</section>')


def _alan_html(f: Form, a: Alan, degerler: dict[str, str]) -> str:
    kimlik = f"{f.kimlik}-{a.ad.strip('-')}"
    v = degerler.get(a.ad, a.varsayilan)
    zorunlu = " required" if a.zorunlu else ""
    yildiz = " *" if a.zorunlu else ""
    if a.tur == "bayrak":
        isaret = " checked" if degerler.get(a.ad) else ""     # bayraklar varsayılan olarak kapalı
        return (f'<label class="kutu"><input type="checkbox" name="{_e(a.ad)}" value="1"{isaret}>'
                f'<span>{_e(a.etiket)}</span></label>')
    if a.tur == "secim":
        ops = "".join(f'<option value="{_e(o)}"{" selected" if o == v else ""}>{_e(o)}</option>' for o in a.secenekler)
        bos = "" if a.zorunlu else '<option value="">—</option>'
        return (f'<label for="{kimlik}">{_e(a.etiket)}{yildiz}</label>'
                f'<select id="{kimlik}" name="{_e(a.ad)}"{zorunlu}>{bos}{ops}</select>')
    if a.uzun or a.tur == "tekrar":
        return (f'<label for="{kimlik}">{_e(a.etiket)}{yildiz}</label>'
                f'<textarea id="{kimlik}" name="{_e(a.ad)}"{zorunlu}>{_e(v)}</textarea>')
    return (f'<label for="{kimlik}">{_e(a.etiket)}{yildiz}</label>'
            f'<input type="text" id="{kimlik}" name="{_e(a.ad)}" value="{_e(v)}"{zorunlu}>')


def form_html(f: Form, belirtec: str, degerler: dict[str, str], acik: bool) -> str:
    komut = " ".join(f.onek)
    alanlar = "".join(_alan_html(f, a, degerler) for a in f.alanlar)
    notu = f'<p class="not">{_e(f.aciklama)}</p>' if f.aciklama else ""
    return (f'<details{" open" if acik else ""}><summary>{_e(f.baslik)} <code>{_e(komut)}</code></summary>'
            f'<form method="post" action="/calistir">{notu}<input type="hidden" name="_form" value="{_e(f.kimlik)}">'
            f'<input type="hidden" name="_belirtec" value="{_e(belirtec)}">{alanlar}'
            f'<button type="submit">Çalıştır</button></form></details>')


ILKE = ("Yalnız Kur'an verisi delildir. Lane, Sâmî ve meal hipotez / ikincil katmandır. Her sayının birimi "
        "kayıt satırında yazılıdır; boş çıktı yokluk delili değildir. Okunuş aktarımdır, delil değildir.")


def sayfa(ekran: str, belirtec: str, calisma: Calisma | None = None, form_kimlik: str = "",
          degerler: dict[str, str] | None = None) -> str:
    tum = ekranlar()
    baslik, formlar = tum[ekran]
    nav = "".join(f'<a href="/{k}" class="{"secili" if k == ekran else ""}">{_e(b)}</a>' for k, (b, _) in tum.items())
    sol = "".join(form_html(f, belirtec, degerler if f.kimlik == form_kimlik else {},
                            f.kimlik == form_kimlik or (not form_kimlik and i == 0)) for i, f in enumerate(formlar))
    sag = cikti_html(calisma) if calisma else '<section class="sonuc"><div class="bos">Soldan bir sorgu çalıştırın. ' \
        'Çıktı süzülmeden gösterilir; kayıt satırı panelin altında sabit durur.</div></section>'
    return (f'<!doctype html><html lang="tr"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>Çalışma Masası — {_e(baslik)}</title><style>{CSS}</style></head><body>'
            f'<header><h1>Kur\'an Çalışma Masası</h1><p class="ilke">{_e(ILKE)}</p></header>'
            f'<nav>{nav}</nav><main><div>{sol}</div><div>{sag}</div></main></body></html>')


# --- sunucu --------------------------------------------------------------------------------

class Isleyici(BaseHTTPRequestHandler):
    server: "Sunucu"

    def log_message(self, bicim, *args):   # sessiz; hata kaydı stderr'e
        pass

    def _host_gecerli(self) -> bool:
        port = self.server.server_address[1]
        return self.headers.get("Host", "") in {f"127.0.0.1:{port}", f"localhost:{port}"}

    def _gonder(self, kod: int, govde: str, tur: str = "text/html; charset=utf-8") -> None:
        veri_ = govde.encode("utf-8")
        self.send_response(kod)
        self.send_header("Content-Type", tur)
        self.send_header("Content-Length", str(len(veri_)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Content-Security-Policy", "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'")
        self.end_headers()
        self.wfile.write(veri_)

    def do_GET(self):
        if not self._host_gecerli():
            return self._gonder(403, "Yalnız 127.0.0.1 / localhost", "text/plain; charset=utf-8")
        yol = urlsplit(self.path).path.strip("/") or "tarama"
        if yol not in ekranlar():
            return self._gonder(404, "Bulunamadı", "text/plain; charset=utf-8")
        self._gonder(200, sayfa(yol, self.server.belirtec))

    def do_POST(self):
        if not self._host_gecerli():
            return self._gonder(403, "Yalnız 127.0.0.1 / localhost", "text/plain; charset=utf-8")
        if urlsplit(self.path).path != "/calistir":
            return self._gonder(404, "Bulunamadı", "text/plain; charset=utf-8")
        uzunluk = int(self.headers.get("Content-Length") or 0)
        if uzunluk > 1_000_000:
            return self._gonder(413, "İstek çok büyük", "text/plain; charset=utf-8")
        alanlar = {k: v[0] for k, v in parse_qs(self.rfile.read(uzunluk).decode("utf-8"), keep_blank_values=True).items()}
        if not secrets.compare_digest(alanlar.get("_belirtec", ""), self.server.belirtec):
            return self._gonder(403, "Oturum belirteci geçersiz — sayfayı yenileyin.", "text/plain; charset=utf-8")
        bulunan = form_bul(alanlar.get("_form", ""))
        if bulunan is None:
            return self._gonder(400, "Bilinmeyen form", "text/plain; charset=utf-8")
        ekran, form = bulunan
        try:
            argv = argv_kur(form, alanlar)
        except FormHatasi as e:
            c = _calistirilmadi(list(form.onek), str(e))
        else:
            c = calistir(argv)
        self._gonder(200, sayfa(ekran, self.server.belirtec, c, form.kimlik, alanlar))


class Sunucu(HTTPServer):
    def __init__(self, port: int):
        super().__init__(("127.0.0.1", port), Isleyici)
        self.belirtec = secrets.token_urlsafe(24)


def baslat(port: int = VARSAYILAN_PORT, tarayici: bool = True) -> int:
    try:
        s = Sunucu(port)
    except OSError as e:
        print(f"HATA: {port} numaralı bağlantı noktası açılamadı ({e}). Başka port deneyin: --port 8766")
        return 2
    adres = f"http://127.0.0.1:{s.server_address[1]}/"
    print(f"Çalışma masası arayüzü: {adres}  (yalnız bu bilgisayardan erişilir; durdurmak için Ctrl+C)")
    sys.stdout.flush()
    if tarayici:
        with contextlib.suppress(Exception):
            webbrowser.open(adres)
    try:
        s.serve_forever()
    except KeyboardInterrupt:
        print("\nDurduruldu.")
    finally:
        s.server_close()
    return 0
