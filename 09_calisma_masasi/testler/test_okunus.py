"""Aşama 2a okunuş sağlaması: test ayetleri, tüm korpus taraması, ortak harf tablosu."""

import collections
import contextlib
import io
import re
import unicodedata
import unittest

import _ortak  # noqa: F401
from tezgah import harf, okunus, veri
from tezgah.__main__ import main

# Test ayetleri: beklenen okunuş kurallardan (okunus_kurallari.md) elle çıkarıldı.
BEKLENEN = {
    (1, 1): "bismi llâhi rraḥmâni rraḥîm",
    (2, 3): "allaẕîna yuʾminûna bilgaybi vayuqîmûna ṣṣalâta vamimmâ razaqnâhum yunfiqûn",
    (30, 30): "faʾaqim vachaka liddîni ḥanîfan fiṭrata llâhi llatî faṭara nnâsa ʿalayhâ lâ "
              "tabdîla liḫalqi llâhi ẕâlika ddînu lqayyimu valâkinna ʾaks̱ara nnâsi lâ yaʿlamûn",
    (107, 4): "favaylul lilmuṣallîn",
}

# Her satır bir kurala karşılık gelir (okunus_kurallari.md §3–4): (ayet, Tanzil kelimesi, beklenen)
KURAL_ORNEKLERI = [
    ((2, 1), "الٓمٓ", "ʾalif lâm mîm"),                    # mukattaa
    ((19, 1), "كٓهيعٓصٓ", "kâf hâ yâ ʿayn ṣâd"),
    ((9, 1), "عَٰهَدتُّم", "ʿâhattum"),                     # kelime içi idgam (د → تّ)
    ((2, 245), "مَّن", "man"),                              # ayet başı şedde
    ((2, 33), "أَنۢبِئْهُم", "ʾambiʾhum"),                   # iklab ۢ
    ((2, 95), "أَبَدًۢا", "ʾabadam"),                       # tenvin iklabı
    ((2, 9), "ءَامَنُوا۟", "ʾâmanû"),                       # ۟
    ((2, 258), "أَنَا۠", "ʾana"),                           # ۠ vaslda
    ((33, 10), "ٱلظُّنُونَا۠", "ẓẓunûnâ"),                  # ۠ vakfta
    ((2, 4), "وَبِٱلْـَٔاخِرَةِ", "vabilʾâḫirati"),          # ـٔ
    ((2, 245), "وَيَبْصُۜطُ", "vayabsuṭu"),                 # ۜ
    ((9, 1), "وَرَسُولِهِۦٓ", "varasûlihî"),                # ۦ sıla
    ((2, 124), "إِبْرَٰهِـۧمَ", "ʾibrâhîma"),               # ۧ
    ((21, 88), "نُـۨجِى", "nuncî"),                         # ۨ
    ((11, 41), "مَجْر۪ىٰهَا", "macrêhâ"),                   # ۪ imâle
    ((41, 44), "ءَا۬عْجَمِىٌّ", "ʾaʾaʿcamiyyun"),           # ۬ teshil
    ((2, 61), "عَصَوا۟", "ʿaṣav"),                          # diftong + kelimeler arası idgam
    ((2, 61), "وَّكَانُوا۟", "vakânû"),
    ((2, 5), "هُدًى", "hudam"),                             # tenvin + ى, sonra idgam (مِّن)
]


def ayet(s, a):
    return okunus.oku(s, a)


