#!/usr/bin/env python3
"""Classify QAC 'aAmana verb occurrences by immediate complement pattern.

Purpose
-------
This script tests, rather than assumes, whether the Qur'anic 'aAmana / yu'minu
family behaves like a relational trust/commitment verb. It reads the pinned
QAC v0.4 morphology plus the generated word annotations and produces an audit
that separates:

- immediately following bi- prepositional complements,
- immediately following li- prepositional complements,
- immediately following 'an / 'anna complement clauses,
- other prepositions,
- bare/other continuations requiring contextual review.

Important limitation: this is a surface-syntax audit, not a dependency parser.
Only morphologically explicit patterns are classified automatically. Ambiguous
or non-adjacent complements are left in review instead of being forced into a
category.
"""
from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QAC = ROOT / "02_morphology" / "qac" / "quranic-corpus-morphology-0.4.txt"
WORDS = ROOT / "03_indices" / "generated" / "qac_word_annotations.csv"
OUT = ROOT / "07_analyses" / "generated" / "root_profiles" / "Amn" / "verb_syntax"
LOCATION_RE = re.compile(r"^\((\d+):(\d+):(\d+):(\d+)\)$")
EXPECTED_AMANA_VERBS = 537
DIACRITICS = set("aiuoFNK~`")


def consonants(text: str) -> str:
    return "".join(ch for ch in text if ch not in DIACRITICS)


def feature_values(features: str, key: str) -> list[str]:
    out: list[str] = []
    for item in features.split("|"):
        if item.startswith(key + ":"):
            out.append(item.split(":", 1)[1])
    return out


def parse_qac_words() -> dict[tuple[int, int, int], list[dict[str, str]]]:
    words: dict[tuple[int, int, int], list[dict[str, str]]] = defaultdict(list)
    with QAC.open("r", encoding="utf-8-sig", errors="strict") as f:
        for line_no, raw in enumerate(f, 1):
            line = raw.rstrip("\r\n")
            if not line.startswith("("):
                continue
            parts = line.split("\t")
            if len(parts) != 4:
                raise ValueError(f"line {line_no}: expected 4 TSV fields")
            location, form, tag, features = parts
            m = LOCATION_RE.match(location)
            if not m:
                raise ValueError(f"line {line_no}: malformed location {location!r}")
            s, a, w, seg = map(int, m.groups())
            words[(s, a, w)].append({
                "segment": str(seg), "form": form, "tag": tag, "features": features,
            })
    for key in words:
        words[key].sort(key=lambda x: int(x["segment"]))
    return dict(words)


def load_word_annotations() -> tuple[
    dict[tuple[int, int, int], dict[str, str]],
    dict[tuple[int, int], list[dict[str, str]]],
]:
    by_key: dict[tuple[int, int, int], dict[str, str]] = {}
    by_ayah: dict[tuple[int, int], list[dict[str, str]]] = defaultdict(list)
    with WORDS.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            key = (int(row["surah"]), int(row["ayah"]), int(row["word"]))
            by_key[key] = row
            by_ayah[(key[0], key[1])].append(row)
    for key in by_ayah:
        by_ayah[key].sort(key=lambda r: int(r["word"]))
    return by_key, dict(by_ayah)


def has_amana_lemma(segments: list[dict[str, str]]) -> bool:
    return any("'aAmana" in feature_values(seg["features"], "LEM") for seg in segments)


def preposition_code(segments: list[dict[str, str]]) -> tuple[str | None, str]:
    """Return (code, evidence). code is bi/li/other or None.

    QAC normally tags prepositions as P. PREFIX metadata differs by segment, so
    both the tag and a conservative consonantal-form fallback are retained in
    the evidence string.
    """
    for seg in segments:
        tag = seg["tag"]
        cons = consonants(seg["form"])
        feats = seg["features"]
        is_prep = tag == "P" or "POS:P" in feats
        if not is_prep:
            continue
        if cons == "b":
            return "bi", f"{seg['form']}|{tag}|{feats}"
        if cons == "l":
            return "li", f"{seg['form']}|{tag}|{feats}"
        return f"other_prep:{cons or seg['form']}", f"{seg['form']}|{tag}|{feats}"
    return None, ""


def is_an_clause(segments: list[dict[str, str]]) -> bool:
    for seg in segments:
        cons = consonants(seg["form"])
        lemmas = feature_values(seg["features"], "LEM")
        if cons in {">n", "<n"}:
            return True
        if any(consonants(lemma) in {">n", "<n"} for lemma in lemmas):
            return True
        if seg["tag"] in {"SUB", "ACC"} and cons in {">n", "<n"}:
            return True
    return False


def context(by_ayah: dict[tuple[int, int], list[dict[str, str]]], s: int, a: int, w: int, window: int = 4) -> str:
    verse = by_ayah[(s, a)]
    idx = next(i for i, row in enumerate(verse) if int(row["word"]) == w)
    lo, hi = max(0, idx - window), min(len(verse), idx + window + 1)
    return " ".join(row["form_arabic"] for row in verse[lo:hi])


