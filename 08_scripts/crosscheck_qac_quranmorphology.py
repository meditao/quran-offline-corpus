#!/usr/bin/env python3
"""QAC v0.4 ↔ mustafa0x/quran-morphology konum bazında çapraz denetim (Aşama 4).

Önkoşul (veri depoya işlenmez; lisans doğrulanmadı):
    cd 09_calisma_masasi && python -m tezgah kur quran-morphology

Çıktılar (03_indices/audits/):
    qac_quranmorphology.md              özet rapor
    qac_quranmorphology.json            bütün sayılar
    qac_quranmorphology_kok_farklari.tsv  kök ataması farklı her kelime konumu
    qac_quranmorphology_kok_sayilari.tsv  kelime konumu sayısı farklı her kök (iki korpus ayrı sütun)

Kök karşılaştırması hemze yazımı nötrlenerek yapılır (tezgah.qm.notr). Satır sonları iki dosyada
da \\r\\n olarak soyulur; QAC dosyası CRLF'dir. Uyuşmazlık hata sayılmaz; iki annotation arasındaki
fark olarak ölçülür. Hiçbir korpus diğerinin doğrulaması değildir.

Beklenen değerler (kullanıcı, 24.09.2026) tutmazsa betik 1 ile çıkar ve farkı yazar.
"""

from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "09_calisma_masasi"))
from tezgah import qm, veri  # noqa: E402

OUT = ROOT / "03_indices" / "audits"
BEKLENEN = {
    "kelime_konumu_qac": 77_429, "kelime_konumu_qm": 77_429,
    "segment_qm": 130_030, "segment_qac": 128_219,
    "kok_qm": 1_651, "kok_qac": 1_642,
    "notr_ortak": 1_638, "notr_yalniz_qm": 13, "notr_yalniz_qac": 4,
}


def binlik(n: int) -> str:
    return f"{n:,}".replace(",", ".")


def crlf_olcumu() -> dict[str, int]:
    ham = veri.QAC_YOLU.read_bytes()
    naif, temiz = set(), set()
    for satir in ham.decode("utf-8-sig").split("\n"):
        if not satir.startswith("("):
            continue
        for oz in satir.split("\t")[3].split("|"):
            if oz.startswith("ROOT:"):
                naif.add(oz[5:])
                temiz.add(oz[5:].rstrip("\r"))
    return {
        "qac_crlf_satir": ham.count(b"\r\n"),
        "qac_toplam_satir": ham.count(b"\n"),
        "qac_kok_satir_sonu_soyulmadan": len(naif),
        "qac_kok_soyulunca": len(temiz),
        "qm_cr": qm.QM_YOLU.read_bytes().count(b"\r"),
    }


