#!/usr/bin/env python3
"""Build a reproducible Qur'anic profile for mu'min / mu'minat forms.

This is a distribution audit, not a final semantic definition. It extracts the
three QAC lemma labels used for human/divine mu'min forms and preserves the
special 59:23 divine title as a separate case instead of mixing it silently
with human uses.
"""
from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QAC = ROOT / "02_morphology" / "qac" / "quranic-corpus-morphology-0.4.txt"
WORDS = ROOT / "03_indices" / "generated" / "qac_word_annotations.csv"
TANZIL = ROOT / "01_raw" / "tanzil" / "quran-uthmani.txt"
OUT = ROOT / "07_analyses" / "generated" / "root_profiles" / "Amn" / "mumin"
LOCATION_RE = re.compile(r"^\((\d+):(\d+):(\d+):(\d+)\)$")
LEMMAS = {"mu&omin", "m~u&omina`t", "m~u&ominap"}
EXPECTED = 230
ANCHOR_AYAHS = {
    (8,2),(8,3),(8,4),(9,71),(23,1),(23,2),(23,3),(23,4),(23,5),(23,6),(23,7),(23,8),(23,9),(23,10),(23,11),
    (24,51),(24,52),(49,15),(58,22),(59,23)
}


def feature_values(features: str, key: str) -> list[str]:
    vals=[]
    for item in features.split("|"):
        if item.startswith(key+":"):
            vals.append(item.split(":",1)[1])
    return vals


def load_morph():
    out={}
    with QAC.open("r",encoding="utf-8-sig") as f:
        for raw in f:
            line=raw.rstrip("\r\n")
            if not line.startswith("("):
                continue
            loc,form,tag,feat=line.split("\t")
            m=LOCATION_RE.match(loc)
            if not m:
                continue
            s,a,w,seg=map(int,m.groups())
            out.setdefault((s,a,w),[]).append({"seg":seg,"form":form,"tag":tag,"feat":feat})
    return out


def load_words():
    by_key={}
    with WORDS.open("r",encoding="utf-8",newline="") as f:
        for r in csv.DictReader(f):
            by_key[(int(r["surah"]),int(r["ayah"]),int(r["word"]))]=r
    return by_key


def load_tanzil():
    verses={}
    with TANZIL.open("r",encoding="utf-8") as f:
        for raw in f:
            line=raw.rstrip("\r\n")
            if not line or line.startswith("#"):
                continue
            p=line.split("|",2)
            if len(p)==3 and p[0].isdigit() and p[1].isdigit():
                verses[(int(p[0]),int(p[1]))]=p[2]
    return verses


def matching_lemma(segs):
    found=[]
    for seg in segs:
        for lemma in feature_values(seg["feat"],"LEM"):
            if lemma in LEMMAS:
                found.append(lemma)
    return found[0] if found else None


def main():
    morph=load_morph(); words=load_words(); verses=load_tanzil()
    hits=[]
    for key,segs in morph.items():
        lemma=matching_lemma(segs)
        if lemma:
            hits.append((key,lemma))
    hits.sort()
    if len(hits)!=EXPECTED:
        raise SystemExit(f"Expected {EXPECTED} mu'min-family occurrences; found {len(hits)}")

    rows=[]; lemma_counts=Counter(); surface_counts=Counter(); surahs=set(); ayahs=set()
    divine=[]
    for (s,a,w),lemma in hits:
        r=words[(s,a,w)]
        role="divine_title" if (s,a)==(59,23) else "human_or_group"
        if role=="divine_title": divine.append((s,a,w))
        lemma_counts[lemma]+=1; surface_counts[r["form_arabic"]]+=1; surahs.add(s); ayahs.add((s,a))
        rows.append({
            "surah":s,"ayah":a,"word":w,"location":f"{s}:{a}:{w}",
            "lemma_bw":lemma,"form_arabic":r["form_arabic"],"form_bw":r["form_bw"],
            "role":role,"full_verse_uthmani":verses.get((s,a),"")
        })
    if len(divine)!=1:
        raise SystemExit(f"Expected exactly one 59:23 divine al-Mu'min occurrence; found {len(divine)}")

    OUT.mkdir(parents=True,exist_ok=True)
    with (OUT/"occurrences.csv").open("w",encoding="utf-8",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=list(rows[0])); wr.writeheader(); wr.writerows(rows)

    md=[
        "# Mu'min / mu'minat distribution audit","",
        "Generated from pinned QAC v0.4; verse display from pinned Tanzil Uthmani v1.1.",
        "This is a distribution profile, not a semantic conclusion.","",
        f"- Total mu'min-family occurrences: **{len(rows)}**",
        f"- Distinct ayat containing the forms: **{len(ayahs)}**",
        f"- Surahs: **{len(surahs)}**",
        f"- Human/group uses: **{len(rows)-len(divine)}**",
        f"- Divine title `al-Mu'min` (59:23): **{len(divine)}**","",
        "## QAC lemma counts","","| lemma | count |","|---|---:|"
    ]
    for k,v in lemma_counts.most_common(): md.append(f"| `{k}` | {v} |")
    md += ["","## Frequent surface forms","","| form | count |","|---|---:|"]
    for k,v in surface_counts.most_common(25): md.append(f"| `{k}` | {v} |")

    md += ["","## Analyst-selected anchor passages for manual semantic review","",
           "These passages are listed as review anchors because they explicitly characterize believers or strongly couple the label with conduct. They are not automatically treated as definitions.",""]
    for s,a in sorted(ANCHOR_AYAHS):
        if (s,a) in verses:
            md.append(f"- **{s}:{a}** — {verses[(s,a)]}")

    md += ["","## Guardrails","",
           "- The human/group count excludes the divine title at 59:23 from human semantic generalization.",
           "- `mu'min` is morphologically the active-participle family of Form IV `amana`; morphology alone does not settle the full Qur'anic concept.",
           "- Final semantic claims require passage-level review, especially 8:2–4, 23:1–11, 49:15 and the divine-title exception 59:23."]
    (OUT/"report.md").write_text("\n".join(md)+"\n",encoding="utf-8")
    print("mu'min-family occurrences:",len(rows))
    print("lemma counts:",dict(lemma_counts))
    print("distinct ayat:",len(ayahs),"surahs:",len(surahs))
    print("divine title occurrences:",divine)

if __name__=="__main__":
    main()
