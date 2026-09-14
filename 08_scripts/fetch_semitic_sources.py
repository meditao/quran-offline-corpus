#!/usr/bin/env python3
"""CC lisanslı, commit'e sabitlenmiş Sami dil kaynaklarını vendor klasörüne indirir.

Kaynak kilitleri:
    04_lexicons/semitic/VENDOR_LOCK.json

Bu script CAL veya SEDRA'yı toplu olarak indirmez; onların yeniden dağıtım koşulları
ayrıca teyit edilmeden yalnız online referans olarak kullanılır.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "04_lexicons" / "semitic" / "VENDOR_LOCK.json"


def run(*args: str, cwd: Path | None = None) -> None:
    print("+", " ".join(args))
    subprocess.run(args, cwd=cwd, check=True)


def main() -> None:
    data = json.loads(LOCK.read_text(encoding="utf-8"))
    for source in data["sources"]:
        target = ROOT / source["target"]
        if target.exists():
            shutil.rmtree(target)
        target.parent.mkdir(parents=True, exist_ok=True)

        run("git", "clone", "--no-checkout", "--filter=blob:none", source["repo"], str(target))
        run("git", "fetch", "--depth", "1", "origin", source["ref"], cwd=target)
        run("git", "checkout", "--detach", source["ref"], cwd=target)

        actual = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=target, text=True
        ).strip()
        if actual != source["ref"]:
            raise SystemExit(
                f"Commit mismatch for {source['name']}: {actual} != {source['ref']}"
            )
        print(f"OK: {source['name']} @ {actual}")


if __name__ == "__main__":
    main()
