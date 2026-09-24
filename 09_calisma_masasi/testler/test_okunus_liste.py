"""Tarama listelerinde Latin okunuş: biçim = ayet içindeki okunuş, lemma = bağlamsız lemma okunuşu
(okunus_kurallari.md §6). Buckwalter yalnız --bw ile, ek sütun olarak."""

import contextlib
import io
import re
import unittest

import _ortak  # noqa: F401
from tezgah import okuma, okunus, veri
from tezgah.__main__ import main


def calistir(*argv):
    t = io.StringIO()
    with contextlib.redirect_stdout(t):
        kod = main(list(argv))
    return kod, t.getvalue()


def tablo_satiri(cikti: str, konum: str) -> str:
    return next(s for s in cikti.splitlines() if s.startswith(konum + " "))


class LemmaOkunusu(unittest.TestCase):
    ORNEKLER = {
        "Salaw`p": "ṣalât",          # kural 3: ة t kalır (vakf biçimi ṣalâh değil)
        "<insa`n": "ʾinsân",         # kural 5: kelime başı hemze yazılır (§1)
        "{som": "ism",               # kural 1: vasl elifi ibtidâ ile
        "qaAla": "qâla",             # kural 2: yazıldığı harekelerle
        "A^dam": "ʾâdam",            # kural 6: QAC A^ = Tanzil ءَا
        "{ll~ah": "allâh",           # kural 7
        "m~ula`quwA": "mulâqû",      # kural 8
        "hudFY": "hudâ",             # kural 4: ى üzerinde fetha tenvini â
        ">abN": "ʾab",               # kural 4: zamme tenvini düşer
        "<i*FA": "ʾiẕan",            # kural 4: ـًا kalır
        "nasofaEF[": "nasfaʿan",     # kural 9: sondaki iklab yok sayılır
        ">an[ba>a": "ʾambaʾa",       # kural 9: kelime içi iklab uygulanır
        "EaSaA2": "ʿaṣâ (2)",        # kural 10
    }

    def test_ornekler(self):
        for bw, beklenen in self.ORNEKLER.items():
            with self.subTest(bw=bw):
                self.assertEqual(okunus.lemma_okunusu(bw).gosterim, beklenen)

    def test_butun_lemmalar_hatasiz(self):
        lemmalar = sorted({x for k in veri.korpus().kelimeler for x in k.lemmalar})
        self.assertEqual(len(lemmalar), 4_832)
        belirsiz = [x for x in lemmalar if okunus.lemma_okunusu(x).belirsiz]
        self.assertEqual(len(belirsiz), 6, belirsiz)        # okunus_kurallari.md §6 son paragraf
        for x in lemmalar:
            latin = okunus.lemma_okunusu(x).latin
            self.assertTrue(latin, x)
            self.assertIsNone(re.search(r"[A-Z`{}~^#<>&*$\[\]؀-ۿ]", latin), (x, latin))


class ListeSutunlari(unittest.TestCase):
    def test_varsayilan_latin(self):
        _, c = calistir("kok", "Slw", "--limit", "3")
        self.assertIn("biçim (ayet içinde okunuş)", c)
        self.assertIn("lemma (okunuş)", c)
        satir = tablo_satiri(c, "2:3:5")
        self.assertIn("ṣṣalâta", satir)
        self.assertIn("ṣalât", satir)
        self.assertNotIn("Buckwalter", c)
        self.assertNotIn("Salaw`p", c)
        self.assertNotIn("{lS~alaw", c)

    def test_bw_ek_sutun(self):
        _, c = calistir("kok", "Slw", "--limit", "3", "--bw")
        self.assertIn("biçim (Buckwalter)", c)
        self.assertIn("lemma (Buckwalter)", c)
        satir = tablo_satiri(c, "2:3:5")
        self.assertIn("ṣṣalâta", satir)          # Latin sütun yerinde kalır
        self.assertIn("Salaw`p", satir)
        self.assertIn("{lS~alaw`pa", satir)

    def test_ayet_gorunumuyle_ayni_okunus(self):
        _, ayet = calistir("ayet", "2:3")
        for kno in range(1, 6):
            latin, not_ = okuma.konum_okunusu(2, 3, kno)
            with self.subTest(kelime=kno):
                self.assertEqual(not_, "")
                self.assertIn(latin, tablo_satiri(ayet, f"  2:3:{kno}").strip())

    def test_hizalama_farki_notu(self):
        notlu = {}
        for (s, a) in okunus.tanzil():
            for kno, (latin, not_) in okuma._ayet_okunus_haritasi(s, a).items():
                if not_:
                    notlu[f"{s}:{a}:{kno}"] = not_
        self.assertEqual(len(notlu), 7, notlu)                 # okunus_kurallari.md §6
        self.assertEqual(notlu["2:181:3"], "2 Tanzil tokenı = 1 QAC kelimesi")
        self.assertEqual(notlu["2:72:4"], "Tanzil↔QAC yazım farkı")
        _, c = calistir("kok", "bEd", "--limit", "0")
        self.assertIn("baʿda mâ [not: 2 Tanzil tokenı = 1 QAC kelimesi]", tablo_satiri(c, "2:181:3"))

    def test_etiket_kalip_dagilim(self):
        _, c = calistir("etiket", "ROOT:Slw", "--limit", "2")
        self.assertIn("kelime (ayet içinde okunuş)", c)
        self.assertNotIn("segment (Buckwalter)", c)
        _, c = calistir("etiket", "ROOT:Slw", "--limit", "2", "--bw")
        self.assertIn("segment (Buckwalter)", c)
        _, c = calistir("kalip", "ROOT:Slw", "--limit", "2")
        self.assertIn("TAG dizisi", c)
        self.assertNotIn("Buckwalter", c)
        _, c = calistir("dagilim", "--kok", "Slw", "--gore", "lemma")
        self.assertIn("ṣalât", c)
        self.assertNotIn("Salaw`p", c)
        _, c = calistir("dagilim", "--kok", "Slw", "--gore", "lemma", "--bw")
        self.assertIn("Salaw`p", c)

    def test_lemma_basligi(self):
        _, c = calistir("lemma", "Salaw`p", "--limit", "1")
        self.assertIn("Lemma: ṣalât (QAC: Salaw`p)", c)


if __name__ == "__main__":
    unittest.main()
