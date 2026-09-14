#!/usr/bin/env python3
"""Açık Kuran API'den yalnız kök metadata'sını snapshot eder.

Bu script meal/ayet verisini topluca kopyalamaz. Amaç Açık Kuran kök sözlüğünü
QAC'a ikincil çapraz kontrol katmanı olarak offline kullanılabilir hale getirmektir.

Kullanım:
    python 08_scripts/fetch_acikkuran_roots.py --i-accept-acikkuran-license
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "04_lexicons" / "acikkuran"
OUT_FILE = OUT_DIR / "roots.jsonl"
MANIFEST = OUT_DIR / "manifest.local.json"
BASE = "https://api.acikkuran.com"


def get_json(path: str) -> dict:
    req = Request(
        BASE + path,
        headers={"User-Agent": "quran-offline-corpus/1.0 (+https://github.com/meditao/quran-offline-corpus)"},
    )
    with urlopen(req, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--i-accept-acikkuran-license",
        action="store_true",
        help="Açık Kuran API projesinin CC BY-NC-SA 4.0 lisansını kabul ettiğinizi belirtir.",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.20,
        help="API istekleri arasındaki saniye; varsayılan 0.20.",
    )
    args = parser.parse_args()
    if not args.i_accept_acikkuran_license:
        raise SystemExit(
            "Snapshot alınmadı. Önce https://github.com/acik-kuran/acikkuran-api lisansını okuyun; "
            "sonra --i-accept-acikkuran-license kullanın."
        )

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    rootchars_payload = get_json("/rootchars")
    rootchars = rootchars_payload.get("data")
    if not isinstance(rootchars, list):
        raise RuntimeError(f"Beklenmeyen /rootchars yanıtı: {rootchars_payload}")

    # Önce bütün root latin anahtarlarını rootchar gruplarından keşfet.
    roots_basic: dict[str, dict] = {}
    for rc in rootchars:
        rc_id = rc["id"]
        payload = get_json(f"/rootchar/{rc_id}")
        items = payload.get("data")
        if not isinstance(items, list):
            raise RuntimeError(f"Beklenmeyen /rootchar/{rc_id} yanıtı: {payload}")
        for item in items:
            latin = item.get("latin")
            if latin:
                roots_basic[latin] = item
        time.sleep(max(args.delay, 0.0))

    # Sonra her kökün anlam/transkripsiyon/varyant metadata'sını al.
    records: list[dict] = []
    for i, latin in enumerate(sorted(roots_basic), 1):
        payload = get_json(f"/root/latin/{quote(latin, safe='')}")
        data = payload.get("data")
        if not isinstance(data, dict) or data.get("error"):
            raise RuntimeError(f"Kök alınamadı {latin}: {payload}")
        records.append(data)
        if i % 100 == 0:
            print(f"Fetched {i}/{len(roots_basic)} roots")
        time.sleep(max(args.delay, 0.0))

    # Deterministik sıralama ve newline-delimited JSON.
    records.sort(key=lambda x: (str(x.get("latin", "")), int(x.get("id", 0))))
    with OUT_FILE.open("w", encoding="utf-8", newline="\n") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")

    manifest = {
        "provider": "Açık Kuran",
        "project_repo": "https://github.com/acik-kuran/acikkuran-api",
        "api_base": BASE,
        "license": "CC BY-NC-SA 4.0 (API project license; underlying fields remain provenance-sensitive)",
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "rootchars_endpoint": "/rootchars",
        "rootchar_endpoint_pattern": "/rootchar/{id}",
        "root_detail_endpoint_pattern": "/root/latin/{latin}",
        "records": len(records),
        "output": str(OUT_FILE.relative_to(ROOT)),
        "sha256": sha256(OUT_FILE),
        "note": "Auxiliary root metadata only; not a canonical Quran text or final etymological authority.",
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Roots: {len(records):,}")
    print(f"Saved: {OUT_FILE.relative_to(ROOT)}")
    print(f"SHA-256: {manifest['sha256']}")


if __name__ == "__main__":
    main()
