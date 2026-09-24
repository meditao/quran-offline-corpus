"""İşletim sisteminden bağımsızlık: karakter kodlaması ve satır sonu (Windows'ta bildirilen iki hata).

1. Windows'ta çıktı dosyaya yönlendirilince Python yerel kod sayfasını (ör. cp1254) kullanır; ṣ gibi harfler
   orada yoktur. Program -X utf8 olmadan UTF-8 yazmalıdır.
2. Windows metin kipi yazarken \\n'yi \\r\\n'ye çevirir. Hash'lenen dosya ikili kipte yazılmalı, sha diskteki
   baytlardan alınmalıdır; öteki metin dosyaları newline="\\n" ile yazılır.

Windows davranışı Linux'ta da benzetilir (Path.open sarmalanır; PYTHONIOENCODING=cp1254); CI ayrıca gerçek
Windows'ta çalışır (.github/workflows/calisma-masasi-testleri.yml).
"""

import ast
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import _ortak  # noqa: F401
from tezgah import kavram, tez

MASA = _ortak.MASA
DEPO = MASA.parent
TARANAN = [*sorted((MASA / "tezgah").rglob("*.py")), *sorted((MASA / "testler").glob("*.py")),
           *[DEPO / "08_scripts" / ad for ad in ("measure_secondary_layers.py", "crosscheck_qac_quranmorphology.py",
                                                 "fetch_tanzil_marks.py", "fetch_semitic_sources.py")]]


def _sabit(dugum):
    return dugum.value if isinstance(dugum, ast.Constant) and isinstance(dugum.value, str) else None


def dosya_cagrilari(yol: Path):
    """(satır, işlem, kip, anahtar sözcükler) — open / Path.open / read_text / write_text / subprocess."""
    for d in ast.walk(ast.parse(yol.read_text(encoding="utf-8"))):
        if not isinstance(d, ast.Call):
            continue
        f = d.func
        kw = {k.arg for k in d.keywords}
        kip_kw = next((_sabit(k.value) for k in d.keywords if k.arg == "mode"), None)
        if isinstance(f, ast.Name) and f.id == "open":
            kip = kip_kw or (_sabit(d.args[1]) if len(d.args) > 1 else "r")
            yield d.lineno, "open", kip, kw
        elif isinstance(f, ast.Attribute) and f.attr == "open" and not (
                isinstance(f.value, ast.Name) and f.value.id in {"webbrowser", "zipfile", "z"}):
            kip = kip_kw or (_sabit(d.args[0]) if d.args else "r")
            yield d.lineno, ".open", kip, kw
        elif isinstance(f, ast.Attribute) and f.attr in ("read_text", "write_text"):
            yield d.lineno, f.attr, "w" if f.attr == "write_text" else "r", kw
        elif isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name) and f.value.id == "subprocess":
            yield d.lineno, "subprocess." + f.attr, None, kw


class KaynakDenetimi(unittest.TestCase):
    def test_metin_kipi_her_zaman_utf8(self):
        eksik = [f"{y.relative_to(DEPO)}:{s} {islem}" for y in TARANAN for s, islem, kip, kw in dosya_cagrilari(y)
                 if kip is not None and "b" not in kip and "encoding" not in kw]
        self.assertEqual(eksik, [], "metin kipinde encoding belirtilmeli")

    def test_metin_yazimi_satir_sonu_sabit(self):
        eksik = [f"{y.relative_to(DEPO)}:{s} {islem}" for y in TARANAN for s, islem, kip, kw in dosya_cagrilari(y)
                 if kip is not None and "b" not in kip and set(kip) & set("wax+") and "newline" not in kw]
        self.assertEqual(eksik, [], "metin yazımında newline belirtilmeli (Windows \\r\\n çevirisi)")

    def test_alt_surec_ortami(self):
        eksik = [f"{y.relative_to(DEPO)}:{s} {islem}" for y in TARANAN for s, islem, kip, kw in dosya_cagrilari(y)
                 if islem.startswith("subprocess.") and islem.split(".")[1] in {"run", "check_output", "Popen", "call"}
                 and "env" not in kw]
        self.assertEqual(eksik, [], "alt süreçlere ortam açıkça geçirilmeli")


_ASIL_OPEN = Path.open


