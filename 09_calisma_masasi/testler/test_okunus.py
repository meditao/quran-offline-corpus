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
# İkinci alan: Tanzil'de sûre başı besmele öneki var mı.
BEKLENEN = {
    (1, 1): ("bismi llâhi rraḥmâni rraḥîm", False),
    (2, 3): ("allaẕîna yuʾminûna bilgaybi vayuqîmûna ṣṣalâta vamimmâ razaqnâhum yunfiqûn", False),
    (30, 30): ("faʾaqim vachaka liddîni ḥanîfan fiṭrata llâhi llatî faṭara nnâsa ʿalayhâ lâ "
               "tabdîla liḫalqi llâhi ẕâlika ddînu lqayyimu valâkinna ʾaks̱ara nnâsi lâ yaʿlamûn", False),
    (107, 4): ("favaylul lilmuṣallîn", False),
    # hurûf-ı mukattaa
    (2, 1): ("ʾalif lâm mîm", True),
    (19, 1): ("kâf hâ yâ ʿayn ṣâd", True),
    (42, 1): ("ḥâ mîm", True),
    (42, 2): ("ʿayn sîn qâf", False),
    # kelime başında vasl elifinin ünlüsü (ibtidâ): i ve u
    (1, 6): ("ihdinâ ṣṣirâṭa lmustaqîm", False),
    (96, 1): ("iqraʾ bismi rabbika llaẕî ḫalaq", True),
    (16, 125): ("udʿu ʾilâ sabîli rabbika bilḥikmati valmavʿiẓati lḥasanati vacâdilhum billatî hiya "
                "ʾaḥsanu ʾinna rabbaka huva ʾaʿlamu biman żalla ʿan sabîlihî vahuva ʾaʿlamu bilmuhtadîn", False),
    (4, 50): ("unẓur kayfa yaftarûna ʿalâ llâhi lkaẕiba vakafâ bihî ʾis̱mam mubînâ", False),
    # sekte yerleri: Tanzil v1.1'de işaret yok (okunus_kurallari.md §3b)
    (18, 1): ("alḥamdu lillâhi llaẕî ʾanzala ʿalâ ʿabdihi lkitâba valam yacʿal lahû ʿivacâ", True),
    (18, 2): ("qayyimal liyunẕira baʾsan şadîdam mil ladunhu vayubaşşira lmuʾminîna llaẕîna yaʿmalûna "
              "ṣṣâliḥâti ʾanna lahum ʾacran ḥasanâ", False),
    (36, 52): ("qâlû yâvaylanâ mam baʿas̱anâ mim marqadinâ hâẕâ mâ vaʿada rraḥmânu vaṣadaqa lmursalûn", False),
    (69, 28): ("mâ ʾagnâ ʿannî mâliyah", False),   # sekte Hafs'ta isteğe bağlı (§3b)
    (75, 27): ("vaqîla man râq", False),
    (83, 14): ("kallâ bal râna ʿalâ qulûbihim mâ kânû yaksibûn", False),
    # özel işaretler
    (21, 88): ("fastacabnâ lahû vanaccaynâhu mina lgammi vakaẕâlika nuncî lmuʾminîn", False),
    (11, 41): ("vaqâla rkabû fîhâ bismi llâhi macrêhâ vamursâhâ ʾinna rabbî lagafûrur raḥîm", False),
    (112, 1): ("qul huva llâhu ʾaḥad", True),
    (112, 2): ("allâhu ṣṣamad", False),
}

