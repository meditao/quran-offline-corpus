"""Okuyan meali (kullanıcı dosyası) ve çoklu meal görünümü; arayüzde klasik sözlük formları.

Okuyan meali telifli; açık lisanslı kaynağı yok, kullanıcının verdiği dosyadan kurulur. Testler gerçek meal metni
kullanmaz: deneme dosyası Tanzil ayet kümesinden "DENEME s:a" metinleriyle üretilir, geçici dizinde kurulur.
"""

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import _ortak  # noqa: F401
from tezgah import arayuz, okuma, okunus, veri
from tezgah.__main__ import main


def calistir(argv):
    t = io.StringIO()
    with contextlib.redirect_stdout(t):
        kod = main(argv)
    return kod, t.getvalue()


def satirlar(ayirici="|", baslik=True):
    govde = "\n".join(f"{s}{ayirici}{a}{ayirici}DENEME {s}:{a}" for s, a in okunus.tanzil())
    return (("sure" + ayirici + "ayet" + ayirici + "metin\n") if baslik else "") + govde + "\n# son yorum\n"


class DosyaBicimleri(unittest.TestCase):
    def test_boru_sekme_virgul_ve_iki_nokta(self):
        for ayirici in ("|", "\t", ","):
            with self.subTest(ayirici=repr(ayirici)):
                m = okuma.meal_dosyasi_oku(satirlar(ayirici).encode("utf-8"))
                self.assertEqual(len(m), 6_236)
                self.assertEqual(m[(107, 4)], "DENEME 107:4")
        m = okuma.meal_dosyasi_oku("1:1\tbir\n1:2\tiki\n".encode("utf-8"))
        self.assertEqual(m, {(1, 1): "bir", (1, 2): "iki"})

    def test_tirnakli_csv_ve_bom(self):
        m = okuma.meal_dosyasi_oku('﻿sure,ayet,metin\n1,1,"virgüllü, ""tırnaklı"" metin"\n'.encode("utf-8"))
        self.assertEqual(m, {(1, 1): 'virgüllü, "tırnaklı" metin'})

    def test_json_bicimleri(self):
        a = {"quran": [{"chapter": 1, "verse": 1, "text": "x  y"}]}
        b = [{"sure": 1, "ayet": 1, "metin": "x y"}]
        self.assertEqual(okuma.meal_dosyasi_oku(json.dumps(a).encode()), {(1, 1): "x y"})
        self.assertEqual(okuma.meal_dosyasi_oku(json.dumps(b).encode()), {(1, 1): "x y"})

    def test_cozulemeyen_satir_sessizce_atlanmaz(self):
        with self.assertRaises(veri.VeriHatasi):
            okuma.meal_dosyasi_oku("1|1|bir\nbu satır bozuk\n".encode("utf-8"))

    def test_ayni_ayet_iki_kez(self):
        with self.assertRaises(veri.VeriHatasi):
            okuma.meal_dosyasi_oku("1|1|bir\n1|1|yine\n".encode("utf-8"))

    def test_utf8_olmayan_dosya(self):
        with self.assertRaises(veri.VeriHatasi):
            okuma.meal_dosyasi_oku("1|1|ğüş".encode("cp1254"))

    def test_ayet_kumesi_ve_bos_metin(self):
        tam = okuma.meal_dosyasi_oku(satirlar().encode("utf-8"))
        okuma.meal_ayetleri_dogrula(tam, "deneme")
        eksik = dict(tam)
        del eksik[(2, 286)]
        with self.assertRaisesRegex(veri.VeriHatasi, "eksik 1: 2:286"):
            okuma.meal_ayetleri_dogrula(eksik, "deneme")
        with self.assertRaisesRegex(veri.VeriHatasi, "fazla 1"):
            okuma.meal_ayetleri_dogrula({**tam, (1, 8): "x"}, "deneme")
        with self.assertRaisesRegex(veri.VeriHatasi, "boş"):
            okuma.meal_ayetleri_dogrula({**tam, (1, 1): "  "}, "deneme")


