#!/usr/bin/env python3
"""Tanzil Quran Text v1.1 kaynaklarını indir ve bütünlük manifesti üret.

Kullanım:
    python fetch_tanzil.py --i-agree-to-tanzil-terms

Önce Tanzil kullanım şartlarını okuyun:
    https://tanzil.net/download/
    https://tanzil.net/docs/Text_License

Ham kaynak dosyaları içerik olarak değiştirilmez. `txt-2` biçimi sûre|ayet|metin
alanlarını taşıdığı için doğrulama ve ayet bazlı indeksleme için tercih edilmiştir.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE_URL = "https://tanzil.net/pub/download/index.php"
METADATA_URL = "https://tanzil.net/res/text/metadata/quran-data.xml"
ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "01_raw" / "tanzil"

SOURCES = {
    "quran-uthmani.txt": {
        "quranType": "uthmani",
        "outType": "txt-2",
        "agree": "true",
    },
    "quran-simple-clean.txt": {
        "quranType": "simple-clean",
        "outType": "txt-2",
        "agree": "true",
    },
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def get_bytes(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "quran-offline-corpus/1.0"})
    with urlopen(request, timeout=60) as response:
        return response.read()


def save_download(name: str, url: str) -> dict[str, object]:
    target = RAW_DIR / name
    data = get_bytes(url)
    target.write_bytes(data)
    return {
        "file": str(target.relative_to(ROOT)),
        "source_url": url,
        "bytes": len(data),
        "sha256": sha256(target),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--i-agree-to-tanzil-terms",
        action="store_true",
        help="Tanzil kullanım şartlarını okuyup kabul ettiğinizi belirtir.",
    )
    args = parser.parse_args()
    if not args.i_agree_to_tanzil_terms:
        raise SystemExit(
            "İndirme yapılmadı. Önce Tanzil şartlarını okuyun ve "
            "--i-agree-to-tanzil-terms parametresini kullanın."
        )

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, object] = {
        "provider": "Tanzil Project",
        "declared_text_version": "1.1",
        "declared_metadata_version": "1.0",
        "license": "Creative Commons Attribution 3.0; Quran text must remain verbatim",
        "download_page": "https://tanzil.net/download/",
        "files": [],
    }

    files = manifest["files"]
    assert isinstance(files, list)

    for name, params in SOURCES.items():
        url = f"{BASE_URL}?{urlencode(params)}"
        print(f"Downloading {name} ...")
        files.append(save_download(name, url))

    print("Downloading quran-data.xml ...")
    files.append(save_download("quran-data.xml", METADATA_URL))

    manifest_path = RAW_DIR / "manifest.local.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Manifest: {manifest_path}")
    print("Next: python 08_scripts/validate_tanzil.py")


if __name__ == "__main__":
    main()