SEKTE_AYETLERI = [(18, 1), (36, 52), (69, 28), (75, 27), (83, 14)]


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
        for (s, a), (beklenen, besmele_var) in BEKLENEN.items():
            with self.subTest(ayet=f"{s}:{a}"):
                o = ayet(s, a)
                self.assertEqual(o.latin, beklenen)
                self.assertEqual(o.belirsiz, [])
                self.assertEqual(bool(o.besmele), besmele_var)
                if besmele_var:
                    self.assertEqual(" ".join(k.latin for k in o.besmele), BEKLENEN[(1, 1)][0])
                self.assertEqual(len(o.kelimeler) + len(o.besmele), len(okunus.tanzil()[(s, a)].split(" ")))

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

    def test_ibtida_vasl_elifli_isimler_i(self):
        # Korpusta ayet başında geçmeyen isimler: kuralın fiil/isim ayrımı birim düzeyinde sınanır.
        for kelime, beklenen in (("ٱبْنُ", "ibnu"), ("ٱسْمُهُۥ", "ismuhû"), ("ٱمْرُؤٌا۟", "imruʾun"),
                                 ("ٱثْنَانِ", "is̱nâni"), ("ٱنظُرْ", "unẓur"), ("ٱدْعُ", "udʿu"),
                                 ("ٱسْمَعْ", "ismaʿ"), ("ٱقْرَأْ", "iqraʾ"),
                                 ("ٱمْرَأَتُ", "imraʾatu"), ("ٱمْرَأَةً", "imraʾatan"),
                                 ("ٱثْنَتَا", "is̱natâ"), ("ٱثْنَتَيْنِ", "is̱natayni"),
                                 ("ٱسْتَغْفِرْ", "istagfir"), ("ٱسْتُهْزِئَ", "ustuhziʾa")):
            with self.subTest(kelime=kelime):
                self.assertEqual(okunus._metin(okunus.kelime_oku(kelime, True)[0]), beklenen)

    def test_ibtida_qac_ile_bagimsiz_dogrulama(self):
        """Ayet başı vasl elifli kelimeler: araç ↔ ham QAC (IMPV etiketi, bab, gövde harekesi).

        QAC tarafı: IMPV + I. bab -> 2. kök harfinin gövde harekesi u ise u (yâ ile biten kök hariç);
        türemiş bab, PERF etken ve isim -> i; PERF edilgen -> u.
        """
        bablar = {f"({b})" for b in ("II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII")}
        isaret = set("aiuo~`FNK^@{")
        qac = {}
        with veri.QAC_YOLU.open(encoding="utf-8-sig", newline="") as f:
            for satir in f:
                alan = satir.rstrip("\r\n").split("\t")
                if len(alan) == 4 and alan[0].startswith("("):
                    s_, a_, k_, _ = map(int, alan[0].strip("()").split(":"))
                    if k_ == 1 and "STEM" in alan[3].split("|"):
                        qac[(s_, a_)] = (alan[1], alan[3].split("|"))

        def govde_unlusu(bicim):
            n = 0
            for i, c in enumerate(bicim[1:], 1):
                if c not in isaret:
                    n += 1
                    if n == 2:
                        return next((d for d in bicim[i + 1:] if d in "aui"), None)
            return None

        def beklenen(bicim, oz):
            kok = next((x[5:] for x in oz if x.startswith("ROOT:")), "")
            if "POS:V" in oz and "IMPV" in oz and not bablar & set(oz):
                return "u" if govde_unlusu(bicim) == "u" and not kok.endswith("y") else "i"
            if "POS:V" in oz and "PASS" in oz:
                return "u"
            return "i"

        sayac = collections.Counter()
        for (s, a), metin in okunus.tanzil().items():
            ilk = okunus.ayet_oku(s, a, metin).kelimeler[0]
            if not (ilk.arapca.startswith(okunus.VASL_ELIF) and ilk.arapca[1:2] != "ل"):
                continue
            bicim, oz = qac[(s, a)]
            with self.subTest(ayet=f"{s}:{a}"):
                self.assertTrue(bicim.startswith("{"), "QAC'ta da vasl elifi olmalı")
                self.assertEqual(ilk.latin[0], beklenen(bicim, oz), (ilk.latin, bicim))
            sayac["IMPV" if "IMPV" in oz else ("V" if "POS:V" in oz else "N")] += 1
        self.assertEqual(sum(sayac.values()), 54)
        self.assertEqual(dict(sayac), {"IMPV": 46, "V": 7, "N": 1})

    def test_mukattaa_tablosu_belge_ve_harf_tablosuyla_ayni(self):
        belge = (_ortak.MASA / "okunus_kurallari.md").read_text(encoding="utf-8")
        blok = belge.split("<!-- MUKATTAA_TABLOSU_BASI -->")[1].split("<!-- MUKATTAA_TABLOSU_SONU -->")[0]
        belgedeki = tuple(tuple(h.strip() for h in s.strip("|").split("|"))
                          for s in blok.strip().splitlines()[2:])
        self.assertEqual(belgedeki, okunus.MUKATTAA_TABLOSU)
        for h, ad in okunus.MUKATTAA_TABLOSU:
            ilk = harf.HARF_LATIN["ء" if h == "ا" else h]
            self.assertTrue(ad.startswith(ilk), (h, ad, ilk))

    def test_mukattaa_ham_qac_ile_bagimsiz_dogrulama(self):
        """Tanzil taraması ↔ ham QAC INL satırları: ayet, kelime konumu ve harf dizisi birebir.

        QAC tarafı veri.py ayrıştırıcısını kullanmaz; ham dosya burada ayrıca okunur.
        """
        bw = {"A": "ا", "l": "ل", "m": "م", "S": "ص", "r": "ر", "k": "ك", "h": "ه", "y": "ي",
              "E": "ع", "T": "ط", "s": "س", "H": "ح", "q": "ق", "n": "ن"}
        qac = {}
        with veri.QAC_YOLU.open(encoding="utf-8-sig", newline="") as f:
            for satir in f:
                alan = satir.rstrip("\r\n").split("\t")
                if len(alan) == 4 and alan[2] == "INL":
                    s, a, k, _ = map(int, alan[0].strip("()").split(":"))
                    qac[(s, a, k)] = "".join(bw[c] for c in alan[1].replace("^", ""))
        tanzil = {(s, a, i): hf for s, a, i, hf, _ in okunus.mukattaa_taramasi()}
        self.assertEqual(len(qac), 30)
        self.assertEqual(tanzil, qac)
        ayetler = {(s, a) for s, a, _ in tanzil}
        self.assertEqual((len(ayetler), len({s for s, _ in ayetler})), (30, 29))

    def test_mukattaa_okunusu_harf_sayisi_kadar_ad(self):
        for s, a, _, hf, latin in okunus.mukattaa_taramasi():
            with self.subTest(ayet=f"{s}:{a}"):
                self.assertEqual(latin.split(" "), [okunus.MUKATTAA_ADLARI[h] for h in hf])

    def test_sekte_isareti_tanzilde_yok(self):
        """U+06DC yalnız 2:245 ve 7:69'da, ص üzerinde; sekte ayetlerinde hiçbir sekte işareti yok."""
        yerler = {k for k, m in okunus.tanzil().items() if "\u06DC" in m}
        self.assertEqual(yerler, {(2, 245), (7, 69)})
        for k in yerler:
            for w in okunus.tanzil()[k].split():
                if "\u06DC" in w:
                    oncesi = [c for c in w[: w.index("\u06DC")] if c not in okunus.HAREKELER]
                    self.assertEqual(oncesi[-1], "ص", (k, w))
        for k in SEKTE_AYETLERI:
            self.assertFalse(any("\u06D6" <= c <= "\u06DC" for c in okunus.tanzil()[k]), k)

    def test_komut_kaydi(self):
        tampon = io.StringIO()
        with contextlib.redirect_stdout(tampon):
            kod = main(["okunus", "107:4"])
        satirlar = tampon.getvalue().rstrip("\n").splitlines()
        self.assertEqual(kod, 0)
        # Durak işaretli sürüm kuruluysa ikinci kaynak ve izi de yazılır (okunus_komutu).
        kaynak, iz = "Tanzil Uthmani v1.1", okunus.TANZIL_SHA256[:12]
        if okunus.DURAK_YOLU.exists():
            kaynak += f" | + {okunus.DURAK_KAYNAK_ADI}"
            iz += f" | {veri.sha256(okunus.DURAK_YOLU)[:12]}"
        self.assertEqual(satirlar[-5], f"Kaynak      : {kaynak}")
        self.assertEqual(satirlar[-2], f"Veri izi    : {iz}")
        self.assertEqual(satirlar[-1], "Durum       : çalıştırıldı")
        with contextlib.redirect_stdout(io.StringIO()) as t:
            kod = main(["okunus", "2:999"])
        self.assertEqual(kod, 2)
        self.assertIn("Durum       : çalıştırılmadı", t.getvalue())


if __name__ == "__main__":
    unittest.main()
