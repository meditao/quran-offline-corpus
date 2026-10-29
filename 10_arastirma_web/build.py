"""İnternet kullanmadan taşınabilir Kur'an araştırma sitesi üretir."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WEB = Path(__file__).resolve().parent
if str(WEB) not in sys.path:
    sys.path.insert(0, str(WEB))
from data_adapter import build_site  # noqa: E402
from tezgah import utf8_akislar  # noqa: E402


def build(output: str | Path | None = None) -> Path:
    """Statik çıktıyı üretir ve mutlak çıktı dizinini döndürür."""
    return build_site(output)


def main(argv: list[str] | None = None) -> int:
    utf8_akislar()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Çıktı dizini (varsayılan: 10_arastirma_web/dist)")
    args = parser.parse_args(argv)
    try:
        target = build(args.output)
        catalog = json.loads((target / "data/catalog.json").read_text(encoding="utf-8"))
    except Exception as error:
        print(f"Site üretilemedi: {error}", file=sys.stderr)
        return 1
    stats = catalog["stats"]
    print(f"Site hazır: {target}")
    print(f"{stats['surahs']} sûre · {stats['verses']} ayet · {stats['words']} QAC kelime konumu · "
          f"{stats['segments']} segment · {stats['roots']} kök · {stats['translatedVerses']} çevirili ayet")
    print(f"Veri izi: {catalog['buildId']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
