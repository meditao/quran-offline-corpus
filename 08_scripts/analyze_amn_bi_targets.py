#!/usr/bin/env python3
"""Audit immediate `bi-` targets of Qur'anic QAC lemma `'aAmana`.

This is deliberately conservative. It consumes the already-generated
`verb_syntax/occurrences.csv`, reopens pinned QAC morphology to distinguish
lexical targets from preposition+pronoun forms, and attaches the full Tanzil
Uthmani verse for manual review.

It does NOT resolve pronominal antecedents automatically.
"""
from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QAC = ROOT / "02_morphology" / "qac" / "quranic-corpus-morphology-0.4.txt"
TANZIL = ROOT / "01_raw" / "tanzil" / "quran-uthmani.txt"
SYNTAX = ROOT / "07_analyses" / "generated" / "root_profiles" / "Amn" / "verb_syntax" / "occurrences.csv"
OUT = ROOT / "07_analyses" / "generated" / "root_profiles" / "Amn" / "bi_targets"
LOCATION_RE = re.compile(r"^\((\d+):(\d+):(\d+):(\d+)\)$")
EXPECTED_BI = 163


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
            words[(s, a, w)].append({"segment": str(seg), "form": form, "tag": tag, "features": features})
    for key in words:
        words[key].sort(key=lambda x: int(x["segment"]))
    return dict(words)


def load_tanzil() -> dict[tuple[int, int], str]:
    verses: dict[tuple[int, int], str] = {}
    with TANZIL.open("r", encoding="utf-8-sig") as f:
        for raw in f:
            line = raw.rstrip("\r\n")
            if not line or line.startswith("#"):
                continue
            parts = line.split("|", 2)
            if len(parts) != 3:
                continue
            try:
                s, a = int(parts[0]), int(parts[1])
            except ValueError:
                continue
            verses[(s, a)] = parts[2]
    return verses


def feature_values(features: str, key: str) -> list[str]:
    vals: list[str] = []
    for item in features.split("|"):
        if item.startswith(key + ":"):
            vals.append(item.split(":", 1)[1])
    return vals


def segment_evidence(segments: list[dict[str, str]]) -> str:
    return " ; ".join(f"{s['form']}[{s['tag']}|{s['features']}]" for s in segments)


def has_pronoun_suffix(segments: list[dict[str, str]]) -> bool:
    # QAC pronoun clitics are tagged PRON and/or carry PRON:* feature data.
    return any(s["tag"] == "PRON" or "PRON:" in s["features"] for s in segments)


def lexical_roots(segments: list[dict[str, str]]) -> set[str]:
    roots: set[str] = set()
    for seg in segments:
        roots.update(feature_values(seg["features"], "ROOT"))
    return roots


def lexical_lemmas(segments: list[dict[str, str]]) -> set[str]:
    lemmas: set[str] = set()
    for seg in segments:
        lemmas.update(feature_values(seg["features"], "LEM"))
    return lemmas


def classify(segments: list[dict[str, str]], roots: set[str], lemmas: set[str]) -> str:
    # Pronoun-only `bi-hi/ha/him...`: no lexical ROOT on the target word and a
    # real PRON segment. Keep unresolved rather than guessing antecedent.
    if has_pronoun_suffix(segments) and not roots:
        return "pronominal_unresolved"

    # Explicit lexical target classes. These are structural labels, not semantic
    # conclusions about the whole verse.
    if "Alh" in roots:
        return "explicit_allah"
    if "rbb" in roots:
        return "explicit_rabb"
    if "rsl" in roots:
        return "explicit_messenger"
    if "Ayy" in roots:
        return "explicit_ayah"
    if "ktb" in roots:
        return "explicit_book"
    if "gyb" in roots:
        return "explicit_unseen"
    if "Axr" in roots:
        return "explicit_afterlife"
    if "ywm" in roots:
        return "explicit_day"

    # Relative/nominal clause heads such as bi-ma and bi-alladhi are kept as a
    # separate structural class because the semantic target is the following
    # proposition, not the clitic itself.
    if any(x in {"maA", "{l~a*iY", "man"} for x in lemmas):
        return "relative_or_clause_head"

    return "explicit_other_lexical"


