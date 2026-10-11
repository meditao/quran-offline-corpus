# 08_scripts

Doğrulama, normalizasyon, sayım, konkordans ve indeks üretim scriptleri burada tutulur.

Hedefler:
- ayet sayısını doğrulama
- kelime-birimi sayısını doğrulama
- kök/lemma frekanslarını üretme
- sure/ayet dağılımını çıkarma
- ham veri ile türetilmiş indeksler arasındaki tutarlılığı sınama

Script çıktıları mümkün olduğunca deterministik ve yeniden üretilebilir olmalıdır.

`python 08_scripts/analyze_tawakkul_comparison.py`: sabit QAC v0.4 üzerinde ʾ-m-n, w-k-l ve f-w-ḍ köklerini; tam lemma, tür ve bâb sorgularını; 106:4 / 12:17 kritik segmentlerini ve ortak ayet kümelerini ayrı hesaplar. Çıktılar `07_analyses/generated/tawakkul_comparison/` altındadır. Kaynak hashleri, ham segment alanları, ayet düzeyinde Tanzil metni ve üretim manifesti korunur. Betik tarihsel veya semantik hüküm üretmez; yorum [karşılaştırma analizinde](../07_analyses/roots/Tawakkul-Wakil-analysis.md) tutulur.
