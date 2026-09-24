"""Komutlar arası iç tutarlılık: aynı soru farklı yoldan aynı sayıyı vermeli."""

import re
import unittest

import _ortak  # noqa: F401
from tezgah import tara, veri

KOKLER = ("Slw", "fTr", "rwH", "qdr", "gfr", "Amn")


class TutarlilikTesti(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kor = veri.korpus()

    def test_etiket_ve_kalip_kok_sayimiyla_ayni(self):
        for kok in KOKLER:
            with self.subTest(kok=kok):
                s = tara.sayim(self.kor, kok=kok).veri
                e = tara.sayim(self.kor, etiketler=[f"ROOT:{kok}"]).veri
                k = tara.kalip(self.kor, f"ROOT:{kok}").veri
                for ad in ("kelime konumu", "ayet", "sûre"):
                    self.assertEqual(e[ad], s[ad], ad)
                    self.assertEqual(k[ad], s[ad], ad)

    def test_sure_dagilimi_toplami(self):
        for kok in KOKLER:
            with self.subTest(kok=kok):
                d = tara.dagilim(self.kor, "sure", kok=kok).veri
                self.assertEqual(sum(w for w, _ in d["dagilim"].values()), d["kelime konumu"])
                self.assertEqual(sum(a for _, a in d["dagilim"].values()), d["ayet"])
                self.assertEqual(len(d["dagilim"]), d["sûre"])

    def test_bab_fiil_ve_isim_ayri_sutun(self):
        for kok in KOKLER:
            with self.subTest(kok=kok):
                d = tara.dagilim(self.kor, "bab", kok=kok)
                self.assertTrue(any("fiil" in x and "isim" in x for x in d.satirlar))
                self.assertEqual(d.birimler, ["segment"])
                govde = sum(len([s for s in k.segmentler if s.kok == kok])
                            for k in self.kor.kok_kelimeleri[kok])
                self.assertEqual(sum(d.veri["fiil"].values()) + sum(d.veri["isim"].values()), govde)

    def test_bab_fiilde_isaretsiz_I_isimde_isaretsiz(self):
        """Ham dosyadan (ayrıştırıcıdan bağımsız) sayılan değerlerle karşılaştırılır."""
        bab_re = re.compile(r"\|\((?:II|III|IV|V|VI|VII|VIII|IX|X|XI|XII)\)(?:\||$)")
        with veri.QAC_YOLU.open(encoding="utf-8-sig", newline="") as f:
            satirlar = [s.rstrip("\r\n").split("\t") for s in f if s.startswith("(")]
        for kok in KOKLER:
            with self.subTest(kok=kok):
                hedef = [s[3] for s in satirlar if f"|ROOT:{kok}|" in s[3] + "|"]
                fiil = [o for o in hedef if "|POS:V|" in o + "|"]
                isim = [o for o in hedef if "|POS:V|" not in o + "|"]
                d = tara.dagilim(self.kor, "bab", kok=kok).veri
                self.assertEqual(d["fiil"].get("I", 0), sum(1 for o in fiil if not bab_re.search(o)))
                self.assertEqual(d["isim"].get(tara.ISARETSIZ, 0), sum(1 for o in isim if not bab_re.search(o)))
                self.assertNotIn("I", d["isim"], "isimde işaretsiz gövde I. bab diye raporlanmamalı")
                self.assertNotIn(tara.ISARETSIZ, d["fiil"])

    def test_birlikte_kendisiyle(self):
        for kok in KOKLER:
            with self.subTest(kok=kok):
                b = tara.birlikte(self.kor, kok, kok).veri
                self.assertEqual(b["ortak_ayet"], tara.sayim(self.kor, kok=kok).veri["ayet"])

    def test_birlikte_simetrik(self):
        ab = tara.birlikte(self.kor, "Amn", "Eml", pencere=3).veri
        ba = tara.birlikte(self.kor, "Eml", "Amn", pencere=3).veri
        self.assertEqual(ab["ortak_ayet"], ba["ortak_ayet"])
        self.assertEqual(ab["pencere_ayet"], ba["pencere_ayet"])
        self.assertEqual(ab["pencere_cift"], ba["pencere_cift"])

    def test_korpus_toplamlari_sayim_komutuyla_ayni(self):
        s = tara.sayim(self.kor).veri
        self.assertEqual((s["ayet"], s["kelime konumu"], s["segment"], s["benzersiz kök"]),
                         (6_236, 77_429, 128_219, 1_642))


if __name__ == "__main__":
    unittest.main()
