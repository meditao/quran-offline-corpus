"""OpenITI mARkdown metnini sözlük maddelerine ayırır (İbn Fâris Mekâyîs, Râgıb Müfredât).

`klasik.kur()` bunu çağırır; tek başına çalıştırılmaz. Çıktı hipotez katmanıdır (CLAUDE.md §2.1).

İki eser:
  ibnfaris  Mu'cemü Mekâyîsi'l-lüga — İbn Fâris (ö. 395/1004), thk. A. M. Hârûn
  ragib     el-Müfredât fî garîbi'l-Kur'ân — Râgıb el-İsfahânî, thk. S. A. Dâvûdî

Ezberden kurulamayacak ayrıştırma kuralları (dijital metnin kusurlarından çıkar):
  1. '~~' satırı önceki satırın devamıdır.
  2. '### |' başlıklarının bir kısmı sahtedir: dönüşüm kelimenin ORTASINDA satır kesip parçayı
     başlık yapmıştır ("و" + "### | اح" + "د" = "واحد"). Geçerli başlık değilse metne
     boşluksuz geri katılır.
  3. Geçerli başlık, içinde bulunduğu "kitab"ın harfiyle başlamak zorundadır.
  4. (yalnız Râgıb) Başlık bölünebilir: "### | أخ" + sonraki satır "ذ" = أخذ.
     İbn Fâris'e uygulanmaz: "(ليل)" + "ال" -> "ليلال" olur, madde kaybolur.
  5. (yalnız Râgıb) Geçerli başlıklar KAYMIŞTIR: başlık, maddenin asıl tanım satırından birkaç
     paragraf, bazen iki madde önce durur. Bu yüzden madde sınırı başlığın yerinden değil,
     başlıktan sonraki ilk TANIM satırından ("العلم: ...", "أصل ...", "العقل يقال ...") alınır.
     Önceki satır noktalamasız bir harfle bitiyorsa başlık metni o cümlenin parçasıdır ve
     metne geri katılır ("مترشحة ل" + "فعل" + "من الأفعال").

Veri üzerinde ölçülen sonuç: İbn Fâris 4.649 madde, Râgıb 1.662 madde (klasik.kur denetler).
"""

from __future__ import annotations

import re

TASH = re.compile("[\u0610-\u061a\u064b-\u065f\u0670\u06d6-\u06ed\u0640]")
HARF = "ء-ي"
PENCERE = 40          # kural 5: tanım satırı başlıktan en fazla bu kadar paragraf sonra

HARF_ADI = {
    "الهمزة": "ا", "الألف": "ا", "الالف": "ا", "الباء": "ب", "التاء": "ت", "الثاء": "ث",
    "الجيم": "ج", "الحاء": "ح", "الخاء": "خ", "الدال": "د", "الذال": "ذ", "الراء": "ر",
    "الزاء": "ز", "الزاي": "ز", "السين": "س", "الشين": "ش", "الصاد": "ص", "الضاد": "ض",
    "الطاء": "ط", "الظاء": "ظ", "العين": "ع", "الغين": "غ", "الفاء": "ف", "القاف": "ق",
    "الكاف": "ك", "اللام": "ل", "الميم": "م", "النون": "ن", "الهاء": "ه", "الواو": "و",
    "الياء": "ي",
}


def norm(s: str | None) -> str:
    """Hareke at, hemzeyi elife, ى'yi ي'ye, ة'yi ه'ye indir."""
    s = TASH.sub("", s or "")
    return re.sub("[أإآٱءؤئ]", "ا", s).replace("ى", "ي").replace("ة", "ه")


def _kitab_harfi(baslik: str) -> str | None:
    m = re.search(r"كتاب\s+(\S+)", baslik)
    return HARF_ADI.get(m.group(1).strip("[]()= ")) if m else None


def _harfle_bitiyor(s: str | None) -> bool:
    s = re.sub(r"(«\d+»|\s)+$", "", s or "")
    return bool(s) and re.match("[%s]" % HARF, s[-1]) is not None


def _ilk_kelime(metin: str) -> str:
    return norm(re.split(r"[\s،:,.]", metin.strip(), maxsplit=1)[0])


def _alt_dizi(kok: str, kelime: str) -> bool:
    it = iter(kelime)
    return all(h in it for h in kok)


def _sert(kok: str) -> str:
    """Kökün yüzeyde kaybolmayan harfleri: ilk harf her zaman kalır; sonraki illetli harfler
    (و ي ى ve hemzesiz elif) atılır. Hemze gerçek ünsüzdür, kalır ve 'ا' olarak yazılır
    (أم -> ام, وطأ -> وطا, قول -> قل)."""
    k = TASH.sub("", kok)
    k = re.sub("[أإآٱءؤئ]", "\x00", k)               # hemzeyi işaretle
    sert = k[0] + "".join(h for h in k[1:] if h not in "ويىا")
    sert = sert.replace("\x00", "ا").replace("ة", "ه")
    return sert if len(sert) >= 2 else norm(kok)


