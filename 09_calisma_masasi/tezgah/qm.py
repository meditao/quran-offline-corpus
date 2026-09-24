"""İkinci annotation katmanı: mustafa0x/quran-morphology (Aşama 4) — çapraz kontrol, delil değil.

quran-morphology, QAC v0.4'ün çatalıdır: Buckwalter yerine Arapça harf, düzeltilmiş kök/lemma,
farklı segmentasyon. Kelime konumu QAC ile birebir aynıdır; segment ve kök envanteri farklıdır.

Lisans: depoda lisans dosyası yok; QAC v0.4 kullanım şartı değiştirilmiş kopyayı yasaklar.
Bu yüzden veri depoya işlenmez: 09_calisma_masasi/yerel/quran-morphology/ altında, commit ve
sha256 ile sabitlenmiş olarak tutulur (CLAUDE.md §9).

Kök karşılaştırması hemze yazımı nötrlenerek yapılır: ء أ إ آ ؤ ئ ٱ ا -> tek sembol. QAC kök
alanında hemze hep "A" (ا) yazılır; quran-morphology hemzeyi yerine göre أ/ء/ؤ/ئ yazar.

Dosya LF satır sonludur; QAC dosyası CRLF'dir. İki ayrıştırıcı da satır sonunu \\r\\n olarak soyar
(1.651/1.642 tarihsel artefaktı CR kaynaklıydı: 03_indices/audits/qac_1651_vs_1642.md).
"""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date
from functools import lru_cache
from pathlib import Path
from urllib.request import Request, urlopen

from . import veri
from .harf import HARF_LATIN

MASA = Path(__file__).resolve().parents[1]
QM_DIZINI = MASA / "yerel" / "quran-morphology"
QM_YOLU = QM_DIZINI / "quran-morphology.txt"
QM_MANIFEST = QM_DIZINI / "manifest.json"
QM_DEPO = "mustafa0x/quran-morphology"
QM_COMMIT = "8f38b39016824284f9ed16ae15069ff9102c4acf"
QM_SHA256 = "742bfac59941b2cb09736d5b7aae694af50792261fb8450cbf6afafcc340645f"
QM_URL = f"https://raw.githubusercontent.com/{QM_DEPO}/{QM_COMMIT}/quran-morphology.txt"
KAYNAK_ADI = "quran-morphology"

HEMZE_BICIMLERI = set("ءأإآؤئٱا")


def notr(kok_arapca: str) -> str:
    """Hemze yazımını nötrler: bütün hemze/elif biçimleri -> ء."""
    return "".join("ء" if c in HEMZE_BICIMLERI else c for c in kok_arapca)


def qac_notr(kok_bw: str) -> str:
    return notr(veri.bw_arapca(kok_bw))


def arapca_latin(kok_arapca: str) -> str:
    """quran-morphology kökünü ortak harf tablosuyla ayrık Latin yazar (ör. طمءن -> ṭ-m-ʾ-n)."""
    return "-".join(HARF_LATIN["ء"] if c in HEMZE_BICIMLERI else HARF_LATIN.get(c, c) for c in kok_arapca)


@dataclass
class QmKorpus:
    sha256: str
    segment: int = 0
    kokler: dict[tuple[int, int, int], set[str]] = field(default_factory=lambda: defaultdict(set))
    segment_sayisi: dict[tuple[int, int, int], int] = field(default_factory=lambda: defaultdict(int))
    ham_kokler: set[str] = field(default_factory=set)

    @property
    def kelimeler(self) -> set[tuple[int, int, int]]:
        return set(self.segment_sayisi)

    @property
    def veri_izi(self) -> str:
        return self.sha256[:12]

    def kok_konumlari(self) -> dict[str, list[tuple[int, int, int]]]:
        d: dict[str, list[tuple[int, int, int]]] = defaultdict(list)
        for konum in sorted(self.kokler):
            for k in self.kokler[konum]:
                d[notr(k)].append(konum)
        return d

    def notr_kokler(self, konum: tuple[int, int, int]) -> set[str]:
        return {notr(k) for k in self.kokler.get(konum, set())}


def ayristir(yol: Path) -> QmKorpus:
    kor = QmKorpus(sha256=veri.sha256(yol))
    with yol.open("r", encoding="utf-8-sig", newline="") as f:
        for no, ham in enumerate(f, 1):
            satir = ham.rstrip("\r\n")
            if not satir:
                continue
            alan = satir.split("\t")
            if len(alan) != 4:
                raise veri.VeriHatasi(f"quran-morphology satır {no}: 4 TSV alanı bekleniyordu")
            s, a, k, _ = map(int, alan[0].split(":"))
            kor.segment += 1
            kor.segment_sayisi[(s, a, k)] += 1
            for oz in alan[3].split("|"):
                if oz.startswith("ROOT:"):
                    kor.kokler[(s, a, k)].add(oz[5:])
                    kor.ham_kokler.add(oz[5:])
    return kor


