#!/usr/bin/env python3
"""Audit the Qur'anic noun lemma <iyma`n (iman) in pinned QAC v0.4.

Produces a reproducible list of all 45 noun occurrences with local context and
mechanical flags for key constructions relevant to semantic analysis. No final
semantic definition is encoded by the script.
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
OUT = ROOT / "07_analyses" / "generated" / "root_profiles" / "Amn" / "iman_noun"
LOCATION_RE = re.compile(r"^\((\d+):(\d+):(\d+):(\d+)\)$")
EXPECTED = 45
LEMMA = "<iyma`n"


def load_morph() -> dict[tuple[int,int,int], list[dict[str,str]]]:
    out: dict[tuple[int,int,int], list[dict[str,str]]] = {}
    with QAC.open("r", encoding="utf-8-sig") as f:
        for raw in f:
            line = raw.rstrip("\r\n")
            if not line.startswith("("):
                continue
            loc, form, tag, feat = line.split("\t")
            m = LOCATION_RE.match(loc)
            if not m:
                continue
            s,a,w,seg = map(int, m.groups())
            out.setdefault((s,a,w), []).append({"seg":str(seg),"form":form,"tag":tag,"feat":feat})
    return out


def has_lemma(segs: list[dict[str,str]]) -> bool:
    return any(f"LEM:{LEMMA}" in x["feat"].split("|") for x in segs)


def load_words():
    by_key = {}
    by_ayah = {}
    with WORDS.open("r", encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            k=(int(r["surah"]),int(r["ayah"]),int(r["word"]))
            by_key[k]=r
            by_ayah.setdefault((k[0],k[1]),[]).append(r)
    for arr in by_ayah.values(): arr.sort(key=lambda r:int(r["word"]))
    return by_key, by_ayah


def load_tanzil():
    verses={}
    with TANZIL.open("r",encoding="utf-8") as f:
        for raw in f:
            line=raw.rstrip("\r\n")
            if not line or line.startswith("#"): continue
            p=line.split("|",2)
            if len(p)==3 and p[0].isdigit() and p[1].isdigit():
                verses[(int(p[0]),int(p[1]))]=p[2]
    return verses


def window(arr, w, n=5):
    i=next(i for i,r in enumerate(arr) if int(r["word"])==w)
    return " ".join(r["form_arabic"] for r in arr[max(0,i-n):min(len(arr),i+n+1)])


def roots_near(arr, w, radius=5):
    i=next(i for i,r in enumerate(arr) if int(r["word"])==w)
    rows=arr[max(0,i-radius):min(len(arr),i+radius+1)]
    roots=[]
    for r in rows:
        roots.extend(x for x in r["roots_bw"].split(";") if x)
    return set(roots)


def main():
    morph=load_morph(); ann, by_ayah=load_words(); tanzil=load_tanzil()
    hits=sorted(k for k,segs in morph.items() if has_lemma(segs))
    if len(hits)!=EXPECTED:
        raise SystemExit(f"Expected {EXPECTED} iman noun occurrences; found {len(hits)}")

    rows=[]; flags=Counter()
    for s,a,w in hits:
        verse_rows=by_ayah[(s,a)]
        nearby=roots_near(verse_rows,w,6)
        f=[]
        for root,label in [
            ("zyd","near_z-y-d_increase"), ("kfr","near_k-f-r"),
            ("dxl","near_d-kh-l_enter"), ("Hbb","near_h-b-b_love"),
            ("zyn","near_z-y-n_adorn"), ("hdy","near_h-d-y_guidance"),
            ("Dye","near_D-y-E_lose/waste"), ("bdl","near_b-d-l_exchange"),
        ]:
            if root in nearby:
                f.append(label); flags[label]+=1
        r=ann[(s,a,w)]
        rows.append({
            "surah":s,"ayah":a,"word":w,"location":f"{s}:{a}:{w}",
            "form_arabic":r["form_arabic"],"form_bw":r["form_bw"],
            "flags":";".join(f),"context_arabic":window(verse_rows,w),
            "full_verse_uthmani":tanzil.get((s,a),"")
        })

    OUT.mkdir(parents=True,exist_ok=True)
    with (OUT/"occurrences.csv").open("w",encoding="utf-8",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=list(rows[0])); wr.writeheader(); wr.writerows(rows)

    surfaces=Counter(r["form_arabic"] for r in rows)
    md=["# Iman noun audit (`<iyma`n`)","",
        "Generated from pinned QAC v0.4; verse display from pinned Tanzil Uthmani v1.1.",
        "Mechanical proximity flags are candidate-finders only, not dependency/semantic conclusions.","",
        f"- Exact noun-lemma occurrences: **{len(rows)}**","",
        "## Surface forms","","| form | count |","|---|---:|"]
    for k,v in surfaces.most_common(): md.append(f"| `{k}` | {v} |")
    md += ["","## Candidate construction flags","","| flag | count |","|---|---:|"]
    for k,v in flags.most_common(): md.append(f"| `{k}` | {v} |")
    md += ["","## All occurrences",""]
    for r in rows:
        suffix=f" — flags: `{r['flags']}`" if r["flags"] else ""
        md.append(f"- **{r['location']}** `{r['form_arabic']}` — {r['full_verse_uthmani']}{suffix}")
    md += ["","## Guardrail","",
           "- A proximity flag means only that the indicated root appears within ±6 orthographic words.",
           "- Every decisive semantic claim must be manually checked against the full verse/passage."]
    (OUT/"report.md").write_text("\n".join(md)+"\n",encoding="utf-8")
    print("iman noun occurrences:",len(rows)); print("flags:",dict(flags))

if __name__=="__main__": main()
