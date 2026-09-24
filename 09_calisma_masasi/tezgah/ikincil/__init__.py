"""İkincil katmanlar (Aşama 5): Lane ve Sâmî — yalnız hipotez kaynağı, delil değil.

Zincir tek yönlüdür (CLAUDE.md §2.1): dış katman hipotez üretir, korpus sınar, sonuç korpus
bulgusuyla yazılır. Bu paketteki her çıktı satırı "[hipotez]" etiketi taşır.
"""

from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen

from .. import veri

HIPOTEZ = "[hipotez]"


def etiketle(satirlar: list[str], ek: str = "") -> list[str]:
    """Her boş olmayan satırın başına hipotez etiketi koyar."""
    etiket = f"[hipotez{' · ' + ek if ek else ''}]"
    return [f"{etiket} {s}" if s.strip() else s for s in satirlar]


def indir(url: str, beklenen_sha: str) -> bytes:
    istek = Request(url, headers={"User-Agent": "quran-offline-corpus/1.0"})
    with urlopen(istek, timeout=300) as yanit:
        ham = yanit.read()
    sha = hashlib.sha256(ham).hexdigest()
    if sha != beklenen_sha:
        raise veri.VeriHatasi(f"İndirilen dosyanın sha256'sı beklenenden farklı: {url}\n  beklenen: {beklenen_sha}\n  bulunan : {sha}")
    return ham


def manifest_yaz(yol: Path, bilgi: dict) -> None:
    bilgi = {**bilgi, "fetched": date.today().isoformat()}
    yol.write_text(json.dumps(bilgi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def arapca_latin_metin(arapca: str) -> str:
    """Harekeli Arapça kelimeyi okunuş kurallarıyla Latinleştirir; kurallar tutmazsa Buckwalter'a düşer."""
    from .. import okunus
    try:
        birimler, belirsiz = okunus.kelime_oku(arapca, ayet_basi=True)
        if not belirsiz:
            return okunus._metin(birimler)
    except okunus.BilinmeyenKarakter:
        pass
    bw = "".join(veri.ARAPCA_BW.get(c, "") for c in arapca)
    return f"bw:{bw}" if bw else ""
