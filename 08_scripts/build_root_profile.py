#!/usr/bin/env python3
"""Build a reproducible Quran-internal profile for one QAC root.

Outputs per root:
- occurrence table from generated QAC word annotations
- lemma distribution
- POS distribution
- surface-form distribution
- neighboring-word context windows (QAC token positions only)

This script does not assign semantics. It produces evidence for later analysis.
"""
from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORDS = ROOT / "03_indices" / "generated" / "qac_word_annotations.csv"
OUT_BASE = ROOT / "07_analyses" / "generated" / "root_profiles"


def values(cell: str) -> set[str]:
    return {x for x in cell.split(";") if x}


def load_words() -> list[dict[str, str]]:
    with WORDS.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--root", required=True, help="QAC Buckwalter root, e.g. Amn")
    p.add_argument("--window", type=int, default=2, help="neighbor word window")
    args = p.parse_args()

    rows = load_words()
    by_ayah: dict[tuple[int, int], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_ayah[(int(row["surah"]), int(row["ayah"]))].append(row)
    for key in by_ayah:
        by_ayah[key].sort(key=lambda r: int(r["word"]))

    hits = [r for r in rows if args.root in values(r["roots_bw"])]
    if not hits:
        raise SystemExit(f"Root not found: {args.root}")

    lemmas = Counter()
    poses = Counter()
    forms_ar = Counter()
    forms_bw = Counter()
    surahs: set[int] = set()
    ayat: set[tuple[int, int]] = set()

    out_rows: list[dict[str, str | int]] = []
    for hit in hits:
        s, a, w = int(hit["surah"]), int(hit["ayah"]), int(hit["word"])
        surahs.add(s); ayat.add((s, a))
        for x in values(hit["lemmas_bw"]): lemmas[x] += 1
        for x in values(hit["pos"]): poses[x] += 1
        forms_ar[hit["form_arabic"]] += 1
        forms_bw[hit["form_bw"]] += 1

        verse_words = by_ayah[(s, a)]
        idx = next(i for i, r in enumerate(verse_words) if int(r["word"]) == w)
        lo = max(0, idx - args.window); hi = min(len(verse_words), idx + args.window + 1)
        context = verse_words[lo:hi]
        out_rows.append({
            "surah": s, "ayah": a, "word": w, "location": hit["location"],
            "form_arabic": hit["form_arabic"], "form_bw": hit["form_bw"],
            "lemmas_bw": hit["lemmas_bw"], "lemmas_arabic": hit["lemmas_arabic"],
            "pos": hit["pos"],
            "context_arabic": " ".join(r["form_arabic"] for r in context),
            "context_locations": " ".join(r["location"] for r in context),
        })

    out_dir = OUT_BASE / args.root
    out_dir.mkdir(parents=True, exist_ok=True)

    occ = out_dir / "occurrences.csv"
    with occ.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(out_rows[0]))
        writer.writeheader(); writer.writerows(out_rows)

    def write_counter(path: Path, key: str, counter: Counter[str]) -> None:
        with path.open("w", encoding="utf-8", newline="") as f:
            w = csv.writer(f); w.writerow([key, "count"])
            for value, count in sorted(counter.items(), key=lambda x: (-x[1], x[0])):
                w.writerow([value, count])

    write_counter(out_dir / "lemmas.csv", "lemma_bw", lemmas)
    write_counter(out_dir / "pos.csv", "pos", poses)
    write_counter(out_dir / "forms_arabic.csv", "form_arabic", forms_ar)

    md = [
        f"# Root profile: {args.root}", "",
        "Automatically generated from `qac_word_annotations.csv`. No semantic conclusion is encoded here.", "",
        f"- Word occurrences: **{len(hits):,}**",
        f"- Ayat: **{len(ayat):,}**",
        f"- Surahs: **{len(surahs):,}**", "",
        "## Lemmas", "", "| lemma (BW) | count |", "|---|---:|",
    ]
    md += [f"| `{k}` | {v} |" for k, v in sorted(lemmas.items(), key=lambda x: (-x[1], x[0]))]
    md += ["", "## POS", "", "| POS | count |", "|---|---:|"]
    md += [f"| `{k}` | {v} |" for k, v in sorted(poses.items(), key=lambda x: (-x[1], x[0]))]
    md += ["", "## Most frequent surface forms", "", "| Arabic form | count |", "|---|---:|"]
    md += [f"| {k} | {v} |" for k, v in forms_ar.most_common(40)]
    (out_dir / "profile.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(f"Root: {args.root}")
    print(f"Occurrences: {len(hits):,}; ayat: {len(ayat):,}; surahs: {len(surahs):,}")
    print("Top lemmas:", lemmas.most_common(20))
    print("POS:", poses.most_common())
    print(f"Output: {out_dir.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