def hesapla() -> dict:
    """Bütün ölçümleri ve rapor metnini üretir; dosyaya yazmaz (testler bunu kullanır)."""
    q = qm.korpus()
    if q is None:
        raise SystemExit("quran-morphology kurulu değil: cd 09_calisma_masasi && python -m tezgah kur quran-morphology")
    kor = veri.korpus()

    qac_konum = {k.anahtar for k in kor.kelimeler}
    qac_notr = {qm.qac_notr(k) for k in kor.kok_kelimeleri}
    qm_notr = {qm.notr(k) for k in q.ham_kokler}
    olcum = {
        "kelime_konumu_qac": len(qac_konum), "kelime_konumu_qm": len(q.kelimeler),
        "segment_qm": q.segment, "segment_qac": len(kor.segmentler),
        "kok_qm": len(q.ham_kokler), "kok_qac": len(kor.kok_kelimeleri),
        "notr_ortak": len(qac_notr & qm_notr), "notr_yalniz_qm": len(qm_notr - qac_notr),
        "notr_yalniz_qac": len(qac_notr - qm_notr),
    }
    ek = {
        "konum_kumeleri_ayni": qac_konum == q.kelimeler,
        "notr_carpisma_qac": len(kor.kok_kelimeleri) - len(qac_notr),
        "notr_carpisma_qm": len(q.ham_kokler) - len(qm_notr),
        **crlf_olcumu(),
    }

    # konum bazında kök ataması
    kategori: Counter[str] = Counter()
    ciftler: Counter[tuple[str, str]] = Counter()
    farklar = []
    seg_fark: Counter[int] = Counter()
    for k in kor.kelimeler:
        a = {qm.qac_notr(r) for r in k.kokler}
        b = q.notr_kokler(k.anahtar)
        seg_fark[q.segment_sayisi[k.anahtar] - len(k.segmentler)] += 1
        if a == b:
            kategori["aynı"] += 1
            continue
        tur = ("yalnız quran-morphology kök atıyor" if not a else
               "yalnız QAC kök atıyor" if not b else "farklı kök")
        kategori[tur] += 1
        qac_s = ";".join(sorted(k.kokler))
        qm_s = ";".join(sorted(q.kokler.get(k.anahtar, set())))
        ciftler[(qac_s or "—", qm_s or "—")] += 1
        farklar.append({
            "konum": k.konum, "kategori": tur,
            "qac_kok_bw": qac_s, "qac_kok_latin": ";".join(veri.kok_latin(r) for r in sorted(k.kokler)),
            "qm_kok": qm_s, "qm_kok_latin": ";".join(qm.arapca_latin(r) for r in sorted(q.kokler.get(k.anahtar, set()))),
            "qac_bicim_bw": k.bicim,
        })

    # kök başına kelime konumu sayıları (nötr anahtar)
    qac_say = Counter()
    for bw, kelimeler in kor.kok_kelimeleri.items():
        qac_say[qm.qac_notr(bw)] += len(kelimeler)
    qm_say = Counter({anahtar: len(konumlar) for anahtar, konumlar in q.kok_konumlari().items()})
    kok_fark = sorted(
        ({"notr": k, "qac": qac_say.get(k, 0), "qm": qm_say.get(k, 0)}
         for k in set(qac_say) | set(qm_say) if qac_say.get(k, 0) != qm_say.get(k, 0)),
        key=lambda r: (-abs(r["qm"] - r["qac"]), r["notr"]))
    notr_bw = {qm.qac_notr(bw): bw for bw in kor.kok_kelimeleri}

    denetim = {ad: (BEKLENEN[ad], olcum[ad], BEKLENEN[ad] == olcum[ad]) for ad in BEKLENEN}
    ozet = {
        "qm_depo": qm.QM_DEPO, "qm_commit": qm.QM_COMMIT, "qm_sha256": q.sha256, "qac_sha256": kor.sha256,
        "olcum": olcum, "ek": ek,
        "beklenen_denetimi": {k: {"beklenen": b, "bulunan": o, "tuttu": t} for k, (b, o, t) in denetim.items()},
        "kok_atamasi": dict(kategori), "segment_farki_dagilimi": {str(k): v for k, v in sorted(seg_fark.items())},
        "yalniz_qm_kokler": sorted(qm.arapca_latin(k) for k in qm_notr - qac_notr),
        "yalniz_qac_kokler": sorted(f"{notr_bw[k]} ({veri.kok_latin(notr_bw[k])})" for k in qac_notr - qm_notr),
        "en_sik_farkli_atama": [{"qac": a, "qm": b, "kelime_konumu": n} for (a, b), n in ciftler.most_common(30)],
        "sayisi_farkli_kok": len(kok_fark),
    }

    kok_satirlari = [[qm.arapca_latin(r["notr"]), notr_bw.get(r["notr"], "—"), r["qac"], r["qm"], r["qm"] - r["qac"]]
                     for r in kok_fark]

    md = [
        "# QAC v0.4 ↔ quran-morphology — konum bazında çapraz denetim",
        "",
        "Üretici: `08_scripts/crosscheck_qac_quranmorphology.py`. İkinci annotation katmanı çapraz kontroldür, "
        "delil değildir. Hiçbir korpus diğerinin doğrulaması sayılmaz; iki sayının aynı çıkması doğrulama değildir.",
        "",
        "## Kaynaklar",
        "",
        f"- QAC v0.4: `02_morphology/qac/quranic-corpus-morphology-0.4.txt`, sha256 `{kor.sha256}`",
        f"- quran-morphology: `{qm.QM_DEPO}` commit `{qm.QM_COMMIT}`, `quran-morphology.txt`, sha256 `{q.sha256}`. "
        "Depoda lisans dosyası yok ve veri QAC v0.4'ün değiştirilmiş kopyası; QAC şartı değiştirilmiş kopyayı yasakladığı "
        "için veri bu depoya işlenmez, `09_calisma_masasi/yerel/` altında tutulur.",
        "",
        "## Beklenen değerler",
        "",
        "| ölçü | beklenen | bulunan | sonuç |",
        "|---|---:|---:|---|",
        *[f"| {ad} | {binlik(b)} | {binlik(o)} | {'tuttu' if t else '**TUTMADI**'} |" for ad, (b, o, t) in denetim.items()],
        "",
        "Birimler: kelime konumu `(sûre, ayet, kelime)`; segment `(sûre, ayet, kelime, segment)`; kök = farklı ROOT "
        "değeri. Farklı birimler toplanmaz.",
        "",
        f"- Kelime konumu kümeleri birebir aynı: **{'evet' if ek['konum_kumeleri_ayni'] else 'hayır'}**.",
        f"- Hemze nötrleme çakışması (iki ham kökün aynı anahtara düşmesi): QAC {ek['notr_carpisma_qac']}, "
        f"quran-morphology {ek['notr_carpisma_qm']}.",
        "",
        "## CRLF tuzağı",
        "",
        f"QAC dosyasında CRLF ile biten satır: {binlik(ek['qac_crlf_satir'])} / {binlik(ek['qac_toplam_satir'])}. Satır "
        f"sonu soyulmadan okunursa QAC'ta **{binlik(ek['qac_kok_satir_sonu_soyulmadan'])}** \"kök\" çıkar (sonunda CR "
        f"taşıyan kopyalar); soyulunca **{binlik(ek['qac_kok_soyulunca'])}**. quran-morphology dosyasında CR sayısı "
        f"{ek['qm_cr']}; oradaki {binlik(olcum['kok_qm'])} gerçek sayıdır, artefakt değildir. İki ayrıştırıcı da satır "
        "sonunu `\\r\\n` olarak soyar. Tarihsel 1.651 kaydı için: `qac_1651_vs_1642.md`.",
        "",
        "## Kök envanteri (hemze yazımı nötrlenerek)",
        "",
        f"- Ortak: {binlik(olcum['notr_ortak'])} · yalnız quran-morphology: {olcum['notr_yalniz_qm']} · yalnız QAC: "
        f"{olcum['notr_yalniz_qac']}",
        f"- Yalnız quran-morphology: {', '.join(ozet['yalniz_qm_kokler'])}",
        f"- Yalnız QAC: {', '.join(ozet['yalniz_qac_kokler'])}",
        "",
        "## Kelime konumu bazında kök ataması",
        "",
        "| kategori | kelime konumu |",
        "|---|---:|",
        *[f"| {k} | {binlik(v)} |" for k, v in sorted(kategori.items(), key=lambda x: -x[1])],
        f"| toplam | {binlik(sum(kategori.values()))} |",
        "",
        "En sık farklı atamalar (kelime konumu; ham kök değerleri):",
        "",
        "| QAC (Buckwalter) | quran-morphology | kelime konumu |",
        "|---|---|---:|",
        *[f"| {a} | {qm.arapca_latin(b) if b != '—' else '—'} | {n} |" for (a, b), n in ciftler.most_common(20)],
        "",
        f"Tam liste: `qac_quranmorphology_kok_farklari.tsv` ({binlik(len(farklar))} satır). Kelime konumu sayısı iki "
        f"korpusta farklı olan kök: {len(kok_fark)} (`qac_quranmorphology_kok_sayilari.tsv`).",
        "",
        "## Segment farkı",
        "",
        f"Toplam: {binlik(olcum['segment_qm'])} − {binlik(olcum['segment_qac'])} = "
        f"{binlik(olcum['segment_qm'] - olcum['segment_qac'])} segment. Kelime konumu başına fark "
        "(quran-morphology − QAC):",
        "",
        "| fark | kelime konumu |",
        "|---:|---:|",
        *[f"| {k:+d} | {binlik(v)} |" for k, v in sorted(seg_fark.items())],
        "",
        "Ayrıntı: quran-morphology README'si bazı ekleri ayrı segment yapar (işaret isimlerinde ATT/DIST/ADDR, "
        "يومئذ'deki ئذ). Bu rapor segmentleri tek tek eşlemez; yalnız sayıları karşılaştırır.",
        "",
    ]
    return {"ozet": ozet, "farklar": farklar, "kok_satirlari": kok_satirlari, "md": md,
            "tuttu": all(t for _, _, t in denetim.values())}


def main() -> int:
    h = hesapla()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "qac_quranmorphology.json").write_text(json.dumps(h["ozet"], ensure_ascii=False, indent=2) + "\n",
                                                  encoding="utf-8")
    with (OUT / "qac_quranmorphology_kok_farklari.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(h["farklar"][0]), delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(h["farklar"])
    with (OUT / "qac_quranmorphology_kok_sayilari.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["kok_notr_latin", "qac_kok_bw", "qac_kelime_konumu", "qm_kelime_konumu", "fark_qm_eksi_qac"])
        w.writerows(h["kok_satirlari"])
    (OUT / "qac_quranmorphology.md").write_text("\n".join(h["md"]), encoding="utf-8")
    md = h["md"]
    print("\n".join(md[md.index("## Beklenen değerler"):md.index("## CRLF tuzağı")]))
    print("Çıktılar:", ", ".join(p.name for p in sorted(OUT.glob("qac_quranmorphology*"))))
    return 0 if h["tuttu"] else 1


if __name__ == "__main__":
    sys.exit(main())
