"""Aşama 7: klasik kök sözlükleri (İbn Fâris Mekâyîs, Râgıb Müfredât) — hipotez katmanı.

Veri yerel/klasik/ altındadır (depoya işlenmez; OpenITI CC BY-NC-SA 4.0); kurulu değilse veriye bağlı testler
atlanır. Ayrıştırıcı, etiketleme ve eşleştirme kuralları veriden bağımsız sınanır.

Ölçülmüş beklenen değerler (QAC v0.4'ün 1.642 köküne göre, `klasik kapsam`) test kırılırsa değiştirilmez;
önce sebep bulunur ve raporlanır.
"""

import contextlib
import io
import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import _ortak  # noqa: F401
from tezgah import veri
from tezgah.__main__ import main
from tezgah.ikincil import klasik
from tezgah.ikincil import klasik_ayristir as ay

KURULU = klasik.yukle() is not None

# Ölçüm: python -m tezgah klasik kapsam (QAC v0.4, birim: kök)
KAPSAM = {"ibnfaris": dict(madde=4649, kesin=1560, zayif=33, yok=49),
          "ragib": dict(madde=1662, kesin=1522, zayif=16, yok=104)}


def calistir(argv):
    t = io.StringIO()
    with contextlib.redirect_stdout(t):
        kod = main(argv)
    return kod, t.getvalue()


def icerik_satirlari(cikti):
    """Kayıt bloğundan önceki boş olmayan satırlar."""
    return [s for s in cikti.split("-" * 60)[0].splitlines() if s.strip()]


class AyristiriciKurallari(unittest.TestCase):
    def test_hareke_regex_harf_silmez(self):
        # Regresyon: aralık uçları yer değiştirince TASH bütün Arapça harfleri siliyordu.
        for harf in "ابتثجحخدذرزسشصضطظعغفقكلمنهوي":
            self.assertEqual(ay.TASH.sub("", harf), harf, harf)
        self.assertEqual(ay.TASH.sub("", "صَلَاةٌ"), "صلاة")
        self.assertEqual(ay.TASH.sub("", "الله"), "الله")

    def test_norm(self):
        self.assertEqual(ay.norm("صَلاة"), "صلاه")
        self.assertEqual(ay.norm("أَمَنَ"), "امن")
        self.assertEqual(ay.norm("هدى"), "هدي")

    def test_baslik_latin_elif_kurali(self):
        self.assertEqual(klasik.baslik_latin("صلا"), "ṣ-l-â")     # son elif illetli harf, hemze değil
        self.assertEqual(klasik.baslik_latin("أمن"), "ʾ-m-n")     # hemzeli kök
        self.assertEqual(klasik.baslik_latin("ابل"), "ʾ-b-l")     # ilk yalın elif hemzedir
        self.assertEqual(klasik.baslik_latin("فطر"), "f-ṭ-r")     # ط/ت ayrımı korunur
        self.assertNotEqual(klasik.baslik_latin("سلو"), klasik.baslik_latin("صلو"))

    def test_eslestir_kesin_ve_zayif(self):
        idx = {"صلو": 1, "صلي": 1, "مد": 1, "قل": 1, "قرا": 1}
        kurallar = lambda kok: [(k.split(" ")[0], a) for k, a in ay.eslestir(idx, kok)]
        self.assertEqual(kurallar("صلو"), [("birebir", "صلو"), ("illetli", "صلي")])   # vâvî/yâî çift madde
        self.assertEqual(kurallar("زكو"), [], "idx'te olmayan kök boş döner")
        self.assertEqual(ay.eslestir({"صلو": 1}, "صلو"), [("birebir", "صلو")])
        self.assertTrue(all(not k.startswith("ZAYIF") for k, _ in ay.eslestir(idx, "صلي")))
        self.assertEqual(ay.eslestir(idx, "مدد")[0][1], "مد")           # mudâaf
        z = ay.eslestir({"قل": 1}, "قول")                                # orta illetli düşürüldü
        self.assertTrue(z and z[0][0].startswith("ZAYIF"))
        self.assertEqual(ay.eslestir({"abc": 1}, "صلو"), [])             # eşleşme yoksa boş

    def test_anahtarlar_ibn_faris_cift_yazim(self):
        self.assertEqual(ay.anahtarlar("بلوي", "ibnfaris"), {"بلوي", "بلو", "بلي"})
        self.assertEqual(ay.anahtarlar("بلوي", "ragib"), {"بلوي"})


