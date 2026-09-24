"""Aşama 2b kavram.py: dosya düzeni, gömülü sorgular, zorunlu öneri alanları, denetim."""

import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import _ortak  # noqa: F401
from tezgah import kavram, okuma

TAM = dict(anlam="Deneme önerisi", ic_tanim="iç-tanım yok", falsifikasyon="şu kullanım çürütürdü",
           bulunan_ayetler="107:4", muhalif="en güçlü muhalif okuma", kurulan_orneklem="isim kullanımları",
           uygulanan_orneklem="fiil kullanımları", mantiksal_durum="Yalnız uyumlu", delil_derecesi="Muhtemel")


class KavramTesti(unittest.TestCase):
    def setUp(self):
        self.dizin = Path(tempfile.mkdtemp())
        self.yamalar = [mock.patch.object(kavram, "KAVRAMLAR", self.dizin),
                        mock.patch.object(okuma, "CEVIRI_YOLU", self.dizin / "cv.tsv")]
        for y in self.yamalar:
            y.start()
        kavram.ac("deneme", "Araştırma sorusu?", ["Slw"])
        self.yol = self.dizin / "deneme" / "kavram.md"

    def tearDown(self):
        for y in self.yamalar:
            y.stop()

    def metin(self):
        return self.yol.read_text(encoding="utf-8")

    def test_duzen_ve_bolum_kayitlari(self):
        m = self.metin()
        konumlar = [m.index(f"<!-- tezgah:bolum {a} -->") for a, _ in kavram.BOLUMLER]
        self.assertEqual(konumlar, sorted(konumlar), "bölümler standart sırada")
        for _, baslik in kavram.BOLUMLER:
            self.assertIn(f"## {baslik}", m)
        self.assertEqual(m.count("<!-- tezgah:bolum-kaydi -->"), len(kavram.BOLUMLER))
        self.assertIn("hipotez / ikincil, delil değil", m)

    def test_asama1_sorgudan_uretilir(self):
        m = self.metin()
        self.assertEqual(m.count("<!-- tezgah:sorgu "), 4)
        self.assertIn("kelime konumu: 99 | ayet: 90 | sûre: 37", m)       # §6 Slw
        self.assertIn("Sorgu       : python -m tezgah dagilim --kok Slw --gore bab", m)
        self.assertIn("Sorgu       : 4 sorgu", m)

    def test_latin_kok_ve_yasak_sorgular(self):
        from tezgah.tara import GirdiHatasi
        with self.assertRaises(GirdiHatasi):
            kavram.ac("latin", "soru", ["s-l-v"])
        with self.assertRaises(kavram.KavramHatasi):
            kavram.sorgu_ekle("deneme", "kritik", ["ayet", "107:4", "--meal"])
        for yasak in (["test"], ["kur", "meal"], ["ceviri", "1:1", "x"], ["kavram", "yenile", "deneme"]):
            with self.assertRaises(kavram.KavramHatasi):
                kavram.sorgu_ekle("deneme", "asama2", yasak)
        with self.assertRaises(kavram.KavramHatasi):
            kavram.ac("deneme", "soru", ["Slw"])   # üzerine yazmaz

    def test_oneri_zorunlu_alanlar(self):
        for alan in ("anlam", "ic_tanim", "falsifikasyon", "muhalif", "kurulan_orneklem",
                     "uygulanan_orneklem", "bulunan_ayetler"):
            with self.subTest(bos=alan):
                with self.assertRaises(kavram.KavramHatasi):
                    kavram.oneri_ekle("deneme", **{**TAM, alan: "  "})
        with self.assertRaises(kavram.KavramHatasi):
            kavram.oneri_ekle("deneme", **{**TAM, "mantiksal_durum": "Doğru"})
        with self.assertRaises(kavram.KavramHatasi):
            kavram.oneri_ekle("deneme", **{**TAM, "delil_derecesi": "Kesin"})
        with self.assertRaises(kavram.KavramHatasi):
            kavram.oneri_ekle("deneme", **{**TAM, "bulunan_ayetler": "yok"})   # tarama belirtilmeli
        from tezgah.tara import GirdiHatasi
        with self.assertRaises(GirdiHatasi):
            kavram.oneri_ekle("deneme", **{**TAM, "bulunan_ayetler": "2:999"})
        self.assertEqual(json.loads((self.dizin / "deneme" / "oneriler.json").read_text()), [])

    def test_oneri_eklenir_eskisi_silinmez(self):
        kavram.oneri_ekle("deneme", **{**TAM, "mantiksal_durum": "yalniz uyumlu", "delil_derecesi": "spekülatif"})
        kavram.oneri_ekle("deneme", **{**TAM, "anlam": "İkinci öneri", "bulunan_ayetler": "yok",
                                       "bulunan_sorgu": "kalip ROOT:Slw&POS:V",
                                       "mantiksal_durum": "Destek gösterilemedi"})
        kayitlar = json.loads((self.dizin / "deneme" / "oneriler.json").read_text())
        self.assertEqual([k["mantiksal_durum"] for k in kayitlar], ["Yalnız uyumlu", "Destek gösterilemedi"])
        self.assertEqual(kayitlar[0]["delil_derecesi"], "Spekülatif")
        m = self.metin()
        self.assertIn("#### Öneri 1", m)
        self.assertIn("#### Öneri 2", m)
        self.assertIn("yok — tarama: kalip ROOT:Slw&POS:V", m)
        self.assertIn("**Son öneri (Öneri 2):** İkinci öneri", m)

    def test_denetle_ve_yenile(self):
        self.assertEqual(kavram.denetle("deneme"), ([], []))
        m = self.metin().replace("kelime konumu: 99 | ayet: 90", "kelime konumu: 98 | ayet: 90", 1)
        m = m.replace("## 8. Sentez ve anlam önerileri\n",
                      "## 8. Sentez ve anlam önerileri\n\nKök 99 kez geçer; bkz. 2:3 ve 107:4.\n", 1)
        self.yol.write_text(m, encoding="utf-8")
        hatalar, uyarilar = kavram.denetle("deneme")
        self.assertEqual(len(hatalar), 1)
        self.assertIn("sayim --kok Slw", hatalar[0])
        self.assertEqual(uyarilar, ["[sentez] sorgu dışında sayı: 99 (sayımlar sorgudan gömülmeli)"])
        kavram.yenile("deneme")
        hatalar, uyarilar = kavram.denetle("deneme")
        self.assertEqual(hatalar, [])
        self.assertIn("Kök 99 kez geçer; bkz. 2:3 ve 107:4.", self.metin(), "elle yazılan metin korunur")

    def test_ayet_gomme_calisma_cevirisi_meal_yok(self):
        kavram.sorgu_ekle("deneme", "kritik", ["ayet", "107:4"])
        self.assertIn("— (yok; eklemek için", self.metin())
        okuma.ceviri_ekle("107:4", "çalışma çevirisi denemesi")
        kavram.yenile("deneme")
        m = self.metin()
        self.assertIn("çalışma çevirisi denemesi", m)
        self.assertNotIn("Meal", m)
        self.assertIsNone(re.search("[؀-ۿ]", m), "kavram dosyasında Arapça harf olmamalı")


if __name__ == "__main__":
    unittest.main()
