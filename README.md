# Quran Offline Corpus

Bu depo, Kur'an merkezli dilsel ve kavramsal analizler için denetlenebilir, sürümlenebilir ve mümkün olduğunca offline çalışabilen bir veri altyapısı oluşturmak amacıyla kurulmuştur.

## Temel ilke

Ham kaynak verisi ile türetilmiş indeksler, sözlük/not katmanı ve yorum/analiz katmanı kesin biçimde birbirinden ayrılır. Kaynağı ve lisansı doğrulanmamış veri ham korpusa eklenmez.

## Dizin yapısı

- `01_raw/` — doğrulanmış ham Kur'an metni ve temel metadata
- `02_morphology/` — morfoloji, lemma, kök ve sözcük türü katmanları
- `03_indices/` — ham veriden türetilen kök/lemma/frekans/ayet indeksleri
- `04_lexicons/` — Arapça kök sözlükleri ve mümkün olduğunda Sami kognat kaynakları
- `05_translations/` — lisansı uygun çeviri/metin katmanı
- `06_methodology/` — analiz metodolojisi ve veri kullanım kuralları
- `07_analyses/` — kavram ve ayet analizleri; ham veriden ayrı tutulur
- `08_scripts/` — doğrulama, sayım, konkordans ve indeksleme scriptleri

## Veri bütünlüğü

Her dış kaynak `SOURCES.md` içinde sürüm, URL, lisans, indirme tarihi ve mümkün olduğunda SHA-256 ile kaydedilir. Ham dosyalar değiştirilirse bu ayrıca belgelenir.

## Hedef

Aynı sabit korpus üzerinden tekrar üretilebilir analizler yapmak; kök, lemma, morfoloji, bağlam ve dağılım iddialarını doğrudan denetlenebilir hale getirmek.
