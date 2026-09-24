"""Aşama 4: quran-morphology ikinci annotation katmanı ve konum bazında çapraz denetim.

Veriye bağlı testler yerel/quran-morphology kuruluysa çalışır (python -m tezgah kur quran-morphology);
kurulu değilse atlanır. Nötrleme ve CRLF ayrıştırması her zaman sınanır.
"""

import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

import _ortak  # noqa: F401
from tezgah import qm, veri
from tezgah.__main__ import main

DEPO = _ortak.MASA.parent
BETIK = DEPO / "08_scripts" / "crosscheck_qac_quranmorphology.py"
AUDIT = DEPO / "03_indices" / "audits"


def betik():
    spec = importlib.util.spec_from_file_location("crosscheck_qm", BETIK)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def kurulu():
    return qm.QM_YOLU.exists()


class NotrlemeVeAyristirma(unittest.TestCase):
    def test_hemze_notrleme(self):
        for a, b in (("أمن", "امن"), ("ءمن", "أمن"), ("سأل", "سءل"), ("بوأ", "بوء"), ("نشأ", "نشئ")):
            self.assertEqual(qm.notr(a), qm.notr(b))
        self.assertNotEqual(qm.notr("طمن"), qm.notr("طمءن"))
        self.assertEqual(qm.qac_notr("Amn"), qm.notr("أمن"))
        self.assertEqual(qm.arapca_latin("طمءن"), "ṭ-m-ʾ-n")

    def test_crlf_ve_lf_ayni_ayristirilir(self):
        # ROOT satırın son özelliği: QAC'taki tarihsel CR artefaktı bu durumda oluşuyordu.
        satirlar = ["1:1:1:1\tبِ\tP\tP|PREF|LEM:ب", "1:1:1:2\tسْمِ\tN\tLEM:اسْم|M|GEN|ROOT:سمو"]
        sonuclar = []
        for son in ("\n", "\r\n"):
            yol = Path(tempfile.mkdtemp()) / "q.txt"
            yol.write_bytes((son.join(satirlar) + son).encode("utf-8"))
            k = qm.ayristir(yol)
            sonuclar.append((k.segment, dict(k.kokler), k.ham_kokler))
        self.assertEqual(sonuclar[0], sonuclar[1])
        self.assertEqual(sonuclar[0][2], {"سمو"}, "kök değerinde \\r kalmamalı")


class SayiFarkiUyarisi(unittest.TestCase):
    """Depodaki audit TSV'lerinden beslenir; yerel veri gerekmez (CI'da da çalışır)."""

    def cikti(self, argv):
        t = io.StringIO()
        with contextlib.redirect_stdout(t):
            kod = main(argv)
        return kod, t.getvalue()

    def test_farkli_kokler_uyari_basar(self):
        import csv
        with (AUDIT / "qac_quranmorphology_kok_sayilari.tsv").open(encoding="utf-8", newline="") as f:
            satirlar = list(csv.DictReader(f, delimiter="\t"))
        self.assertEqual(len(satirlar), 34)
        qac_kokleri = [r["qac_kok_bw"] for r in satirlar if r["qac_kok_bw"] != "—"]
        self.assertEqual(len(qac_kokleri), 21)
        for kok in qac_kokleri:
            with self.subTest(kok=kok):
                kod, c = self.cikti(["sayim", "--kok", kok])
                self.assertEqual(kod, 0)
                self.assertTrue(c.startswith("UYARI (çapraz kontrol — quran-morphology, delil değil)"), c[:80])

    def test_ans_ve_nws(self):
        _, c = self.cikti(["sayim", "--kok", "Ans"])
        self.assertIn("QAC 97, quran-morphology 338", c)
        self.assertIn("QAC bu konumları nws (n-v-s) köküne bağlar (QAC lemma: n~aAs) — bu 241 konum QAC sonucunda yok", c)
        _, c = self.cikti(["kok", "nws", "--limit", "1"])
        self.assertIn("QAC'ın bu köke bağladığı 241 konumu quran-morphology ʾ-n-s köküne bağlar", c)

    def test_farksiz_kokte_uyari_yok(self):
        for kok in ("Slw", "Amn", "gfr"):
            with self.subTest(kok=kok):
                self.assertNotIn("çapraz kontrol", self.cikti(["sayim", "--kok", kok])[1])

    def test_yalniz_qm_kokunde_hata_notu(self):
        kod, c = self.cikti(["sayim", "--kok", "Adm"])
        self.assertEqual(kod, 2)
        self.assertIn("QAC'ta bu kök yok, ama quran-morphology'de var", c)
        self.assertIn("QAC 0, quran-morphology 25", c)


