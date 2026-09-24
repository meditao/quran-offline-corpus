"""§6 kök sağlaması: kelime konumu / ayet / sûre (QAC v0.4)."""

import csv
import unittest

import _ortak  # noqa: F401
from tezgah import tara, veri

# CLAUDE.md §6 — (kelime konumu, ayet, sûre)
BEKLENEN = {
    "Slw": (99, 90, 37),
    "fTr": (20, 19, 17),
    "rwH": (57, 52, 40),
    "qdr": (132, 121, 58),
    "gfr": (234, 202, 56),
    "Amn": (879, 723, 77),
}


class KokSaglamaTesti(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kor = veri.korpus()

    def test_alti_kok(self):
        for kok, (kelime, ayet, sure) in BEKLENEN.items():
            with self.subTest(kok=kok):
                s = tara.sayim(self.kor, kok=kok).veri
                self.assertEqual(
                    (s["kelime konumu"], s["ayet"], s["sûre"]), (kelime, ayet, sure)
                )

    def test_root_index_ile_butun_kokler_ayni(self):
        """Aracın kendi hesabı, 03_indices/generated/root_index.csv ile bütün köklerde aynı."""
        hesap = tara.kokler(self.kor).veri["kokler"]
        with veri.ROOT_INDEX_YOLU.open(encoding="utf-8", newline="") as f:
            indeks = {
                r["root_bw"]: (int(r["word_occurrences"]), int(r["ayah_count"]), int(r["surah_count"]))
                for r in csv.DictReader(f)
            }
        self.assertEqual(len(indeks), 1_642)
        self.assertEqual(set(hesap), set(indeks), "kök kümeleri farklı")
        farkli = {k: (hesap[k], indeks[k]) for k in indeks if hesap[k] != indeks[k]}
        self.assertEqual(farkli, {}, "sayımı farklı kökler: (araç, root_index.csv)")

    def test_lemma_index_ile_butun_lemmalar_ayni(self):
        hesap = {l: tara.ozet(ks) for l, ks in self.kor.lemma_kelimeleri.items()}
        with veri.LEMMA_INDEX_YOLU.open(encoding="utf-8", newline="") as f:
            indeks = {
                r["lemma_bw"]: (int(r["word_occurrences"]), int(r["ayah_count"]), int(r["surah_count"]))
                for r in csv.DictReader(f)
            }
        self.assertEqual(set(hesap), set(indeks), "lemma kümeleri farklı")
        farkli = {
            l: ((o["kelime konumu"], o["ayet"], o["sûre"]), indeks[l])
            for l, o in hesap.items() if (o["kelime konumu"], o["ayet"], o["sûre"]) != indeks[l]
        }
        self.assertEqual(farkli, {}, "sayımı farklı lemmalar: (araç, lemma_index.csv)")


if __name__ == "__main__":
    unittest.main()
