"""Yalnız Yûnus için sade, ayetleri alt alta sunan meal verisi."""

from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path

WEB = Path(__file__).resolve().parent
SNAPSHOT = WEB / "yerel" / "acikkuran-yunus.json"
AUTHORS = (
    {"id": "okuyan", "name": "Mehmet Okuyan", "sourceId": 107},
    {"id": "aktas", "name": "Erhan Aktaş", "sourceId": 105},
    {"id": "biz", "name": "Bizim tefsirli çevirimiz"},
)


class _PlainText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.suppressed = 0

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style"}:
            self.suppressed += 1
        elif not self.suppressed and tag in {"br", "p", "div", "li"}:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in {"script", "style"} and self.suppressed:
            self.suppressed -= 1
        elif not self.suppressed and tag in {"p", "div", "li"}:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.suppressed:
            self.parts.append(data)


def plain_text(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("Meal ve açıklama metni bir metin olmalıdır")
    parser = _PlainText()
    parser.feed(value)
    parser.close()
    return re.sub(r"\n{3,}", "\n\n", "".join(parser.parts)).strip()


def normalize_translation(raw: dict, expected_id: int) -> dict:
    """Yazar kimliği ve dipnot referanslarını doğrular; sürümleri karıştırmaz."""
    author = next((item for item in AUTHORS if item.get("sourceId") == expected_id), None)
    if author is None:
        raise ValueError("Bu yazar sade Yûnus okumasının kapsamında değil")
    source_author = raw.get("author", {})
    if source_author.get("id") != expected_id or source_author.get("name") != author["name"]:
        raise ValueError(f"Yanlış meal sürümü: yalnız {author['name']} (yazar {expected_id}) kabul edilir")
    text = plain_text(raw.get("text", ""))
    if not text:
        raise ValueError("Meal metni boş olamaz")
    notes, by_number = [], {}
    raw_notes = raw.get("footnotes") or []
    if not isinstance(raw_notes, list):
        raise ValueError("Açıklamalar liste olmalıdır")
    for note in raw_notes:
        number = str(note.get("number", ""))
        if not number.isdigit() or number in by_number:
            raise ValueError("Açıklama numarası eksik veya yinelenmiş")
        note_text = plain_text(note.get("text", ""))
        if not note_text:
            raise ValueError("Açıklama metni boş olamaz")
        record = {"id": number, "label": "*", "number": int(number), "text": note_text,
                  "sourceId": note.get("id")}
        by_number[number] = record
        notes.append(record)
    parts = []
    last = 0
    referenced = set()
    for match in re.finditer(r"\[(\d+)\]", text):
        number = match.group(1)
        if number not in by_number:
            raise ValueError(f"Metindeki [{number}] açıklaması eksik")
        if match.start() > last:
            parts.append({"text": text[last:match.start()]})
        parts.append({"noteId": number, "label": "*"})
        referenced.add(number)
        last = match.end()
    if last < len(text):
        parts.append({"text": text[last:]})
    # Metin içinde işaretlenmeyen kaynak açıklamaları da kaybolmaz.
    for number in by_number:
        if number not in referenced:
            parts.append({"noteId": number, "label": "*"})
    return {"authorId": author["id"], "author": author["name"], "available": True,
            "text": text, "parts": parts, "footnotes": notes}


def load_external(path: Path = SNAPSHOT) -> tuple[dict[int, dict[str, dict]], dict | None]:
    """Kullanıcı metnini veya açık izinle alınmış yerel snapshot'ı okur; ağ kullanmaz."""
    if not path.exists():
        return {}, None
    snapshot = json.loads(path.read_text(encoding="utf-8"))
    if snapshot.get("surah") != 10:
        raise ValueError("Yerel meal dosyası yalnız Yûnus sûresi (10) olmalıdır")
    rights = snapshot.get("rights", {})
    if rights.get("status") not in {"user-provided", "open-license"} or not rights.get("source"):
        raise ValueError("Yerel meal için kullanıcı dosyası veya açık izin kaynağı kaydedilmelidir")
    rows = snapshot.get("verses", [])
    if not isinstance(rows, list):
        raise ValueError("Yerel meal ayetleri liste olmalıdır")
    result = {}
    for row in rows:
        ayah = row.get("ayah")
        if type(ayah) is not int or not 1 <= ayah <= 109 or ayah in result:
            raise ValueError("Yerel meal ayet numarası geçersiz veya yinelenmiş")
        translations = {}
        for raw in row.get("translations", []):
            source_id = raw.get("author", {}).get("id")
            if source_id not in {105, 107}:
                raise ValueError("Yalnız Mehmet Okuyan (107) ve Erhan Aktaş (105) alınabilir")
            value = normalize_translation(raw, source_id)
            if value["authorId"] in translations:
                raise ValueError("Aynı ayette aynı yazar yinelenmiş")
            value["sourceUrl"] = f"https://acikkuran.com/10/{ayah}?author={source_id}"
            translations[value["authorId"]] = value
        result[ayah] = translations
    if set(result) != set(range(1, 110)):
        raise ValueError("Yerel meal dosyası Yûnus'un 109 ayetini içermelidir")
    return result, {"source": snapshot.get("source", "Açık Kuran"), "rights": rights}


def export_reader(stage: Path, build_id: str, surahs: list[dict], translations: dict,
                  readings: dict[int, tuple[str, list[str]]], write_json) -> None:
    external, provenance = load_external()
    verses = []
    missing = set()
    for ayah in range(1, 110):
        versions = []
        for author in AUTHORS[:2]:
            value = external.get(ayah, {}).get(author["id"])
            if value is None:
                missing.add(author["name"])
                value = {"authorId": author["id"], "author": author["name"], "available": False,
                         "text": "", "footnotes": [], "parts": [],
                         "sourceUrl": f"https://acikkuran.com/10/{ayah}?author={author['sourceId']}"}
            versions.append(value)
        versions.append({"authorId": "biz", "author": AUTHORS[2]["name"], "available": True,
                         "text": translations[(10, ayah)]["tafsir"], "footnotes": [],
                         "sourcePath": translations[(10, ayah)]["source"]})
        reading, notes = readings[ayah]
        verses.append({"ayah": ayah, "ref": f"10:{ayah}", "reading": reading,
                       "readingNotes": notes, "translations": versions})
    source_notes = []
    if missing:
        names = " ve ".join(a["name"] for a in AUTHORS[:2] if a["name"] in missing)
        source_notes.append(f"{names}: tam meal ve açıklama metinleri henüz yerel olarak eklenmedi. "
                            "Kaynak bağlantıları Açık Kuran'ı açar; "
                            "tefsirli çevirimiz ve okunuşlar offline çalışır.")
    catalog = {"schemaVersion": 1, "buildId": build_id,
               "surahs": [{"id": s["id"], "name": s["name"], "verseCount": s["verseCount"],
                           "available": s["id"] == 10} for s in surahs],
               "authors": list(AUTHORS), "sourceNotes": source_notes,
               "sources": [{"name": "Açık Kuran", "url": "https://acikkuran.com/10"},
                           {"name": "Bizim Yûnus tefsirli çevirimiz",
                            "path": "07_analyses/surahs/Yunus-001-109-meal-tefsir.md"}],
               "externalProvenance": provenance}
    write_json(stage / "data/reader/catalog.json", catalog)
    write_json(stage / "data/reader/010.json", {"surah": 10, "name": "Yûnus", "verses": verses})
