# Sami Dil Karşılaştırma Katmanı

**Durum: INFRASTRUCTURE + HEBREW LEXICAL INDEX + FIRST REVIEWED PILOT.**

`cognates.tsv` artık boş değildir. İlk pilot olarak QAC `Amn / امن` kökü için İbranice, Aramice ve Süryanice kanıt kayıtları eklenmiştir. Bu durum yalnız `Amn` kökü için filolojik pilotun başladığı anlamına gelir; 1.642 Kur'an kökünün tamamı için Sami kognat katmanı hazır değildir.

İlk ayrıntılı inceleme: `reviews/Amn.md`.

İbranice için Open Scriptures Hebrew Lexicon'dan üretilmiş offline lexical index vardır; bu indeks Kur'an kökleriyle otomatik eşleştirme yapmaz. Kognat bağlantısı ancak tek tek filolojik inceleme sonrası `cognates.tsv` içine alınır.

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
- SEDRA / Beth Mardutho ve diğer güvenilir Süryanice lexical kaynaklar — Süryanice kontrol.

Toplu yeniden dağıtım lisansı açıkça teyit edilmeyen kaynaklar repo içine snapshot olarak alınmaz.

## Kognat kayıt standardı

Her `cognates.tsv` satırı şu kanıt alanlarını taşımak zorundadır: Kur'an kökü, karşılaştırılan dil/dönem, kognat biçimi ve transliterasyonu, lexical root, gloss, kaynak/locator/URL, fonolojik uygunluk, semantik uygunluk, güven derecesi, Kur'an analizine etkisi ve inceleme tarihi. Arapça lemma alanı yalnız kayıt belirli bir lemmaya bağlanıyorsa doldurulur.

`validate_cognates.py` artık dolu kayıtlarda kanıt alanlarını zorunlu kılar, QAC kök evrenini denetler, kontrollü güven/etki değerlerini sınar ve yinelenen kanıt kayıtlarını reddeder. Varsayılan davranışta sıfır veri satırı FAIL'dir.

## Kapsam ilkesi

Bir kök için kognat kaydı bulunmaması “Sami dillerinde kognatı yoktur” anlamına gelmez. Yalnızca o kökün henüz bu projede incelenmediği anlamına gelebilir. Kapsam ile negatif filolojik sonuç birbirine karıştırılmaz.
