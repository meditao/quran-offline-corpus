# Sayım Birimleri — karıştırılmaması gereken düzeyler

Kur'an korpusunda tek bir 'kelime sayısı' yoktur. Kullanılan tokenizasyon/segmentasyon şemasına göre farklı ve aynı anda doğru sayılar çıkabilir. Bu nedenle bütün istatistikler hangi birimi saydığını açıkça belirtmelidir.

## 1. Ayet

Sabit referans anahtarı: `(sûre, ayet)`.

Bu projede kanonik numaralı ayet sayısı: **6.236**.

## 2. QAC ortografik kelime konumu

QAC anahtarı: `(sûre, ayet, kelime)`.

QAC v0.4 için sayı: **77.429 kelime konumu**.

Örnek: `وبالآخرة` yazı düzeyinde tek kelime konumu olabilir; içinde bağlaç/edat/determiner/stem gibi birden fazla morfolojik segment bulunabilir.

## 3. Tanzil whitespace tokenı ≠ QAC kelime konumu

Tanzil v1.1 `Simple Clean` metnini boşluklardan bölmek, QAC'ın `word` konumlarıyla aynı tokenizasyonu vermez.

Başlıca nedenler:
- Tanzil txt çıktısında birçok sûrenin ilk ayetine sûre başı besmelesi eklenmiştir; QAC bu besmeleyi aynı `(sûre,1,kelime)` dizisine katmaz.
- Tanzil v1.1 ile QAC'ın dayandığı eski Tanzil katmanı arasında bazı split/merge güncellemeleri vardır.

Bu nedenle **Tanzil ile QAC arasında `(sûre,ayet,kelime)` doğrudan join anahtarı değildir.** Güvenli ortak anahtar ayet düzeyinde `(sûre,ayet)`tir. Kelime düzeyinde eşleştirme için:

- `03_indices/generated/tanzil_qac_alignment.csv`
- `03_indices/audits/tanzil_qac_alignment.md`

kullanılır.

## 4. Morfolojik segment / clitic

QAC anahtarı: `(sûre, ayet, kelime, segment)`.

QAC v0.4 için beklenen toplam: **128.219 segment**.

Prefix, stem ve suffix aynı ortografik kelimenin ayrı segmentleri olabilir. Bu sayı 77.429 ile toplanamaz veya onun yerine doğrudan 'kelime sayısı' diye kullanılamaz.

## 5. Kök/lemma occurrence

Kök veya lemma frekansı sayarken varsayılan birim **kök/lemma taşıyan QAC ortografik kelime konumu**dur. Aynı kelime konumunda aynı kök birden fazla segmentte tekrar görünse bile bir kez sayılır.

Her kök için üç sayı ayrı tutulur:

- `word_occurrences`: kaç kelime konumu
- `ayah_count`: kaç farklı ayet
- `surah_count`: kaç farklı sûre

Bu, örneğin `61 birim / 59 ayet / 32 sûre` gibi raporların tam olarak neyi ifade ettiğini sabitler.

## 6. Eski 130.030 kelime-birimi kaydı

Önceki çalışma korpusunda kullanılan **130.030 kelime-birimi** sayısı şimdilik ayrı bir tokenizasyon katmanı olarak kabul edilir. QAC'ın 128.219 segmenti veya 77.429 ortografik kelimesiyle eşit olduğu varsayılmayacaktır.

Bu fark çözülmeden şu ifadeler kullanılmamalıdır:

- 'QAC toplam kelime sayısı 130.030'dur.'
- '128.219 segment ile 130.030 kelime-birimi aynı şeydir.'

İleride eski korpusun üretim kuralı/ham verisi repoya alındığında iki tokenizasyon konum bazında karşılaştırılacak ve farkın kaynağı raporlanacaktır.

## İlke

Her istatistik şu soruya cevap vermelidir: **Tam olarak neyi saydık?**

Kaynak, tokenizasyon şeması ve sayım birimi belirtilmeden verilen sayı analitik kanıt sayılmaz.
