#!/usr/bin/env python3
"""QAC lemma/kök annotationlarını QuranMorph lemma annotationlarıyla konum bazında karşılaştırır.

Önkoşul:
    python 08_scripts/build_qac_indices.py
    python 08_scripts/validate_quranmorph.py

Çıktılar:
    03_indices/generated/qac_quranmorph_lemma_map.csv
    03_indices/generated/qac_root_quranmorph_lemma_map.csv

Bu script uyuşmazlığı hata saymaz; editoryal/lexikografik fark olarak ölçer.
"""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QAC = ROOT / "03_indices" / "generated" / "qac_word_annotations.csv"
QM = ROOT / "02_morphology" / "quranmorph" / "quran-dataset.csv"
OUT = ROOT / "03_indices" / "generated"


def split_values(value: str) -> list[str]:
    return [x for x in value.split(";") if x]


def main() -> None:
    if not QAC.exists():
        raise SystemExit(f"Önce QAC indeksini üretin: {QAC}")
    if not QM.exists():
        raise SystemExit(f"QuranMorph bulunamadı: {QM}")

    qm_by_loc: dict[tuple[int, int, int], dict[str, str]] = {}
    qm_totals: Counter[str] = Counter()
    with QM.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            loc = (int(row["surah_number"]), int(row["verse_number"]), int(row["word_position"]))
            if loc in qm_by_loc:
                raise ValueError(f"Tekrarlanan QuranMorph konumu: {loc}")
            qm_by_loc[loc] = row
            qm_totals[row["qabas_lemma"]] += 1

    lemma_pairs: Counter[tuple[str, str]] = Counter()
    root_pairs: Counter[tuple[str, str]] = Counter()
    qac_lemma_totals: Counter[str] = Counter()
    qac_root_totals: Counter[str] = Counter()
    missing_qm: list[tuple[int, int, int]] = []

    with QAC.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            loc = (int(row["surah"]), int(row["ayah"]), int(row["word"]))
            qm = qm_by_loc.get(loc)
            if qm is None:
                missing_qm.append(loc)
                continue
            qm_lemma = qm["qabas_lemma"]
            for qac_lemma in set(split_values(row["lemmas_bw"])):
                qac_lemma_totals[qac_lemma] += 1
                lemma_pairs[(qac_lemma, qm_lemma)] += 1
            for qac_root in set(split_values(row["roots_bw"])):
                qac_root_totals[qac_root] += 1
                root_pairs[(qac_root, qm_lemma)] += 1

    if missing_qm:
        raise SystemExit(f"QuranMorph'ta bulunmayan QAC konumları var: {missing_qm[:10]}")

    OUT.mkdir(parents=True, exist_ok=True)

    with (OUT / "qac_quranmorph_lemma_map.csv").open("w", encoding="utf-8", newline="") as f:
        fields = [
            "qac_lemma_bw", "quranmorph_lemma", "overlap_words",
            "qac_lemma_total", "quranmorph_lemma_total", "share_of_qac_lemma",
        ]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for (qac_lemma, qm_lemma), count in sorted(
            lemma_pairs.items(), key=lambda x: (x[0][0], -x[1], x[0][1])
        ):
            total = qac_lemma_totals[qac_lemma]
            w.writerow({
                "qac_lemma_bw": qac_lemma,
                "quranmorph_lemma": qm_lemma,
                "overlap_words": count,
                "qac_lemma_total": total,
                "quranmorph_lemma_total": qm_totals[qm_lemma],
                "share_of_qac_lemma": f"{count / total:.6f}",
            })

    with (OUT / "qac_root_quranmorph_lemma_map.csv").open("w", encoding="utf-8", newline="") as f:
        fields = [
            "qac_root_bw", "quranmorph_lemma", "overlap_words",
            "qac_root_total", "quranmorph_lemma_total", "share_of_qac_root",
        ]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for (qac_root, qm_lemma), count in sorted(
            root_pairs.items(), key=lambda x: (x[0][0], -x[1], x[0][1])
        ):
            total = qac_root_totals[qac_root]
            w.writerow({
                "qac_root_bw": qac_root,
                "quranmorph_lemma": qm_lemma,
                "overlap_words": count,
                "qac_root_total": total,
                "quranmorph_lemma_total": qm_totals[qm_lemma],
                "share_of_qac_root": f"{count / total:.6f}",
            })

    # Tek bir QuranMorph lemmasına %100 oturan QAC lemma sayısı bir kalite/istikrar göstergesidir;
    # bu 'doğruluk' değildir, annotation şemalarının ne kadar örtüştüğünü ölçer.
    distributions: dict[str, int] = defaultdict(int)
    for (qac_lemma, _), _count in lemma_pairs.items():
        distributions[qac_lemma] += 1
    one_to_one = sum(1 for n in distributions.values() if n == 1)

    print(f"QAC lemmas compared: {len(distributions):,}")
    print(f"QAC lemmas mapping to one QuranMorph lemma: {one_to_one:,}")
    print(f"QAC roots compared: {len(qac_root_totals):,}")
    print(f"Output: {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
