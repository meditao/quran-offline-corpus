"""Ortak Arapça harf → Latin tablosu.

Kök gösterimi (veri.kok_latin) ve okunuş (okunus.py) aynı tabloyu kullanır;
tablonun tek kaynağı burasıdır. Belgesi: 09_calisma_masasi/okunus_kurallari.md
(testler belge ile bu tablonun birebir aynı olduğunu denetler).

Eşleme ünsüzlerde kayıpsızdır: iki farklı ünsüz aynı Latin karşılığa gitmez.
Hemze taşıyıcıları (ء أ إ ؤ ئ) tek ünsüzdür: ʾ. ي ile ى ünsüz olarak y'dir.
"""

from __future__ import annotations

# (Arapça harf, Latin, Türkçe harf adı) — tablo sırası belgedeki sıradır.
HARF_TABLOSU: tuple[tuple[str, str, str], ...] = (
    ("ء", "ʾ", "hemze"),
    ("ب", "b", "be"),
    ("ت", "t", "te"),
    ("ث", "s̱", "se"),
    ("ج", "c", "cim"),
    ("ح", "ḥ", "ha"),
    ("خ", "ḫ", "hı"),
    ("د", "d", "dal"),
    ("ذ", "ẕ", "zel"),
    ("ر", "r", "ra"),
    ("ز", "z", "ze"),
    ("س", "s", "sin"),
    ("ش", "ş", "şın"),
    ("ص", "ṣ", "sad"),
    ("ض", "ż", "dad"),
    ("ط", "ṭ", "tı"),
    ("ظ", "ẓ", "zı"),
    ("ع", "ʿ", "ayn"),
    ("غ", "g", "gayn"),
    ("ف", "f", "fe"),
    ("ق", "q", "kaf"),
    ("ك", "k", "kef"),
    ("ل", "l", "lam"),
    ("م", "m", "mim"),
    ("ن", "n", "nun"),
    ("ه", "h", "he"),
    ("و", "v", "vav"),
    ("ي", "y", "ye"),
)

HARF_LATIN: dict[str, str] = {a: l for a, l, _ in HARF_TABLOSU}

# Aynı ünsüzün yazım varyantları.
HEMZE_TASIYICILARI = ("أ", "إ", "ؤ", "ئ")
for _h in HEMZE_TASIYICILARI:
    HARF_LATIN[_h] = HARF_LATIN["ء"]
HARF_LATIN["ى"] = HARF_LATIN["ي"]
HARF_LATIN["ة"] = HARF_LATIN["ت"]   # vakfta "h" olur (okunus.py)

# Kurallı ünlüler (okunus.py). Kısa ünlüler Türkçe a/e uyumu uygulanmadan
# tek karşılıkla yazılır; bkz. okunus_kurallari.md.
UNLU_TABLOSU: tuple[tuple[str, str, str], ...] = (
    ("َ", "a", "fetha"),
    ("ِ", "i", "kesre"),
    ("ُ", "u", "damme"),
    ("ً", "an", "tenvin fetha"),
    ("ٍ", "in", "tenvin kesre"),
    ("ٌ", "un", "tenvin damme"),
)
UNLU_LATIN: dict[str, str] = {a: l for a, l, _ in UNLU_TABLOSU}
UZUN = {"a": "â", "i": "î", "u": "û"}
