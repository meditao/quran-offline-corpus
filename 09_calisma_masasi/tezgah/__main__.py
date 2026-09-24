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

from . import kavram, okuma, okunus, qm, tara, tez, veri
from .ikincil import lane, sami
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
    gecen = sonuc.testsRun - len(sonuc.failures) - len(sonuc.errors) - len(sonuc.skipped)
    satirlar = [
        "",
        f"Sağlama testleri: {sonuc.testsRun} çalıştı | {gecen} geçti | "
        f"{len(sonuc.failures)} başarısız | {len(sonuc.errors)} hata | {len(sonuc.skipped)} atlandı",
    ]
    return tara.Sonuc(satirlar, [], basarili=sonuc.wasSuccessful())


def _capraz_ekle(kor, ns, sonuc: tara.Sonuc) -> tara.Sonuc:
    """--capraz: QAC sonucunun altına quran-morphology sonucunu ayrı tablolarla ekler."""
    if not getattr(ns, "capraz", False):
        return sonuc
    if "kok" not in sonuc.veri:
        raise tara.GirdiHatasi("--capraz yalnız kök sorgusuyla kullanılır (kok X / sayim --kok X).")
    satirlar, veri_ = qm.capraz(kor, sonuc.veri["kok"])
    sonuc.satirlar += satirlar
    sonuc.veri["capraz"] = veri_
    sonuc.kaynak = f"{sonuc.kaynak or veri.KAYNAK_ADI} | + {qm.KAYNAK_ADI}"
    sonuc.veri_izi = f"{sonuc.veri_izi or kor.veri_izi} | {qm.korpus().veri_izi}"
    return sonuc


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
    s.add_argument("--capraz", action="store_true", help="quran-morphology sonucunu ayrı tabloda yan yana göster")
    s.add_argument("--bw", action="store_true", help="Buckwalter biçim/lemma ek sütun olarak (varsayılan: Latin okunuş)")
    s.set_defaults(islev=lambda k, n: _capraz_ekle(k, n, tara.kok(k, n.kok, n.limit, n.bw)))

    s = alt.add_parser("lemma", help="bir lemmanın geçişleri (kelime konumu)")
    s.add_argument("lemma")
    s.add_argument("--limit", type=int, default=50)
    s.add_argument("--bw", action="store_true", help="Buckwalter biçim/lemma ek sütun olarak (varsayılan: Latin okunuş)")
    s.set_defaults(islev=lambda k, n: tara.lemma(k, n.lemma, n.limit, n.bw))

    s = alt.add_parser("sayim", help="sayım: korpus toplamı, kök, lemma veya etiket")
    g = s.add_mutually_exclusive_group()
    g.add_argument("--kok")
    g.add_argument("--lemma")
    g.add_argument("--etiket", nargs="+", help="tam eşleşme; birden fazlası aynı segmentte aranır")
    s.add_argument("--alt-dize", action="store_true", help="etiketi alt-dize olarak eşle (uyarı basılır)")
    s.add_argument("--capraz", action="store_true", help="--kok ile: quran-morphology sonucunu ayrı tabloda göster")
    s.set_defaults(islev=lambda k, n: _capraz_ekle(k, n, tara.sayim(k, n.kok, n.lemma, n.etiket, n.alt_dize)))

    s = alt.add_parser("dagilim", help="dağılım: tür / lemma / bab / iyelik / sûre")
    _secici_ekle(s)
    s.add_argument("--gore", required=True, choices=["tur", "lemma", "bab", "iyelik", "sure"])
    s.add_argument("--bw", action="store_true", help="Buckwalter biçim/lemma ek sütun olarak (varsayılan: Latin okunuş)")
    s.set_defaults(islev=lambda k, n: tara.dagilim(k, n.gore, n.kok, n.lemma, n.bw))

    s = alt.add_parser("etiket", help="segment düzeyi etiket sorgusu (tam eşleşme)")
    s.add_argument("etiketler", nargs="+", help='ör. "(IV)" PRON:3MP ROOT:Amn TAG:V')
    s.add_argument("--alt-dize", action="store_true")
    s.add_argument("--limit", type=int, default=50)
    s.add_argument("--bw", action="store_true", help="Buckwalter biçim/lemma ek sütun olarak (varsayılan: Latin okunuş)")
    s.set_defaults(islev=lambda k, n: tara.etiket(k, n.etiketler, n.alt_dize, n.limit, n.bw))

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
    s.add_argument("--bw", action="store_true", help="Buckwalter biçim/lemma ek sütun olarak (varsayılan: Latin okunuş)")
    s.set_defaults(islev=lambda k, n: tara.kalip(k, n.desen, n.kelime_ici, n.alt_dize, n.limit, n.bw))

    s = alt.add_parser("okunus", help="ayet okunuşu (Tanzil Uthmani'den kurallı Latin aktarım)")
    s.add_argument("ayetler", nargs="*", help="sûre:ayet, ör. 2:3 30:30")
    s.add_argument("--arapca", action="store_true", help="denetim için Tanzil kelimesini yanında göster")
    s.add_argument("--mukattaa", action="store_true", help="tüm korpusta hurûf-ı mukattaa taraması")
    s.add_argument("--durak", action="store_true",
                   help="sekte dışı durak işaretlerini de göster (geleneksel — yorum içerebilir)")
    s.set_defaults(islev=lambda k, n: okunus.mukattaa_komutu() if n.mukattaa
                   else okunus.okunus_komutu(n.ayetler, n.arapca, n.durak),
                   korpus_gerekmez=True, veri_kaynagi="tanzil")

    s = alt.add_parser("ayet", help="ayet görünümü: okunuş + kelime çözümlemesi + çalışma çevirisi (+ meal)")
    s.add_argument("ayet", help="sûre:ayet, ör. 2:3")
    s.add_argument("--meal", action="store_true", help="meal (kurumsal okuma — sınanan, delil değil)")
    s.add_argument("--arapca", action="store_true", help="denetim için Tanzil kelimesini yanında göster")
    s.set_defaults(islev=lambda k, n: okuma.ayet_komutu(n.ayet, n.meal, n.arapca))

    s = alt.add_parser("ceviri", help="çalışma çevirisi ekle/göster (kullanıcının yorumu)")
    s.add_argument("ayet")
    s.add_argument("metin", nargs="?", help="verilirse yeni sürüm olarak eklenir")
    s.set_defaults(islev=lambda k, n: okuma.ceviri_komutu(n.ayet, n.metin), korpus_gerekmez=True)

    s = alt.add_parser("kur", help="yerel/ katmanı kur (meal, quran-morphology, lane, sedra)")
    s.add_argument("ne", choices=["meal", "quran-morphology", "lane", "sedra"])
    s.set_defaults(islev=lambda k, n: okuma.kur_komutu(n.ne), korpus_gerekmez=True)

    s = alt.add_parser("lane", help="Lane sözlüğü (hipotez): kok / kapsam / sigla")
    la = s.add_subparsers(dest="lane_komut", required=True, metavar="işlem")
    x = la.add_parser("kok", help="kök maddeleri")
    x.add_argument("kok")
    x.add_argument("--tam", action="store_true")
    x.add_argument("--madde", type=int)
    x.set_defaults(islev=lambda k, n: lane.kok_komutu(k, n.kok, n.tam, n.madde))
    x = la.add_parser("kapsam", help="QAC köklerinin Lane eşleşmesi ve bölge yoğunluğu (ölçüm)")
    x.set_defaults(islev=lambda k, n: lane.kapsam_komutu(k))
    x = la.add_parser("sigla", help="kaynak kısaltmaları (ölçüm + kategori)")
    x.set_defaults(islev=lambda k, n: lane.sigla_komutu(), korpus_gerekmez=True)

    s = alt.add_parser("sami", help="Sâmî katmanı (hipotez): kok / gurultu / denklik / atif")
    sa = s.add_subparsers(dest="sami_komut", required=True, metavar="işlem")
    x = sa.add_parser("kok", help="İbranice ve Süryanice kognat adayları")
    x.add_argument("kok")
    x.add_argument("--tek-dil", action="store_true", help="tek dil vuruşlarının adaylarını da göster (etiketli)")
    x.add_argument("--tam", action="store_true")
    x.add_argument("--zayif-son", action="store_true",
                   help="son harfi zayıf kök için İbranice ה / Süryanice Alef eşlemesi (ölçümde gürültüyü artırıyor)")
    x.set_defaults(islev=lambda k, n: sami.kok_komutu(k, n.kok, n.tek_dil, n.tam, n.zayif_son))
    x = sa.add_parser("gurultu", help="rastgele kontrolle gürültü tabanı (ölçüm)")
    x.add_argument("--tekrar", type=int, default=10)
    x.add_argument("--tohum", type=int, default=20260924)
    x.set_defaults(islev=lambda k, n: sami.gurultu_komutu(k, n.tekrar, n.tohum))
    x = sa.add_parser("denklik", help="ünsüz denklik tablosu")
    x.set_defaults(islev=lambda k, n: sami.denklik_komutu(), korpus_gerekmez=True)
    x = sa.add_parser("atif", help="SEDRA atıf metni")
    x.set_defaults(islev=lambda k, n: sami.atif_komutu(), korpus_gerekmez=True)

    kavram.parser_ekle(alt)
    tez.parser_ekle(alt)

    s = alt.add_parser("arayuz", help="yerel web arayüzü (yalnız 127.0.0.1; aynı komutları çalıştırır)")
    s.add_argument("--port", type=int, default=8765)
    s.add_argument("--tarayici-acma", action="store_true", help="tarayıcıyı kendiliğinden açma")
    s.set_defaults(sunucu=True)
    return p


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    ns = parser_kur().parse_args(args)
    if getattr(ns, "sunucu", False):
        from . import arayuz
        return arayuz.baslat(ns.port, not ns.tarayici_acma)
    sorgu = komut_metni(args)
    veri_izi = "—"
    try:
        kor = None
        if not getattr(ns, "korpus_gerekmez", False):
            kor = veri.korpus()
            veri_izi = kor.veri_izi
        sonuc = ns.islev(kor, ns)
    except (tara.GirdiHatasi, veri.VeriHatasi, okunus.BilinmeyenKarakter) as hata:
        tanzil_mi = getattr(ns, "veri_kaynagi", "") == "tanzil"
        yol = okunus.TANZIL_YOLU if tanzil_mi else veri.QAC_YOLU
        if veri_izi == "—" and yol.exists():
            veri_izi = veri.sha256(yol)[:12]
        sebep = "girdi hatası" if isinstance(hata, tara.GirdiHatasi) else "veri hatası"
        kaynaklar = [okunus.KAYNAK_ADI if tanzil_mi else veri.KAYNAK_ADI]
        print(f"HATA: {hata}")
        print(Kayit(sorgu, kaynaklar=kaynaklar, veri_izi=veri_izi, durum=CALISTIRILMADI, sebep=sebep).metin())
        return 2
    if sonuc.veri_izi is not None:
        veri_izi = sonuc.veri_izi
    elif kor is None:
        veri_izi = veri.sha256(veri.QAC_YOLU)[:12] if veri.QAC_YOLU.exists() else "—"
    print("\n".join(sonuc.satirlar))
    print(Kayit(sorgu, birimler=sonuc.birimler, kaynaklar=[sonuc.kaynak or veri.KAYNAK_ADI],
                veri_izi=veri_izi).metin())
    return 0 if sonuc.basarili else 1


if __name__ == "__main__":
    from . import utf8_akislar
    utf8_akislar()
    sys.exit(main())
