# 06_methodology

Kur'an içi semantik analiz metodolojisi, veri kullanım kuralları, doğrulama ilkeleri ve falsifikasyon ölçütleri burada tutulur.

## Ana protokol

- [`analiz_protokolu.md`](./analiz_protokolu.md) — kavram, kök, ayet, pasaj ve tez analizlerinde kullanılacak ana çalışma protokolü.
- [`kavramsal_ceviri_ilkesi.md`](./kavramsal_ceviri_ilkesi.md) — terimleri koruyan çeviri ile tefsirli çeviri arasındaki farkı, geniş anlam alanlı kavramların Türkçede tek kelimeye indirgenmemesi kuralını ve sûre girişindeki okuma anahtarları yöntemini tanımlar.
- [`sure_meal_tefsir_protokolu.md`](./sure_meal_tefsir_protokolu.md) — sûre ve pasajları tek çalışma döngüsünde denetlenebilir dilsel analiz, Kur'an içi bağlantı fişleri, her ayette tek ana çeviri, yalnız gerekirse tefsirli çeviri ve bütünleşik kısa tefsirle işleme yöntemi. Kavram/tez protokolü yerine geçmez; sûre iş ritmi ve çıktı biçimi için özel kuraldır.

## Temel ayrım

- `01_raw/` ve `02_morphology/`: kaynak/veri katmanı
- `03_indices/`: türetilmiş hesaplama katmanı
- `04_lexicons/` ve `05_translations/`: yardımcı referans katmanı
- `06_methodology/`: yöntem katmanı
- `07_analyses/`: yorum ve sonuç katmanı

Bir yorum, ham veri gibi sunulmaz. Bir sayım, yeniden üretilebilecek script veya açık yöntemle desteklenir. Bir anlam önerisi, mümkün olduğunda Kur'an içi dağılım ve karşı örneklerle sınanır.