class EtiketlemeKurallari(unittest.TestCase):
    def test_her_etiketin_deseni_derlenir_ve_aciklamasi_var(self):
        for ad, (acik, desen) in klasik.ETIKET.items():
            self.assertTrue(acik and re.compile(desen), ad)

    def test_hadis_ile_rivayet_ayrilir(self):
        self.assertEqual(klasik.birim_etiketle("وقال عليه السلام: إذا دعي أحدكم", "ragib").count("HADİS"), 1)
        et = klasik.birim_etiketle("وصلاة الله: رحمته. وفي الحديث: كذا", "ibnfaris")
        self.assertIn("RİVAYET", et)
        self.assertNotIn("HADİS", et, "sahibi yazılmamış rivayet Peygamber'e nisbet edilmemeli")

    def test_statu(self):
        self.assertEqual(klasik.statu(["ŞER", "KULLANIM"]), "şer'î / ıstılâhî")
        self.assertEqual(klasik.statu(["KULLANIM", "RİVAYET"]), "dil-içi tanıklı (+ rivayet)")
        self.assertEqual(klasik.statu(["ŞİİR"]), "dil-içi tanıklı")
        self.assertEqual(klasik.statu(["RİVAYET"]), "YALNIZ rivayetle tanıklı")
        self.assertEqual(klasik.statu(["HADİS", "KUR"]), "YALNIZ rivayetle tanıklı")
        self.assertEqual(klasik.statu(["NAKİL"]), "yalnız yorumcu nakli")
        self.assertEqual(klasik.statu(["KUR"]), "sözlükçünün ayet okuması")
        self.assertEqual(klasik.statu([]), "tanıksız: sözlükçünün açıklaması")

    def test_anlam_birimi_tanigi_oncekine_baglar(self):
        metin = "الصلاة: الدعاء والتبريك. وقال تعالى: صلوا عليه [الأحزاب/ 56] ، وقال الشاعر: ... كذا وكذا"
        birimler = klasik.anlam_birimleri(metin)
        self.assertEqual(len(birimler), 1, birimler)    # ayet ve şiir tanığı kendi başına anlam sayılmaz

    def test_uc_nokta_cumle_sonu_degildir(self):
        birimler = klasik.anlam_birimleri("وقال الشاعر: تجعل العود ... والرند الزكي طيب الأرجاء")
        self.assertEqual(len(birimler), 1, birimler)

    def test_sure_adlari_114_sureyi_kapsar(self):
        self.assertEqual(set(klasik.SURE_NO.values()), set(range(1, 115)))
        self.assertEqual(klasik.SURE_NO[ay.norm("الأحزاب")], 33)
        self.assertEqual(klasik.SURE_NO[ay.norm("الفاتحة")], 1)

    def test_kaynak_sabitleri(self):
        self.assertEqual(set(klasik.ESERLER), {"ibnfaris", "ragib"})
        for e in klasik.ESERLER.values():
            self.assertRegex(e["sha256"], r"^[0-9a-f]{64}$")
            self.assertRegex(e["commit"], r"^[0-9a-f]{40}$")
        self.assertEqual(klasik.BEKLENEN_MADDE, {"ibnfaris": 4649, "ragib": 1662})


class GirdiVeKayit(unittest.TestCase):
    def test_latin_giris_reddedilir_bos_sonuc_uretilmez(self):
        kod, c = calistir(["klasik", "kok", "salat"])
        self.assertEqual(kod, 2)
        self.assertIn("HATA:", c)
        self.assertIn("Durum       : çalıştırılmadı (girdi hatası)", c)

    def test_arama_arapca_ifade_ister(self):
        kod, c = calistir(["klasik", "ara", "salat"])
        self.assertEqual(kod, 2)
        self.assertIn("HATA:", c)

    def test_etiketler_veriye_ihtiyac_duymaz(self):
        kod, c = calistir(["klasik", "etiketler"])
        self.assertEqual(kod, 0)
        self.assertIn("[RİVAYET", c)
        self.assertIn("Kaynak      : klasik", c)
        for s in icerik_satirlari(c):
            self.assertTrue(s.startswith("[hipotez · klasik]"), s)

    def test_kayit_birimleri_gecerli(self):
        from tezgah import kayit
        self.assertIn("madde", kayit.GECERLI_BIRIMLER)
        self.assertIn("anlam birimi", kayit.GECERLI_BIRIMLER)


