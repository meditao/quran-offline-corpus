"""Tek giriş noktası: python -m tezgah <komut> ...

Çalıştırma (depo kökünden):
    PYTHONPATH=09_calisma_masasi python -m tezgah kok Slw
veya 09_calisma_masasi/ içinden:
    python -m tezgah kok Slw
"""

from __future__ import annotations

import argparse
import sys
import unittest
from pathlib import Path

from . import tara, veri
from .kayit import CALISTIRILMADI, Kayit, komut_metni

TESTLER = Path(__file__).resolve().parents[1] / "testler"


def _denetim(_kor, _ns) -> tara.Sonuc:
    sonuclar = veri.kurulum_denetimi()
    tablo = [[d.ad, d.beklenen, d.bulunan, "GEÇTİ" if d.gecti else "KALDI"] for d in sonuclar]
    satirlar = ["Kurulum denetimi (QAC v0.4):", *tara._tablo(["denetim", "beklenen", "bulunan", "sonuç"], tablo)]
    basarili = all(d.gecti for d in sonuclar)
    satirlar.append(f"Sonuç: {sum(d.gecti for d in sonuclar)} / {len(sonuclar)} denetim geçti.")
    return tara.Sonuc(satirlar, ["sûre", "ayet", "kelime konumu", "segment"], basarili=basarili)


def _test(_kor, ns) -> tara.Sonuc:
    yukleyici = unittest.TestLoader()
    paket = yukleyici.discover(str(TESTLER), top_level_dir=str(TESTLER))
    sonuc = unittest.TextTestRunner(verbosity=2 if ns.ayrintili else 1, stream=sys.stdout).run(paket)
    gecen = sonuc.testsRun - len(sonuc.failures) - len(sonuc.errors)
    satirlar = [
        "",
        f"Sağlama testleri: {sonuc.testsRun} çalıştı | {gecen} geçti | "
        f"{len(sonuc.failures)} başarısız | {len(sonuc.errors)} hata | {len(sonuc.skipped)} atlandı",
    ]
    return tara.Sonuc(satirlar, [], basarili=sonuc.wasSuccessful())


def _secici_ekle(p: argparse.ArgumentParser) -> None:
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--kok", help="Kök: Arapça harf veya Buckwalter (ör. Slw). Latin okunuş reddedilir.")
    g.add_argument("--lemma", help="QAC lemma (Buckwalter veya Arapça)")


