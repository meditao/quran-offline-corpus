"""§4 etiket kuralı: --etiket tam eşleşmedir; alt-dize yalnız açık bayrakla ve uyarıyla."""

import unittest

import _ortak  # noqa: F401
from tezgah import tara, veri


class EtiketTesti(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kor = veri.korpus()

    def test_def_indef_sizintisi_yok(self):
        # "DEF" envanterde tam etiket olarak yok; tam eşleşme INDEF'e sızmamalı.
        with self.assertRaises(tara.GirdiHatasi):
            tara.sayim(self.kor, etiketler=["DEF"])

    def test_alt_dize_acik_bayrakla_ve_uyariyla(self):
        s = tara.sayim(self.kor, etiketler=["DEF"], alt_dize=True)
        self.assertTrue(any(x.startswith("UYARI: alt-dize") for x in s.satirlar))
        self.assertEqual(s.veri["segment"], tara.sayim(self.kor, etiketler=["INDEF"]).veri["segment"])

    def test_tam_eslesme_yalniz_ayni_etiketi_alir(self):
        for e in ("M", "PRON:3M", "(V)", "3MP"):
            if e not in self.kor.etiket_envanteri:
                with self.subTest(etiket=e):
                    with self.assertRaises(tara.GirdiHatasi):
                        tara.etiket_coz(self.kor, e)
                continue
            with self.subTest(etiket=e):
                grup, uyarilar = tara.etiket_coz(self.kor, e)
                self.assertEqual(grup, frozenset({e}))
                self.assertEqual(uyarilar, [])
                n = tara.sayim(self.kor, etiketler=[e]).veri["segment"]
                self.assertEqual(n, self.kor.etiket_envanteri[e])

    def test_bab_v_x_e_sizmaz(self):
        # "(V)" tam eşleşmesi "(VI)", "(VII)", "(VIII)" segmentlerini almamalı.
        segler, _, _ = tara._etiket_segmentleri(self.kor, ["(V)"], False)
        self.assertTrue(segler)
        self.assertTrue(all(s.bab == "V" for s in segler))

    def test_alt_dize_bab_birlestirir_ve_uyarir(self):
        grup, uyarilar = tara.etiket_coz(self.kor, "(V", alt_dize=True)
        self.assertTrue({"(V)", "(VI)", "(VII)", "(VIII)"} <= grup)
        self.assertTrue(uyarilar)

    def test_bab_i_etiketi_yok(self):
        with self.assertRaises(tara.GirdiHatasi):
            tara.etiket_coz(self.kor, "(I)")

    def test_iyelik_eki_ayri_segment(self):
        # İsim gövdesinin kendi etiketlerinde PRON:* bulunmaz; zamir sonraki segmenttedir.
        for s in self.kor.segmentler:
            if s.tur == "STEM" and s.pos in {"N", "ADJ", "PN"}:
                self.assertFalse(any(e.startswith("PRON:") for e in s.ozellikler), s.konum)


if __name__ == "__main__":
    unittest.main()
