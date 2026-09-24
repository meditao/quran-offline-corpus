"""Aşama 3 tez.py: dondurma, sürümleme, eksen/raf kuralları, sonuç tutarlılığı, kurcalama tespiti."""

import json
import os
import re
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import _ortak  # noqa: F401
from tezgah import kavram, tez

TEZ = "Kur'an'da ṣ-l-v kökünün fiil kullanımları bir eylemi ifade eder."
AC = dict(tez=TEZ, tanim=["eylem=öznenin yaptığı iş"], eksen=["kip=tanımlayıcı", "düzlem=oluşum"],
          karsi=["kalip ROOT:Slw&POS:V --limit 0"])
AYNI = ["kip=tanımlayıcı", "düzlem=oluşum"]
FARKLI = ["kip=normatif", "düzlem=oluşum"]
SORGU = ["kalip", "ROOT:Slw&POS:V", "--limit", "0"]


def ilk_ayet(cikti):
    m = re.search(r"^(\d+):(\d+):\d+:\d+ ", cikti, re.M)
    return f"{m.group(1)}:{m.group(2)}"


class TezTesti(unittest.TestCase):
    def setUp(self):
        self.dizin = Path(tempfile.mkdtemp())
        self.yama = mock.patch.object(tez, "TEZLER", self.dizin)
        self.yama.start()

    def tearDown(self):
        self.yama.stop()
        for yol in self.dizin.rglob("surum-*.json"):
            os.chmod(yol, 0o644)

    def ac(self, ad="t"):
        return tez.ac(ad, **AC)

    # --- dondurma ---------------------------------------------------------
    def test_dondurma_ve_olduğu_gibi_saklama(self):
        t = self.ac()
        s = t.surum()
        self.assertEqual(s["tez"], TEZ, "tez ifadesi değiştirilmez/güçlendirilmez")
        self.assertEqual(s["eksenler"], {"kip": "tanımlayıcı", "düzlem": "oluşum"})
        self.assertEqual([k["tur"] for k in t.kayitlar], ["surum"], "havuz açılışta taranmaz")
        yol = self.dizin / "t" / "surum-001.json"
        self.assertFalse(os.access(yol, os.W_OK) and os.stat(yol).st_mode & 0o222)
        self.assertEqual(tez.eksenler(["duzlem=olusum", "KIP=normatif", "özel=bir değer"]),
                         {"düzlem": "oluşum", "kip": "normatif", "ozel": "bir değer"})

    def test_acilis_zorunluluklari(self):
        for bozuk in ({"tez": "Birinci cümle. İkinci cümle."}, {"tez": "  "}, {"tez": "satır\nsatır"},
                      {"tanim": []}, {"tanim": ["eylem="]}, {"tanim": ["tanımsız"]},
                      {"eksen": []}, {"eksen": ["kip=belki"]}, {"karsi": []},
                      {"karsi": ["kavram yenile x"]}, {"karsi": ["ayet 2:3 --meal"]}, {"karsi": ["kalip"]}):
            with self.subTest(bozuk=bozuk):
                with self.assertRaises(tez.TezHatasi):
                    tez.ac("b", **{**AC, **bozuk})
        self.assertFalse((self.dizin / "b").exists())
        self.assertEqual(tez.tek_cumle("Sayı 1.642 ve ayet 2:3 geçer."), "Sayı 1.642 ve ayet 2:3 geçer.")
        self.ac()
        with self.assertRaises(tez.TezHatasi):
            self.ac()  # üzerine yazılmaz

    # --- bulgu ------------------------------------------------------------
    def test_eksen_ve_raf_kurallari(self):
        self.ac()
        for raf in ("çelişen", "destekleyen", "yalnız uyumlu", "belirsiz"):
            with self.subTest(farkli_eksen=raf):
                with self.assertRaises(tez.TezHatasi):
                    tez.bulgu("t", FARKLI, raf, "normatif bulgu", ["sayim", "--kok", "Slw"])
        with self.assertRaises(tez.TezHatasi):   # farklı eksen için gerekçe zorunlu
            tez.bulgu("t", FARKLI, "farklı eksen", "normatif bulgu", ["sayim", "--kok", "Slw"])
        with self.assertRaises(tez.TezHatasi):
            tez.bulgu("t", FARKLI, "farklı eksen", "normatif bulgu", ["sayim", "--kok", "Slw"], gerekce="  ")
        k = tez.bulgu("t", FARKLI, "farklı eksen", "normatif bulgu", ["sayim", "--kok", "Slw"],
                      gerekce="bulgu buyruk kipinde, tez tanımlayıcı")
        self.assertEqual((k["raf"], k["gerekce"]), ("farklı eksen", "bulgu buyruk kipinde, tez tanımlayıcı"))
        with self.assertRaises(tez.TezHatasi):
            tez.bulgu("t", AYNI, "farklı eksen", "aynı eksen", ["sayim", "--kok", "Slw"])
        with self.assertRaises(tez.TezHatasi):
            tez.bulgu("t", ["kip=tanımlayıcı"], "belirsiz", "eksik boyut", ["sayim", "--kok", "Slw"])
        with self.assertRaises(tez.TezHatasi):
            tez.bulgu("t", AYNI, "belirsiz", "  ", ["sayim", "--kok", "Slw"])
        for argv in ([], ["ayet", "2:3", "--arapca"], ["ayet", "2:3", "--meal"], ["tez", "tara", "t"]):
            with self.subTest(argv=argv):
                with self.assertRaises((tez.TezHatasi, kavram.KavramHatasi)):
                    tez.bulgu("t", AYNI, "belirsiz", "x", argv)

    def test_ayet_sorgudan_gelmeli(self):
        self.ac()
        cikti = kavram.sorgu_calistir(SORGU)
        ayet = ilk_ayet(cikti)
        with self.assertRaises(tez.TezHatasi):
            tez.bulgu("t", AYNI, "yalnız uyumlu", "x", SORGU, ["1:1"])   # 1:1'de Slw fiili yok
        k = tez.bulgu("t", AYNI, "yalnız uyumlu", "fiil kullanımları var", SORGU, [ayet])
        self.assertEqual(k["ayetler"], [ayet])

    # --- sonuç ------------------------------------------------------------
    def test_sonuc_tutarliligi(self):
        self.ac()
        with self.assertRaises(tez.TezHatasi):
            tez.sonuc("t", "Belirsiz", "Spekülatif", "tarama yok")          # önce tara
        tez.tara("t")
        tez.bulgu("t", FARKLI, "farklı eksen", "normatif", ["sayim", "--kok", "Slw"], gerekce="normatif kip")
        with self.assertRaises(tez.TezHatasi):
            tez.sonuc("t", "Çelişiyor", "Muhtemel", "farklı eksen çelişki sayılmaz")
        tez.bulgu("t", AYNI, "yalnız uyumlu", "uyumlu ama ayırt edici değil", SORGU)
        with self.assertRaises(tez.TezHatasi):
            tez.sonuc("t", "Destekleniyor", "Sağlam", "yalnız uyumlu destek değildir")
        tez.sonuc("t", "yalniz uyumlu", "muhtemel", "ayırt edici bulgu yok")
        tez.bulgu("t", AYNI, "destekleyen", "ayırt edici bulgu", SORGU)
        with self.assertRaises(tez.TezHatasi):   # desteklenen kapsam zorunlu
            tez.sonuc("t", "Destekleniyor", "Muhtemel", "ayırt edici bulgu var")
        k = tez.sonuc("t", "Destekleniyor", "Muhtemel", "ayırt edici bulgu var",
                      kapsam="yalnız ṣ-l-v fiil kullanımları (kalip ROOT:Slw&POS:V)")
        self.assertIn("Desteklenen kapsam:** yalnız ṣ-l-v fiil", (self.dizin / "t" / "tez.md").read_text(encoding="utf-8"))
        tez.bulgu("t", AYNI, "çelişen", "çelişen bulgu", ["sayim", "--kok", "Slw"])
        for durum in ("Destekleniyor", "Yalnız uyumlu"):
            with self.assertRaises(tez.TezHatasi):
                tez.sonuc("t", durum, "Muhtemel", "çelişen varken")
        tez.sonuc("t", "Çelişiyor", "Muhtemel", "çelişen bulgu var")
        hatalar, uyarilar = tez.denetle("t")
        self.assertEqual(hatalar, [])
        self.assertTrue(any("sonradan bulgu eklendi" in u or "bulgu eklendi" in u for u in uyarilar))

    # --- sürümleme --------------------------------------------------------
    def test_yeni_surum_eskisi_silinmez(self):
        t = self.ac()
        eski = (self.dizin / "t" / "surum-001.json").read_bytes()
        tez.bulgu("t", AYNI, "yalnız uyumlu", "x", SORGU)
        with self.assertRaises(tez.TezHatasi):
            tez.yeni_surum("t", "gerekçe", tanim=AC["tanim"])            # değişiklik yok
        with self.assertRaises(tez.TezHatasi):
            tez.yeni_surum("t", " ", tanim=["eylem=daraltılmış tanım"])  # gerekçe yok
        v = tez.yeni_surum("t", "tanım daraltıldı", tanim=["eylem=öznenin bedeniyle yaptığı iş"])
        self.assertEqual((v["surum"], v["degisen_alanlar"], v["onceki_surumdeki_bulgu"]), (2, ["tanimlar"], 1))
        self.assertEqual((self.dizin / "t" / "surum-001.json").read_bytes(), eski)
        t = tez.Tez("t")
        self.assertEqual(t.guncel_no, 2)
        self.assertEqual(sum(t.raf_sayilari(2).values()), 0, "eski sürüm bulguları yeni sürüme taşınmaz")
        self.assertIn("Sürüm 1", tez.rapor(t))

    # --- kurcalama --------------------------------------------------------
    def test_kurcalama_tespiti(self):
        self.ac()
        tez.tara("t")
        tez.bulgu("t", AYNI, "yalnız uyumlu", "x", SORGU)
        d = self.dizin / "t"
        self.assertEqual(tez.denetle("t"), ([], []))

        yol = d / "surum-001.json"
        yedek = yol.read_text(encoding="utf-8")
        os.chmod(yol, 0o644)
        yol.write_text(yedek.replace("ifade eder", "kesin olarak ifade eder"), encoding="utf-8")
        self.assertIn("Dondurulmuş sürüm değiştirilmiş", tez.denetle("t")[0][0])
        yol.write_text(yedek, encoding="utf-8")

        defter = d / "defter.json"
        yedek_d = defter.read_text(encoding="utf-8")
        kayitlar = json.loads(yedek_d)
        kayitlar[-1]["raf"] = "destekleyen"
        defter.write_text(json.dumps(kayitlar, ensure_ascii=False), encoding="utf-8")
        self.assertIn("zinciri bozuk", tez.denetle("t")[0][0])

        # zinciri de yeniden hesaplanmış sahte çıktı: sorgu yeniden çalıştırılınca yakalanır
        kayitlar = json.loads(yedek_d)
        kayitlar[-1]["cikti"] = kayitlar[-1]["cikti"].replace("Kalıp", "Kalip")
        onceki = ""
        for k in kayitlar:
            k["zincir"] = tez.Tez._zincir(onceki, k)
            onceki = k["zincir"]
        defter.write_text(json.dumps(kayitlar, ensure_ascii=False), encoding="utf-8")
        tez.rapor_yaz(tez.Tez("t"))
        self.assertTrue(any("sorgu çıktısı değişti" in h for h in tez.denetle("t")[0]))
        defter.write_text(yedek_d, encoding="utf-8")
        tez.rapor_yaz(tez.Tez("t"))

        rapor = d / "tez.md"
        rapor.write_text(rapor.read_text(encoding="utf-8").replace(TEZ, "Güçlendirilmiş tez."), encoding="utf-8")
        self.assertTrue(any("tez.md defterle uyuşmuyor" in h for h in tez.denetle("t")[0]))

    def test_farkli_eksen_rafi_ayri_ve_gorunur(self):
        self.ac()
        tez.bulgu("t", AYNI, "yalnız uyumlu", "uyumlu", SORGU)
        tez.bulgu("t", FARKLI, "farklı eksen", "normatif ifade", ["sayim", "--kok", "Slw"],
                  gerekce="bulgu normatif kipte")
        r = (self.dizin / "t" / "tez.md").read_text(encoding="utf-8")
        bolum = r.split("## 5b. Farklı eksen rafı (1 bulgu")[1].split("## 6.")[0]
        self.assertIn("Bulgu 2", bolum)
        self.assertIn("Eksen farkı: kip: bulgu **normatif** ↔ tez **tanımlayıcı**", bolum)
        self.assertIn("Gerekçe (farklı eksen): bulgu normatif kipte", bolum)
        self.assertNotIn("Bulgu 2", r.split("## 5. Bulgular")[1].split("## 5b.")[0])

    def test_yeniden_degerlendirme(self):
        self.ac()
        tez.tara("t")
        tez.bulgu("t", AYNI, "yalnız uyumlu", "ilk okuma", SORGU)
        tez.sonuc("t", "Yalnız uyumlu", "Muhtemel", "ilk değerlendirme")
        onceki_kayit = len(tez.Tez("t").kayitlar)
        with self.assertRaises(tez.TezHatasi):
            tez.degerlendir("t", 1, "destekleyen", "  ")                     # gerekçe zorunlu
        with self.assertRaises(tez.TezHatasi):
            tez.degerlendir("t", 1, "yalnız uyumlu", "aynı raf")              # değişiklik yok
        with self.assertRaises(tez.TezHatasi):
            tez.degerlendir("t", 1, "çelişen", "g", eksen=FARKLI)             # farklı eksen → çelişen olmaz
        with self.assertRaises(tez.TezHatasi):
            tez.degerlendir("t", 9, "çelişen", "g")                          # bulgu yok
        tez.degerlendir("t", 1, "destekleyen", "karşı okuma bu ayetleri açıklayamıyor")
        tez.degerlendir("t", 1, "farklı eksen", "etiket normatif olmalıydı", eksen=FARKLI)
        t = tez.Tez("t")
        b = t.turler("bulgu")[0]
        self.assertEqual(b["raf"], "yalnız uyumlu", "ilk kayıt silinmez/değişmez")
        self.assertEqual(t.etkin(b)["raf"], "farklı eksen")
        self.assertEqual(len(t.kayitlar), onceki_kayit + 2)
        self.assertEqual(t.raf_sayilari(1)["farklı eksen"], 1)
        r = (self.dizin / "t" / "tez.md").read_text(encoding="utf-8")
        self.assertIn("Değerlendirme geçmişi (ilk kayıt: yalnız uyumlu", r)
        self.assertIn("yalnız uyumlu → **destekleyen** — karşı okuma bu ayetleri açıklayamıyor", r)
        self.assertIn("destekleyen → **farklı eksen** (eksen etiketi değişti) — etiket normatif olmalıydı", r)
        hatalar, uyarilar = tez.denetle("t")
        self.assertEqual(hatalar, [])
        self.assertTrue(any("yeniden değerlendirildi" in u for u in uyarilar))
        tez.yeni_surum("t", "tanım daraltıldı", tanim=["eylem=daraltılmış"])
        with self.assertRaises(tez.TezHatasi):
            tez.degerlendir("t", 1, "belirsiz", "eski sürüm bulgusu")        # yalnız güncel sürüm

    def test_tezler_adi_kavrama_ayrilmaz(self):
        with self.assertRaises(kavram.KavramHatasi):
            kavram._dizin("tezler")


if __name__ == "__main__":
    unittest.main()
