"""Durak işaretli Tanzil sürümü: yükleme denetimleri, sekte, diğer durakların etiketli gösterimi.

Gerçek dosya (01_raw/tanzil/quran-uthmani-durak.txt) kurulu değilse o test atlanır. Mantık,
gerçek Tanzil metnine işaret eklenerek kurulan sentetik bir dosyayla sınanır.
"""

import contextlib
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import _ortak  # noqa: F401
from tezgah import okunus, veri
from tezgah.__main__ import main

SEKTE, SLA, CIM, RUB, SECDE, TATVIL = "\u06DC", "\u06D6", "\u06DA", "\u06DE", "\u06E9", "\u0640"

# Hafs'ta tek başına duran sekte yerleri; 69:28'de sekte isteğe bağlıdır (okunus_kurallari.md §3b).
SEKTE_YERLERI = {(18, 1), (36, 52), (69, 28), (75, 27), (83, 14)}


def sentetik_metin(degistir=None):
    """Taban metne işaret ekler: (sûre, ayet) -> token listesini değiştiren işlev."""
    satirlar = []
    for (s, a), metin in okunus.tanzil().items():
        tok = metin.split(" ")
        if degistir and (s, a) in degistir:
            tok = degistir[(s, a)](tok)
        satirlar.append(f"{s}|{a}|{' '.join(tok)}")
    return "\n".join(satirlar) + "\n"


def ekle_sonra(i, isaret):
    return lambda t: t[: i + 1] + [isaret] + t[i + 1:]


def bitistir(i, isaret):
    return lambda t: t[:i] + [t[i] + isaret] + t[i + 1:]


def tatvil_ekle(i):
    return lambda t: t[:i] + [t[i][:2] + TATVIL + t[i][2:]] + t[i + 1:]


DEGISIKLIK = {
    (18, 1): lambda t: t + [SEKTE],                 # ayet sonu, besmele önekli ayet
    (36, 52): ekle_sonra(5, SEKTE),                 # ayet içi (مَّرْقَدِنَا sonrası)
    (69, 28): lambda t: t + [SEKTE],                # ayet sonu (مَالِيَهْ), isteğe bağlı sekte
    (75, 27): ekle_sonra(1, SEKTE),                 # مَنْ sonrası
    (83, 14): ekle_sonra(1, SEKTE),                 # بَلْ sonrası
    (2, 3): bitistir(2, SLA),                       # kelimeye bitişik durak
    (2, 1): ekle_sonra(4, CIM),                     # besmele önekinden sonraki ilk kelime
    (2, 2): tatvil_ekle(1),                         # sürümün eklediği tatvil
    (2, 26): lambda t: [RUB] + t,                   # rubʿ işareti (kullanılmaz)
    (7, 206): lambda t: t + [SECDE],                # secde işareti (kullanılmaz)
}