def main() -> None:
    if not QAC.exists() or not WORDS.exists():
        raise SystemExit("Missing QAC or generated word annotations")

    morph = parse_qac_words()
    ann, by_ayah = load_word_annotations()

    hits = [key for key, segs in morph.items() if has_amana_lemma(segs)]
    hits.sort()
    if len(hits) != EXPECTED_AMANA_VERBS:
        raise SystemExit(f"Expected {EXPECTED_AMANA_VERBS} 'aAmana verb words; found {len(hits)}")

    rows: list[dict[str, str | int]] = []
    construction_counts: Counter[str] = Counter()
    bi_targets: Counter[str] = Counter()
    li_targets: Counter[str] = Counter()
    review_next: Counter[str] = Counter()

    for s, a, w in hits:
        current = ann[(s, a, w)]
        next_key = (s, a, w + 1)
        nxt = ann.get(next_key)
        nxt_segments = morph.get(next_key, [])

        construction = "verse_final_or_no_next"
        prep_evidence = ""
        if nxt is not None:
            prep, prep_evidence = preposition_code(nxt_segments)
            if prep is not None:
                construction = prep
            elif is_an_clause(nxt_segments):
                construction = "an_clause"
            else:
                construction = "bare_or_other"

        construction_counts[construction] += 1

        next_lemma = nxt["lemmas_bw"] if nxt else ""
        next_root = nxt["roots_bw"] if nxt else ""
        next_form_ar = nxt["form_arabic"] if nxt else ""
        next_form_bw = nxt["form_bw"] if nxt else ""
        target_key = next_root or next_lemma or next_form_bw or "(none)"
        if construction == "bi":
            bi_targets[target_key] += 1
        elif construction == "li":
            li_targets[target_key] += 1
        elif construction == "bare_or_other":
            review_next[next_form_bw or "(none)"] += 1

        rows.append({
            "surah": s, "ayah": a, "word": w,
            "location": f"{s}:{a}:{w}",
            "verb_arabic": current["form_arabic"],
            "verb_bw": current["form_bw"],
            "construction": construction,
            "next_form_arabic": next_form_ar,
            "next_form_bw": next_form_bw,
            "next_lemmas_bw": next_lemma,
            "next_roots_bw": next_root,
            "prep_evidence": prep_evidence,
            "context_arabic": context(by_ayah, s, a, w),
        })

    OUT.mkdir(parents=True, exist_ok=True)
    csv_path = OUT / "occurrences.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)

    summary_path = OUT / "summary.csv"
    with summary_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f); writer.writerow(["construction", "count"])
        for k, v in sorted(construction_counts.items(), key=lambda x: (-x[1], x[0])):
            writer.writerow([k, v])

    md: list[str] = [
        "# Amn / 'aAmana verb syntax audit", "",
        "Automatically generated from pinned QAC v0.4. This is a surface-syntax audit, not a semantic conclusion or full dependency parse.", "",
        f"- Exact `'aAmana` lemma occurrences: **{len(hits)}**", "",
        "## Immediate construction counts", "", "| construction | count |", "|---|---:|",
    ]
    for k, v in sorted(construction_counts.items(), key=lambda x: (-x[1], x[0])):
        md.append(f"| `{k}` | {v} |")

    md += ["", "## All immediate li- cases", ""]
    li_rows = [r for r in rows if r["construction"] == "li"]
    if li_rows:
        for r in li_rows:
            md.append(f"- **{r['location']}** `{r['verb_arabic']} {r['next_form_arabic']}` — {r['context_arabic']}")
    else:
        md.append("- none detected")

    md += ["", "## Immediate 'an / 'anna clause cases", ""]
    an_rows = [r for r in rows if r["construction"] == "an_clause"]
    if an_rows:
        for r in an_rows:
            md.append(f"- **{r['location']}** `{r['verb_arabic']} {r['next_form_arabic']}` — {r['context_arabic']}")
    else:
        md.append("- none detected")

    md += ["", "## Frequent bi- target roots/lemmas", "", "| target key | count |", "|---|---:|"]
    for k, v in bi_targets.most_common(30):
        md.append(f"| `{k}` | {v} |")

    md += ["", "## li- target roots/lemmas", "", "| target key | count |", "|---|---:|"]
    for k, v in li_targets.most_common():
        md.append(f"| `{k}` | {v} |")

    md += ["", "## Most frequent immediate continuations in review bucket", "", "| next word (BW) | count |", "|---|---:|"]
    for k, v in review_next.most_common(40):
        md.append(f"| `{k}` | {v} |")

    md += [
        "", "## Interpretation guardrails", "",
        "- `bi`, `li`, and `an_clause` mean only that the immediately following QAC word has that explicit morphology.",
        "- `bare_or_other` is not equivalent to 'no complement'; a non-adjacent or coordinated complement may occur later in the verse.",
        "- Semantic conclusions require manual review of decisive contrasts, especially human targets and verses where `bi-` and `li-` alternate.",
    ]
    (OUT / "report.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print("'aAmana verbs:", len(hits))
    print("Construction counts:", dict(construction_counts))
    print("li cases:", [r["location"] for r in li_rows])
    print("an-clause cases:", [r["location"] for r in an_rows])
    print("Output:", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
