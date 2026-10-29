"""Kullanıcının sağladığı Yûnus meal JSON dosyalarını yerel okuma katmanına alır."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from reader_data import SNAPSHOT, load_external, normalize_translation


def read_author(path: Path, source_id: int) -> dict[int, dict]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    data = payload.get("data", payload) if isinstance(payload, dict) else payload
    if isinstance(data, dict) and data.get("id", data.get("surah", 10)) != 10:
        raise ValueError("Yalnız Yûnus sûresi kabul edilir")
    rows = data.get("verses", []) if isinstance(data, dict) else data
    if not isinstance(rows, list):
        raise ValueError("JSON dosyası verses listesi veya ayet dizisi olmalıdır")
    result = {}
    for row in rows:
        ayah = row.get("verse_number", row.get("ayah"))
        if type(ayah) is not int or not 1 <= ayah <= 109 or ayah in result:
            raise ValueError("Ayet numarası geçersiz veya yinelenmiş")
        raw = row.get("translation", row)
        normalize_translation(raw, source_id)
        result[ayah] = raw
    if set(result) != set(range(1, 110)):
        raise ValueError("Her meal dosyası 109 Yûnus ayetini içermelidir")
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--okuyan", type=Path, help="Mehmet Okuyan (107) JSON dosyası")
    parser.add_argument("--aktas", type=Path, help="Erhan Aktaş (105) JSON dosyası")
    parser.add_argument("--source", required=True, help="Sağlanan dosyanın kaynağı veya kullanım izni")
    args = parser.parse_args(argv)
    if not args.okuyan and not args.aktas:
        parser.error("En az bir meal dosyası belirtilmelidir")
    staged = None
    try:
        imported = []
        for path, source_id in ((args.okuyan, 107), (args.aktas, 105)):
            if path is not None:
                imported.append(read_author(path, source_id))
        snapshot = {"surah": 10, "source": "Kullanıcının sağladığı meal dosyaları",
                    "rights": {"status": "user-provided", "source": args.source},
                    "verses": [{"ayah": ayah, "translations": [data[ayah] for data in imported]}
                               for ayah in range(1, 110)]}
        if SNAPSHOT.exists():
            raise ValueError("Yerel meal dosyası zaten var; mevcut kaydı silmeden ayrı yedek alın")
        SNAPSHOT.parent.mkdir(parents=True, exist_ok=True)
        candidate = SNAPSHOT.with_suffix(".tmp.json")
        with candidate.open("x", encoding="utf-8", newline="\n") as output:
            staged = candidate
            json.dump(snapshot, output, ensure_ascii=False, indent=2)
        load_external(staged)
        staged.replace(SNAPSHOT)
        print("Meal ve açıklamalar yerel olarak eklendi. Başlatma komutuyla yeniden üretin.")
        return 0
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(f"İçe aktarılamadı: {error}", file=sys.stderr)
        return 1
    finally:
        if staged is not None and staged.is_file():
            staged.unlink()


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    raise SystemExit(main())
