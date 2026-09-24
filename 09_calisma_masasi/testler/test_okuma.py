"""Aşama 2b okuma.py: QAC ↔ Tanzil ayet/kelime eşleşmesi, ayet görünümü, çalışma çevirisi, meal."""

import contextlib
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import _ortak  # noqa: F401
from tezgah import okuma, okunus, veri
from tezgah.__main__ import main


def calistir(argv):
    t = io.StringIO()
    with contextlib.redirect_stdout(t):
        kod = main(argv)
    return kod, t.getvalue()


class KabulTesti(unittest.TestCase):
    """Kabul (CLAUDE.md §7): ayet referansı QAC ve Tanzil'de aynı ayete düşer."""

    def test_ayet_kumeleri_ayni(self):
        qac = {(k.sure, k.ayet) for k in veri.korpus().kelimeler}
        self.assertEqual(qac, set(okunus.tanzil()))
        self.assertEqual(len(qac), 6_236)

    def test_tum_kelime_konumlari_hizalanir(self):
        toplam = hizali = 0
        iskelet_farki, durumlar, birlestirilen = [], {}, 0
        for (s, a), metin in okunus.tanzil().items():
            o = okunus.ayet_oku(s, a, metin)
            eslesmeler, durum = okuma.hizala(s, a, o)
            durumlar[durum] = durumlar.get(durum, 0) + 1
            for e in eslesmeler:
                toplam += 1
                hizali += bool(e.tanzil)
                birlestirilen += len(e.tanzil) > 1
                if not e.iskelet_ayni:
                    iskelet_farki.append(e.kelime.konum)
            kullanilan = [i for e in eslesmeler for i in e.tanzil]
            self.assertEqual(kullanilan, list(range(len(o.kelimeler))), f"{s}:{a} token atlandı/tekrarlandı")
        self.assertEqual(toplam, 77_429)
        self.assertEqual(hizali, 77_429)
        self.assertEqual(durumlar, {"count_match": 6_120, "basmala_offset": 112, "tokenization_difference": 4})
        self.assertEqual(birlestirilen, 4)
        # Tanzil v1.1 ↔ QAC yazım farkları (iskelet düzeyinde); değişirse sebep araştırılır.
        self.assertEqual(sorted(iskelet_farki), ["12:39:1", "12:41:1", "2:72:4"])


class AyetGorunumuTesti(unittest.TestCase):
    def setUp(self):
        self.dizin = Path(tempfile.mkdtemp())
        self.yamalar = [mock.patch.object(okuma, "CEVIRI_YOLU", self.dizin / "cv.tsv"),
                        mock.patch.object(okuma, "MEAL_YOLU", self.dizin / "yok.json")]
        for y in self.yamalar:
            y.start()
        okuma.meal.cache_clear()

    def tearDown(self):
        for y in self.yamalar:
            y.stop()
        okuma.meal.cache_clear()

    def test_2_3(self):
        kod, cikti = calistir(["ayet", "2:3"])
        self.assertEqual(kod, 0)
        self.assertIn("allaẕîna yuʾminûna bilgaybi", cikti)
        self.assertIn("2:3:2  yuʾminûna   Amn (ʾ-m-n)", cikti)
        self.assertIn("2:3:5  ṣṣalâta     Slw (ṣ-l-v)", cikti)
        self.assertIn("Kaynak      : QAC v0.4 | + Tanzil Uthmani v1.1", cikti)
        self.assertIn("Sayım birimi: kelime konumu", cikti)
        self.assertNotIn("Meal", cikti, "meal varsayılan olarak kapalı")
        self.assertIsNone(__import__("re").search("[؀-ۿ]", cikti), "sunumda Arapça harf olmamalı")

    def test_ceviri_ve_meal_sirasi(self):
        okuma.ceviri_ekle("107:4", "ilk sürüm")
        okuma.ceviri_ekle("107:4", "ikinci   sürüm")
        with self.assertRaises(ValueError):
            okuma.ceviri_ekle("107:4", "   ")
        meal_yolu = self.dizin / "meal.json"
        meal_yolu.write_text(json.dumps({"quran": [
            {"chapter": s, "verse": a, "text": okuma.MEAL_PARMAK_IZI.get((s, a), f"M{s}:{a}")}
            for s, a in okunus.tanzil()]}), encoding="utf-8")
        (self.dizin / "manifest.json").write_text(json.dumps(
            {"sha256": hashlib.sha256(meal_yolu.read_bytes()).hexdigest()}), encoding="utf-8")
        with mock.patch.object(okuma, "MEAL_YOLU", meal_yolu), \
                mock.patch.object(okuma, "MEAL_MANIFEST", self.dizin / "manifest.json"):
            okuma.meal.cache_clear()
            _, cikti = calistir(["ayet", "107:4", "--meal"])
        self.assertIn("ikinci sürüm   [", cikti)
        self.assertIn("1 önceki sürüm", cikti)
        self.assertIn("Meal — kurumsal okuma — sınanan, delil değil", cikti)
        self.assertIn(okuma.MEAL_PARMAK_IZI[(107, 4)], cikti)
        self.assertLess(cikti.index("Çalışma çevirisi (kullanıcının yorumu)"), cikti.index("Meal —"),
                        "meal çalışma çevirisinin altında gösterilir")

    def test_meal_parmak_izi(self):
        tam = {"quran": [{"chapter": s, "verse": a, "text": okuma.MEAL_PARMAK_IZI.get((s, a), "x")}
                         for s, a in okunus.tanzil()]}
        self.assertEqual(len(okuma.meal_dogrula(tam)), 6_236)
        for anahtar in okuma.MEAL_PARMAK_IZI:
            with self.subTest(bozuk=anahtar):
                bozuk = {"quran": [dict(r, text="başka meal") if (r["chapter"], r["verse"]) == anahtar else r
                                   for r in tam["quran"]]}
                with self.assertRaises(veri.VeriHatasi):
                    okuma.meal_dogrula(bozuk)
        eksik = {"quran": tam["quran"][:-1]}
        with self.assertRaises(veri.VeriHatasi):
            okuma.meal_dogrula(eksik)

    def test_kurulu_meal_parmak_izi(self):
        gercek = okuma.MASA / "yerel" / "meal" / "tur-diyanetisleri.json"
        if not gercek.exists():
            self.skipTest("meal kurulu değil (python -m tezgah kur meal)")
        m = okuma.meal_dogrula(json.loads(gercek.read_text(encoding="utf-8")))
        self.assertEqual(len(m), 6_236)

    def test_meal_kurulu_degil(self):
        _, cikti = calistir(["ayet", "1:1", "--meal"])
        self.assertIn("meal kurulu değil", cikti)

    def test_hizalamasi_farkli_ayet(self):
        _, cikti = calistir(["ayet", "37:130"])
        self.assertIn("37:130:3  ʾil yâsîn", cikti)
        self.assertIn("2 Tanzil tokenı tek QAC kelimesi", cikti)

    def test_gecersiz_ayet(self):
        kod, cikti = calistir(["ayet", "2:999"])
        self.assertEqual(kod, 2)
        self.assertIn("Durum       : çalıştırılmadı", cikti)


if __name__ == "__main__":
    unittest.main()
