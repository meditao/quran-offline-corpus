#!/usr/bin/env python3
"""QAC v0.4'ün doğrulanmış birebir kamu kopyasını indirir.

Kanonik kaynak: https://corpus.quran.com/download/

Resmî indirme sayfası e-posta adımı içerdiği için bu script, QAC şartlarının
izin verdiği verbatim redistribüsyon kopyalarından birini kullanır. İki bağımsız
GitHub kopyasının aynı Git blob SHA'sını taşıdığı doğrulanmıştır.

Kullanım:
    python 08_scripts/fetch_qac.py --i-accept-qac-terms
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "02_morphology" / "qac" / "quranic-corpus-morphology-0.4.txt"

EXPECTED_GIT_BLOB_SHA1 = "b91cec6e95d5e0306550b4aedacc7380dc71152a"
MIRRORS = [
    "https://raw.githubusercontent.com/bnjasim/quranic-corpus/master/quranic-corpus-morphology-0.4.txt",
    "https://raw.githubusercontent.com/taziksh/quran-frequencies/main/data/quranic-corpus-morphology-0.4.txt",
]


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def download(url: str) -> bytes:
    req = Request(url, headers={"User-Agent": "quran-offline-corpus/1.0"})
    with urlopen(req, timeout=90) as response:
        return response.read()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--i-accept-qac-terms",
        action="store_true",
        help="QAC v0.4 dosyasındaki kullanım şartlarını kabul ettiğinizi belirtir.",
    )
    args = parser.parse_args()
    if not args.i_accept_qac_terms:
        raise SystemExit(
            "İndirme yapılmadı. Önce https://corpus.quran.com/download/ şartlarını okuyun; "
            "sonra --i-accept-qac-terms kullanın."
        )

    errors: list[str] = []
    for url in MIRRORS:
        try:
            print(f"Trying {url}")
            data = download(url)
            blob = git_blob_sha1(data)
            if blob != EXPECTED_GIT_BLOB_SHA1:
                errors.append(f"{url}: blob SHA mismatch {blob}")
                continue

            # Telif bloğunun da gerçekten içerikte bulunduğunu doğrula.
            text_head = data[:5000].decode("utf-8-sig", errors="strict")
            required = [
                "Quranic Arabic Corpus (morphology, version 0.4)",
                "Copyright (C) 2011 Kais Dukes",
                "CHANGING IT IS NOT ALLOWED",
            ]
            if not all(item in text_head for item in required):
                errors.append(f"{url}: required copyright/version header missing")
                continue

            TARGET.parent.mkdir(parents=True, exist_ok=True)
            TARGET.write_bytes(data)
            print(f"Saved: {TARGET.relative_to(ROOT)}")
            print(f"Git blob SHA-1: {blob}")
            print(f"SHA-256: {sha256(data)}")
            print("Next: python 08_scripts/validate_qac.py")
            return
        except Exception as exc:
            errors.append(f"{url}: {exc}")

    raise SystemExit("QAC indirilemedi / doğrulanamadı:\n- " + "\n- ".join(errors))


if __name__ == "__main__":
    main()
