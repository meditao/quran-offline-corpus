"""Statik araştırma katmanının kaynak bütünlüğü ve çevrimdışı kapsamı.

Beklentiler ihracat kodundan değil, ham Tanzil/QAC ve kaynak indekslerinden
okunur. Bir geçici site oluşturulur; araştırma deposuna yazılması denetlenir.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import unittest
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from unittest import mock
from urllib.error import HTTPError
from urllib.request import Request, urlopen


WEB = Path(__file__).resolve().parents[1]
DEPO = WEB.parent
sys.path.insert(0, str(WEB))


def kaynak_izleri():
    """Eski katmanlar ve kökteki araştırma belgeleri; çalışma önbelleği hariç."""
    dosyalar = [p for p in DEPO.iterdir() if p.is_file()]
    for dizin in DEPO.iterdir():
        if dizin.is_dir() and re.match(r"^0[1-9]_", dizin.name):
            dosyalar.extend(p for p in dizin.rglob("*") if p.is_file()
                            and "__pycache__" not in p.parts and p.suffix != ".pyc")
    return {str(p.relative_to(DEPO)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in dosyalar}


def ham_tanzil():
    ayetler = {}
    with (DEPO / "01_raw/tanzil/quran-uthmani.txt").open(encoding="utf-8") as f:
        for satir in f:
            satir = satir.rstrip("\r\n")
            if not satir or satir.startswith("#"):
                continue
            sure, ayet, metin = satir.split("|", 2)
            ayetler[(int(sure), int(ayet))] = metin
    return ayetler


def ham_qac():
    """QAC dosyasını tezgâh/ihracat ayrıştırıcısı kullanmadan okur."""
    segmentler = defaultdict(list)
    with (DEPO / "02_morphology/qac/quranic-corpus-morphology-0.4.txt").open(
            encoding="utf-8") as f:
        for satir in f:
            if not satir.startswith("("):
                continue
            konum, bicim, etiket, ozellikler = satir.rstrip("\r\n").split("\t")
            sure, ayet, kelime, segment = map(int, konum.strip("()").split(":"))
            ozellikler = ozellikler.split("|")
            kok = next((x[5:] for x in ozellikler if x.startswith("ROOT:")), "")
            lemma = next((x[4:] for x in ozellikler if x.startswith("LEM:")), "")
            segmentler[(sure, ayet, kelime)].append({
                "id": segment, "bw": bicim, "tag": etiket,
                "features": ozellikler, "root": kok, "lemma": lemma,
            })
    return dict(segmentler)


class KaynakButunlugu(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.once = kaynak_izleri()
        cls.gecici = tempfile.TemporaryDirectory(prefix="kuran-web-test-")
        cls.addClassCleanup(cls.gecici.cleanup)
        spec = importlib.util.spec_from_file_location("arastirma_build", WEB / "build.py")
        build = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(build)
        cls.builder = build
        # İlk üretim de ağsız çalışmalıdır; yerel kaynaklar yeterlidir.
        with mock.patch.object(socket, "create_connection", side_effect=AssertionError("Ağ çağrısı")), \
                mock.patch("urllib.request.urlopen", side_effect=AssertionError("Ağ çağrısı")):
            cls.cikti = Path(build.build(Path(cls.gecici.name) / "site"))
        cls.sonra = kaynak_izleri()
        cls.catalog = cls.json_oku("data/catalog.json")
        cls.sureler = {s: cls.json_oku(f"data/surahs/{s:03d}.json") for s in range(1, 115)}
        cls.ayetler = {(a["surah"], a["ayah"]): a
                       for sure in cls.sureler.values() for a in sure["verses"]}
        cls.tanzil = ham_tanzil()
        cls.qac = ham_qac()

    @classmethod
    def json_oku(cls, yol):
        return json.loads((cls.cikti / yol).read_text(encoding="utf-8"))

    def test_arastirma_kaynaklarina_yazilmaz(self):
        self.assertEqual(self.once, self.sonra,
                         "Üretim eski araştırma katmanlarından birini değiştirdi veya ek dosya yazdı")

    def test_kaynak_dizinini_cikti_olarak_kullanmak_reddedilir(self):
        for hedef in (DEPO, WEB, DEPO / "01_raw", DEPO / "07_analyses" / "yeni-site"):
            with self.subTest(hedef=hedef):
                with self.assertRaises(ValueError):
                    self.builder.build(hedef)
        self.assertEqual(self.sonra, kaynak_izleri())

    def test_ilgisiz_dolu_dizin_ve_kullanici_notu_korunur(self):
        diger = Path(self.gecici.name) / "kullanici-dizini"
        diger.mkdir()
        not_yolu = diger / "calisma-notu.txt"
        not_yolu.write_bytes(b"Kullanicinin baska calismasi\n")
        with self.assertRaises(ValueError):
            self.builder.build(diger)
        self.assertEqual(not_yolu.read_bytes(), b"Kullanicinin baska calismasi\n")
        ek_not = self.cikti / "kullanici-notu.txt"
        ek_not.write_bytes(b"Bu dosya site tarafindan uretilmedi\n")
        once = (self.cikti / "manifest.json").read_bytes()
        try:
            with self.assertRaises(ValueError):
                self.builder.build(self.cikti)
            self.assertEqual(ek_not.read_bytes(), b"Bu dosya site tarafindan uretilmedi\n")
            self.assertEqual((self.cikti / "manifest.json").read_bytes(), once)
        finally:
            ek_not.unlink()

    def test_butun_ayetlerde_tanzil_metin_birebir(self):
        self.assertEqual(len(self.tanzil), 6236)
        self.assertEqual(set(self.ayetler), set(self.tanzil))
        for konum, metin in self.tanzil.items():
            with self.subTest(ayet=konum):
                ayet = self.ayetler[konum]
                self.assertEqual(ayet["arabic"], metin)
                self.assertEqual(ayet["ref"], f"{konum[0]}:{konum[1]}")
                self.assertEqual(" ".join(k["text"] for k in ayet["tokens"]), metin)
                self.assertTrue(ayet["reading"], "Mevcut okunuş bütün ayetlere aktarılmalı")

    def test_qac_segmentleri_eksiksiz_ve_aynen(self):
        aktarilan = {(s, a, k["id"]): k for (s, a), ayet in self.ayetler.items()
                     for k in ayet["words"]}
        self.assertEqual(len(self.qac), 77429)
        self.assertEqual(set(aktarilan), set(self.qac))
        self.assertEqual(sum(len(s) for s in self.qac.values()), 128219)
        for konum, beklenen in self.qac.items():
            kelime = aktarilan[konum]
            self.assertEqual(len(kelime["segments"]), len(beklenen), str(konum))
            for gercek, ham in zip(kelime["segments"], beklenen):
                for alan in ("id", "bw", "tag", "features"):
                    self.assertEqual(gercek[alan], ham[alan], f"{konum} {alan}")
                for alan in ("root", "lemma"):
                    self.assertEqual(gercek[alan] or "", ham[alan], f"{konum} {alan}")
            self.assertEqual(set(kelime["roots"]), {s["root"] for s in beklenen if s["root"]})
            self.assertEqual(set(kelime["lemmas"]), {s["lemma"] for s in beklenen if s["lemma"]})

    def test_kok_sayimlari_indeksle_ayni_buyuk_kucuk_harf_korunur(self):
        with (DEPO / "03_indices/generated/root_index.csv").open(encoding="utf-8", newline="") as f:
            kaynak = {r["root_bw"]: r for r in csv.DictReader(f)}
        kokler = {r["bw"]: r for r in self.catalog["roots"]}
        self.assertEqual(len(kokler), 1642)
        self.assertEqual(set(kokler), set(kaynak))
        for kok, r in kaynak.items():
            for kaynak_alan, web_alan in (("word_occurrences", "wordCount"),
                                         ("ayah_count", "verseCount"), ("surah_count", "surahCount")):
                self.assertEqual(kokler[kok][web_alan], int(r[kaynak_alan]), f"{kok} {web_alan}")
        self.assertEqual(kokler["Slw"]["wordCount"], 99)
        self.assertNotEqual(kokler["Slw"]["wordCount"], kokler["slw"]["wordCount"])
        self.assertNotEqual(kokler["Slw"]["latin"], kokler["slw"]["latin"])
        self.assertEqual(kokler["Amn"]["wordCount"], 879)

    def test_istatistikler_birimleri_karistirmaz(self):
        stats = self.catalog["stats"]
        self.assertEqual({k: stats[k] for k in ("surahs", "verses", "words", "segments", "roots")},
                         {"surahs": 114, "verses": 6236, "words": 77429,
                          "segments": 128219, "roots": 1642})

    def test_ceviri_kapsami_tam_ve_uretilmis_meal_yok(self):
        beklenen = {(2, a) for a in range(2, 118)} | {(10, a) for a in range(1, 110)}
        mevcut = {konum for konum, a in self.ayetler.items() if a["translation"] is not None}
        self.assertEqual(mevcut, beklenen)
        self.assertEqual(self.catalog["stats"]["translatedVerses"], len(beklenen))
        for konum in beklenen:
            ceviri = self.ayetler[konum]["translation"]
            self.assertTrue(ceviri["terms"], str(konum))
            self.assertTrue(ceviri["tafsir"], str(konum))
            self.assertIn(ceviri["documentId"], self.ayetler[konum]["documentIds"])

    def test_ceviri_metinleri_kaynakta_kalan_icerigi_de_korur(self):
        # Farklı Markdown biçimleri ve uzun çok paragraflı son sürümler.
        for konum in ((2, 2), (2, 66), (2, 67), (2, 111), (2, 117), (10, 1), (10, 109)):
            ayet = self.ayetler[konum]
            ceviri = ayet["translation"]
            doc = next(d for d in self.catalog["documents"] if d["id"] == ceviri["documentId"])
            ham = (DEPO / doc["path"]).read_text(encoding="utf-8")
            # İhracat her katmanın kaynak metnini uydurmadan / yeniden yazmadan taşır.
            for alan in ("terms", "tafsir"):
                self.assertIn(ceviri[alan].strip(), ham, f"{konum} {alan} kaynakta yok")

    def test_markdown_dosyalarinin_asillari_ve_belge_govdeleri_korunur(self):
        belgeler = self.catalog["documents"]
        self.assertEqual(len({d["id"] for d in belgeler}), len(belgeler))
        for doc in belgeler:
            kaynak = DEPO / doc["path"]
            self.assertTrue(kaynak.is_file(), doc["path"])
            kopya = self.cikti / "sources/repository" / doc["path"]
            self.assertEqual(kopya.read_bytes(), kaynak.read_bytes(), doc["path"])
            belge = self.json_oku(doc["url"])
            self.assertEqual(belge["content"], kaynak.read_bytes().decode("utf-8"), doc["path"])
        yollar = {d["path"] for d in belgeler}
        for ad in ("07_analyses/surahs/Asr-103-analysis.md", "07_analyses/roots/Amn-concept-card.md",
                   "07_analyses/roots/Mumin-concept-card.md", "07_analyses/roots/Iman-analysis.md",
                   "06_methodology/analiz_protokolu.md"):
            self.assertIn(ad, yollar)
        asr = next(d for d in belgeler if d["path"] == "07_analyses/surahs/Asr-103-analysis.md")
        for a in range(1, 4):
            self.assertIn(asr["id"], self.ayetler[(103, a)]["documentIds"])

    def test_hizalama_ayni_indeksi_izler(self):
        with (DEPO / "03_indices/generated/tanzil_qac_alignment.csv").open(
                encoding="utf-8", newline="") as f:
            kaynak = {(int(r["surah"]), int(r["ayah"])): r["status"] for r in csv.DictReader(f)}
        self.assertEqual(Counter(a["alignmentStatus"] for a in self.ayetler.values()),
                         Counter({"count_match": 6120, "basmala_offset": 112,
                                  "tokenization_difference": 4}))
        for konum, durum in kaynak.items():
            self.assertEqual(self.ayetler[konum]["alignmentStatus"], durum, str(konum))
            ayet = self.ayetler[konum]
            self.assertEqual({w for t in ayet["tokens"] for w in t["wordIds"]},
                             {w["id"] for w in ayet["words"]}, str(konum))

    def test_37_130_bir_kelime_iki_tanzil_tokeni(self):
        ayet = self.ayetler[(37, 130)]
        self.assertEqual(len(ayet["words"]), 3)
        self.assertEqual(len(ayet["tokens"]), 4)
        self.assertEqual(ayet["tokens"][2]["wordIds"], [3])
        self.assertEqual(ayet["tokens"][3]["wordIds"], [3])
        self.assertEqual(ayet["words"][2]["reading"], "ʾil yâsîn")
        self.assertTrue(ayet["words"][2]["alignmentNote"])

    def test_sure_basi_besmele_qac_kelimelerine_kaymaz(self):
        ayet = self.ayetler[(2, 1)]
        self.assertTrue(ayet["basmala"])
        self.assertEqual(len(ayet["words"]), 1)
        self.assertEqual([t["wordIds"] for t in ayet["tokens"][:4]], [[], [], [], []])
        self.assertEqual(ayet["tokens"][4]["wordIds"], [1])
        self.assertFalse(self.ayetler[(1, 1)]["basmala"])
        self.assertFalse(self.ayetler[(9, 1)]["basmala"])

    def test_arama_indeksi_butun_kelime_ve_ayetleri_tasir(self):
        indeks = self.json_oku("data/search-index.json")
        self.assertEqual(len(indeks["words"]), 77429)
        self.assertEqual(len(indeks["verses"]), 6236)
        self.assertEqual({(r[0], r[1], r[2]) for r in indeks["words"]}, set(self.qac))
        self.assertEqual({(r[0], r[1]): r[2] for r in indeks["verses"]}, self.tanzil)
        # Kök ailesi indekste, UI'nin kayıplı Latinleştirmesine ihtiyaç duymaz.
        for kok, sayi in (("Slw", 99), ("Amn", 879)):
            self.assertEqual(sum(kok in r[6] for r in indeks["words"]), sayi)

    def test_cevrimdisi_manifest_tum_dosyalari_ve_guvenli_goreli_yollari_kapsar(self):
        manifest = self.json_oku("manifest.json")
        self.assertTrue(manifest["buildId"])
        dosyalar = manifest["files"]
        self.assertEqual(len(dosyalar), len(set(dosyalar)))
        for yol in dosyalar:
            p = PurePosixPath(yol)
            self.assertFalse(p.is_absolute(), yol)
            self.assertNotIn("..", p.parts, yol)
            self.assertNotRegex(yol, r"^[a-zA-Z]+:|[\\?#]", yol)
            self.assertTrue((self.cikti / yol).is_file(), yol)
        gercek = {p.relative_to(self.cikti).as_posix() for p in self.cikti.rglob("*") if p.is_file()}
        self.assertEqual(set(dosyalar) | {"manifest.json"}, gercek)
        for yol in ("index.html", "app.js", "style.css", "sw.js", "data/catalog.json",
                    "data/search-index.json", "data/surahs/114.json"):
            self.assertIn(yol, dosyalar)

    def test_service_worker_veri_surumu_katalogla_ayni(self):
        sw = (self.cikti / "sw.js").read_text(encoding="utf-8")
        surum = re.search(r"self\.CORPUS_BUILD_ID\s*=\s*['\"]([a-f0-9]+)['\"]", sw)
        self.assertIsNotNone(surum, "Yalnız veri değişince de tarayıcı yeni offline sürümü kurmalı")
        self.assertEqual(surum.group(1), self.catalog["buildId"])

    def test_kaynak_kopyalari_ve_telif_bildirimleri_eksiksiz(self):
        for kaynak, kopya, bildirim in (
                ("01_raw/tanzil/quran-uthmani.txt", "sources/quran-uthmani.txt", "sources/TANZIL-NOTICE.txt"),
                ("02_morphology/qac/quranic-corpus-morphology-0.4.txt",
                 "sources/quranic-corpus-morphology-0.4.txt", "sources/QAC-NOTICE.txt")):
            ham = (DEPO / kaynak).read_bytes()
            self.assertEqual((self.cikti / kopya).read_bytes(), ham)
            notice = (self.cikti / bildirim).read_text(encoding="utf-8")
            self.assertIn("PLEASE DO NOT REMOVE OR CHANGE THIS COPYRIGHT BLOCK", notice)
            self.assertIn("Copyright", notice)
            self.assertIn("TERMS OF USE", notice)
            self.assertIn("CHANGING IT IS NOT ALLOWED", notice)

    def test_yerel_http_sunucusu_gercek_dosyalari_utf8_ve_salt_okunur_sunar(self):
        from serve import create_server
        sunucu = create_server(self.cikti, port=0)
        self.assertEqual(sunucu.server_address[0], "127.0.0.1")
        islem = threading.Thread(target=sunucu.serve_forever, daemon=True)
        islem.start()
        kok = f"http://127.0.0.1:{sunucu.server_port}"
        try:
            for yol, mime in (("/", "text/html"), ("/data/catalog.json", "application/json"),
                              ("/data/surahs/002.json", "application/json"),
                              ("/app.js", "text/javascript"), ("/sw.js", "text/javascript")):
                with urlopen(kok + yol, timeout=5) as yanit:
                    self.assertEqual(yanit.status, 200)
                    self.assertIn(mime, yanit.headers["Content-Type"])
                    self.assertIn("charset=utf-8", yanit.headers["Content-Type"])
                    self.assertEqual(yanit.headers["X-Content-Type-Options"], "nosniff")
                    self.assertTrue(yanit.read().decode("utf-8"))
            for yol in ("/data/", "/../CLAUDE.md", "/%2e%2e/01_raw/tanzil/quran-uthmani.txt"):
                with self.assertRaises(HTTPError) as hata:
                    urlopen(kok + yol, timeout=5)
                self.assertEqual(hata.exception.code, 404)
            with self.assertRaises(HTTPError) as hata:
                urlopen(Request(kok + "/data/catalog.json", data=b"{}", method="POST"), timeout=5)
            self.assertEqual(hata.exception.code, 501)
        finally:
            sunucu.shutdown()
            sunucu.server_close()
            islem.join(timeout=5)
        self.assertEqual(self.sonra, kaynak_izleri())

    def worker_calistir(self, dosya):
        node = shutil.which("node")
        if node is None:
            bundled = Path(sys.executable).parent.parent / "node/bin/node.exe"
            if bundled.is_file():
                node = str(bundled)
        if node is None:
            self.skipTest("Worker sağlama testi için isteğe bağlı Node.js çalışma ortamı bulunamadı")
        sonuc = subprocess.run([node, str(WEB / "testler" / dosya), str(self.cikti)],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               text=True, encoding="utf-8", timeout=30)
        self.assertEqual(sonuc.returncode, 0, sonuc.stdout + sonuc.stderr)
        return sonuc.stdout

    def test_gercek_arama_worker_korpus_sayimlari_ve_harf_ayrimi(self):
        sonuc = self.worker_calistir("arama_worker_test.js")
        self.assertIn("16 korpus sağlama örneği geçti", sonuc)

    def test_service_worker_eksik_guncellemede_tam_kopyayi_korur(self):
        sonuc = self.worker_calistir("offline_worker_test.js")
        self.assertIn("kaynak değişimi ve alt dizin güvenliği doğrulandı", sonuc)


if __name__ == "__main__":
    unittest.main()
