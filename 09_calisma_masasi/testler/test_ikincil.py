"""Aşama 5: ikincil katmanlar (Lane, Sâmî) — hipotez etiketi, katman kuralları, ölçümlerin yeniden üretilmesi.

Lane ve SEDRA verisi yerel/ altındadır (depoya işlenmez); kurulu değilse o testler atlanır.
İbranice dizin ve incelenmiş kognatlar depodadır; o testler her zaman çalışır.
"""

import contextlib
import importlib.util
import io
import json
import unittest

import _ortak  # noqa: F401
from tezgah import veri
from tezgah.__main__ import main
from tezgah.ikincil import etiketle, lane, sami

DEPO = _ortak.MASA.parent
AUDIT = DEPO / "03_indices" / "audits"


def calistir(argv):
    t = io.StringIO()
    with contextlib.redirect_stdout(t):
        kod = main(argv)
    return kod, t.getvalue()


def icerik_satirlari(cikti):
    """Kayıt bloğundan önceki boş olmayan satırlar."""
    return [s for s in cikti.split("-" * 60)[0].splitlines() if s.strip()]


class VeridenBagimsiz(unittest.TestCase):
    def test_etiketle(self):
        self.assertEqual(etiketle(["a", "", "b"]), ["[hipotez] a", "", "[hipotez] b"])

    def test_denklik_tablolari_tam(self):
        from tezgah.harf import HARF_LATIN
        arapca = {a for a in HARF_LATIN if a not in "أإؤئىة"}
        self.assertEqual(set(sami.IBRANICE_DENKLIK), arapca)
        self.assertEqual(set(sami.SURYANICE_DENKLIK), arapca)
        for kodlar in sami.SURYANICE_DENKLIK.values():
            self.assertTrue(set(kodlar) <= set(sami.SEDRA_LATIN))

    def test_ibranice_normallestirme(self):
        self.assertEqual(sami.ibranice_normal("מֶלֶךְ"), "מלכ")
        self.assertEqual(sami.ibranice_normal("אָרֶץ"), "ארצ")

    def test_ibranice_dizini_yerinde_okunur(self):
        self.assertEqual(sami.IBRANICE_YOLU, DEPO / "04_lexicons" / "generated" / "hebrew_lexical_index.tsv")
        self.assertEqual(list(_ortak.MASA.rglob("hebrew_lexical_index*")), [], "İbranice dizin kopyalanmamalı")
        self.assertGreater(len(sami.ibranice()), 1000)

    def test_incelenmis_kognat_ve_etiket(self):
        kod, c = calistir(["sami", "kok", "Amn"])
        self.assertEqual(kod, 0)
        self.assertIn("İncelenmiş kayıt (04_lexicons/semitic/cognates.tsv): Hebrew ʾ-m-n", c)
        self.assertIn("Kognat anlam değildir", c)
        for s in icerik_satirlari(c):
            self.assertTrue(s.startswith("[hipotez"), s)
        self.assertIn("Kaynak      : QAC v0.4 | + Sâmî", c)

    def test_latin_kok_girisi_reddedilir(self):
        self.assertEqual(calistir(["sami", "kok", "s-l-v"])[0], 2)
        self.assertEqual(calistir(["lane", "kok", "s-l-v"])[0], 2)


@unittest.skipUnless(sami.sedra_kurulu(), "SEDRA kurulu değil (python -m tezgah kur sedra)")
class SamiKatmani(unittest.TestCase):
    def test_tek_dil_vurusu_tek_basina_raporlanmaz(self):
        heb, sur = sami.vurus(sami.qac_harfleri("Elm"))
        self.assertTrue(heb and not sur)
        _, c = calistir(["sami", "kok", "Elm"])
        self.assertIn("tek dil vuruşu tek başına raporlanmaz", c)
        self.assertNotIn("  İbranice ", c, "tek dil adayları --tek-dil olmadan gösterilmez")
        _, c = calistir(["sami", "kok", "Elm", "--tek-dil"])
        self.assertIn("  İbranice ", c)

    def test_iki_dil_ve_son_zayif(self):
        _, c = calistir(["sami", "kok", "Slw"])
        self.assertIn("İki dilde aday var", c)
        self.assertIn("İbranice ṣ-l-h", c)     # lamed-he yazımı
        self.assertIn("Süryanice ṣ-l-ʾ", c)    # Alef yazımı
        for s in icerik_satirlari(c):
            self.assertTrue(s.startswith("[hipotez"), s)

    def test_sedra_degismemis_olmali(self):
        for ad, sha in sami.SEDRA_DOSYALARI.items():
            self.assertEqual(veri.sha256(sami.SEDRA_DIZINI / ad), sha)
        self.assertEqual(sami.sedra_bagsiz(), {"LEXEMES.TXT": 36, "ENGLISH.TXT": 229})

    def test_gurultu_yeniden_uretilebilir(self):
        g = sami.gurultu(10, 20260924)
        self.assertEqual(g["kok"], 1_642)
        for dil in ("ibranice", "suryanice", "ikisi"):
            self.assertLess(g["rastgele"][dil]["ortalama"], g["gercek"][dil])
        if (AUDIT / "ikincil_katmanlar.json").exists():
            kayitli = json.loads((AUDIT / "ikincil_katmanlar.json").read_text(encoding="utf-8"))
            self.assertEqual(kayitli["sami_gurultu"], json.loads(json.dumps(g)))


@unittest.skipUnless(lane.LANE_YOLU.exists(), "Lane kurulu değil (python -m tezgah kur lane)")
class LaneKatmani(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.k = lane.kapsam(veri.korpus())

    def test_kapsam_toplami(self):
        self.assertEqual(sum(self.k["eslesme"].values()), 1_642)
        self.assertEqual((self.k["lane_kok"], self.k["lane_madde"]), (5_160, 47_919))
        a, b = self.k["bolge_yogunluk"]["ا-ق"], self.k["bolge_yogunluk"]["ك-ي (seyrek)"]
        self.assertGreater(a, b, "ك sonrası seyrelme ölçümde görünmeli")

    def test_kayitli_olcum_ayni(self):
        kayitli = json.loads((AUDIT / "ikincil_katmanlar.json").read_text(encoding="utf-8"))["lane_kapsam"]
        taze = json.loads(json.dumps({**self.k, "zayif": [list(z) for z in self.k["zayif"]]}))
        self.assertEqual(kayitli, taze)

    def test_zayif_eslesme_dogrula_ister(self):
        for kok, _ in self.k["zayif"][:3]:
            with self.subTest(kok=kok):
                self.assertIn("<< DOĞRULA", calistir(["lane", "kok", kok])[1])
        self.assertEqual(lane.eslestir("mrA")[1], "zayıf: son hemze düşürüldü")

    def test_yokluk_bulgu_degil_ve_seyrek_bolge(self):
        _, c = calistir(["lane", "kok", "khf"])
        self.assertIn("bu bir bulgu değildir", c)
        self.assertIn("yokluk argümanı kurulamaz", c)

    def test_harekeli_kok_tablosu(self):
        self.assertEqual(lane.eslestir("jhl")[1], "tam")

    def test_isaretler_ve_etiket(self):
        _, c = calistir(["lane", "kok", "Slw"])
        self.assertIn("tefsir: Bd", c)
        self.assertIn("Kur'an atfı — dairesellik riski", c)
        self.assertIn("Dairesellik", c)
        for s in icerik_satirlari(c):
            self.assertTrue(s.startswith("[hipotez"), s)
        self.assertIsNone(__import__("re").search("[؀-ۿ]", c), "sunumda Arapça harf olmamalı")


if __name__ == "__main__":
    unittest.main()