class OkunusTesti(unittest.TestCase):
    def test_tanzil_sabit(self):
        self.assertEqual(veri.sha256(okunus.TANZIL_YOLU), okunus.TANZIL_SHA256)
        self.assertEqual(len(okunus.tanzil()), 6_236)

    def test_test_ayetleri(self):
        for (s, a), beklenen in BEKLENEN.items():
            with self.subTest(ayet=f"{s}:{a}"):
                o = ayet(s, a)
                self.assertEqual(o.latin, beklenen)
                self.assertEqual(o.belirsiz, [])
                self.assertEqual(o.besmele, [])
                self.assertEqual(len(o.kelimeler), len(okunus.tanzil()[(s, a)].split(" ")))

    def test_kural_ornekleri(self):
        for (s, a), arapca, beklenen in KURAL_ORNEKLERI:
            with self.subTest(ayet=f"{s}:{a}", beklenen=beklenen):
                # İşaret sırası yazıma göre değişebilir; kanonik (NFD) biçimde karşılaştırılır.
                nfd = unicodedata.normalize("NFD", arapca)
                eslesen = [k.latin for k in ayet(s, a).kelimeler
                           if unicodedata.normalize("NFD", k.arapca) == nfd]
                self.assertTrue(eslesen, f"Tanzil kelimesi ayette yok: {arapca}")
                self.assertEqual(set(eslesen), {beklenen})

    def test_tum_korpus(self):
        """6.236 ayet: bilinmeyen karakter yok, belirsiz yok, çıktıda Arapça harf yok."""
        arapca = re.compile("[؀-ۿ]")
        hatali, belirsiz, arapcali = [], [], []
        for (s, a), metin in okunus.tanzil().items():
            try:
                o = okunus.ayet_oku(s, a, metin)
            except okunus.BilinmeyenKarakter as e:
                hatali.append((s, a, str(e)))
                continue
            belirsiz += [(s, a, b) for b in o.belirsiz]
            if arapca.search(o.latin):
                arapcali.append((s, a))
        self.assertEqual(hatali, [])
        self.assertEqual(belirsiz, [])
        self.assertEqual(arapcali, [])

    def test_besmele_oneki_112(self):
        onekli = [k for k, m in okunus.tanzil().items() if okunus.ayet_oku(*k, m).besmele]
        self.assertEqual(len(onekli), 112)
        self.assertNotIn((1, 1), onekli)
        self.assertFalse(any(s == 9 for s, _ in onekli))

    def test_lafzatullah_deseni_qac_ile_ayni(self):
        """Kural 13'ün deseni, ayet ayet QAC {ll~ah + {ll~ahum~a lemma sayısıyla aynı."""
        kor = veri.korpus()
        qac = collections.Counter()
        for lemma in ("{ll~ah", "{ll~ahum~a"):
            for k in kor.lemma_kelimeleri[lemma]:
                qac[(k.sure, k.ayet)] += 1
        tanzil = collections.Counter()
        for (s, a), metin in okunus.tanzil().items():
            o = okunus.ayet_oku(s, a, metin)
            n = sum(1 for k in o.kelimeler if okunus.ALLAH_RE.search(k.arapca))
            if n:
                tanzil[(s, a)] = n
        self.assertEqual(sum(qac.values()), sum(tanzil.values()))
        self.assertEqual(dict(qac), dict(tanzil))

    def test_kok_gosterimi_ile_ortak_harf_tablosu(self):
        for bw, latin in veri.KOK_LATIN.items():
            arapca = "ء" if bw == "A" else veri.BW_ARAPCA[bw]
            self.assertEqual(latin, harf.HARF_LATIN[arapca], bw)
        self.assertEqual(veri.kok_latin("Amn"), "ʾ-m-n")
        self.assertEqual(veri.kok_latin("Slw"), "ṣ-l-v")
        unsuzler = [l for _, l, _ in harf.HARF_TABLOSU]
        self.assertEqual(len(unsuzler), len(set(unsuzler)), "iki ünsüz aynı Latin karşılığa düştü")

    def test_belge_tablosu_kod_ile_ayni(self):
        belge = (_ortak.MASA / "okunus_kurallari.md").read_text(encoding="utf-8")
        blok = belge.split("<!-- UNSUZ_TABLOSU_BASI -->")[1].split("<!-- UNSUZ_TABLOSU_SONU -->")[0]
        satirlar = [s for s in blok.strip().splitlines()[2:]]
        belgedeki = tuple(tuple(h.strip() for h in s.strip("|").split("|")) for s in satirlar)
        self.assertEqual(belgedeki, harf.HARF_TABLOSU)

    def test_komut_kaydi(self):
        tampon = io.StringIO()
        with contextlib.redirect_stdout(tampon):
            kod = main(["okunus", "107:4"])
        satirlar = tampon.getvalue().rstrip("\n").splitlines()
        self.assertEqual(kod, 0)
        self.assertEqual(satirlar[-5], "Kaynak      : Tanzil Uthmani v1.1")
        self.assertEqual(satirlar[-2], f"Veri izi    : {okunus.TANZIL_SHA256[:12]}")
        self.assertEqual(satirlar[-1], "Durum       : çalıştırıldı")
        with contextlib.redirect_stdout(io.StringIO()) as t:
            kod = main(["okunus", "2:999"])
        self.assertEqual(kod, 2)
        self.assertIn("Durum       : çalıştırılmadı", t.getvalue())


if __name__ == "__main__":
    unittest.main()