class SentetikDurak(unittest.TestCase):
    def setUp(self):
        self.dizin = Path(tempfile.mkdtemp())
        self.yol = self.dizin / "quran-uthmani-durak.txt"
        self.manifest = self.dizin / "manifest.local.json"

    def yaz(self, metin, sha=None):
        self.yol.write_text(metin, encoding="utf-8")
        gercek = hashlib.sha256(self.yol.read_bytes()).hexdigest()
        self.manifest.write_text(json.dumps({"files": [
            {"file": "01_raw/tanzil/quran-uthmani-durak.txt", "sha256": sha or gercek}]}), encoding="utf-8")

    def yukle(self):
        return okunus.durak_yukle(self.yol, self.manifest, okunus.tanzil())

    def test_isaret_konumlari(self):
        self.yaz(sentetik_metin(DEGISIKLIK))
        d = self.yukle()
        self.assertEqual(d, {
            (18, 1): {14: [SEKTE]},
            (36, 52): {5: [SEKTE]},
            (69, 28): {3: [SEKTE]},
            (75, 27): {1: [SEKTE]},
            (83, 14): {1: [SEKTE]},
            (2, 3): {2: [SLA]},
            (2, 1): {4: [CIM]},
        })
        self.assertNotIn((2, 245), d, "ص üzerindeki ۜ (tabanda da var) durak sayılmamalı")
        for k in ((2, 2), (2, 26), (7, 206)):
            self.assertNotIn(k, d, "tatvil, rubʿ ve secde durak sayılmaz")
        self.assertEqual({k for k, v in d.items() if any(SEKTE in x for x in v.values())}, SEKTE_YERLERI)

    def test_bitisik_fazla_sekte_reddedilir(self):
        bozuk = dict(DEGISIKLIK)
        bozuk[(75, 27)] = bitistir(1, SEKTE)   # yalnız tek başına duran U+06DC çıkarılır
        self.yaz(sentetik_metin(bozuk))
        with self.assertRaises(veri.VeriHatasi):
            self.yukle()

    def test_sekte_okunusta_diger_duraklar_gizli(self):
        self.yaz(sentetik_metin(DEGISIKLIK))
        d = self.yukle()
        tz = okunus.tanzil()
        o = okunus.ayet_oku(18, 1, tz[(18, 1)], d[(18, 1)])
        self.assertTrue(o.kelimeler[-1].sekte)
        self.assertTrue(o.latin_isaretli.endswith("ʿivacâ [sekte]"))
        self.assertEqual(o.latin, okunus.ayet_oku(18, 1, tz[(18, 1)]).latin, "sekte harfleri değiştirmemeli")
        o = okunus.ayet_oku(36, 52, tz[(36, 52)], d[(36, 52)])
        self.assertIn("mim marqadinâ [sekte] hâẕâ", o.latin_isaretli)
        o = okunus.ayet_oku(75, 27, tz[(75, 27)], d[(75, 27)])
        self.assertEqual(o.latin_isaretli, "vaqîla man [sekte] râq")
        o = okunus.ayet_oku(69, 28, tz[(69, 28)], d[(69, 28)])
        self.assertEqual(o.latin_isaretli, "mâ ʾagnâ ʿannî mâliyah [sekte]")
        o = okunus.ayet_oku(83, 14, tz[(83, 14)], d[(83, 14)])
        self.assertTrue(o.latin_isaretli.startswith("kallâ bal [sekte] râna"))
        o = okunus.ayet_oku(2, 3, tz[(2, 3)], d[(2, 3)])
        self.assertEqual(o.kelimeler[2].duraklar, ["ṣlâ (vasl evlâ)"])
        self.assertNotIn("ṣlâ", o.latin_isaretli)
        o = okunus.ayet_oku(2, 1, tz[(2, 1)], d[(2, 1)])
        self.assertEqual(o.kelimeler[0].duraklar, ["cîm (vakf câiz)"])

    def test_bozuk_metin_reddedilir(self):
        bozuk = dict(DEGISIKLIK)
        bozuk[(1, 1)] = lambda t: ["بِسْمِ", "ٱللَّهِ", "ٱلرَّحْمَٰنِ", "ٱلرَّحِيم"]  # son hareke silindi
        self.yaz(sentetik_metin(bozuk))
        with self.assertRaises(veri.VeriHatasi):
            self.yukle()

    def test_sha_uyusmazligi_reddedilir(self):
        self.yaz(sentetik_metin(DEGISIKLIK), sha="0" * 64)
        with self.assertRaises(veri.VeriHatasi):
            self.yukle()

    def test_komut_durak_etiketi(self):
        self.yaz(sentetik_metin(DEGISIKLIK))
        with mock.patch.object(okunus, "DURAK_YOLU", self.yol), \
                mock.patch.object(okunus, "MANIFEST_YOLU", self.manifest):
            okunus.durak_isaretleri.cache_clear()
            try:
                cikti = {}
                for argv in (["okunus", "2:3"], ["okunus", "2:3", "--durak"], ["okunus", "75:27"]):
                    t = io.StringIO()
                    with contextlib.redirect_stdout(t):
                        self.assertEqual(main(argv), 0)
                    cikti[" ".join(argv)] = t.getvalue()
            finally:
                okunus.durak_isaretleri.cache_clear()
        self.assertNotIn("ṣlâ", cikti["okunus 2:3"])
        self.assertIn("ṣlâ (vasl evlâ)", cikti["okunus 2:3 --durak"])
        self.assertIn("geleneksel — yorum içerebilir", cikti["okunus 2:3 --durak"])
        self.assertIn("man [sekte] râq", cikti["okunus 75:27"])
        self.assertIn("Kaynak      : Tanzil Uthmani v1.1 | + Tanzil Uthmani v1.1 durak işaretli", cikti["okunus 75:27"])


class GercekDurakDosyasi(unittest.TestCase):
    def test_gercek_dosya(self):
        if not okunus.DURAK_YOLU.exists():
            self.skipTest("durak işaretli Tanzil sürümü kurulu değil (08_scripts/fetch_tanzil_marks.py)")
        d = okunus.durak_isaretleri()
        sekte = {k for k, v in d.items() if any(okunus.SEKTE in x for x in v.values())}
        # Hafs'ta tek başına duran sekte (69:28 isteğe bağlı); tutmazsa sebep araştırılır, test değiştirilmez
        self.assertEqual(sekte, SEKTE_YERLERI)
        self.assertEqual(len(d), len({k for k in d}))


if __name__ == "__main__":
    unittest.main()
