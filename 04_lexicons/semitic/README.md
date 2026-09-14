# Sami Dil Karşılaştırma Katmanı

**Durum: INFRASTRUCTURE + HEBREW LEXICAL INDEX; REVIEWED COGNATE DATA NOT YET POPULATED.**

`cognates.tsv` şu anda yalnız şema başlığı içerir; filolojik olarak incelenmiş Arapça↔İbranice/Aramice/Süryanice kognat satırları henüz eklenmemiştir. Bu nedenle bu klasörün varlığı 'Sami kognatlar doğrulandı' anlamına gelmez.

İbranice için Open Scriptures Hebrew Lexicon'dan üretilmiş offline lexical index vardır; fakat bu indeks Kur'an kökleriyle otomatik eşleştirme yapmaz.

## Yöntem kuralı

Sami kognatları birincil anlam belirleyici değildir. Kullanım sırası:

1. Kur'an içi dağılım, sentaks, eşdizim ve bağlam
2. Kur'anik Arapça morfoloji ve kök ailesi
3. Filolojik olarak incelenmiş İbranice, Aramice ve Süryanice kognatlar
4. Gerektiğinde daha uzak Sami karşılaştırmaları

Bir biçim yalnız benzer göründüğü için kognat kabul edilmez. Düzenli ses denklikleri, tarihsel olasılık, lexical kaynak ve semantik süreklilik aranır. Sami verisi Kur'an içindeki açık kullanımın önüne geçirilmez; destek, sınama veya falsifikasyon için kullanılır.

## Kaynaklar

### Offline mevcut

- Open Scriptures Hebrew Lexicon — CC BY 4.0; üretilmiş lexical index mevcuttur.
- Open Scriptures Hebrew Bible / morphhb — commit'e sabitlenmiş aday kaynak; gerektiğinde metin içi morfoloji kontrolü.

### Online referans

- Comprehensive Aramaic Lexicon (CAL) — Aramice tarihsel/lehçesel kontrol.
- SEDRA / Beth Mardutho — Süryanice lexical/morfoloji kontrolü.

Toplu yeniden dağıtım lisansı açıkça teyit edilmeyen kaynaklar repo içine snapshot olarak alınmaz.

## Kognat kayıt standardı

Her `cognates.tsv` satırı mümkün olduğunca şu kanıtları taşır: Kur'an kökü, Arapça lemma, karşılaştırılan dil/dönem, kognat biçimi, lexical root, kaynak/locator, temel anlam, fonolojik uyum, semantik uyum, güven derecesi ve Kur'an analizine etkisi.

`validate_cognates.py` varsayılan olarak sıfır veri satırında FAIL verir. Yalnız şema/altyapı CI'ı `--allow-empty` ile çalıştırılabilir ve bu durumda çıktı açıkça **SCHEMA-ONLY** olarak işaretlenir.
