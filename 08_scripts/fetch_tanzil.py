#!/usr/bin/env python3
"""Tanzil Quran Text v1.1 kaynaklarını indir ve temel bütünlük kaydı üret.

Kullanım:
    python fetch_tanzil.py --i-agree-to-tanzil-terms

Tanzil kullanım şartlarını önce okuyun:
    https://tanzil.net/download/
    https://tanzil.net/docs/Text_License

Bu script ham dosyanın içeriğini değiştirmez.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE_URL = "https://tanzil.net/pub/download/index.php"
ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "01_raw" / "tanzil"

SOURCES = {
    "quran-uthmani.txt": {
        "quranType": "uthmani",
        "outType": "txt",
        "agree": "true",
    },
    "quran-simple-clean.txt": {
        "quranType": "simple-clean",
        "outType": "txt",
        "agree": "true",
    },
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download(name: str, params: dict[str, str]) -> dict[str, object]:
    url = f"{BASE_URL}?{urlencode(params)}"
    target = RAW_DIR / name
    request = Request(url, headers={"User-Agent": "quran-offline-corpus/1.0"})
    with urlopen(request, timeout=60) as response:
        data = response.read()
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
    manifest = {
        "provider": "Tanzil Project",
        "declared_version": "1.1",
        "license": "Creative Commons Attribution 3.0; verbatim text must not be changed",
        "download_page": "https://tanzil.net/download/",
        "files": [],
    }

    for name, params in SOURCES.items():
        print(f"Downloading {name} ...")
        manifest["files"].append(download(name, params))

    manifest_path = RAW_DIR / "manifest.local.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
