# QAC v0.4 ↔ quran-morphology — konum bazında çapraz denetim

Üretici: `08_scripts/crosscheck_qac_quranmorphology.py`. İkinci annotation katmanı çapraz kontroldür, delil değildir. Hiçbir korpus diğerinin doğrulaması sayılmaz; iki sayının aynı çıkması doğrulama değildir.

## Kaynaklar

- QAC v0.4: `02_morphology/qac/quranic-corpus-morphology-0.4.txt`, sha256 `a1d12923815341face765083805d2148ed2d9f5cc3f7d6665219d887675d8c46`
- quran-morphology: `mustafa0x/quran-morphology` commit `8f38b39016824284f9ed16ae15069ff9102c4acf`, `quran-morphology.txt`, sha256 `742bfac59941b2cb09736d5b7aae694af50792261fb8450cbf6afafcc340645f`. Depoda lisans dosyası yok ve veri QAC v0.4'ün değiştirilmiş kopyası; QAC şartı değiştirilmiş kopyayı yasakladığı için veri bu depoya işlenmez, `09_calisma_masasi/yerel/` altında tutulur.

## Beklenen değerler

| ölçü | beklenen | bulunan | sonuç |
|---|---:|---:|---|
| kelime_konumu_qac | 77.429 | 77.429 | tuttu |
| kelime_konumu_qm | 77.429 | 77.429 | tuttu |
| segment_qm | 130.030 | 130.030 | tuttu |
| segment_qac | 128.219 | 128.219 | tuttu |
| kok_qm | 1.651 | 1.651 | tuttu |
| kok_qac | 1.642 | 1.642 | tuttu |
| notr_ortak | 1.638 | 1.638 | tuttu |
| notr_yalniz_qm | 13 | 13 | tuttu |
| notr_yalniz_qac | 4 | 4 | tuttu |

Birimler: kelime konumu `(sûre, ayet, kelime)`; segment `(sûre, ayet, kelime, segment)`; kök = farklı ROOT değeri. Farklı birimler toplanmaz.

- Kelime konumu kümeleri birebir aynı: **evet**.
- Hemze nötrleme çakışması (iki ham kökün aynı anahtara düşmesi): QAC 0, quran-morphology 0.

## CRLF tuzağı

QAC dosyasında CRLF ile biten satır: 128.276 / 128.276. Satır sonu soyulmadan okunursa QAC'ta **1.652** "kök" çıkar (sonunda CR taşıyan kopyalar); soyulunca **1.642**. quran-morphology dosyasında CR sayısı 0; oradaki 1.651 gerçek sayıdır, artefakt değildir. İki ayrıştırıcı da satır sonunu `\r\n` olarak soyar. Tarihsel 1.651 kaydı için: `qac_1651_vs_1642.md`.

## Kök envanteri (hemze yazımı nötrlenerek)

- Ortak: 1.638 · yalnız quran-morphology: 13 · yalnız QAC: 4
- Yalnız quran-morphology: b-r-z-ḫ, h-l-m, h-ʾ-ʾ, m-r-v, n-d-y, n-m-r-q, q-r-ş, r-m-ż, s-b-ʾ, z-r-b, ʾ-d-m, ʾ-v-n, ṭ-m-ʾ-n
- Yalnız QAC: Tmn (ṭ-m-n), mEn (m-ʿ-n), ndw (n-d-v), nws (n-v-s)

## Kelime konumu bazında kök ataması

| kategori | kelime konumu |
|---|---:|
| aynı | 76.672 |
| yalnız quran-morphology kök atıyor | 374 |
| farklı kök | 310 |
| yalnız QAC kök atıyor | 73 |
| toplam | 77.429 |

En sık farklı atamalar (kelime konumu; ham kök değerleri):

| QAC (Buckwalter) | quran-morphology | kelime konumu |
|---|---|---:|
| nws | ʾ-n-s | 241 |
| — | ʾ-y-y | 215 |
| — | y-v-m | 70 |
| ndw | n-d-y | 53 |
| Awl | — | 45 |
| Any | — | 28 |
| — | ʾ-d-m | 25 |
| Tmn | ṭ-m-ʾ-n | 13 |
| — | m-s-ḥ | 11 |
| — | m-d-n | 10 |
| — | h-v-d | 9 |
| — | ʾ-v-n | 8 |
| — | ḥ-y-y | 5 |
| — | ḥ-m-d | 5 |
| — | b-r-z-ḫ | 3 |
| lmm | h-l-m | 2 |
| — | s-b-ʾ | 2 |
| — | m-r-v | 1 |
| — | r-m-ż | 1 |
| — | ʿ-r-f | 1 |

Tam liste: `qac_quranmorphology_kok_farklari.tsv` (757 satır). Kelime konumu sayısı iki korpusta farklı olan kök: 34 (`qac_quranmorphology_kok_sayilari.tsv`).

## Segment farkı

Toplam: 130.030 − 128.219 = 1.811 segment. Kelime konumu başına fark (quran-morphology − QAC):

| fark | kelime konumu |
|---:|---:|
| -1 | 12 |
| +0 | 76.126 |
| +1 | 759 |
| +2 | 532 |

Ayrıntı: quran-morphology README'si bazı ekleri ayrı segment yapar (işaret isimlerinde ATT/DIST/ADDR, يومئذ'deki ئذ). Bu rapor segmentleri tek tek eşlemez; yalnız sayıları karşılaştırır.
