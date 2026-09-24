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

## 6. Eski 130.030 kelime-birimi kaydı — karşılaştırıldı (Aşama 4)

Önceki çalışma korpusundaki **130.030** birimlik sayı, çalışma masasının Aşama 4'ünde ikinci annotation katmanı olarak alınan `mustafa0x/quran-morphology` dosyasıyla (commit `8f38b39`, sha256 `742bfac59941…`) QAC v0.4'e (sha256 `a1d129238153…`) konum bazında karşılaştırıldı. Rapor: [`03_indices/audits/qac_quranmorphology.md`](../03_indices/audits/qac_quranmorphology.md) (üretici `08_scripts/crosscheck_qac_quranmorphology.py`; aşağıdaki sayılar raporun `.json` çıktısından alınmıştır).

Sonuç:

| ölçü | quran-morphology | QAC v0.4 | birim |
|---|---:|---:|---|
| kelime konumu | 77.429 | 77.429 | kelime konumu (sûre, ayet, kelime) |
| segment | 130.030 | 128.219 | segment |
| benzersiz kök | 1.651 | 1.642 | kök |

- **130.030 bir kelime sayısı değil, quran-morphology'nin segment sayısıdır.** Kelime konumu kümeleri iki korpusta birebir aynıdır (77.429). Fark tokenizasyondan değil **segmentasyondan** gelir: 130.030 − 128.219 = 1.811 segment.
- Kelime konumu başına segment farkı (quran-morphology − QAC): -1 → 12, +0 → 76.126, +1 → 759, +2 → 532 kelime konumu. Fark 1.303 kelime konumunda yoğunlaşır; quran-morphology bazı ekleri ayrı segment yapar (işaret isimlerinde ATT/DIST/ADDR, يومئذ'deki ئذ; kaynak: o deponun README'si). Rapor segmentleri tek tek eşlemez, yalnız sayıları karşılaştırır: segment düzeyinde farkın her bir kalemi ayrıca listelenmemiştir.
- Kök envanteri (hemze yazımı nötrlenerek): ortak 1.638, yalnız quran-morphology 13, yalnız QAC 4. Kelime konumu bazında kök ataması: aynı 76.672, farklı kök 310, yalnız quran-morphology kök atıyor 374, yalnız QAC kök atıyor 73.

Sınır: eski korpusun bu dosya olduğu, sayının (130.030) tam tutması ve `CLAUDE.md` §5'teki kayda dayanır; eski korpusun üretim kuralı depoda ayrıca yoktur. Sayı eşitliği tek başına kimlik kanıtı değildir.

Kullanım kuralı (değişmedi, gerekçesi artık ölçülü):

- '130.030' QAC kelime sayısı değildir; QAC'ın kelime konumu sayısı 77.429, segment sayısı 128.219'dir.
- '128.219 segment ile 130.030 birim aynı şeydir' denmez: iki ayrı segmentasyondur.
- Kanonik korpus QAC v0.4'tür; quran-morphology çapraz kontroldür, delil değildir (`CLAUDE.md` §3, §5).

## İlke

Her istatistik şu soruya cevap vermelidir: **Tam olarak neyi saydık?**

Kaynak, tokenizasyon şeması ve sayım birimi belirtilmeden verilen sayı analitik kanıt sayılmaz.
