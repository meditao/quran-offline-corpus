"""Kur'an çalışma masası — tek giriş noktası: python -m tezgah

Kanonik korpus QAC v0.4'tür. Ham veri katmanları (01–04) salt okunur;
bu paket onlardan okur, onlara yazmaz.
"""

import codecs
import io
import os
import sys

__all__ = ["veri", "tara", "kayit", "utf8_akislar", "utf8_ortam"]


def utf8_akislar() -> None:
    """stdout ve stderr'i UTF-8'e ayarlar.

    Windows'ta çıktı dosyaya ya da boruya yönlendirilince Python yerel kod sayfasını (ör. cp1254)
    kullanır; ṣ, ḥ, ʾ gibi harfler orada yoktur ve program çöker. -X utf8 gerekmesin diye giriş
    noktaları bunu çağırır. Yönlendirilmiş (TextIOWrapper olmayan) akışlara dokunmaz.
    """
    for ad in ("stdout", "stderr"):
        akis = getattr(sys, ad, None)
        if isinstance(akis, io.TextIOWrapper) and codecs.lookup(akis.encoding).name != "utf-8":
            akis.reconfigure(encoding="utf-8", errors=akis.errors)


def utf8_ortam(taban: dict[str, str] | None = None) -> dict[str, str]:
    """Alt süreçlere geçirilecek ortam: Python UTF-8 kipi ve UTF-8 akışlar."""
    ortam = dict(os.environ if taban is None else taban)
    ortam.update(PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    return ortam