def parser_kur() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python -m tezgah", description="Kur'an çalışma masası (QAC v0.4)")
    alt = p.add_subparsers(dest="komut", required=True, metavar="komut")

    s = alt.add_parser("denetim", help="kurulum denetimi (sha256, telif bloğu, temel sayımlar)")
    s.set_defaults(islev=_denetim, korpus_gerekmez=True)

    s = alt.add_parser("test", help="sağlama testlerini çalıştır")
    s.add_argument("-v", "--ayrintili", action="store_true")
    s.set_defaults(islev=_test, korpus_gerekmez=True)

    s = alt.add_parser("kokler", help="bütün kökler ve sayımları")
    s.add_argument("--limit", type=int, default=0, help="gösterilecek satır; 0 = tümü")
    s.add_argument("--siralama", choices=["siklik", "alfabe"], default="siklik")
    s.set_defaults(islev=lambda k, n: tara.kokler(k, n.limit, n.siralama))

    s = alt.add_parser("kok", help="bir kökün geçişleri (kelime konumu)")
    s.add_argument("kok", help="Arapça harf veya Buckwalter (ör. Slw)")
    s.add_argument("--limit", type=int, default=50, help="gösterilecek geçiş; 0 = tümü")
    s.set_defaults(islev=lambda k, n: tara.kok(k, n.kok, n.limit))

    s = alt.add_parser("lemma", help="bir lemmanın geçişleri (kelime konumu)")
    s.add_argument("lemma")
    s.add_argument("--limit", type=int, default=50)
    s.set_defaults(islev=lambda k, n: tara.lemma(k, n.lemma, n.limit))

    s = alt.add_parser("sayim", help="sayım: korpus toplamı, kök, lemma veya etiket")
    g = s.add_mutually_exclusive_group()
    g.add_argument("--kok")
    g.add_argument("--lemma")
    g.add_argument("--etiket", nargs="+", help="tam eşleşme; birden fazlası aynı segmentte aranır")
    s.add_argument("--alt-dize", action="store_true", help="etiketi alt-dize olarak eşle (uyarı basılır)")
    s.set_defaults(islev=lambda k, n: tara.sayim(k, n.kok, n.lemma, n.etiket, n.alt_dize))

    s = alt.add_parser("dagilim", help="dağılım: tür / lemma / bab / iyelik / sûre")
    _secici_ekle(s)
    s.add_argument("--gore", required=True, choices=["tur", "lemma", "bab", "iyelik", "sure"])
    s.set_defaults(islev=lambda k, n: tara.dagilim(k, n.gore, n.kok, n.lemma))

    s = alt.add_parser("etiket", help="segment düzeyi etiket sorgusu (tam eşleşme)")
    s.add_argument("etiketler", nargs="+", help='ör. "(IV)" PRON:3MP ROOT:Amn TAG:V')
    s.add_argument("--alt-dize", action="store_true")
    s.add_argument("--limit", type=int, default=50)
    s.set_defaults(islev=lambda k, n: tara.etiket(k, n.etiketler, n.alt_dize, n.limit))

    s = alt.add_parser("birlikte", help="iki kökün aynı ayette ortak geçişi")
    s.add_argument("kok_a")
    s.add_argument("kok_b")
    s.add_argument("--pencere", type=int, help="± kelime konumu penceresi (aynı ayet içinde)")
    s.add_argument("--limit", type=int, default=50)
    s.set_defaults(islev=lambda k, n: tara.birlikte(k, n.kok_a, n.kok_b, n.pencere, n.limit))

    s = alt.add_parser("kalip", help="ardışık segment deseni")
    s.add_argument("desen", help='boşlukla ayrılmış segmentler; & = aynı segmentte, !X = X olmasın, * = herhangi. '
                                 'ör. "ROOT:Amn&POS:V PRON:3MP bi+"')
    s.add_argument("--kelime-ici", action="store_true", help="yalnız aynı kelime konumu içinde ara")
    s.add_argument("--alt-dize", action="store_true")
    s.add_argument("--limit", type=int, default=50)
    s.set_defaults(islev=lambda k, n: tara.kalip(k, n.desen, n.kelime_ici, n.alt_dize, n.limit))
    return p


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    ns = parser_kur().parse_args(args)
    sorgu = komut_metni(args)
    veri_izi = "—"
    try:
        kor = None
        if not getattr(ns, "korpus_gerekmez", False):
            kor = veri.korpus()
            veri_izi = kor.veri_izi
        sonuc = ns.islev(kor, ns)
    except (tara.GirdiHatasi, veri.VeriHatasi) as hata:
        if veri_izi == "—" and veri.QAC_YOLU.exists():
            veri_izi = veri.sha256(veri.QAC_YOLU)[:12]
        sebep = "girdi hatası" if isinstance(hata, tara.GirdiHatasi) else "veri hatası"
        print(f"HATA: {hata}")
        print(Kayit(sorgu, veri_izi=veri_izi, durum=CALISTIRILMADI, sebep=sebep).metin())
        return 2
    if kor is None:
        veri_izi = veri.sha256(veri.QAC_YOLU)[:12] if veri.QAC_YOLU.exists() else "—"
    print("\n".join(sonuc.satirlar))
    print(Kayit(sorgu, birimler=sonuc.birimler, veri_izi=veri_izi).metin())
    return 0 if sonuc.basarili else 1


if __name__ == "__main__":
    sys.exit(main())