class OkuyanKurulumu(unittest.TestCase):
    def setUp(self):
        self.dizin = Path(tempfile.mkdtemp())
        self.kaynak = self.dizin / "deneme.txt"
        self.kaynak.write_text(satirlar(), encoding="utf-8", newline="\n")
        self.yamalar = [mock.patch.object(okuma, "OKUYAN_YOLU", self.dizin / "okuyan.json"),
                        mock.patch.object(okuma, "OKUYAN_MANIFEST", self.dizin / "okuyan.manifest.json"),
                        mock.patch.object(okuma, "MEAL_DIZINI", self.dizin),
                        mock.patch.object(okuma, "MEAL_YOLU", self.dizin / "diyanet-yok.json"),
                        mock.patch.object(okuma, "CEVIRI_YOLU", self.dizin / "cv.tsv")]
        for y in self.yamalar:
            y.start()
        okuma.okuyan_meal.cache_clear()
        okuma.meal.cache_clear()

    def tearDown(self):
        for y in self.yamalar:
            y.stop()
        okuma.okuyan_meal.cache_clear()
        okuma.meal.cache_clear()

    def test_kurulum_ve_gorunum(self):
        kod, c = calistir(["kur", "meal-okuyan", "--dosya", str(self.kaynak)])
        self.assertEqual(kod, 0, c)
        self.assertIn("ayet: 6236", c)
        self.assertIn("kimlik: kullanıcı beyanı", c)
        self.assertIn("Sayım birimi: ayet", c)
        manifest = json.loads((self.dizin / "okuyan.manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["parmak_izi"]["107:4"], "DENEME 107:4")
        self.assertEqual(manifest["sha256"], veri.sha256(self.dizin / "okuyan.json"))
        okuma.okuyan_meal.cache_clear()
        kod, c = calistir(["ayet", "107:4", "--meal"])
        self.assertEqual(kod, 0)
        self.assertIn("DENEME 107:4", c)
        self.assertIn("Mehmet Okuyan, kullanıcının verdiği dosya — kimliği araçla doğrulanmadı", c)
        self.assertLess(c.index("Çalışma çevirisi (kullanıcının yorumu)"), c.index("(Diyanet İşleri"))
        self.assertLess(c.index("(Diyanet İşleri"), c.index("(Mehmet Okuyan"), "sıra: çalışma çevirisi, Diyanet, Okuyan")
        self.assertIn("| + meal Mehmet Okuyan (kullanıcı dosyası; sınanan, delil değil)", c)
        kod, c = calistir(["ayet", "107:4"])
        self.assertNotIn("Okuyan", c, "meal varsayılan olarak kapalı")

    def test_ikinci_kurulum_reddedilir(self):
        self.assertEqual(calistir(["kur", "meal-okuyan", "--dosya", str(self.kaynak)])[0], 0)
        kod, c = calistir(["kur", "meal-okuyan", "--dosya", str(self.kaynak)])
        self.assertEqual(kod, 2)
        self.assertIn("zaten kurulu", c)

    def test_degistirilmis_dosya_reddedilir(self):
        okuma.okuyan_kur(self.kaynak)
        yol = self.dizin / "okuyan.json"
        yol.write_bytes(yol.read_bytes().replace(b"DENEME 2:3", b"BOZUK 2:3"))
        okuma.okuyan_meal.cache_clear()
        with self.assertRaises(veri.VeriHatasi):
            okuma.okuyan_meal()

    def test_eksik_dosya_kurulmaz(self):
        bozuk = self.dizin / "eksik.txt"
        bozuk.write_text("1|1|bir\n", encoding="utf-8", newline="\n")
        kod, c = calistir(["kur", "meal-okuyan", "--dosya", str(bozuk)])
        self.assertEqual(kod, 2)
        self.assertIn("ayet kümesi Tanzil ile aynı değil", c)
        self.assertFalse((self.dizin / "okuyan.json").exists(), "doğrulanmayan dosya yazılmamalı")

    def test_dosya_bayragi_kurallari(self):
        kod, c = calistir(["kur", "meal-okuyan"])
        self.assertEqual(kod, 2)
        self.assertIn("--dosya", c)
        kod, c = calistir(["kur", "lane", "--dosya", str(self.kaynak)])
        self.assertEqual(kod, 2)
        self.assertIn("yalnız meal-okuyan", c)

    def test_kurulu_degilken_bilgi_verir(self):
        kod, c = calistir(["ayet", "1:1", "--meal"])
        self.assertEqual(kod, 0)
        self.assertIn("Okuyan meali kurulu değil (python -m tezgah kur meal-okuyan --dosya <yol>)", c)


class ArayuzKlasikFormlari(unittest.TestCase):
    def test_klasik_izinli_ve_formlar_var(self):
        self.assertIn("klasik", arayuz.IZINLI)
        kimlikler = {f.kimlik for _, (_, formlar) in arayuz.ekranlar().items() for f in formlar}
        for k in ("klasik_kok", "klasik_isaret", "klasik_asl", "klasik_ayet", "klasik_ara", "klasik_kapsam",
                  "klasik_etiketler"):
            self.assertIn(k, kimlikler)

    def test_argv(self):
        f = arayuz.form_bul("klasik_kok")[1]
        self.assertEqual(arayuz.argv_kur(f, {"kok": "Slw Amn", "--eser": ""}), ["klasik", "kok", "Slw", "Amn"])
        self.assertEqual(arayuz.argv_kur(f, {"kok": "Slw", "--eser": "ragib", "--tam": "1"}),
                         ["klasik", "kok", "Slw", "--eser", "ragib", "--tam"])
        f = arayuz.form_bul("klasik_ara")[1]
        self.assertEqual(arayuz.argv_kur(f, {"ifade": "x", "--limit": "5", "--limit:tumu": "1"}),
                         ["klasik", "ara", "x", "--limit", "0"])

    def test_etiketler_arayuzden_calisir(self):
        c = arayuz.calistir(["klasik", "etiketler"])
        self.assertEqual(c.kod, 0)
        self.assertIn("[hipotez · klasik]", c.cikti)
        self.assertIn("hipotez", arayuz.satir_siniflari(c.cikti.splitlines()))


if __name__ == "__main__":
    unittest.main()
