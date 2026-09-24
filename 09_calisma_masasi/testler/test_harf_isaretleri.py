"""Hemze ve ayn işaretleri: çıktıda U+02BE (ʾ) ve U+02BF (ʿ) kullanılır; düz kesme (U+0027) ya da ona benzeyen
işaretler (’ ʼ ʻ ` ´) kök gösteriminde ve okunuşta hiç geçmez (CLAUDE.md §2.8)."""

import contextlib
import io
import unittest

import _ortak  # noqa: F401
from tezgah import okunus, veri
from tezgah.__main__ import main
from tezgah.harf import HARF_LATIN

HEMZE, AYN = "ʾ", "ʿ"
BENZERLER = {"'": "düz kesme", "’": "sağ tek tırnak", "ʼ": "harf kesmesi",
             "ʻ": "ters virgül harfi", "`": "ters kesme", "´": "akut"}


def calistir(*argv):
    t = io.StringIO()
    with contextlib.redirect_stdout(t):
        main(list(argv))
    return t.getvalue()


def benzer_var(metin: str) -> list[str]:
    return [f"U+{ord(c):04X} {ad}" for c, ad in BENZERLER.items() if c in metin]


class HarfTablosu(unittest.TestCase):
    def test_hemze_ve_ayn_kod_noktasi(self):
        self.assertEqual(HARF_LATIN["ء"], HEMZE)
        self.assertEqual(HARF_LATIN["ع"], AYN)
        for ar, lat in HARF_LATIN.items():
            with self.subTest(harf=ar):
                self.assertEqual(benzer_var(lat), [])

    def test_butun_kokler(self):
        kokler = list(veri.korpus().kok_kelimeleri)
        self.assertEqual(len(kokler), 1_642)
        for k in kokler:
            latin = veri.kok_latin(k)
            with self.subTest(kok=k):
                self.assertEqual(benzer_var(latin), [])
                self.assertEqual("A" in k, HEMZE in latin)
                self.assertEqual("E" in k, AYN in latin)

    def test_butun_ayet_okunuslari_ve_lemmalar(self):
        hemze = ayn = 0
        for (s, a) in okunus.tanzil():
            o = okunus.oku(s, a)
            metin = " ".join(k.latin for k in o.besmele + o.kelimeler)
            self.assertEqual(benzer_var(metin), [], f"{s}:{a}")
            hemze += metin.count(HEMZE)
            ayn += metin.count(AYN)
        self.assertGreater(hemze, 0)
        self.assertGreater(ayn, 0)
        for x in {x for k in veri.korpus().kelimeler for x in k.lemmalar}:
            self.assertEqual(benzer_var(okunus.lemma_okunusu(x).latin), [], x)


class KomutCiktisi(unittest.TestCase):
    """ʾ-m-n, ʿ-l-m ve ʾ-n-s komut çıktısında doğru kod noktasıyla yazılır."""

    def test_uc_kok(self):
        for bw, latin in (("Amn", "ʾ-m-n"), ("Elm", "ʿ-l-m"), ("Ans", "ʾ-n-s")):
            c = calistir("kok", bw, "--limit", "20")
            with self.subTest(kok=bw):
                self.assertIn(f"Kök: {bw} ({latin})", c)
                tablo = [s for s in c.splitlines() if s[:1].isdigit()]
                self.assertTrue(tablo)
                for satir in tablo:
                    self.assertEqual(benzer_var(satir), [], satir)
        self.assertIn(AYN, calistir("kok", "Elm", "--limit", "3").split("Geçişler", 1)[1])
        self.assertIn(HEMZE, calistir("kok", "Amn", "--limit", "3").split("Geçişler", 1)[1])


if __name__ == "__main__":
    unittest.main()
