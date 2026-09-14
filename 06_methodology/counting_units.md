# Sayım Birimleri — karıştırılmaması gereken düzeyler

Kur'an korpusunda tek bir 'kelime sayısı' yoktur. Kullanılan tokenizasyon/segmentasyon şemasına göre farklı ve aynı anda doğru sayılar çıkabilir. Bu nedenle bütün istatistikler hangi birimi saydığını açıkça belirtmelidir.

## 1. Ayet

Sabit referans anahtarı: `(sûre, ayet)`.

Bu projede kanonik numaralı ayet sayısı: **6.236**.

## 2. Ortografik kelime konumu

QAC/QuranMorph ortak anahtarı: `(sûre, ayet, kelime)`.

QAC v0.4 / QuranMorph hizasında beklenen sayı: **77.429 kelime konumu**.

Örnek: `وبالآخرة` yazı düzeyinde tek kelime konumu olabilir; içinde bağlaç/edat/determiner/stem gibi birden fazla morfolojik segment bulunabilir.

## 3. Morfolojik segment / clitic

QAC anahtarı: `(sûre, ayet, kelime, segment)`.

QAC v0.4 için beklenen toplam: **128.219 segment**.

Prefix, stem ve suffix aynı ortografik kelimenin ayrı segmentleri olabilir. Bu sayı 77.429 ile toplanamaz veya onun yerine doğrudan 'kelime sayısı' diye kullanılamaz.

## 4. Kök/lemma occurrence

Kök veya lemma frekansı sayarken varsayılan birim **kök/lemma taşıyan ortografik kelime konumu** olacaktır. Aynı kelime konumunda aynı kök birden fazla segmentte tekrar görünse bile bir kez sayılır.

Her kök için üç sayı ayrı tutulur:

- `word_occurrences`: kaç kelime konumu
- `ayah_count`: kaç farklı ayet
- `surah_count`: kaç farklı sûre

Bu, örneğin `61 birim / 59 ayet / 32 sûre` gibi raporların tam olarak neyi ifade ettiğini sabitler.

## 5. Eski 130.030 kelime-birimi kaydı

Önceki çalışma korpusunda kullanılan **130.030 kelime-birimi** sayısı şimdilik ayrı bir tokenizasyon katmanı olarak kabul edilir. QAC'ın 128.219 segmenti veya 77.429 ortografik kelimesiyle eşit olduğu varsayılmayacaktır.

Bu fark çözülmeden şu ifadeler kullanılmamalıdır:

- 'QAC toplam kelime sayısı 130.030'dur.'
- '128.219 segment ile 130.030 kelime-birimi aynı şeydir.'

İleride eski korpusun üretim kuralı/ham verisi repoya alındığında iki tokenizasyon konum bazında karşılaştırılacak ve 1.811 birimlik farkın kaynağı raporlanacaktır.

## İlke

Her istatistik şu soruya cevap vermelidir: **Tam olarak neyi saydık?**

Kaynak, tokenizasyon şeması ve sayım birimi belirtilmeden verilen sayı analitik kanıt sayılmaz.
