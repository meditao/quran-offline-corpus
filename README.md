# Quran Offline Corpus

Bu depo, Kur'an merkezli dilsel ve kavramsal analizler için denetlenebilir, sürümlenebilir ve mümkün olduğunca offline çalışan bir veri altyapısıdır.

## Mevcut durum

**Çekirdek veri katmanı hazır:** Tanzil Uthmani v1.1 + QAC v0.4 + yeniden üretilebilir kök/lemma/POS indeksleri.

**Kısmen hazır:** İbranice lexical index mevcut, fakat incelenmiş Arapça↔Sami kognat eşlemeleri henüz populate edilmedi.

**Henüz veri yok:** QuranMorph, çeviriler ve `07_analyses` katmanı. Bu klasörlerde altyapı/README bulunması veri setinin mevcut olduğu anlamına gelmez.

**Opsiyonel yardımcı kaynak:** Açık Kuran. Eski REST API çekirdek workflow'un parçası değildir.

## Temel ilke

Ham kaynak verisi ile türetilmiş indeksler, sözlük katmanı ve yorum/analiz katmanı ayrıdır. Kaynağı ve lisansı doğrulanmamış veri ham korpusa eklenmez.

## Dizin yapısı

- `01_raw/` — doğrulanmış Tanzil metni ve metadata
- `02_morphology/` — QAC ve aday bağımsız annotation katmanları
- `03_indices/` — script ile üretilen kök/lemma/POS ve alignment indeksleri
- `04_lexicons/` — İbranice lexical index + Sami kognat altyapısı
- `05_translations/` — şu anda boş/planlanan yardımcı çeviri katmanı
- `06_methodology/` — kaynak, lisans, sayım ve alignment kuralları
- `07_analyses/` — şu anda boş; ileride yorum/sentez katmanı
- `08_scripts/` — doğrulama, sayım, sorgu ve audit scriptleri

## Kaynak hiyerarşisi

1. Arapça metin: **Tanzil Uthmani v1.1**
2. Morfoloji / kök / lemma: **Quranic Arabic Corpus v0.4**
3. Kur'an içi dağılım: **ham QAC'dan kendi scriptlerimizin ürettiği indeksler**
4. Bağımsız kontroller: mevcutsa QuranMorph / Açık Kuran / sözlükler
5. Tarihsel anlam alanı: İbranice → Aramice/Süryanice → diğer Sami dilleri
6. Nihai yorum: yukarıdaki veri katmanlarından ayrı

## Kritik tokenizasyon kuralı

Tanzil ile QAC aynı ayet anahtarlarını paylaşır fakat kelime tokenizasyonları birebir aynı değildir. `(sûre,ayet)` ortak referanstır; Tanzil↔QAC kelime düzeyi join için `03_indices/generated/tanzil_qac_alignment.csv` kullanılmalıdır. Ayrıntı: `06_methodology/counting_units.md`.

## Offline kök sorguları

```bash
python 08_scripts/query_qac.py --root Slw
python 08_scripts/query_root.py --root Amn
```

Her iki kök sorgu aracı da `--root` biçimini kullanır. `query_root.py` ayrıca varsa incelenmiş Sami kognat kayıtlarını gösterir; sıfır kayıt, 'kognat yok' anlamına gelmez.

## Üretilen temel indeksler

`build_qac_indices.py` ham QAC dosyasından şunları yeniden üretir:

- `qac_word_annotations.csv`
- `root_index.csv`
- `lemma_index.csv`
- `pos_index.csv`

`build_tanzil_qac_alignment.py` ise Tanzil Uthmani v1.1 ile QAC arasındaki ayet-düzeyi kelime sayısı/alignment farklarını yeniden üretir.

## Otomatik bütünlük garantisi

`.github/workflows/core-integrity.yml` **her push ve pull request'te**:

1. Tanzil dosyalarının sabit SHA-256 değerlerini ve 114 sûre / 6236 ayet yapısını kontrol eder.
2. QAC v0.4 dosyasının sabit SHA-256'sını ve 128.219 segment / 77.429 kelime / 6236 ayet / 114 sûre yapısını kontrol eder.
3. QAC indekslerini yeniden üretir.
4. Tanzil↔QAC alignment raporunu yeniden üretir.
5. Üretilen çekirdek dosyaların commit'li dosyalarla byte düzeyinde aynı olmasını zorunlu kılar.

## Kök sayım notu

Sabitlenmiş QAC v0.4 annotation dosyasında sağlam parser ile **1.642 benzersiz ROOT etiketi** vardır. Tarihsel `1.651` sonucu, CRLF ve virgül-ayırıcı kaynaklı bir shell-pipeline artefaktı olarak yeniden üretilip belgelenmiştir. Bu sayı 'Kur'an ontolojik olarak tam 1.642 kökten oluşur' anlamına gelmez; annotation snapshot'ına bağlıdır.

## Lisans

Üçüncü taraf veri koşulları `LICENSES.md` ve `SOURCES.md` içinde ayrı ayrı kaydedilir. Repo-geneli için tek bir lisans seçilmiş değildir.
