"""§2.8 giriş kuralı: Arapça veya Buckwalter kabul, Latin okunuş ret, boş sonuç yok."""

import unittest

import _ortak  # noqa: F401
from tezgah import tara, veri


class GirisTesti(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kor = veri.korpus()

    def test_latin_okunus_reddedilir(self):
        for girdi in ("s-l-v", "ṣ-l-v", "e-m-n", "q-d-r", "salat", "ṣlv", "s l v"):
            with self.subTest(girdi=girdi):
                with self.assertRaises(tara.GirdiHatasi):
                    tara.kok_coz(self.kor, girdi)

    def test_latin_retinde_buckwalter_adayi_gosterilir(self):
        with self.assertRaises(tara.GirdiHatasi) as ctx:
            tara.kok_coz(self.kor, "s-l-v")
        self.assertIn(tara.LATIN_ISARETI, str(ctx.exception))
        self.assertIn("Slw", str(ctx.exception))

    def test_envanterde_olmayan_kok_bos_sonuc_degil_hata(self):
        for girdi in ("slv", "xyz", "Qdr"):
            with self.subTest(girdi=girdi):
                with self.assertRaises(tara.GirdiHatasi):
                    tara.sayim(self.kor, kok=girdi)

    def test_arapca_giris(self):
        for girdi, beklenen in (("صلو", "Slw"), ("ص ل و", "Slw"), ("ص-ل-و", "Slw"),
                                ("أمن", "Amn"), ("امن", "Amn"), ("غفر", "gfr"), ("روح", "rwH")):
            with self.subTest(girdi=girdi):
                self.assertEqual(tara.kok_coz(self.kor, girdi).bw, beklenen)

    def test_arapca_ve_buckwalter_ayni_sonuc(self):
        a = tara.sayim(self.kor, kok="صلو").veri
        b = tara.sayim(self.kor, kok="Slw").veri
        self.assertEqual(a, b)

    def test_buyuk_kucuk_harf_ikizi_uyarisi(self):
        # Slw (ص ل و) ile slw (س ل و) ayrı köklerdir; Latin alışkanlığıyla yanlış köke düşmemek için uyarı.
        self.assertIn("slw", self.kor.kok_kelimeleri)
        c = tara.kok_coz(self.kor, "Slw")
        self.assertTrue(any("slw" in u for u in c.uyarilar))

    def test_latin_gosterim_kayipsiz(self):
        latin = [veri.kok_latin(k) for k in self.kor.kok_kelimeleri]
        self.assertEqual(len(set(latin)), len(latin), "iki kök aynı Latin gösterime düştü")
        self.assertEqual(len(set(veri.KOK_LATIN.values())), len(veri.KOK_LATIN))


if __name__ == "__main__":
    unittest.main()
