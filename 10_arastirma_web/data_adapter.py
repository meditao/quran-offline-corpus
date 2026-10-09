"""Salt okunur depo verilerini taşınabilir araştırma sitesi verisine dönüştürür.

Tanzil metni aynen korunur; QAC eşlemesi çalışma masasının hizalama motorundan
gelir. Çeviri ve analizler kaynak Markdown dosyalarındaki yorum katmanıdır.
Bu modül ağ kullanmaz ve yalnız standart Python kütüphanesine ihtiyaç duyar.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

WEB = Path(__file__).resolve().parent
REPO = WEB.parent
sys.path.insert(0, str(REPO / "09_calisma_masasi"))
from tezgah import okuma, okunus, veri  # noqa: E402

# Yalnız kullanıcı arayüzündeki Türkçe adlar; ayet sayıları kaynak XML'den alınır.
SURAH_NAMES = (
    "Fâtiha", "Bakara", "Âl-i İmrân", "Nisâ", "Mâide", "En‘âm", "A‘râf",
    "Enfâl", "Tevbe", "Yûnus", "Hûd", "Yûsuf", "Ra‘d", "İbrâhîm", "Hicr",
    "Nahl", "İsrâ", "Kehf", "Meryem", "Tâhâ", "Enbiyâ", "Hac", "Mü’minûn",
    "Nûr", "Furkân", "Şuarâ", "Neml", "Kasas", "Ankebût", "Rûm", "Lokmân",
    "Secde", "Ahzâb", "Sebe’", "Fâtır", "Yâsîn", "Sâffât", "Sâd", "Zümer",
    "Mü’min", "Fussilet", "Şûrâ", "Zuhruf", "Duhân", "Câsiye", "Ahkâf",
    "Muhammed", "Fetih", "Hucurât", "Kâf", "Zâriyât", "Tûr", "Necm", "Kamer",
    "Rahmân", "Vâkıa", "Hadîd", "Mücâdele", "Haşr", "Mümtehine", "Saff",
    "Cum‘a", "Münâfikûn", "Tegâbün", "Talâk", "Tahrîm", "Mülk", "Kalem",
    "Hâkka", "Meâric", "Nûh", "Cin", "Müzzemmil", "Müddessir", "Kıyâme",
    "İnsân", "Mürselât", "Nebe’", "Nâziât", "Abese", "Tekvîr", "İnfitâr",
    "Mutaffifîn", "İnşikâk", "Bürûc", "Târık", "A‘lâ", "Gâşiye", "Fecr",
    "Beled", "Şems", "Leyl", "Duhâ", "İnşirâh", "Tîn", "Alak", "Kadir",
    "Beyyine", "Zilzâl", "Âdiyât", "Kâria", "Tekâsür", "Asr", "Hümeze",
    "Fîl", "Kureyş", "Mâûn", "Kevser", "Kâfirûn", "Nasr", "Tebbet", "İhlâs",
    "Felak", "Nâs",
)

TRANSLATION_FILES = {
    "07_analyses/surahs/Bakara-002-066-meal-tefsir.md": (2, range(2, 67)),
    "07_analyses/surahs/Bakara-067-117-meal-tefsir.md": (2, range(67, 118)),
    "07_analyses/surahs/Yunus-001-109-meal-tefsir.md": (10, range(1, 110)),
}
SOURCE_DOCS = (
    "SOURCES.md", "LICENSES.md", "SOURCE_TERMS_ACCEPTED.md", "01_raw/README.md",
    "02_morphology/README.md", "02_morphology/qac/README.md", "03_indices/README.md",
    "09_calisma_masasi/okunus_kurallari.md",
)


def read_exact(path: Path) -> str:
    """Satır sonları dahil kaynak metnini korur."""
    with path.open("r", encoding="utf-8", newline="") as stream:
        return stream.read()


def document_id(path: str) -> str:
    """Dosya yolu değişmediği sürece kararlı, URL için güvenli kimlik."""
    readable = re.sub(r"[^a-z0-9-]+", "-", Path(path).stem.lower()).strip("-")
    return readable + "-" + hashlib.sha256(path.encode("utf-8")).hexdigest()[:8]


def markdown_paths() -> list[Path]:
    selected = set((REPO / "07_analyses").rglob("*.md"))
    selected.update((REPO / "06_methodology").rglob("*.md"))
    selected.update(REPO / name for name in SOURCE_DOCS)
    return sorted(selected, key=lambda p: p.relative_to(REPO).as_posix())


def source_paths() -> list[Path]:
    selected = set(markdown_paths())
    selected.update((REPO / "07_analyses").rglob("*.csv"))
    selected.update((REPO / "07_analyses").rglob("*.tsv"))
    selected.update((REPO / "09_calisma_masasi" / "tezgah").rglob("*.py"))
    selected.update((WEB / "static").rglob("*"))
    selected.update({Path(__file__), WEB / "build.py", WEB / "reader_data.py",
                     WEB / "yerel/acikkuran-yunus.json", veri.QAC_YOLU,
                     veri.ROOT_INDEX_YOLU, veri.LEMMA_INDEX_YOLU,
                     okuma.HIZALAMA_YOLU, okunus.TANZIL_YOLU,
                     okunus.DURAK_YOLU, okunus.MANIFEST_YOLU,
                     REPO / "01_raw/tanzil/quran-data.xml"})
    return sorted((p for p in selected if p.is_file()),
                  key=lambda p: p.relative_to(REPO).as_posix())


def fingerprints() -> dict[str, str]:
    return {p.relative_to(REPO).as_posix(): veri.sha256(p) for p in source_paths()}


def copyright_notices() -> dict[str, str]:
    tanzil = read_exact(okunus.TANZIL_YOLU)
    notice_start = tanzil.index("# PLEASE DO NOT REMOVE OR CHANGE THIS COPYRIGHT BLOCK")
    qac = read_exact(veri.QAC_YOLU)
    qac_end = qac.index("LOCATION\tFORM\tTAG\tFEATURES")
    return {"tanzil": tanzil[notice_start:], "qac": qac[:qac_end]}


def load_documents() -> tuple[list[dict], dict[str, str]]:
    documents = []
    contents = {}
    for path in markdown_paths():
        relative = path.relative_to(REPO).as_posix()
        content = read_exact(path)
        doc_id = document_id(relative)
        title = next((line.lstrip("# ").strip() for line in content.splitlines()
                      if line.startswith("# ")), path.stem)
        roots: list[str] = []
        surahs: list[int] = []
        if relative.startswith("07_analyses/roots/") and path.stem != "README":
            category = "Kök / kavram analizi"
            # Bu klasördeki mevcut dosyalar e-m-n araştırmasının parçalarıdır.
            # İleride eklenen başka kökleri otomatik olarak Amn ile etiketleme.
            if path.stem.startswith("Amn-") or path.stem in {"Iman-analysis", "Mumin-concept-card"}:
                roots = ["Amn"]
        elif relative.startswith("07_analyses/generated/root_profiles/"):
            category = "Üretilmiş kök analizi"
            roots = [relative.split("/")[3]]
        elif relative.startswith("07_analyses/surahs/"):
            category = "Sûre / çeviri çalışması"
            if path.stem.startswith("Bakara-"):
                surahs = [2]
            elif path.stem.startswith("Yunus-"):
                surahs = [10]
            elif path.stem.startswith("Asr-"):
                surahs = [103]
        elif relative.startswith("06_methodology/"):
            category = "Yöntem"
        elif relative in SOURCE_DOCS:
            category = "Kaynak / okunuş bilgisi"
        else:
            category = "Araştırma rehberi"
        documents.append({"id": doc_id, "path": relative, "title": title,
                          "category": category, "roots": roots, "surahs": surahs,
                          "url": f"data/documents/{doc_id}.json"})
        contents[doc_id] = content
    return documents, contents


def parse_translations(content: str, surah: int, source: str) -> dict[tuple[int, int], dict]:
    """İki Markdown biçimini çözer; sadece açıkça işaretlenmiş çevirileri alır.

    Bakara: ## Bakara 2:67 / ayrı kalın etiket.
    Yûnus: ## 1. Ayet veya **57. Ayet** / kalın ya da italik satır içi etiket.
    Tefsirden sonraki ayete ait açıklamalar da özgün metinle birlikte korunur.
    """
    verse_heading = re.compile(r"^(?:#{2}\s+Bakara\s+(\d+):(\d+)\s*|"
                               r"#{2}\s+(\d+)\.\s*Ayet\s*|"
                               r"\*\*(\d+)\.\s*Ayet\*\*\s*)$", re.IGNORECASE)
    label = re.compile(r"^\s*(\*{1,2})(Terimleri koruyan çeviri|Tefsirli çeviri)"
                       r"(:?)\1\s*(:?)\s*(.*)$", re.IGNORECASE)
    translations: dict[tuple[int, int], dict] = {}
    ref: tuple[int, int] | None = None
    field = None
    blocks: dict[str, list[str]] = {"terms": [], "tafsir": []}

    def finish() -> None:
        if ref is None:
            return
        fields = {name: "".join(lines).strip() for name, lines in blocks.items()}
        if not fields["terms"] or not fields["tafsir"]:
            raise veri.VeriHatasi(f"Eksik çeviri katmanı: {source}, {ref[0]}:{ref[1]}")
        if ref in translations:
            raise veri.VeriHatasi(f"Yinelenen çeviri başlığı: {source}, {ref}")
        translations[ref] = {**fields, "source": source, "documentId": document_id(source)}

    for line in content.splitlines(keepends=True):
        bare = line.rstrip("\r\n")
        match = verse_heading.match(bare)
        if match:
            finish()
            if match.group(1):
                ref = (int(match.group(1)), int(match.group(2)))
            else:
                ref = (surah, int(match.group(3) or match.group(4)))
            if ref[0] != surah:
                raise veri.VeriHatasi(f"Beklenmeyen sûre: {source}, {ref}")
            field = None
            blocks = {"terms": [], "tafsir": []}
            continue
        # Ayet dışındaki toplu değerlendirme bölümleri son ayete eklenmez.
        if re.match(r"^#{1,2}\s", bare):
            finish()
            ref = None
            field = None
            continue
        if ref is None:
            continue
        marker = label.match(bare)
        if marker:
            field = "terms" if marker.group(2).lower().startswith("terimleri") else "tafsir"
            if blocks[field]:
                raise veri.VeriHatasi(f"Yinelenen çeviri etiketi: {source}, {ref}, {field}")
            inline = marker.group(5)
            if inline:
                blocks[field].append(inline + line[len(bare):])
        elif field and bare.strip() not in {"---", "***", "___"}:
            blocks[field].append(line)
    finish()
    return translations


def load_translations(contents: dict[str, str]) -> dict[tuple[int, int], dict]:
    translations = {}
    for source, (surah, expected) in TRANSLATION_FILES.items():
        parsed = parse_translations(contents[document_id(source)], surah, source)
        expected_refs = {(surah, ayah) for ayah in expected}
        if set(parsed) != expected_refs:
            raise veri.VeriHatasi(f"Çeviri kapsamı uyuşmuyor: {source}; "
                                  f"eksik={sorted(expected_refs - set(parsed))}; "
                                  f"fazla={sorted(set(parsed) - expected_refs)}")
        if set(translations) & set(parsed):
            raise veri.VeriHatasi(f"Çakışan çeviri dosyası: {source}")
        translations.update(parsed)
    return translations


def qac_arabic(bw: str) -> str:
    """QAC genişletilmiş Buckwalter işaretlerini de kayıpsız gösterir."""
    mapping = {**veri.BW_ARAPCA, **okunus.QAC_EK_ISARETLER}
    return "".join(mapping.get(char, char) for char in bw)


def verse_data(surah: int, ayah: int, arabic: str, translations: dict,
               documents: list[dict]) -> dict:
    reading = okunus.oku(surah, ayah)
    matches, alignment_status = okuma.hizala(surah, ayah, reading)
    original_tokens = arabic.split(" ")
    prefix_count = len(reading.besmele)
    if len(original_tokens) != prefix_count + len(reading.kelimeler):
        raise veri.VeriHatasi(f"Tanzil tokenları okunuşla uyuşmuyor: {surah}:{ayah}")
    tokens = [{"text": token, "wordIds": []} for token in original_tokens]
    words = []
    for match in matches:
        word = match.kelime
        # Hizalama indices'i besmelesiz okunuşa göre 0'dan başlar. Yalnız bu
        # harita besmele önek sayısıyla kaydırılır; QAC word numarası değişmez.
        indices = [i + prefix_count for i in match.tanzil]
        for index in indices:
            tokens[index]["wordIds"].append(word.kelime)
        word_form = " ".join(original_tokens[i] for i in indices) if indices else qac_arabic(word.bicim)
        word_reading = " ".join(reading.kelimeler[i].latin +
                                (" [sekte]" if reading.kelimeler[i].sekte else "")
                                for i in match.tanzil) if match.tanzil else "—"
        words.append({
            "id": word.kelime, "form": word_form, "bw": word.bicim,
            "reading": word_reading, "roots": sorted(word.kokler),
            "lemmas": sorted(word.lemmalar), "alignmentNote": match.not_,
            "tanzilIndices": indices,
            "segments": [{"id": segment.no, "form": qac_arabic(segment.bicim),
                          "bw": segment.bicim, "tag": segment.etiket,
                          "type": segment.tur, "features": list(segment.ozellikler),
                          "root": segment.kok, "lemma": segment.lemma}
                         for segment in word.segmentler],
        })
    word_roots = {root for word in words for root in word["roots"]}
    linked_docs = [doc["id"] for doc in documents if
                   word_roots.intersection(doc["roots"]) or surah in doc["surahs"]]
    basmala = None
    if prefix_count:
        # 95:1/97:1 gibi özel başlangıç yazımlarını canonical 1:1 ile değiştirme.
        basmala = {"arabic": " ".join(original_tokens[:prefix_count]),
                   "reading": " ".join(word.latin for word in reading.besmele)}
    return {
        "surah": surah, "ayah": ayah, "ref": f"{surah}:{ayah}",
        "arabic": arabic, "reading": reading.latin_isaretli,
        "readingNotes": reading.belirsiz, "basmala": basmala, "tokens": tokens,
        "words": words, "alignmentStatus": alignment_status,
        "translation": translations.get((surah, ayah)), "documentIds": linked_docs,
    }


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n",
                    encoding="utf-8", newline="\n")


def _copy_sources(stage: Path, documents: list[dict], notices: dict[str, str]) -> None:
    sources = stage / "sources"
    sources.mkdir(parents=True, exist_ok=True)
    for path in (okunus.TANZIL_YOLU, veri.QAC_YOLU, okunus.DURAK_YOLU,
                 okunus.MANIFEST_YOLU, REPO / "01_raw/tanzil/quran-data.xml"):
        if path.exists():
            shutil.copyfile(path, sources / path.name)
    for name, content in notices.items():
        (sources / f"{name.upper()}-NOTICE.txt").write_bytes(content.encode("utf-8"))
    doc_paths = {REPO / doc["path"] for doc in documents}
    doc_paths.update((REPO / "07_analyses").rglob("*.csv"))
    doc_paths.update((REPO / "07_analyses").rglob("*.tsv"))
    for path in sorted(doc_paths):
        target = sources / "repository" / path.relative_to(REPO)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)


def _validate_sources() -> tuple[veri.Korpus, dict[tuple[int, int], str]]:
    # Bir süreçte ikinci üretimde değişmiş kaynağı eski lru_cache ile gizleme.
    for function in (veri.korpus, okunus.tanzil, okunus.durak_isaretleri,
                     okuma.hizalama_tablosu, okuma._ayet_dizini):
        function.cache_clear()
    corpus = veri.korpus()
    arabic = okunus.tanzil()
    failed = [check for check in veri.kurulum_denetimi() if not check.gecti]
    if failed:
        raise veri.VeriHatasi("Korpus denetimi başarısız: " +
                              "; ".join(check.ad for check in failed))
    if set(arabic) != set(corpus.ayet_segmentleri):
        raise veri.VeriHatasi("Tanzil ve QAC ayet kümeleri farklı")
    manifest = json.loads(read_exact(okunus.MANIFEST_YOLU))
    metadata = REPO / "01_raw/tanzil/quran-data.xml"
    record = next((record for record in manifest["files"]
                   if record["file"] == "01_raw/tanzil/quran-data.xml"), None)
    if not record or veri.sha256(metadata) != record["sha256"]:
        raise veri.VeriHatasi("Sûre metadata SHA-256 uyuşmuyor")
    return corpus, arabic


def export(stage: Path, input_hashes: dict[str, str], build_id: str) -> dict:
    corpus, arabic = _validate_sources()
    documents, contents = load_documents()
    translations = load_translations(contents)
    notices = copyright_notices()
    static = WEB / "static"
    if not (static / "index.html").is_file():
        raise FileNotFoundError("Site arayüzü bulunamadı: 10_arastirma_web/static/index.html")
    shutil.copytree(static, stage, dirs_exist_ok=True)
    # Service worker güncellemesi betik baytları değiştiğinde kurulur. Yalnız
    # Markdown/veri değişse de yeni korpusun tarayıcı önbelleğine ulaşması için
    # üretim kimliği çıktıya eklenir; kaynak sw.js dosyası değiştirilmez.
    worker = stage / "sw.js"
    if worker.is_file():
        worker.write_bytes(worker.read_bytes() +
                           f"\n/* Üretilen korpus sürümü */\nself.CORPUS_BUILD_ID = '{build_id}';\n".encode("utf-8"))
    _copy_sources(stage, documents, notices)
    for doc in documents:
        write_json(stage / doc["url"], {"id": doc["id"], "path": doc["path"],
                                      "title": doc["title"], "content": contents[doc["id"]]})

    roots = [{"bw": root, "arabic": veri.bw_arapca(root), "latin": veri.kok_latin(root),
              "wordCount": len(words),
              "verseCount": len({(word.sure, word.ayet) for word in words}),
              "surahCount": len({word.sure for word in words})}
             for root, words in sorted(corpus.kok_kelimeleri.items())]
    stats = {"surahs": len(corpus.sureler), "verses": len(arabic),
             "words": len(corpus.kelimeler), "segments": len(corpus.segmentler),
             "roots": len(roots), "translatedVerses": len(translations)}
    chapter_meta = ET.parse(REPO / "01_raw/tanzil/quran-data.xml").getroot().find("suras")
    if chapter_meta is None or len(chapter_meta) != len(SURAH_NAMES):
        raise veri.VeriHatasi("Sûre metadata yapısı beklenenden farklı")
    surahs = []
    search_words = []
    search_verses = []
    reader_readings = {}
    alignment_counts: Counter = Counter()
    unmatched_words = 0
    for meta in chapter_meta:
        surah = int(meta.attrib["index"])
        verse_count = int(meta.attrib["ayas"])
        actual_refs = {ref for ref in arabic if ref[0] == surah}
        if actual_refs != {(surah, ayah) for ayah in range(1, verse_count + 1)}:
            raise veri.VeriHatasi(f"Sûre metadata ayet sayısı farklı: {surah}")
        chapter = {"id": surah, "name": SURAH_NAMES[surah - 1],
                   "arabicName": meta.attrib["name"], "verseCount": verse_count,
                   "translatedCount": sum(1 for ref in translations if ref[0] == surah)}
        surahs.append(chapter)
        verses = []
        for ayah in range(1, verse_count + 1):
            verse = verse_data(surah, ayah, arabic[(surah, ayah)], translations, documents)
            verses.append(verse)
            if surah == 10:
                reader_readings[ayah] = (verse["reading"], verse["readingNotes"])
            alignment_counts[verse["alignmentStatus"]] += 1
            for word in verse["words"]:
                unmatched_words += int(not word["tanzilIndices"])
                search_words.append([surah, ayah, word["id"], word["form"], word["bw"],
                                     word["reading"], word["roots"], word["lemmas"]])
            translation = verse["translation"] or {}
            search_verses.append([surah, ayah, verse["arabic"], verse["reading"],
                                  translation.get("terms", ""), translation.get("tafsir", "")])
        write_json(stage / f"data/surahs/{surah:03}.json",
                   {**chapter, "verses": verses, "copyrightNotices": notices})
    write_json(stage / "data/search-index.json",
               {"words": search_words, "verses": search_verses, "copyrightNotices": notices})
    sources = [
        {"name": "Tanzil Project — Uthmani v1.1", "url": "https://tanzil.net/",
         "note": "Birincil Arapça metin; aynen korunmuştur. CC BY 3.0 ve değiştirmeme şartı.",
         "sha256": corpus_hash(input_hashes, okunus.TANZIL_YOLU),
         "localUrl": "sources/quran-uthmani.txt", "noticeUrl": "sources/TANZIL-NOTICE.txt"},
        {"name": "Quranic Arabic Corpus (QAC) — v0.4 / Kais Dukes", "url": "https://corpus.quran.com/",
         "note": "Kanonik kök / lemma / morfoloji annotation; birim: kelime konumu ve segment.",
         "sha256": corpus.sha256, "localUrl": "sources/quranic-corpus-morphology-0.4.txt",
         "noticeUrl": "sources/QAC-NOTICE.txt"},
        {"name": "Tanzil sûre metadata — v1.0", "url": "https://tanzil.net/docs/quran_metadata",
         "note": "Sûre adları ve ayet sayıları; Türkçe gösterim adları site katmanındadır.",
         "sha256": input_hashes["01_raw/tanzil/quran-data.xml"], "localUrl": "sources/quran-data.xml"},
        {"name": "Çalışma masası okunuş motoru", "url": "https://github.com/meditao/quran-offline-corpus",
         "note": "Tanzil'den kurallı aktarım; delil değildir. Belirsizlikler ve hizalama notları korunur.",
         "localUrl": "sources/repository/09_calisma_masasi/okunus_kurallari.md"},
        {"name": "Deponun çalışma çevirileri ve araştırma dosyaları",
         "url": "https://github.com/meditao/quran-offline-corpus/tree/main/07_analyses",
         "note": "Yorum / tefsir katmanı; kaynağın özgün Markdown metni korunur."},
    ]
    catalog = {"schemaVersion": 1, "buildId": build_id, "stats": stats,
               "surahs": surahs, "documents": documents, "roots": roots,
               "sources": sources, "copyrightNotices": notices, "sourceHashes": input_hashes,
               "provenance": {"sourceHashes": input_hashes,
                              "alignmentCounts": dict(sorted(alignment_counts.items())),
                              "unmatchedWords": unmatched_words,
                              "countUnits": {"words": "QAC kelime konumu", "segments": "QAC segment",
                                             "verses": "ayet", "surahs": "sûre", "roots": "benzersiz ROOT"},
                              "translationSources": list(TRANSLATION_FILES),
                              "generator": "10_arastirma_web/build.py", "networkUsed": False}}
    write_json(stage / "data/catalog.json", catalog)
    from reader_data import export_reader
    export_reader(stage, build_id, surahs, translations, reader_readings, write_json)
    # Büyük korpuslar dahil her dosya önbellek manifestindedir. Service worker
    # manifest.json'u ayrıca okuyarak kendi önbelleğine koyar.
    files = sorted(path.relative_to(stage).as_posix() for path in stage.rglob("*")
                   if path.is_file() and path != stage / "manifest.json")
    write_json(stage / "manifest.json", {"buildId": build_id, "files": files})
    return catalog


def corpus_hash(input_hashes: dict[str, str], path: Path) -> str:
    return input_hashes[path.relative_to(REPO).as_posix()]


def build_site(output: str | Path | None = None) -> Path:
    """Tam sonucu geçici dizinde üretir; hata halinde önceki çıktı korunur."""
    requested = Path(output) if output is not None else WEB / "dist"
    if requested.is_symlink() or (hasattr(requested, "is_junction") and requested.is_junction()):
        raise ValueError("Çıktı dizini sembolik bağlantı veya junction olamaz")
    target = requested.resolve()
    if target == REPO or target in REPO.parents or target == WEB:
        raise ValueError("Çıktı dizini depo veya site kaynak dizini olamaz")
    # Kaynak katmanlarının içerisine de yanlışlıkla çıktı yazılmaz.
    for layer in (REPO / name for name in
                  ("01_raw", "02_morphology", "03_indices", "04_lexicons", "05_translations",
                   "06_methodology", "07_analyses", "08_scripts", "09_calisma_masasi")):
        if target == layer.resolve() or layer.resolve() in target.parents:
            raise ValueError("Çıktı kaynak/veri katmanının içerisinde olamaz")
    if target == (WEB / "static").resolve() or (WEB / "static").resolve() in target.parents:
        raise ValueError("Çıktı static kaynak dizininin içerisinde olamaz")
    if target.exists() and not target.is_dir():
        raise ValueError("Çıktı bir dizin olmalıdır")
    if target.exists() and any(target.iterdir()):
        try:
            existing_catalog = json.loads(read_exact(target / "data/catalog.json"))
            existing_manifest = json.loads(read_exact(target / "manifest.json"))
            owned = (existing_catalog.get("schemaVersion") == 1 and
                     bool(existing_catalog.get("buildId")) and
                     existing_manifest.get("buildId") == existing_catalog["buildId"] and
                     existing_catalog.get("provenance", {}).get("generator") == "10_arastirma_web/build.py")
        except (OSError, ValueError, TypeError, KeyError):
            owned = False
        if not owned:
            raise ValueError("Dolu çıktı dizini bu uygulamanın ürettiği bir site değil")
        declared_files = set(existing_manifest.get("files", [])) | {"manifest.json"}
        declared_directories = {parent.as_posix() for file in declared_files
                                for parent in Path(file).parents if parent != Path(".")}
        actual_files = {path.relative_to(target).as_posix() for path in target.rglob("*")
                        if path.is_file()}
        actual_directories = {path.relative_to(target).as_posix() for path in target.rglob("*")
                              if path.is_dir()}
        extras = (actual_files - declared_files) | (actual_directories - declared_directories)
        if extras:
            raise ValueError("Çıktıya sonradan eklenen dosyalar korunmak için üretim durduruldu: " +
                             ", ".join(sorted(extras)))
        if any(path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction())
               for path in [target, *target.rglob("*")]):
            raise ValueError("Çıktı dizininde sembolik bağlantı veya junction kullanılamaz")
    target.parent.mkdir(parents=True, exist_ok=True)
    input_hashes = fingerprints()
    build_id = hashlib.sha256(json.dumps(input_hashes, sort_keys=True,
                                         separators=(",", ":")).encode("utf-8")).hexdigest()[:20]
    stage = Path(tempfile.mkdtemp(prefix=f".{target.name}-build-", dir=target.parent)).resolve()
    backup: Path | None = None

    def remove_temporary(path: Path, prefix: str) -> None:
        # Silinecek mutlak hedefler yalnız üretimin oluşturduğu kardeş dizinlerdir.
        resolved = path.resolve()
        if resolved.parent != target.parent or not resolved.name.startswith(prefix):
            raise ValueError("Geçici çıktı temizleme sınırı aşıldı")
        if resolved.exists():
            shutil.rmtree(resolved)

    try:
        export(stage, input_hashes, build_id)
        if fingerprints() != input_hashes:
            raise veri.VeriHatasi("Üretim sırasında kaynak değişti; önceki site çıktısı korundu")
        if target.exists():
            backup = Path(tempfile.mkdtemp(prefix=f".{target.name}-backup-", dir=target.parent)).resolve()
            backup.rmdir()
            target.replace(backup)
        try:
            stage.replace(target)
        except BaseException:
            if backup and backup.exists():
                backup.replace(target)
            raise
        if backup:
            remove_temporary(backup, f".{target.name}-backup-")
        return target
    finally:
        remove_temporary(stage, f".{target.name}-build-")