@unittest.skipUnless(KURULU, "klasik sözlükler kurulu değil (python -m tezgah kur klasik)")
class KurulumdanSonra(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.k = klasik.yukle()
        cls.kor = veri.korpus()

    def test_madde_sayilari_ve_sha(self):
        for eser, n in klasik.BEKLENEN_MADDE.items():
            self.assertEqual(sum(1 for m in self.k.maddeler if m["eser"] == eser), n, eser)
            self.assertEqual(self.k.kaynak[eser]["sha256"], klasik.ESERLER[eser]["sha256"], eser)
        manifest = json.loads(klasik.KLASIK_MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["klasik_sha256"], self.k.sha)

    def test_degistirilmis_dosya_reddedilir(self):
        with tempfile.TemporaryDirectory() as tmp:
            sahte = Path(tmp) / "manifest.json"
            sahte.write_text(json.dumps({"klasik_sha256": "0" * 64}), encoding="utf-8", newline="\n")
            klasik.yukle.cache_clear()
            try:
                with mock.patch.object(klasik, "KLASIK_MANIFEST", sahte):
                    with self.assertRaises(veri.VeriHatasi):
                        klasik.yukle()
            finally:
                klasik.yukle.cache_clear()
        self.assertIsNotNone(klasik.yukle())

    def test_kapsam_olcumu_yeniden_uretilir(self):
        o = klasik.kapsam(self.kor, self.k)
        for eser, beklenen in KAPSAM.items():
            self.assertEqual(o[eser]["madde"], beklenen["madde"], eser)
            self.assertEqual(o[eser]["kesin"], beklenen["kesin"], eser)
            self.assertEqual(len(o[eser]["zayif"]), beklenen["zayif"], eser)
            self.assertEqual(len(o[eser]["yok"]), beklenen["yok"], eser)
            self.assertEqual(beklenen["kesin"] + beklenen["zayif"] + beklenen["yok"],
                             len(self.kor.kok_kelimeleri), eser)

    def test_salat_koku_iki_eserde_kesin_eslesir(self):
        for eser in klasik.ESER_AD:
            cozum = self.k.coz("صلو", eser)
            self.assertTrue(cozum, eser)
            self.assertTrue(all(not kural.startswith("ZAYIF") for kural, _ in cozum), eser)

    def test_kok_sorgusu_etiketli_ve_kayitli(self):
        kod, c = calistir(["klasik", "kok", "Slw"])
        self.assertEqual(kod, 0)
        for s in icerik_satirlari(c):
            self.assertTrue(s.startswith("[hipotez · klasik]"), s)
        self.assertIn("Kaynak      : QAC v0.4 | + klasik", c)
        self.assertIn("Sayım birimi: madde | anlam birimi", c)
        self.assertIn(f"Veri izi    : {self.kor.veri_izi} | {self.k.veri_izi}", c)
        self.assertIn("ṣ-l-v", c)
        self.assertNotIn("ṣ-l-ʾ", c, "başlıktaki illetli elif hemze gibi yazılmamalı")

    def test_isaret_statu_dagilimi_yazar(self):
        kod, c = calistir(["klasik", "isaret", "Slw", "--eser", "ragib"])
        self.assertEqual(kod, 0)
        self.assertIn("anlam birimi ·", c)
        self.assertIn("Statü birimin TANIĞINA göredir", c)

    def test_ayet_denetimi_korpusla_yapilir(self):
        kod, c = calistir(["klasik", "ayet", "Slw", "--eser", "ragib"])
        self.assertEqual(kod, 0)
        self.assertIn("36:64", c)
        self.assertIn("kök VAR:", c)
        self.assertIn("kökünün QAC'taki 90 ayetinden", c)      # CLAUDE.md §6: Slw 90 ayet
        self.assertIn("Sayım birimi: atıf geçişi | ayet", c)

    def test_kurulu_iken_tekrar_kurulum_reddedilir(self):
        kod, c = calistir(["kur", "klasik"])
        self.assertEqual(kod, 2)
        self.assertIn("zaten kurulu", c)

    def test_ara_bulur_ve_yokluk_delili_saymaz(self):
        kod, c = calistir(["klasik", "ara", "العبادة المخصوصة", "--limit", "2"])
        self.assertEqual(kod, 0)
        self.assertIn("Bulunmaması yokluk delili değildir", c)


if __name__ == "__main__":
    unittest.main()
