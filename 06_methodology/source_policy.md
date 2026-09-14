# Kaynak Politikası

Bu depo için amaç yalnızca çok sayıda kaynak toplamak değil, hangi verinin hangi iddiayı taşıyabileceğini açıkça ayırmaktır.

## 1. Kanonik Arapça metin

Birincil metin katmanı Tanzil Uthmani v1.1 olacaktır. Dosya kaynaktan alındığı biçimiyle korunur; Arapça karakterlerde, işaretlerde veya ayet metninde elle değişiklik yapılmaz. Herhangi bir normalize edilmiş sürüm gerekiyorsa yeni bir türetilmiş dosya/script çıktısı olarak oluşturulur ve ham metnin yerine geçmez.

## 2. Morfoloji ve sözdizimi

Quranic Arabic Corpus morfolojik annotation, lemma, kök ve sözdizimsel analiz için ana referans katmanlarından biridir. Bu veri Kur'an metninin kendisi değil, insan yapımı dilsel annotation'dır. Bu nedenle her annotation hata ihtimali taşıyan bir analiz katmanı olarak ele alınır ve gerektiğinde ayet içi dağılım, söz dizimi ve bağımsız sözlüklerle sınanır.

## 3. Açık Kuran

Açık Kuran kök sayfaları, ayet parçaları, kök-ayet bağlantıları ve Türkçe çeviri karşılaştırmaları için yardımcı referanstır. Özellikle hızlı kök dağılımı ve ayet kümeleri üretmekte değerlidir.

Ancak Açık Kuran'daki kök anlamı cümleleri tek başına nihai etimolojik delil sayılmaz. Kök atamaları ve anlam özetleri diğer korpus/sözlük katmanlarıyla kontrol edilir.

Açık Kuran'ın API kaynak kodunun açık olması, veri tabanının tamamının aynı repoda bulunduğu anlamına gelmez. Offline snapshot ayrıca edinilmelidir.

## 4. Ham veri ve yorum ayrımı

- `01_raw`: dış kaynaktan aynen alınmış metin/veri
- `02_morphology`: dış annotation veya buna ait açıkça belgelenmiş kopya
- `03_indices`: script ile hesaplanan sonuçlar
- `04_lexicons`: sözlük/kognat kaynakları
- `07_analyses`: bizim yorum ve sentezlerimiz

Bir yorum hiçbir zaman ham veri alanına yazılmaz.

## 5. İddia sınıfları

Analizlerde mümkün olduğunca şu ayrım korunur:

- **Doğrudan veri:** ayette bulunan biçim, kök/lemma etiketi, frekans, dağılım
- **Türetilmiş bulgu:** script ile hesaplanan eşdizim, oran, ağ, bağlam kümesi
- **Dilbilimsel yorum:** sentaks, semantik alan, olası kök anlamı
- **Tefsir/sentez:** Kur'an içi ağdan çıkarılan kavramsal sonuç

Bu ayrım, bir morfoloji etiketi veya sözlük gloss'unun doğrudan 'ayet bunu söylüyor' diye sunulmasını engeller.

## 6. Çapraz doğrulama

Kritik bir kavram için ideal akış:

1. Tanzil üzerinden ayet metnini sabitle.
2. Quranic Arabic Corpus üzerinden kök/lemma/morfoloji adaylarını çıkar.
3. Açık Kuran üzerinden kök ve ilgili ayet listesini karşılaştır.
4. Uyuşmazlık varsa otomatik olarak karantinaya al; sonuç vermeden önce elle incele.
5. Sonuçları yalnızca doğrulanmış eşleşmeler üzerinden hesapla.

## 7. Tekrarlanabilirlik

Her sayısal iddia mümkün olduğunca bir script tarafından yeniden üretilebilir olmalıdır. Script çıktıları, çalıştırılan kaynak sürümleri ve hash'lerle birlikte kaydedilir.
