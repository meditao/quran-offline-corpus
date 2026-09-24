"""Kayıt satırı (CLAUDE.md §8).

Her sorgu çıktısının sonunda şu blok bulunur:

    Kaynak      : QAC v0.4
    Sayım birimi: kelime konumu | ayet | sûre
    Sorgu       : python -m tezgah kok Slw
    Veri izi    : a1d129238153
    Durum       : çalıştırıldı

Blok yalnız biçimlendirir; sayı üretmez. Veri izi, sorgunun gerçekten
okuduğu dosyanın sha256'sından gelir.
"""

from __future__ import annotations

import shlex
import sys
from dataclasses import dataclass, field

CALISTIRILDI = "çalıştırıldı"
CALISTIRILMADI = "çalıştırılmadı"

GECERLI_BIRIMLER = ("kelime konumu", "segment", "ayet", "sûre", "kök", "atıf geçişi")


def komut_metni(argv: list[str] | None = None) -> str:
    """Çalıştırılan tam komutu yeniden kurar."""
    args = sys.argv[1:] if argv is None else argv
    return "python -m tezgah " + shlex.join(args) if args else "python -m tezgah"


@dataclass
class Kayit:
    sorgu: str
    birimler: list[str] = field(default_factory=list)
    kaynaklar: list[str] = field(default_factory=lambda: ["QAC v0.4"])
    veri_izi: str = "—"
    durum: str = CALISTIRILDI
    sebep: str = ""

    def __post_init__(self) -> None:
        for b in self.birimler:
            if b not in GECERLI_BIRIMLER:
                raise ValueError(f"Geçersiz sayım birimi: {b!r}")

    def satirlar(self) -> list[str]:
        durum = self.durum if not self.sebep else f"{self.durum} ({self.sebep})"
        return [
            f"Kaynak      : {' | '.join(self.kaynaklar)}",
            f"Sayım birimi: {' | '.join(self.birimler) if self.birimler else '—'}",
            f"Sorgu       : {self.sorgu}",
            f"Veri izi    : {self.veri_izi}",
            f"Durum       : {durum}",
        ]

    def metin(self) -> str:
        return "\n".join(["-" * 60, *self.satirlar()])

    def sozluk(self) -> dict[str, object]:
        return {
            "kaynak": list(self.kaynaklar),
            "sayim_birimi": list(self.birimler),
            "sorgu": self.sorgu,
            "veri_izi": self.veri_izi,
            "durum": self.durum,
            "sebep": self.sebep,
        }