def _madde_gibi_basliyor(metin: str, kok: str) -> bool:
    """Yerinde duran başlık: madde kökün kendisiyle, 'أصل', 'قال' ile açılır."""
    ilk = _ilk_kelime(metin)
    if ilk.startswith(("اصل", "قال", "قوله", "وقوله", "يقال")):
        return True
    govde = re.sub("^(وال|ال|و)", "", ilk)
    sert = _sert(kok)
    return len(sert) >= 2 and _alt_dizi(sert[:2], govde)


def _tanim_satiri(metin: str, kok: str) -> bool:
    """Kaymış başlığın asıl yeri: 'أصل <kök>...' ile ya da ilk kelimesi kökün sert harflerini
    sırasıyla taşıyan ve 'ال' ile başlayan / iki noktayla devam eden / yalnız kökten ibaret
    satır ('العلم: ...', 'العقل يقال ...')."""
    m = metin.strip()
    kel = [norm(k) for k in re.split(r"[\s،:,.]+", m) if k][:3]
    if not kel:
        return False
    sert = _sert(kok)
    if len(sert) < 2:
        return False
    if kel[0].startswith("اصل"):
        return len(kel) > 1 and _alt_dizi(sert, re.sub("^(وال|ال)", "", kel[1]))
    govde = re.sub("^(وال|ال)", "", kel[0])
    if not _alt_dizi(sert, govde):
        return False
    return kel[0].startswith("ال") or ":" in m[:25] or norm(m) == kel[0]


def _akis(yol, eser: str):
    """Metni paragraf akışına ve başlık listesine çevirir (kural 1-4)."""
    with open(yol, encoding="utf-8") as f:
        t = f.read().lstrip("﻿")
    if "#META#Header#End#" in t:
        t = t.split("#META#Header#End#", 1)[1]
    t = re.sub(r"\n~~", " ", t)                                   # kural 1
    P, S, B = [], [], []          # paragraflar, sayfaları, başlıklar
    harf, sayfa, on_bolum = None, None, True
    bitisik = False               # sonraki paragraf öncekiyle boşluksuz birleşir
    son_baslik = None             # kural 4 için

    def ekle(metin: str) -> None:
        nonlocal bitisik
        if bitisik and P:
            P[-1] += metin
        else:
            P.append(metin)
            S.append(sayfa)
        bitisik = False

    for ham in t.split("\n"):
        for m in re.finditer(r"PageV(\d+)P(\d+)", ham):
            sayfa = "%d/%d" % (int(m.group(1)), int(m.group(2)))
        satir = re.sub(r"\s*PageV\d+P\d+\s*", " ", ham)
        satir = re.sub(r"<[^>]+>", "", satir)
        satir = re.sub(r"\bms\d+\b", "", satir).strip()
        if not satir:
            continue
        if satir.startswith("### |"):
            b = satir[5:].strip()
            if "فهارس" in b or "فهرس" in b:
                break                                             # fihrist
            kh = _kitab_harfi(b)
            if kh:
                harf, on_bolum, son_baslik = kh, False, None
                continue
            if on_bolum or not b or b.startswith(("[", "باب")):
                continue
            if eser == "ibnfaris":
                m = re.fullmatch(r"\(\s*\[?([%s ]{2,6})\]?\)\s*:?" % HARF, b)
                aday = m.group(1).replace(" ", "") if m else None
            else:
                aday = b if re.fullmatch("[%s]{2,6}" % HARF, b) else None
                if aday and aday.startswith("ال") and len(aday) >= 4 and harf \
                        and norm(aday[2:])[0] == harf:
                    aday = aday[2:]                               # "اليم" -> يم
            if aday and harf and norm(aday)[0] == harf:           # kural 3
                son_baslik = dict(baslik=aday, ham=b, poz=len(P), sayfa=sayfa,
                                  harfle=bool(P) and _harfle_bitiyor(P[-1]))
                B.append(son_baslik)
            else:                                                 # kural 2
                if P:
                    P[-1] += b
                    bitisik = True
            continue
        if satir.startswith("#"):
            metin = satir.lstrip("#").strip()
            if not metin:
                continue
            # kural 4: "أخ" + "ذ"
            if eser == "ragib" and son_baslik and son_baslik["poz"] == len(P) \
                    and not bitisik and metin != "ال" \
                    and re.fullmatch("[%s]{1,2}" % HARF, metin) \
                    and len(son_baslik["baslik"]) + len(metin) <= 5:
                son_baslik["baslik"] += metin
                continue
            ekle(metin)
    for b in B:
        b["kok"] = norm(b["baslik"])
    return P, S, B


def _ara(onceki: str) -> str:
    """Kesik kelime: son kelime 1-2 harfse boşluksuz, değilse boşlukla katılır."""
    son = re.split(r"\s", onceki.rstrip())[-1] if onceki.strip() else ""
    return "" if len(re.sub("[^%s]" % HARF, "", son)) <= 2 else " "


