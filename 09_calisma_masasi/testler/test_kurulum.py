"""§6 kurulum sağlaması: dosya bütünlüğü ve temel sayımlar (QAC v0.4)."""

import unittest

import _ortak  # noqa: F401
from tezgah import veri

# CLAUDE.md §6 — depodan ölçülmüş beklenen değerler. Test kırılırsa burası
# değiştirilmez; önce sebep bulunur ve raporlanır.
QAC_SHA256 = "a1d12923815341face765083805d2148ed2d9f5cc3f7d6665219d887675d8c46"
AYET = 6_236
KELIME_KONUMU = 77_429
SEGMENT = 128_219
BENZERSIZ_KOK = 1_642


class KurulumTesti(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kor = veri.korpus()

    def test_sha256(self):
        self.assertEqual(veri.sha256(veri.QAC_YOLU), QAC_SHA256)
        self.assertEqual(self.kor.sha256, QAC_SHA256)

    def test_telif_blogu_korunmus(self):
        self.assertTrue(self.kor.telif_blogu)

    def test_ayet(self):
        self.assertEqual(len(self.kor.ayet_segmentleri), AYET)

    def test_kelime_konumu(self):
        self.assertEqual(len(self.kor.kelimeler), KELIME_KONUMU)

    def test_segment(self):
        self.assertEqual(len(self.kor.segmentler), SEGMENT)

    def test_benzersiz_kok(self):
        self.assertEqual(len(self.kor.kok_kelimeleri), BENZERSIZ_KOK)

    def test_kok_degerlerinde_satir_sonu_artigi_yok(self):
        # 1.651 artefaktı (03_indices/audits/qac_1651_vs_1642.md) CR/virgül kaynaklıydı.
        for kok in self.kor.kok_kelimeleri:
            self.assertRegex(kok, r"^[A-Za-z$*]+$", kok)

    def test_kurulum_denetimi_gecer(self):
        kalan = [d for d in veri.kurulum_denetimi() if not d.gecti]
        self.assertEqual(kalan, [])


if __name__ == "__main__":
    unittest.main()
