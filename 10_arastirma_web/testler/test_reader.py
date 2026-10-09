"""Sade Yûnus okuma sayfasının kapsam ve kaynak aktarım sınamaları.

Üretim sırasında ağ engellenir. Aynı kaynaktan üretilen eski korpus çıktısı,
okunuş ve mevcut tefsirli çevirinin sade görünümde kaybolmadığını doğrular.
"""

from __future__ import annotations

import importlib.util
import copy
import json
import shutil
import socket
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


WEB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WEB))

from reader_data import load_external, normalize_translation  # noqa: E402


def example_translation(author_id, ayah=1):
    """Gerçek meal metni içermeyen, iki yazarlı aktarım sınama kaydı."""
    name = {107: "Mehmet Okuyan", 105: "Erhan Aktaş"}[author_id]
    return {"id": f"example-{author_id}-{ayah}",
            "text": f"Örnek {ayah}. ayet (kavram). [1] Devamı.",
            "author": {"id": author_id, "name": name},
            "footnotes": [{"id": ayah * 1000 + author_id, "number": 1,
                           "text": f"<p>{name} için örnek {ayah}. açıklama &amp; bilgi.</p>"}]}


class LocalMealImport(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="kuran-reader-import-test-")
        self.addCleanup(self.temporary.cleanup)
        self.path = Path(self.temporary.name) / "invented-yunus.json"
        self.snapshot = {"surah": 10,
                         "rights": {"status": "user-provided", "source": "Yalnız sınama için yazılmış örnek metin"},
                         "verses": [{"ayah": ayah, "translations": [example_translation(107, ayah),
                                                                    example_translation(105, ayah)]}
                                    for ayah in range(1, 110)]}

    def write_snapshot(self, snapshot=None):
        self.path.write_text(json.dumps(snapshot or self.snapshot, ensure_ascii=False), encoding="utf-8")

    def test_complete_user_file_imports_both_exact_authors_without_network(self):
        self.write_snapshot()
        with mock.patch.object(socket, "create_connection", side_effect=AssertionError("Ağ çağrısı")), \
                mock.patch("urllib.request.urlopen", side_effect=AssertionError("Ağ çağrısı")):
            result, provenance = load_external(self.path)
        self.assertEqual(set(result), set(range(1, 110)))
        self.assertEqual(provenance["rights"], self.snapshot["rights"])
        for ayah in range(1, 110):
            with self.subTest(ayah=ayah):
                self.assertEqual(set(result[ayah]), {"okuyan", "aktas"})
                for author_id, short_id in ((107, "okuyan"), (105, "aktas")):
                    translation = result[ayah][short_id]
                    self.assertEqual(translation["text"], f"Örnek {ayah}. ayet (kavram). [1] Devamı.")
                    self.assertEqual(translation["footnotes"][0]["sourceId"], ayah * 1000 + author_id)
                    self.assertEqual(translation["sourceUrl"], f"https://acikkuran.com/10/{ayah}?author={author_id}")

    def test_other_erhan_aktas_editions_are_rejected(self):
        for wrong_id, wrong_name in ((50, "Erhan Aktaş (Eski Baskı)"),
                                     (115, "Erhan Aktaş (10. Baskı)"),
                                     (105, "Erhan Aktaş (Eski Baskı)")):
            raw = example_translation(105)
            raw["author"] = {"id": wrong_id, "name": wrong_name}
            with self.subTest(author=raw["author"]):
                with self.assertRaises(ValueError):
                    normalize_translation(raw, 105)

    def test_note_marker_keeps_source_note_and_becomes_a_star(self):
        result = normalize_translation(example_translation(107), 107)
        self.assertEqual(result["parts"], [{"text": "Örnek 1. ayet (kavram). "},
                                          {"noteId": "1", "label": "*"}, {"text": " Devamı."}])
        self.assertEqual(result["footnotes"], [{"id": "1", "label": "*", "number": 1,
                                              "sourceId": 1107,
                                              "text": "Mehmet Okuyan için örnek 1. açıklama & bilgi."}])

    def test_missing_and_duplicate_notes_are_rejected(self):
        missing = example_translation(107)
        missing["footnotes"] = None
        duplicate = example_translation(107)
        duplicate["footnotes"].append(copy.deepcopy(duplicate["footnotes"][0]))
        for raw in (missing, duplicate):
            with self.subTest(notes=raw["footnotes"]):
                with self.assertRaises(ValueError):
                    normalize_translation(raw, 107)

    def test_unmarked_source_note_is_not_discarded(self):
        raw = example_translation(105)
        raw["text"] = "Yalnız örnek metin."
        translation = normalize_translation(raw, 105)
        self.assertEqual(translation["parts"][-1], {"noteId": "1", "label": "*"})
        self.assertEqual(len(translation["footnotes"]), 1)

    def test_html_is_reduced_to_safe_readable_text(self):
        raw = example_translation(105)
        raw["text"] = '<p>Örnek <b>kavram</b> &amp; bilgi. [1]</p><script>alert("x")</script>'
        raw["footnotes"][0]["text"] = '<div>Açıklama<br>ikinci satır.</div><style>body{color:red}</style>'
        translation = normalize_translation(raw, 105)
        self.assertEqual(translation["text"], "Örnek kavram & bilgi. [1]")
        self.assertEqual(translation["footnotes"][0]["text"], "Açıklama\nikinci satır.")
        self.assertNotIn("alert", translation["text"])
        self.assertNotIn("color", translation["footnotes"][0]["text"])

    def test_incomplete_duplicate_or_wrong_surah_files_are_rejected(self):
        variants = []
        missing = copy.deepcopy(self.snapshot)
        missing["verses"].pop()
        variants.append(missing)
        duplicate = copy.deepcopy(self.snapshot)
        duplicate["verses"].append(copy.deepcopy(duplicate["verses"][0]))
        variants.append(duplicate)
        wrong = copy.deepcopy(self.snapshot)
        wrong["surah"] = 2
        variants.append(wrong)
        for index, snapshot in enumerate(variants):
            self.write_snapshot(snapshot)
            with self.subTest(variant=index):
                with self.assertRaises(ValueError):
                    load_external(self.path)

    def test_missing_file_is_explicitly_empty(self):
        self.assertEqual(load_external(self.path), ({}, None))

    def test_missing_author_stays_missing_without_using_a_different_edition(self):
        self.snapshot["verses"][0]["translations"] = [example_translation(107)]
        self.write_snapshot()
        result, _ = load_external(self.path)
        self.assertEqual(set(result[1]), {"okuyan"})
        self.assertEqual(set(result[2]), {"okuyan", "aktas"})


class YunusReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix="kuran-reader-test-")
        cls.addClassCleanup(cls.temporary.cleanup)
        spec = importlib.util.spec_from_file_location("reader_test_build", WEB / "build.py")
        builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(builder)
        with mock.patch.object(socket, "create_connection", side_effect=AssertionError("Ağ çağrısı")), \
                mock.patch("urllib.request.urlopen", side_effect=AssertionError("Ağ çağrısı")):
            cls.output = Path(builder.build(Path(cls.temporary.name) / "site"))
        cls.catalog = cls.read_json("data/reader/catalog.json")
        cls.yunus = cls.read_json("data/reader/010.json")
        cls.original = cls.read_json("data/surahs/010.json")

    @classmethod
    def read_json(cls, relative):
        return json.loads((cls.output / relative).read_text(encoding="utf-8"))

    def test_only_yunus_is_available(self):
        self.assertEqual(self.catalog["schemaVersion"], 1)
        self.assertEqual([s["id"] for s in self.catalog["surahs"]], list(range(1, 115)))
        self.assertEqual([s["id"] for s in self.catalog["surahs"] if s["available"]], [10])
        yunus = self.catalog["surahs"][9]
        self.assertEqual(yunus["verseCount"], 109)
        self.assertEqual(yunus["name"], "Yûnus")
        self.assertEqual(sorted(p.name for p in (self.output / "data/reader").glob("[0-9]*.json")),
                         ["010.json"])

    def test_all_109_verses_are_in_one_file_and_in_order(self):
        self.assertEqual(self.yunus["surah"], 10)
        self.assertEqual([v["ayah"] for v in self.yunus["verses"]], list(range(1, 110)))
        self.assertEqual([v["ref"] for v in self.yunus["verses"]],
                         [f"10:{ayah}" for ayah in range(1, 110)])

    def test_three_requested_authors_only(self):
        expected = [("okuyan", "Mehmet Okuyan"), ("aktas", "Erhan Aktaş"),
                    ("biz", "Bizim tefsirli çevirimiz")]
        self.assertEqual([(a["id"], a["name"]) for a in self.catalog["authors"]], expected)
        for verse in self.yunus["verses"]:
            with self.subTest(ref=verse["ref"]):
                self.assertEqual([t["authorId"] for t in verse["translations"]],
                                 [a[0] for a in expected])
                self.assertEqual([t["author"] for t in verse["translations"]],
                                 [a[1] for a in expected])
                for translation in verse["translations"]:
                    self.assertIsInstance(translation["available"], bool)
                    self.assertEqual(bool(translation["text"]), translation["available"])
                    self.assertIsInstance(translation["footnotes"], list)

    def test_reading_and_our_tafsir_are_unchanged(self):
        for verse, original in zip(self.yunus["verses"], self.original["verses"]):
            with self.subTest(ref=verse["ref"]):
                self.assertTrue(verse["reading"])
                self.assertEqual(verse["reading"], original["reading"])
                self.assertEqual(verse["readingNotes"], original["readingNotes"])
                ours = next(t for t in verse["translations"] if t["authorId"] == "biz")
                self.assertTrue(ours["available"])
                self.assertEqual(ours["text"], original["translation"]["tafsir"])
        first = self.yunus["verses"][0]["translations"][2]["text"]
        self.assertIn("(ḥakîm)", first)
        self.assertIn("(âyât)", first)

    def test_reader_does_not_export_arabic_or_research_panels(self):
        for verse in self.yunus["verses"]:
            with self.subTest(ref=verse["ref"]):
                self.assertFalse({"arabic", "tokens", "words", "documentIds", "translation"} & verse.keys())
                for translation in verse["translations"]:
                    self.assertNotIn("terms", translation)

    def test_star_notes_are_associated_with_their_own_translation(self):
        for verse in self.yunus["verses"]:
            for translation in verse["translations"]:
                with self.subTest(ref=verse["ref"], author=translation["authorId"]):
                    notes = translation["footnotes"]
                    identifiers = [str(note["id"]) for note in notes]
                    self.assertEqual(len(identifiers), len(set(identifiers)))
                    for note in notes:
                        self.assertTrue(str(note["id"]))
                        self.assertTrue(note["label"])
                        self.assertTrue(note["text"])
                    for part in translation.get("parts", []):
                        if part.get("noteId") is not None:
                            self.assertIn(str(part["noteId"]), identifiers)
                            self.assertTrue(part["label"])

    def test_reader_files_share_the_offline_build(self):
        manifest = self.read_json("manifest.json")
        self.assertEqual(self.catalog["buildId"], manifest["buildId"])
        self.assertIn("data/reader/catalog.json", manifest["files"])
        self.assertIn("data/reader/010.json", manifest["files"])

    def test_reader_chapter_is_readable_with_network_disabled(self):
        node = shutil.which("node")
        if node is None:
            bundled = Path(sys.executable).parent.parent / "node/bin/node.exe"
            if bundled.is_file():
                node = str(bundled)
        if node is None:
            self.skipTest("Çevrimdışı worker sınaması için isteğe bağlı Node.js bulunamadı")
        result = subprocess.run([node, str(WEB / "testler/reader_worker_test.js"), str(self.output)],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, encoding="utf-8", timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("109 ayet ve üç çeviri satırı", result.stdout)


if __name__ == "__main__":
    unittest.main()