def ayristir(yol, eser: str) -> list[dict]:
    """[{baslik, kok, sayfa, metin, kayma}] döndürür. eser: 'ibnfaris' | 'ragib'.
    kayma: başlık ile asıl tanım satırı arasındaki paragraf sayısı (yalnız ragib)."""
    P, S, B = _akis(yol, eser)
    # 1. geçiş: yerinde duran başlıklar paragraflarını önce alır
    alinan: dict[int, dict] = {}
    for b in B:
        poz = b["poz"]
        b["yerinde"] = eser == "ibnfaris" or (
            poz < len(P) and poz not in alinan and _madde_gibi_basliyor(P[poz], b["baslik"]))
        if b["yerinde"] and poz < len(P):
            alinan[poz] = b
    # 2. geçiş (kural 5): kaymış başlıklar ilk tanım satırını arar
    for n, b in enumerate(B):
        if b["yerinde"]:
            continue
        poz = b["poz"]
        if b["harfle"] and 0 < poz < len(P) and P[poz - 1] is not None \
                and P[poz] is not None:
            P[poz - 1] = P[poz - 1].rstrip() + _ara(P[poz - 1]) + b["ham"] + " " + P[poz]
            P[poz] = None                                  # başlık cümlenin parçası
        ust = B[n + 3]["poz"] if n + 3 < len(B) else len(P)
        ust = min(ust, poz + PENCERE, len(P))
        j = next((i for i in range(poz, ust) if i not in alinan and P[i] is not None
                  and _tanim_satiri(P[i], b["baslik"])), None)
        if j is None and not b["harfle"] and poz < len(P) and poz not in alinan \
                and P[poz] is not None:
            j = poz                     # tanım satırı yok ama başlık cümle ortasında değil
        if j is not None:
            alinan[j] = b
    capa = []
    for j in sorted(alinan):
        b = alinan[j]
        if P[j] is None:
            continue
        b["kayma"] = j - b["poz"]
        capa.append((j, b))
    out = []
    for k, (j, b) in enumerate(capa):
        son = capa[k + 1][0] if k + 1 < len(capa) else len(P)
        metin = "\n".join(p.strip() for p in P[j:son] if p and p.strip())
        if metin:
            out.append(dict(baslik=b["baslik"], kok=b["kok"], sayfa=S[j] or b["sayfa"],
                            metin=metin, kayma=b.get("kayma", 0)))
    return out


def anahtarlar(baslik: str, eser: str) -> set[str]:
    """Bir madde başlığından aranabilir kök anahtarları."""
    n = norm(baslik)
    out = {n}
    # İbn Fâris "(بلوي)" yazımı: hem vâvî hem yâî kök -> بلو + بلي
    if eser == "ibnfaris" and len(n) == 4 and n[2:] in ("وي", "يو"):
        out |= {n[:2] + "و", n[:2] + "ي"}
    return out


def eslestir(idx, kok: str) -> list[tuple[str, str]]:
    """Korpus kök yazımını sözlük anahtarına çevir: [(kural, anahtar)].
    Hangi harfin illetli (و/ي), hangisinin hemze olduğu HAM yazımdan okunur;
    norm() hemzeyi elife indirdiği için bu ayrımı kaybeder."""
    ham = TASH.sub("", kok)
    n = norm(kok)
    # Kök yazımında yalın elif hep hemzedir (kökte uzun elif radikal olmaz):
    # QAC 'qrA', 'mlA' yazar, quran-morphology 'قرأ', 'ملأ'. İkisi aynı işlenir.
    W, H = "وي", "اأإآءؤئ"
    out: list[tuple[str, str]] = []

    def ekle(a: str, kural: str) -> None:
        if a in idx and a not in [x[1] for x in out]:
            out.append((kural, a))

    ekle(n, "birebir")
    if len(n) == 3 and n[1] == n[2]:
        ekle(n[:2], "mudâaf (iki harfle yazılmış)")
    if len(n) == 4 and n[:2] == n[2:]:
        ekle(n[:2], "tekrarlı rubâî")
    if len(ham) == 3 and ham[-1] in W:
        for h in "ويا":
            ekle(n[:2] + h, "illetli son harf (و/ي/ا)")
    if len(ham) == 3 and ham[1] in W:
        ekle(n[0] + "ا" + n[2], "illetli orta harf, elifle yazılmış")
    if out:
        return out
    if len(ham) == 3 and ham[-1] in H:
        for h in "وي":
            ekle(n[:2] + h, "ZAYIF: hemzeli kök illetli maddede")
    if len(ham) == 3 and ham[-1] in W:
        ekle(n[:2], "ZAYIF: son illetli harf düşürüldü")
    if len(ham) == 3 and ham[1] in W + H:
        ekle(n[0] + n[2], "ZAYIF: orta illetli/hemzeli harf düşürüldü")
    return out
