# Quran Offline Corpus

Bu depo, Kur'an merkezli dilsel ve kavramsal analizler için denetlenebilir, sürümlenebilir ve mümkün olduğunca offline çalışabilen bir veri altyapısı oluşturmak amacıyla kurulmuştur.

## Temel ilke

Ham kaynak verisi ile türetilmiş indeksler, sözlük/not katmanı ve yorum/analiz katmanı kesin biçimde birbirinden ayrılır. Kaynağı ve lisansı doğrulanmamış veri ham korpusa eklenmez.

## Dizin yapısı

- `01_raw/` — doğrulanmış ham Kur'an metni ve temel metadata
- `02_morphology/` — morfoloji, lemma, kök ve sözcük türü katmanları
- `03_indices/` — ham veriden türetilen kök/lemma/frekans/ayet indeksleri
- `04_lexicons/` — Açık Kuran yardımcı kök katmanı + karşılaştırmalı Sami kaynakları
- `05_translations/` — lisansı uygun çeviri/metin katmanı
- `06_methodology/` — analiz metodolojisi, kaynak hiyerarşisi ve sayım birimleri
- `07_analyses/` — kavram ve ayet analizleri; ham veriden ayrı tutulur
- `08_scripts/` — doğrulama, indirme, sayım, konkordans ve çapraz-korpus scriptleri

## Kaynak hiyerarşisi

1. Arapça kanonik metin: **Tanzil Uthmani**
2. Morfoloji / kök / lemma: **Quranic Arabic Corpus v0.4**
3. Bağımsız lemma/POS kontrolü: **QuranMorph** (erişim koşulları izin verdiğinde)
4. Kök metadata ve Türkçe araştırma arayüzü: **Açık Kuran**
5. Tarihsel anlam alanı kontrolü: **İbranice → Aramice/Süryanice → diğer Sami dilleri**
6. Nihai yorum: yukarıdaki katmanlardan ayrı tutulur

## Bir defalık kurulum akışı

Tanzil şartlarını okuyup kabul ettikten sonra:

```bash
python 08_scripts/fetch_tanzil.py --i-agree-to-tanzil-terms
python 08_scripts/validate_tanzil.py
```

QAC şartlarını okuyup kabul ettikten sonra:

```bash
python 08_scripts/fetch_qac.py --i-accept-qac-terms
python 08_scripts/validate_qac.py
python 08_scripts/build_qac_indices.py
```

Bundan sonra kök/lemma sorguları tamamen offline yapılabilir:

```bash
python 08_scripts/query_qac.py --root Slw
python 08_scripts/query_qac.py --root Amn
python 08_scripts/query_qac.py --root wqy
```

Açık Kuran kök metadata snapshot'ı için:

```bash
python 08_scripts/fetch_acikkuran_roots.py --i-accept-acikkuran-license
```

QuranMorph dosyası izinli/uygun kanaldan edinilirse:

```bash
python 08_scripts/validate_quranmorph.py
python 08_scripts/crosscheck_qac_quranmorph.py
```

## Üretilen temel indeksler

`build_qac_indices.py` şu dosyaları yeniden üretir:

- `qac_word_annotations.csv` — her `(sûre:ayet:kelime)` için biçim, kök, lemma ve POS
- `root_index.csv` — her kök için kelime occurrence / ayet / sûre sayısı
- `lemma_index.csv` — her lemma için kelime occurrence / ayet / sûre sayısı
- `pos_index.csv` — POS dağılımı

Bu nedenle sayı iddiaları hafızadan değil ham korpustan yeniden hesaplanabilir.

## Sayım birimi uyarısı

`kelime`, `morfolojik segment/clitic` ve `kök occurrence` aynı şey değildir. QAC v0.4 77.429 ortografik kelime konumu ve 128.219 morfolojik segment kullanır. Önceki çalışma korpusundaki 130.030 `kelime-birimi` ayrı bir tokenizasyon olarak karantinadadır; ayrıntı için `06_methodology/counting_units.md` dosyasına bakın.

## Sami kognat ilkesi

Sami dillerindeki benzerlik, Kur'an içi anlamı belirlemez. Kognat verisi ancak düzenli ses denkliği, tarihsel ilişki ve semantik süreklilik varsa destekleyici/falsifiye edici kanıt olarak kullanılır.

## Veri bütünlüğü

Her dış kaynak `SOURCES.md` içinde sürüm, URL, lisans, indirme tarihi ve mümkün olduğunda hash ile kaydedilir. Ham dosyalar değiştirilmez. Türetilmiş indeksler her zaman scriptlerle yeniden üretilebilir olmalıdır.

## Hedef

Aynı sabit korpus üzerinden tekrar üretilebilir analizler yapmak; kök, lemma, morfoloji, bağlam, dağılım ve kognat iddialarını doğrudan denetlenebilir hale getirmek.