def main() -> None:
    for p in (QAC, TANZIL, SYNTAX):
        if not p.exists():
            raise SystemExit(f"Missing prerequisite: {p.relative_to(ROOT)}")

    morph = parse_qac_words()
    verses = load_tanzil()

    with SYNTAX.open("r", encoding="utf-8", newline="") as f:
        all_rows = list(csv.DictReader(f))
    bi_rows = [r for r in all_rows if r["construction"] == "bi"]
    if len(bi_rows) != EXPECTED_BI:
        raise SystemExit(f"Expected {EXPECTED_BI} immediate bi cases; found {len(bi_rows)}")

    out_rows: list[dict[str, str]] = []
    counts: Counter[str] = Counter()
    root_counts: Counter[str] = Counter()
    lemma_counts: Counter[str] = Counter()

    for r in bi_rows:
        s, a, w = int(r["surah"]), int(r["ayah"]), int(r["word"])
        target_key = (s, a, w + 1)
        segs = morph.get(target_key, [])
        if not segs:
            raise SystemExit(f"Missing QAC target segments for {target_key}")
        roots = lexical_roots(segs)
        lemmas = lexical_lemmas(segs)
        category = classify(segs, roots, lemmas)
        counts[category] += 1
        for x in roots:
            root_counts[x] += 1
        for x in lemmas:
            lemma_counts[x] += 1

        out_rows.append({
            "surah": str(s),
            "ayah": str(a),
            "verb_word": str(w),
            "verb_location": r["location"],
            "verb_arabic": r["verb_arabic"],
            "target_word": str(w + 1),
            "target_form_arabic": r["next_form_arabic"],
            "target_form_bw": r["next_form_bw"],
            "target_roots_bw": ";".join(sorted(roots)),
            "target_lemmas_bw": ";".join(sorted(lemmas)),
            "category": category,
            "qac_segments": segment_evidence(segs),
            "context_arabic": r["context_arabic"],
            "full_verse_uthmani": verses.get((s, a), ""),
        })

    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "targets.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(out_rows[0]))
        writer.writeheader(); writer.writerows(out_rows)

    with (OUT / "summary.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f); writer.writerow(["category", "count"])
        for k, v in sorted(counts.items(), key=lambda x: (-x[1], x[0])):
            writer.writerow([k, v])

    md = [
        "# Amn / `āman(a) bi-` target audit", "",
        "Automatically generated from pinned QAC v0.4 plus Tanzil Uthmani v1.1 for verse display.",
        "This report classifies only the **immediately following morphologically explicit bi- target word**. It does not infer pronominal antecedents automatically.", "",
        f"- Immediate `bi-` cases: **{len(out_rows)}**", "",
        "## Structural target classes", "", "| class | count |", "|---|---:|",
    ]
    for k, v in sorted(counts.items(), key=lambda x: (-x[1], x[0])):
        md.append(f"| `{k}` | {v} |")

    md += ["", "## Explicit lexical target roots", "", "| root | count |", "|---|---:|"]
    for k, v in root_counts.most_common(30):
        md.append(f"| `{k}` | {v} |")

    md += ["", "## Unresolved pronominal bi- cases", ""]
    pro = [r for r in out_rows if r["category"] == "pronominal_unresolved"]
    if pro:
        for r in pro:
            md.append(f"- **{r['verb_location']}** `{r['verb_arabic']} {r['target_form_arabic']}` — {r['full_verse_uthmani']}")
    else:
        md.append("- none")

    md += ["", "## Explicit messenger/person-adjacent cases", ""]
    for r in out_rows:
        if r["category"] == "explicit_messenger":
            md.append(f"- **{r['verb_location']}** `{r['verb_arabic']} {r['target_form_arabic']}` — {r['full_verse_uthmani']}")

    md += ["", "## Guardrails", "",
           "- A category such as `explicit_allah` means only that the immediate bi-target word carries QAC ROOT:Alh.",
           "- `pronominal_unresolved` is intentionally unresolved; antecedents require manual discourse review.",
           "- Relative/clause-head targets require reading the proposition that follows.",
           "- This report does not equate all `bi-` constructions with one English/Turkish gloss."]

    (OUT / "report.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print("Immediate bi cases:", len(out_rows))
    print("Categories:", dict(counts))
    print("Unresolved pronouns:", len(pro))
    print("Output:", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
