# Sami Dil Karşılaştırma Katmanı

Bu klasör, Kur'an kavram analizlerinde kullanılacak karşılaştırmalı Sami dil verilerini tutar.

## Yöntem kuralı

Sami kognatları **birincil anlam belirleyici değildir**. Kullanım sırası şöyledir:

1. Kur'an içi dağılım, sentaks, eşdizim ve bağlam
2. Klasik/Kur'anik Arapça morfoloji ve kök ailesi
3. İbranice, Aramice ve Süryanice kognatlar
4. Daha uzak Sami karşılaştırmaları

Bir kognat yalnızca biçimsel benzerlik nedeniyle eş anlamlı kabul edilmez. Düzenli ses denklikleri, tarihsel olasılık ve anlam sürekliliği aranır. Sami verisi Kur'an içindeki açık kullanımın anlamını geçersiz kılamaz; yalnızca kökün eski anlam alanı için destek, sınama veya falsifikasyon sağlar.

## Öncelikli diller

- Biblical / Classical Hebrew (İbranice)
- Aramaic (çeşitli dönem ve lehçeler)
- Syriac (Süryanice)
- Gerektiğinde Akkadca, Ge'ez/Etiyopyaca ve diğer Sami dilleri

## Offline kullanılabilecek kaynaklar

### Open Scriptures Hebrew Lexicon

- Proje: Open Scriptures Hebrew Bible
- Repo: https://github.com/openscriptures/HebrewLexicon
- İçerik: BDB tabanı, Strong verisi, lexical index ve ilişkili XML dosyaları
- Lisans: CC BY 4.0
- Rol: İbranice kognat ve anlam alanı kontrolü

### Open Scriptures Hebrew Bible (morphhb)

- Repo: https://github.com/openscriptures/morphhb
- İçerik: İbranice metin, lemma ve morfoloji
- Lisans: lemma/morfoloji CC BY 4.0; WLC metni public domain olarak belirtiliyor
- Rol: Bir İbranice kökün gerçek metin içi dağılımını ve kullanım bağlamını kontrol etmek

### ETCBC BHSA

- Repo: https://github.com/ETCBC/bhsa
- İçerik: Hebrew Bible + ayrıntılı dilbilimsel annotation
- Lisans: CC BY-NC 4.0
- Rol: İleri düzey İbranice morfoloji/sentaks çapraz kontrolü

## Online referans olarak kullanılacak kaynaklar

### Comprehensive Aramaic Lexicon (CAL)

- Site: https://cal.huc.edu/
- Kapsam: MÖ 9. yy'dan MS 13. yy'a çok sayıda Aramice lehçeyi kapsayan geniş metin/lexicon veritabanı
- Durum: Akademik olarak çok değerli; tüm verinin serbest yeniden dağıtım lisansı ayrıca teyit edilmeden repo içine toplu snapshot alınmayacak.
- Rol: Aramice kognatların tarihsel ve lehçesel kontrolü

### SEDRA / Beth Mardutho

- Site: https://sedra.bethmardutho.org/
- Kapsam: Süryanice kök, lexeme, sözlük ve morfoloji kaynakları
- Durum: Site içeriğinin telif koşulları kaynak bazında farklıdır; izin açık değilse toplu veri repoya kopyalanmayacak.
- Rol: Süryanice kognat doğrulaması

## Analiz kaydı standardı

Her kognat iddiasında mümkün olduğunca şu alanlar tutulmalıdır:

- Kur'an Arapçası kökü
- Arapça lemma / biçim
- Karşılaştırılan dil
- Kognat biçimi
- Kaynak
- Temel anlam(lar)
- Fonolojik uygunluk
- Semantik yakınlık
- Güven derecesi: güçlü / orta / zayıf
- Kur'an içi analize etkisi: destekliyor / nötr / zorlaştırıyor

Bu katmanda 'aynı kök = aynı anlam' varsayımı yapılmaz.
