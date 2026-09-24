"""Aşama 6: yerel web arayüzü — standart kütüphane, mantıksız arayüz, gizlenmeyen uyarı / hipotez / kayıt satırı,
meal varsayılan kapalı, yalnız yerel erişim."""

import ast
import contextlib
import html
import io
import re
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from unittest import mock

import _ortak  # noqa: F401
from tezgah import arayuz, kavram, okuma, tez
from tezgah.__main__ import main
from tezgah.ikincil import sami
from tezgah.kayit import komut_metni

KAYNAK = Path(arayuz.__file__)


def cli(argv):
    t = io.StringIO()
    with contextlib.redirect_stdout(t):
        kod = main(argv)
    return kod, t.getvalue()


def duz_metin(sayfa: str) -> str:
    """HTML → görünen metin (etiketler atılır, varlıklar çözülür)."""
    return html.unescape(re.sub(r"<[^>]+>", "", sayfa))


class SunucuTesti(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sunucu = arayuz.Sunucu(0)
        cls.port = cls.sunucu.server_address[1]
        cls.kok = f"http://127.0.0.1:{cls.port}"
        cls.is_parcacigi = threading.Thread(target=cls.sunucu.serve_forever, daemon=True)
        cls.is_parcacigi.start()

    @classmethod
    def tearDownClass(cls):
        cls.sunucu.shutdown()
        cls.sunucu.server_close()

    def get(self, yol, host=None):
        r = urllib.request.Request(self.kok + yol, headers={"Host": host} if host else {})
        with urllib.request.urlopen(r, timeout=120) as y:
            return y.status, y.read().decode("utf-8")

    def post(self, form, alanlar, belirtec=None, host=None):
        veri_ = {"_form": form, "_belirtec": self.sunucu.belirtec if belirtec is None else belirtec, **alanlar}
        r = urllib.request.Request(self.kok + "/calistir", data=urllib.parse.urlencode(veri_).encode("utf-8"),
                                   headers={"Host": host} if host else {})
        try:
            with urllib.request.urlopen(r, timeout=600) as y:
                return y.status, y.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode("utf-8")

    # --- yapı ------------------------------------------------------------------------

    def test_yalniz_standart_kutuphane(self):
        agac = ast.parse(KAYNAK.read_text(encoding="utf-8"))
        disari = set()
        for d in ast.walk(agac):
            if isinstance(d, ast.Import):
                disari |= {a.name.split(".")[0] for a in d.names}
            elif isinstance(d, ast.ImportFrom) and d.level == 0:
                disari.add(d.module.split(".")[0])
        self.assertTrue(disari <= set(sys.stdlib_module_names) | {"__future__"}, disari - set(sys.stdlib_module_names))

    def test_arayuzun_sorgu_mantigi_yok(self):
        agac = ast.parse(KAYNAK.read_text(encoding="utf-8"))
        paket_ici = set()
        for d in ast.walk(agac):
            if isinstance(d, ast.ImportFrom) and d.level > 0:
                paket_ici |= {d.module} if d.module else {a.name for a in d.names}
        # yalnız komut çalıştırıcı (__main__), kayıt biçimi ve form seçenekleri için sabitler
        self.assertTrue(paket_ici <= {"__main__", "kayit", "kavram", "okuma", "tez"}, paket_ici)
        for yasak in ("tara", "qm", "veri", "okunus", "lane", "sami"):
            self.assertNotIn(yasak, paket_ici)

    def test_bilinen_ekranlar(self):
        self.assertEqual(list(arayuz.ekranlar()), ["tarama", "ayet", "kavram", "tez", "ikincil"])
        for ekran in arayuz.ekranlar():
            kod, s = self.get(f"/{ekran}")
            self.assertEqual(kod, 200)
            self.assertIn(arayuz.ILKE.split(".")[0], duz_metin(s))

    # --- çıktı aynen: uyarı, hipotez, kayıt ---------------------------------------------

    def _ayni_cikti(self, form, alanlar, argv):
        _, beklenen = cli(argv)
        kod, s = self.post(form, alanlar)
        self.assertEqual(kod, 200)
        gorunen = duz_metin(s)
        for satir in beklenen.rstrip("\n").split("\n"):
            self.assertIn(satir, gorunen, f"satır arayüzde yok: {satir!r}")
        kayit = re.search(r'<div class="kayit" id="kayit">(.*?)</div>', s, re.S)
        self.assertIsNotNone(kayit, "kayıt satırı ayrı ve sabit panelde olmalı")
        self.assertIn("Sorgu       : " + komut_metni(argv), duz_metin(kayit.group(1)))
        return s

    def test_ikiz_kok_uyarisi_gorunur(self):
        s = self._ayni_cikti("kok", {"kok": "slw", "--limit": "5"}, ["kok", "slw", "--limit", "5"])
        self.assertRegex(s, r'<span class="s uyari">UYARI: Büyük/küçük harfle ayrışan')

    def test_iki_korpus_farki_uyarisi_gorunur(self):
        s = self._ayni_cikti("kok", {"kok": "nws", "--limit": "3"}, ["kok", "nws", "--limit", "3"])
        self.assertRegex(s, r'<span class="s uyari">UYARI \(çapraz kontrol')
        # uyarının girintili ayrıntı satırı da vurgulu
        self.assertRegex(s, r'<span class="s uyari">  QAC&#x27;ın bu köke bağladığı')

    def test_hipotez_etiketi_her_satirda(self):
        s = self._ayni_cikti("sami_kok", {"kok": "Amn"}, ["sami", "kok", "Amn"])
        icerik = s.split('<div class="kayit"')[0]
        satirlar = re.findall(r'<span class="s ([a-z]*)">(.*?)</span>', icerik, re.S)
        hipotez = [m for k, m in satirlar if html.unescape(m).startswith("[hipotez")]
        self.assertGreater(len(hipotez), 3)
        for k, m in satirlar:
            if html.unescape(m).startswith("[hipotez"):
                self.assertEqual(k, "hipotez")

    def test_kayit_satiri_hata_durumunda_da(self):
        kod, s = self.post("kok", {"kok": "s-l-v"})          # Latin giriş reddedilir
        self.assertEqual(kod, 200)
        self.assertIn("Durum       : çalıştırılmadı", duz_metin(s))
        kod, s = self.post("kok", {"kok": ""})               # zorunlu alan boş
        self.assertIn("Zorunlu alan boş", duz_metin(s))
        self.assertIn("Durum       : çalıştırılmadı", duz_metin(s))

    def test_ayni_komut_ayni_cikti(self):
        for argv in (["sayim", "--kok", "Slw"], ["dagilim", "--kok", "fTr", "--gore", "bab"], ["okunus", "107:4"]):
            with self.subTest(argv=argv):
                self.assertEqual(arayuz.calistir(argv).cikti, cli(argv)[1])

    # --- meal ---------------------------------------------------------------------------

    def test_meal_varsayilan_kapali(self):
        _, s = self.get("/ayet")
        kutu = re.search(r'<input type="checkbox" name="--meal"[^>]*>', s)
        self.assertIsNotNone(kutu)
        self.assertNotIn("checked", kutu.group(0))
        self.assertIn(okuma.MEAL_ETIKETI, duz_metin(s))
        _, s = self.post("ayet", {"ayet": "107:4"})
        self.assertNotIn(okuma.MEAL_ETIKETI + " (", duz_metin(s).split("Kayıt satırı")[0])
        self.assertIn("Sorgu       : python -m tezgah ayet 107:4\n", duz_metin(s))

    @unittest.skipUnless(okuma.MEAL_YOLU.exists(), "meal kurulu değil")
    def test_meal_acilinca_etiketli(self):
        _, s = self.post("ayet", {"ayet": "107:4", "--meal": "1"})
        self.assertRegex(s, r'<span class="s meal">Meal — kurumsal okuma — sınanan, delil değil')
        self.assertIn("--meal", duz_metin(s))

    # --- kavram ve tez ekranları -----------------------------------------------------------

    def test_kavram_ve_tez_ekranlari_paketi_cagirir(self):
        with tempfile.TemporaryDirectory() as d:
            kdiz, tdiz = Path(d) / "kavramlar", Path(d) / "kavramlar" / "tezler"
            with mock.patch.object(kavram, "KAVRAMLAR", kdiz), mock.patch.object(tez, "TEZLER", tdiz):
                _, s = self.post("kavram_ac", {"ad": "deneme", "--soru": "ṣ-l-v kökü nasıl kullanılıyor?", "--kok": "Slw"})
                self.assertIn("Kavram dosyası açıldı", duz_metin(s))
                self.assertTrue((kdiz / "deneme" / "kavram.md").exists())
                _, s = self.post("kavram_liste", {})
                self.assertIn("  deneme", duz_metin(s))
                _, s = self.post("kavram_goster", {"ad": "deneme"})
                self.assertIn("ṣ-l-v kökü nasıl kullanılıyor?", duz_metin(s))
                _, s = self.post("tez_ac", {"ad": "t1", "--tez": "Deneme tezi tek cümledir.",
                                            "--tanim": "salât=deneme tanımı", "--eksen": "kip=tanımlayıcı",
                                            "--karsi": 'kalip "ROOT:Slw&POS:V"'})
                self.assertIn("Tez donduruldu", duz_metin(s))
                # tez değiştirilemez: aynı adla ikinci açılış reddedilir, kayıt satırı yine görünür
                _, s = self.post("tez_ac", {"ad": "t1", "--tez": "Başka.", "--tanim": "a=b", "--eksen": "kip=x",
                                            "--karsi": "kok Slw"})
                self.assertIn("Durum       : çalıştırılmadı", duz_metin(s))

    # --- güvenlik -----------------------------------------------------------------------------

    def test_yalniz_yerel(self):
        self.assertEqual(self.sunucu.server_address[0], "127.0.0.1")
        with self.assertRaises(urllib.error.HTTPError) as e:
            self.get("/tarama", host="saldirgan.example:80")
        self.assertEqual(e.exception.code, 403)

    def test_belirtecsiz_post_reddedilir(self):
        kod, _ = self.post("kok", {"kok": "Slw"}, belirtec="yanlis")
        self.assertEqual(kod, 403)
        kod, _ = self.post("bilinmeyen", {})
        self.assertEqual(kod, 400)

    def test_izinsiz_komut_calismaz(self):
        c = arayuz.calistir(["kur", "meal"])
        self.assertEqual(c.kod, 2)
        self.assertIn("çalıştırılmadı", c.cikti)

    # --- hemze / ayn gösterimi ------------------------------------------------------------------

    def test_hemze_ayn_isaretli_ve_metin_ayni(self):
        for bw, latin, sinif, kod in (("Amn", "\u02be-m-n", "hz", "U+02BE"), ("Elm", "\u02bf-l-m", "ay", "U+02BF"),
                                      ("Ans", "\u02be-n-s", "hz", "U+02BE")):
            with self.subTest(kok=bw):
                _, s = self.post("kok", {"kok": bw, "--limit": "3"})
                harf = latin[0]
                self.assertIn(f'<span class="{sinif}" title="{"hemze" if sinif == "hz" else "ayn"} ({kod})">{harf}</span>'
                              "-" + latin[2:], s)
                self.assertIn(f"Kök: {bw} ({latin})", duz_metin(s))          # görünen metin değişmedi
                icerik = s.split('<div class="kayit"')[0]
                # işaretli span dışında kalan hemze/ayn yok; U+0027 hiçbir span'ın içinde değil
                self.assertEqual(icerik.count("\u02be"), icerik.count('class="hz"'))
                self.assertEqual(icerik.count("\u02bf"), icerik.count('class="ay"'))
                self.assertNotRegex(s, r'class="(hz|ay)"[^>]*>\'<')
        _, s = self.get("/tarama")
        self.assertIn("hemze</b> (U+02BE)", s)
        self.assertIn("ayn</b> (U+02BF)", s)
        self.assertIn("düz kesme</b> (U+0027", s)

    # --- sonuç sınırı: tümünü göster -------------------------------------------------------------

    def test_tumunu_goster(self):
        for f in (f for _, (_, formlar) in arayuz.ekranlar().items() for f in formlar):
            if any(a.ad == "--limit" for a in f.alanlar):
                with self.subTest(form=f.kimlik):
                    html_ = arayuz.form_html(f, "b", {}, True)
                    kutu = re.search(r'<input type="checkbox" name="--limit:tumu"[^>]*>', html_)
                    self.assertIsNotNone(kutu, "limitli her formda 'tümünü göster' olmalı")
                    self.assertNotIn("checked", kutu.group(0))
        _, s = self.post("kok", {"kok": "Amn", "--limit": "5", "--limit:tumu": "1"})
        metin = duz_metin(s)
        self.assertIn("gösterilen 879 / 879", metin)
        self.assertIn("Sorgu       : python -m tezgah kok Amn --limit 0", metin)
        _, s = self.post("kok", {"kok": "Amn", "--limit": "5"})
        self.assertIn("gösterilen 5 / 879", duz_metin(s))

    def test_bw_kutusu_varsayilan_kapali(self):
        for kimlik in ("kok", "lemma", "etiket", "kalip", "dagilim"):
            f = arayuz.form_bul(kimlik)[1]
            kutu = re.search(r'<input type="checkbox" name="--bw"[^>]*>', arayuz.form_html(f, "b", {}, True))
            with self.subTest(form=kimlik):
                self.assertIsNotNone(kutu)
                self.assertNotIn("checked", kutu.group(0))
        _, s = self.post("kok", {"kok": "Slw", "--limit": "2", "--bw": "1"})
        self.assertIn("biçim (Buckwalter)", duz_metin(s))

    def test_tire_ile_baslayan_deger(self):
        f = arayuz.form_bul("tez_ac")[1]
        argv = arayuz.argv_kur(f, {"ad": "t", "--tez": "-x tezi", "--tanim": "a=b", "--eksen": "k=v",
                                   "--karsi": "kok Slw"})
        self.assertIn("--tez=-x tezi", argv)


@unittest.skipUnless(sami.sedra_kurulu(), "SEDRA kurulu değil")
class IkincilEkran(unittest.TestCase):
    def test_zayif_son_varsayilan_kapali(self):
        f = arayuz.form_bul("sami_kok")[1]
        self.assertEqual(arayuz.argv_kur(f, {"kok": "Slw"}), ["sami", "kok", "Slw"])
        s = arayuz.form_html(f, "b", {}, True)
        kutu = re.search(r'<input type="checkbox" name="--zayif-son"[^>]*>', s)
        self.assertNotIn("checked", kutu.group(0))


if __name__ == "__main__":
    unittest.main()