@unittest.skipUnless(kurulu(), "quran-morphology kurulu değil (python -m tezgah kur quran-morphology)")
class CaprazDenetim(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.h = betik().hesapla()

    def test_beklenen_degerler(self):
        o = self.h["ozet"]
        self.assertEqual(o["olcum"], {
            "kelime_konumu_qac": 77_429, "kelime_konumu_qm": 77_429,
            "segment_qm": 130_030, "segment_qac": 128_219,
            "kok_qm": 1_651, "kok_qac": 1_642,
            "notr_ortak": 1_638, "notr_yalniz_qm": 13, "notr_yalniz_qac": 4,
        })
        self.assertTrue(o["ek"]["konum_kumeleri_ayni"])
        self.assertEqual((o["ek"]["notr_carpisma_qac"], o["ek"]["notr_carpisma_qm"]), (0, 0))

    def test_crlf_tuzagi(self):
        ek = self.h["ozet"]["ek"]
        self.assertEqual(ek["qac_crlf_satir"], ek["qac_toplam_satir"])
        self.assertEqual((ek["qac_kok_satir_sonu_soyulmadan"], ek["qac_kok_soyulunca"]), (1_652, 1_642))
        self.assertEqual(ek["qm_cr"], 0)
        # eski kabuk denetimiyle tutarlılık: 1.651 / 1.641 ↔ 1.652 / 1.642, aynı 10 CR'li değer, fark wAd
        self.assertEqual((ek["kabuk_ham"], ek["kabuk_cr_soyulunca"]), (1_651, 1_641))
        self.assertEqual(ek["cr_li_kokler"], ek["kabuk_cr_li_kokler"])
        self.assertEqual(len(ek["cr_li_kokler"]), 10)
        self.assertEqual(ek["kabuk_eksik"], ["wAd"])

    def test_konum_toplamlari_tutarli(self):
        o = self.h["ozet"]
        self.assertEqual(sum(o["kok_atamasi"].values()), 77_429)
        self.assertEqual(len(self.h["farklar"]), 77_429 - o["kok_atamasi"]["aynı"])
        fark = sum(int(k) * v for k, v in o["segment_farki_dagilimi"].items())
        self.assertEqual(fark, o["olcum"]["segment_qm"] - o["olcum"]["segment_qac"])

    def test_rapor_yeniden_uretilebilir(self):
        """Depodaki audit dosyaları betiğin güncel çıktısıyla birebir aynı."""
        self.assertEqual(json.loads((AUDIT / "qac_quranmorphology.json").read_text(encoding="utf-8")), self.h["ozet"])
        self.assertEqual((AUDIT / "qac_quranmorphology.md").read_text(encoding="utf-8"), "\n".join(self.h["md"]))
        tsv = (AUDIT / "qac_quranmorphology_kok_farklari.tsv").read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(tsv) - 1, len(self.h["farklar"]))

    def test_capraz_bayragi(self):
        cikti = {}
        for kok in ("Slw", "nws"):
            t = io.StringIO()
            with contextlib.redirect_stdout(t):
                self.assertEqual(main(["sayim", "--kok", kok, "--capraz"]), 0)
            cikti[kok] = t.getvalue()
        self.assertIn("Kök ataması farklı kelime konumları: 0", cikti["Slw"])
        self.assertIn("iki sayının aynı çıkması doğrulama sayılmaz", cikti["Slw"])
        self.assertIn("Kaynak      : QAC v0.4 | + quran-morphology", cikti["Slw"])
        self.assertIn(f"Veri izi    : {veri.QAC_SHA256[:12]} | {qm.QM_SHA256[:12]}", cikti["Slw"])
        self.assertIn("quran-morphology — kök (bu kök yok)", cikti["nws"])
        self.assertIn("Kök ataması farklı kelime konumları: 241", cikti["nws"])
        t = io.StringIO()
        with contextlib.redirect_stdout(t):
            self.assertEqual(main(["sayim", "--etiket", "INDEF", "--capraz"]), 2)


if __name__ == "__main__":
    unittest.main()