@lru_cache(maxsize=1)
def korpus() -> QmKorpus | None:
    if not QM_YOLU.exists():
        return None
    gercek = veri.sha256(QM_YOLU)
    if gercek != QM_SHA256:
        raise veri.VeriHatasi(f"quran-morphology sha256 uyuşmuyor.\n  beklenen: {QM_SHA256}\n  bulunan : {gercek}")
    return ayristir(QM_YOLU)


def kur() -> dict[str, object]:
    if QM_YOLU.exists():
        raise FileExistsError(f"quran-morphology zaten kurulu: {QM_YOLU}")
    istek = Request(QM_URL, headers={"User-Agent": "quran-offline-corpus/1.0"})
    with urlopen(istek, timeout=120) as yanit:
        ham = yanit.read()
    import hashlib
    sha = hashlib.sha256(ham).hexdigest()
    if sha != QM_SHA256:
        raise veri.VeriHatasi(f"İndirilen quran-morphology sha256 beklenenden farklı: {sha}")
    QM_DIZINI.mkdir(parents=True, exist_ok=True)
    QM_YOLU.write_bytes(ham)
    bilgi = {
        "file": QM_YOLU.name, "depo": QM_DEPO, "commit": QM_COMMIT, "source_url": QM_URL,
        "bytes": len(ham), "sha256": sha, "fetched": date.today().isoformat(),
        "lisans": "depoda lisans dosyası yok; QAC v0.4 çatalı (QAC şartı değiştirilmiş kopyayı yasaklar) — "
                  "depoya işlenmez (CLAUDE.md §9)",
        "statu": "ikinci annotation katmanı — çapraz kontrol, delil değil",
    }
    QM_MANIFEST.write_text(json.dumps(bilgi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return bilgi


# --- --capraz ----------------------------------------------------------------

def capraz(kor: veri.Korpus, kok_bw: str) -> tuple[list[str], dict]:
    """Bir kökün iki korpustaki sonucu: ayrı tablolar + kök ataması farklı konumlar."""
    from .tara import GirdiHatasi, _tablo
    q = korpus()
    if q is None:
        raise GirdiHatasi("quran-morphology kurulu değil (python -m tezgah kur quran-morphology).")
    anahtar = qac_notr(kok_bw)
    qac_konum = {k.anahtar for k in kor.kok_kelimeleri.get(kok_bw, [])}
    qm_konum = set(q.kok_konumlari().get(anahtar, []))
    qm_ham = sorted({k for konum in qm_konum for k in q.kokler[konum] if notr(k) == anahtar})

    def o(konumlar: set[tuple[int, int, int]]) -> dict[str, int]:
        return {"kelime konumu": len(konumlar), "ayet": len({(s, a) for s, a, _ in konumlar}),
                "sûre": len({s for s, _, _ in konumlar})}

    oq, om = o(qac_konum), o(qm_konum)
    satirlar = [
        "",
        "=" * 60,
        "Çapraz kontrol — ikinci annotation: quran-morphology (mustafa0x, commit "
        f"{QM_COMMIT[:7]}; delil değil). Tablolar ayrıdır, sayılar toplanmaz.",
        "Kök eşleşmesi hemze yazımı nötrlenerek yapıldı.",
        "",
        f"QAC v0.4 — kök {kok_bw} ({veri.kok_latin(kok_bw)}):",
        *_tablo(["birim", "sayı"], [[k, v] for k, v in oq.items()], sag={1}),
        "",
        f"quran-morphology — kök {' / '.join(arapca_latin(k) for k in qm_ham) or '(bu kök yok)'}:",
        *_tablo(["birim", "sayı"], [[k, v] for k, v in om.items()], sag={1}),
        "",
        "Not: iki sayının aynı çıkması doğrulama sayılmaz; kök atamasının farklı çıktığı yerler aşağıdadır.",
    ]
    farkli = sorted(qac_konum ^ qm_konum)
    satirlar.append(f"Kök ataması farklı kelime konumları: {len(farkli)}")
    if farkli:
        tablo = []
        for konum in farkli:
            qac_k = sorted(kor.kelimeler[_kelime_sirasi(kor)[konum]].kokler)
            qm_k = sorted(q.kokler.get(konum, set()))
            tablo.append([f"{konum[0]}:{konum[1]}:{konum[2]}",
                          ";".join(f"{k} ({veri.kok_latin(k)})" for k in qac_k) or "—",
                          ";".join(arapca_latin(k) for k in qm_k) or "—"])
        satirlar += _tablo(["konum", "QAC kökü", "quran-morphology kökü"], tablo)
    return satirlar, {"qac": oq, "qm": om, "farkli": len(farkli)}


@lru_cache(maxsize=1)
def _kelime_sirasi_onbellek() -> dict[tuple[int, int, int], int]:
    return {k.anahtar: i for i, k in enumerate(veri.korpus().kelimeler)}


def _kelime_sirasi(kor: veri.Korpus) -> dict[tuple[int, int, int], int]:
    return _kelime_sirasi_onbellek() if kor is veri.korpus() else {k.anahtar: i for i, k in enumerate(kor.kelimeler)}


# --- sayısı farklı kökler için uyarı (depodaki audit dosyalarından; yerel veri gerekmez) ----------

AUDIT = veri.DEPO / "03_indices" / "audits"


@lru_cache(maxsize=1)
def _audit() -> tuple[dict[str, dict], list[dict]] | None:
    import csv
    sayilar_yolu = AUDIT / "qac_quranmorphology_kok_sayilari.tsv"
    farklar_yolu = AUDIT / "qac_quranmorphology_kok_farklari.tsv"
    if not (sayilar_yolu.exists() and farklar_yolu.exists()):
        return None
    with sayilar_yolu.open(encoding="utf-8", newline="") as f:
        sayilar = {r["kok_notr_latin"]: r for r in csv.DictReader(f, delimiter="\t")}
    with farklar_yolu.open(encoding="utf-8", newline="") as f:
        farklar = list(csv.DictReader(f, delimiter="\t"))
    return sayilar, farklar


def _kume(deger: str) -> list[str]:
    return [x for x in deger.split(";") if x]


def sayi_farki_uyarisi(kor: veri.Korpus, kok_bw: str | None = None, notr_anahtar: str | None = None) -> str | None:
    """Kök iki korpusta farklı sayıda kelime konumunda geçiyorsa uyarı metni, yoksa None.

    Kaynak: 03_indices/audits/qac_quranmorphology_kok_{sayilari,farklari}.tsv (Aşama 4 raporu).
    """
    a = _audit()
    if a is None:
        return None
    sayilar, farklar = a
    anahtar = notr_anahtar if notr_anahtar is not None else qac_notr(kok_bw)
    latin = arapca_latin(anahtar)
    satir = sayilar.get(latin)
    if satir is None:
        return None
    konum_lemma = {k.konum: ";".join(sorted(k.lemmalar)) for k in kor.kelimeler}
    gelen: dict[str, list[str]] = {}    # qm bu köke bağlar, QAC bağlamaz -> QAC kökü
    giden: dict[str, list[str]] = {}    # QAC bu köke bağlar, qm bağlamaz -> qm kökü
    for r in farklar:
        qm_var = anahtar in {notr(x) for x in _kume(r["qm_kok"])}
        qac_var = anahtar in {qac_notr(x) for x in _kume(r["qac_kok_bw"])}
        if qm_var and not qac_var:
            hedef = ";".join(f"{x} ({veri.kok_latin(x)})" for x in _kume(r["qac_kok_bw"])) or "köksüz"
            gelen.setdefault(hedef, []).append(r["konum"])
        elif qac_var and not qm_var:
            hedef = ";".join(arapca_latin(x) for x in _kume(r["qm_kok"])) or "köksüz"
            giden.setdefault(hedef, []).append(r["konum"])
    parcalar = [f"UYARI (çapraz kontrol — quran-morphology, delil değil): {latin} kökü iki korpusta farklı sayıda "
                f"kelime konumunda geçer: QAC {satir['qac_kelime_konumu']}, quran-morphology {satir['qm_kelime_konumu']}."]
    for hedef, konumlar in sorted(gelen.items(), key=lambda x: -len(x[1])):
        lemmalar = sorted({konum_lemma.get(k, "") for k in konumlar} - {""})
        lem = f" (QAC lemma: {', '.join(lemmalar[:3])})" if lemmalar else ""
        bag = "köksüz bırakır" if hedef == "köksüz" else f"{hedef} köküne bağlar"
        parcalar.append(f"  quran-morphology {len(konumlar)} konumu bu köke bağlar; QAC bu konumları {bag}{lem} — "
                        f"bu {len(konumlar)} konum QAC sonucunda yok.")
    for hedef, konumlar in sorted(giden.items(), key=lambda x: -len(x[1])):
        bag = "köksüz bırakır" if hedef == "köksüz" else f"{hedef} köküne bağlar"
        parcalar.append(f"  QAC'ın bu köke bağladığı {len(konumlar)} konumu quran-morphology {bag}.")
    parcalar.append("  Ayrıntı: --capraz; rapor: 03_indices/audits/qac_quranmorphology.md")
    return "\n".join(parcalar)
