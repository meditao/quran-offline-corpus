"""§8 kayıt satırı: her sorgu çıktısı 5 satırlık kayıt bloğuyla biter."""

import contextlib
import io
import unittest

import _ortak  # noqa: F401
from tezgah import veri
from tezgah.__main__ import main

KOMUTLAR = [
    ["sayim"],
    ["sayim", "--kok", "Slw"],
    ["sayim", "--etiket", "INDEF"],
    ["kokler", "--limit", "3"],
    ["kok", "Slw", "--limit", "2"],
    ["lemma", "Salaw`p", "--limit", "2"],
    ["dagilim", "--kok", "Amn", "--gore", "tur"],
    ["dagilim", "--kok", "Amn", "--gore", "lemma"],
    ["dagilim", "--kok", "Amn", "--gore", "bab"],
    ["dagilim", "--kok", "Amn", "--gore", "iyelik"],
    ["dagilim", "--kok", "Amn", "--gore", "sure"],
    ["etiket", "(X)", "--limit", "2"],
    ["birlikte", "Amn", "Eml", "--limit", "2"],
    ["kalip", "ROOT:Amn&POS:V PRON:3MP bi+", "--limit", "2"],
    ["denetim"],
]


def calistir(argv):
    tampon = io.StringIO()
    with contextlib.redirect_stdout(tampon):
        kod = main(argv)
    return kod, tampon.getvalue().rstrip("\n").splitlines()


class KayitTesti(unittest.TestCase):
    def blok_denetle(self, satirlar, argv, durum):
        son = satirlar[-5:]
        self.assertTrue(son[0].startswith("Kaynak      : QAC v0.4"), son)
        self.assertTrue(son[1].startswith("Sayım birimi: "), son)
        self.assertEqual(son[2], "Sorgu       : python -m tezgah " + " ".join(
            a if " " not in a and "&" not in a and "(" not in a and "`" not in a else f"'{a}'" for a in argv))
        self.assertEqual(son[3], f"Veri izi    : {veri.QAC_SHA256[:12]}")
        self.assertTrue(son[4].startswith(f"Durum       : {durum}"), son)

    def test_her_komut_kayitla_biter(self):
        for argv in KOMUTLAR:
            with self.subTest(argv=argv):
                kod, satirlar = calistir(argv)
                self.assertEqual(kod, 0)
                self.blok_denetle(satirlar, argv, "çalıştırıldı")
                birim = satirlar[-4].split(": ", 1)[1]
                self.assertNotEqual(birim, "—", "sayım birimi yazılmamış")

    def test_calismayan_sorgu_bunu_soyler(self):
        for argv in (["kok", "s-l-v"], ["sayim", "--etiket", "DEF"], ["kok", "slv"]):
            with self.subTest(argv=argv):
                kod, satirlar = calistir(argv)
                self.assertEqual(kod, 2)
                self.assertTrue(satirlar[0].startswith("HATA: "))
                self.blok_denetle(satirlar, argv, "çalıştırılmadı")


if __name__ == "__main__":
    unittest.main()
