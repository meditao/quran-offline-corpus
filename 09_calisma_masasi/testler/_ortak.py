"""Testlerin ortak kurulumu: tezgah paketini içe aktarılabilir yapar."""

import sys
from pathlib import Path

MASA = Path(__file__).resolve().parents[1]
if str(MASA) not in sys.path:
    sys.path.insert(0, str(MASA))

from tezgah import utf8_akislar  # noqa: E402

utf8_akislar()   # python -m unittest ile çalıştırılınca da (Windows, yönlendirilmiş çıktı)