def _windows_path_open(self, mode="r", buffering=-1, encoding=None, errors=None, newline=None):
    """Path.open'ı Windows metin kipi gibi davrandırır: newline=None ile yazarken \\n → \\r\\n.

    Path.write_text / write_bytes / open 3.10–3.14 arasında hep Path.open'dan geçer (io.open'ı sarmak 3.10'da
    işe yaramaz: pathlib onu sınıf tanımında bağlar)."""
    if "b" not in mode and newline is None and set(mode) & set("wax+"):
        newline = "\r\n"
    return _ASIL_OPEN(self, mode, buffering, encoding, errors, newline)


def windows_kipi():
    return mock.patch.object(Path, "open", _windows_path_open)


class WindowsSatirSonu(unittest.TestCase):
    def setUp(self):
        self.gecici = tempfile.TemporaryDirectory()
        self.dizin = Path(self.gecici.name)
        self.addCleanup(self.gecici.cleanup)

    def test_benzetim_gercekten_cevirir(self):
        yol = self.dizin / "x.txt"
        with windows_kipi():
            yol.write_text("a\nb\n", encoding="utf-8", newline=None)   # bilerek: platform çevirisi (benzetim)
        self.assertEqual(yol.read_bytes(), b"a\r\nb\r\n", "benzetim çalışmıyorsa aşağıdaki test anlamsız")

    def test_tez_surumu_windows_metin_kipinde_butun(self):
        with mock.patch.object(tez, "TEZLER", self.dizin / "tezler"), windows_kipi():
            tez.ac("t", "Deneme tezi tek cümledir.", ["salât=deneme"], ["kip=tanımlayıcı"], ['kok Slw'])
            tez.yeni_surum("t", "deneme gerekçesi", tez="Deneme tezi ikinci cümledir.")
            t = tez.Tez("t")        # bütünlük denetimi: sha diskteki baytlarla aynı olmalı
            self.assertEqual(t.guncel_no, 2)
            hatalar, _ = tez.denetle("t")
            self.assertEqual(hatalar, [])
        for dosya in (self.dizin / "tezler" / "t").iterdir():
            with self.subTest(dosya=dosya.name):
                self.assertNotIn(b"\r", dosya.read_bytes())
        for dosya in (self.dizin / "tezler" / "t").glob("surum-*.json"):
            os.chmod(dosya, 0o644)   # geçici dizin Windows'ta silinebilsin

    def test_kavram_dosyasi_windows_metin_kipinde_lf(self):
        with mock.patch.object(kavram, "KAVRAMLAR", self.dizin), windows_kipi():
            kavram.ac("deneme", "ṣ-l-v kökü nasıl kullanılıyor?", ["Slw"])
            hatalar, _ = kavram.denetle("deneme")
            self.assertEqual(hatalar, [])
        for dosya in (self.dizin / "deneme").iterdir():
            with self.subTest(dosya=dosya.name):
                self.assertNotIn(b"\r", dosya.read_bytes())


class YonlendirilmisCikti(unittest.TestCase):
    """Alt süreç bilerek UTF-8 dışı bir kodlamayla başlatılır (Türkçe Windows: cp1254)."""

    def calistir(self, *argv):
        ortam = {k: v for k, v in os.environ.items() if k not in ("PYTHONUTF8", "PYTHONIOENCODING")}
        ortam.update(PYTHONIOENCODING="cp1254", PYTHONUTF8="0")
        return subprocess.run([sys.executable, *argv], cwd=MASA, env=ortam, capture_output=True, timeout=300)

    def test_stdout_utf8(self):
        r = self.calistir("-m", "tezgah", "kok", "Slw", "--limit", "1")
        self.assertEqual(r.returncode, 0, r.stderr.decode("utf-8", "replace"))
        cikti = r.stdout.decode("utf-8")        # UTF-8 değilse burada hata verir
        self.assertIn("ṣ-l-v", cikti)
        self.assertIn("Durum       : çalıştırıldı", cikti)

    def test_stderr_utf8(self):
        r = self.calistir("-c", "import sys; sys.path.insert(0, '.'); import tezgah; tezgah.utf8_akislar(); "
                                "print('\\u1e63-l-v', file=sys.stderr)")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stderr.decode("utf-8").strip(), "ṣ-l-v")

    def test_utf8_ortam(self):
        from tezgah import utf8_ortam
        o = utf8_ortam({"PATH": "x", "PYTHONIOENCODING": "cp1254"})
        self.assertEqual((o["PATH"], o["PYTHONUTF8"], o["PYTHONIOENCODING"]), ("x", "1", "utf-8"))


if __name__ == "__main__":
    unittest.main()
