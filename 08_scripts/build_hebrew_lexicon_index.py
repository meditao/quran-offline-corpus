#!/usr/bin/env python3
"""Pinlenmiş Open Scriptures LexicalIndex.xml'den offline İbranice sözlük indeksi üretir.

Bu script Arapça-Qur'an köklerini otomatik kognat ilan ETMEZ. Yalnız İbranice lexical
kaynağı sorgulanabilir bir TSV'ye dönüştürür. Gerçek kognat eşlemesi insan/filolog
denetiminden sonra `04_lexicons/semitic/cognates.tsv` içine yazılır.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "04_lexicons" / "semitic" / "VENDOR_LOCK.json"
OUT_DIR = ROOT / "04_lexicons" / "generated"
OUT = OUT_DIR / "hebrew_lexical_index.tsv"
MANIFEST = OUT_DIR / "hebrew_lexical_index.manifest.json"

LEXICON_PATH = "LexicalIndex.xml"


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def text_of(el: ET.Element | None) -> str:
    if el is None:
        return ""
    return re.sub(r"\s+", " ", "".join(el.itertext())).strip()


def first_child(entry: ET.Element, name: str) -> ET.Element | None:
    for el in entry.iter():
        if local(el.tag) == name:
            return el
    return None


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_source() -> tuple[dict, bytes, str]:
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    source = next(s for s in lock["sources"] if s["name"] == "Open Scriptures Hebrew Lexicon")
    repo = source["repo"].removesuffix(".git")
    ref = source["ref"]
    url = f"{repo.replace('https://github.com/', 'https://raw.githubusercontent.com/')}/{ref}/{LEXICON_PATH}"
    req = Request(url, headers={"User-Agent": "quran-offline-corpus/1.0"})
    with urlopen(req, timeout=120) as response:
        data = response.read()
    return source, data, url


def main() -> None:
    source, data, url = load_source()
    root = ET.fromstring(data)

    rows: list[dict[str, str]] = []
    for entry in root.iter():
        if local(entry.tag) != "entry":
            continue
        word = first_child(entry, "w")
        if word is None:
            continue
        pos = first_child(entry, "pos")
        definition = first_child(entry, "def")
        xref = first_child(entry, "xref")
        etym = first_child(entry, "etym")

        entry_id = entry.attrib.get("id", "") or entry.attrib.get("{http://www.w3.org/XML/1998/namespace}id", "")
        row = {
            "entry_id": entry_id,
            "hebrew": text_of(word),
            "translit": word.attrib.get("xlit", ""),
            "pos": text_of(pos),
            "definition": text_of(definition),
            "etym_type": etym.attrib.get("type", "") if etym is not None else "",
            "etym_root": etym.attrib.get("root", "") if etym is not None else "",
            "xref_bdb": xref.attrib.get("bdb", "") if xref is not None else "",
            "xref_strong": xref.attrib.get("strong", "") if xref is not None else "",
            "xref_aug": xref.attrib.get("aug", "") if xref is not None else "",
            "xref_twot": xref.attrib.get("twot", "") if xref is not None else "",
        }
        rows.append(row)

    if not rows:
        raise SystemExit("No lexical entries parsed from LexicalIndex.xml")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fields = [
        "entry_id", "hebrew", "translit", "pos", "definition", "etym_type", "etym_root",
        "xref_bdb", "xref_strong", "xref_aug", "xref_twot",
    ]
    with OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    manifest = {
        "source_name": source["name"],
        "source_repo": source["repo"],
        "source_ref": source["ref"],
        "source_path": LEXICON_PATH,
        "source_url": url,
        "source_sha256": sha256(data),
        "license": source["license"],
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "record_count": len(rows),
        "records_with_etym_root": sum(bool(r["etym_root"]) for r in rows),
        "output": str(OUT.relative_to(ROOT)),
        "method_note": "Index only; no automatic Arabic-Hebrew cognate assignment.",
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Lexical entries: {len(rows):,}")
    print(f"Entries with etym_root: {manifest['records_with_etym_root']:,}")
    print(f"Source SHA-256: {manifest['source_sha256']}")
    print(f"Output: {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
