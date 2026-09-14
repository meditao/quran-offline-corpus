# Kaynak Kayıtları

Bu dosya, repoya giren veya aday olarak değerlendirilen her dış veri kaynağının izini tutar.

Her kaynak için aşağıdaki alanlar mümkün olduğunca doldurulur:

- Kaynak adı
- Sağlayıcı / proje
- Sürüm
- Orijinal URL
- Erişim / indirme tarihi
- Lisans
- Repo içindeki dosya yolu
- Dosyada değişiklik yapıldı mı?
- Değişiklik açıklaması
- SHA-256
- Kullanım rolü
- Notlar

## Aday 1 — Tanzil Quran Text

- Kaynak adı: Tanzil Quran Text — Uthmani
- Sağlayıcı / proje: Tanzil Project
- Sürüm: 1.1
- Yayın bilgisi: Şubat 2021
- Orijinal URL: https://tanzil.net/download/
- Lisans: Creative Commons Attribution 3.0
- Temel koşul: Metnin birebir kopyalanmasına/dağıtılmasına izin veriliyor; Kur'an metninin değiştirilmemesi, Tanzil kaynağının belirtilmesi ve lisans bildiriminin korunması gerekiyor.
- Kullanım rolü: **Birincil Arapça metin adayı / kanonik metin katmanı**
- Durum: Doğrulandı; ham dosya henüz repoya eklenmedi.
- Notlar: Tanzil metni yüksek doğrulama odaklıdır ve Quranic Arabic Corpus da kendi morfolojik katmanını bu doğrulanmış metin üzerine kurduğunu belirtir.

## Aday 2 — Quranic Arabic Corpus

- Kaynak adı: Quranic Arabic Corpus Morphological Data
- Sağlayıcı / proje: Quranic Arabic Corpus / Kais Dukes
- Sürüm: 0.4
- Orijinal URL: https://corpus.quran.com/download/
- Lisans / kullanım şartları: İndirme sayfası GNU License bildirimi ve kaynak gösterme şartı içeriyor; dağıtılan annotation dosyasının değiştirilmemesi isteniyor. FAQ ayrıca araştırma/non-commercial kullanım notu taşıyor.
- Kullanım rolü: **Morfoloji, lemma, kök, sözdizimi ve çapraz doğrulama katmanı**
- Durum: Kaynak doğrulandı; lisans ve yeniden dağıtım koşulları nedeniyle ham veri henüz repoya eklenmedi.
- Notlar: Kaynak, morfolojik annotation, syntactic treebank ve semantic ontology sağlıyor ve Tanzil'in doğrulanmış Arapça metni üzerine kurulduğunu açıkça belirtiyor.

## Aday 3 — Açık Kuran

- Kaynak adı: Açık Kuran / Açık Kuran API
- Sağlayıcı / proje: acik-kuran
- Site: https://acikkuran.com
- Kaynak kodu: https://github.com/acik-kuran/acikkuran-api
- Lisans: API projesi CC BY-NC-SA 4.0 olarak yayımlanmış.
- Kullanım rolü: **İkincil kök/ayet-parçası doğrulama, Türkçe meal karşılaştırması ve araştırma arayüzü**
- Durum: Kullanılacak yardımcı kaynak; kanonik Arapça metin kaynağı yapılmayacak.
- Sağladığı başlıca veri: ayet metni, sadeleştirilmiş ayet, ayet parçaları, kelime/kök bağlantıları, kök sayfaları, kök varyantları ve çoklu çeviriler.
- Önemli teknik not: Açık Kuran'ın GitHub API deposu veri tabanının kendisini içermiyor; route kodu PostgreSQL tablolarındaki `acikkuran_roots`, `acikkuran_rootwords` vb. yapılardan veri okuyor. Bu nedenle yalnızca API reposunu klonlamak offline kök/veri korpusu sağlamıyor. İçerik için ayrıca lisansa uygun bir snapshot gerekir.
- Notlar: Kök sayfaları bizim kavram analizlerinde değerli bir çapraz kontrol kaynağıdır; fakat kaynağı açıklanmayan kök anlamlarını tek başına nihai filolojik delil saymayacağız.

## Kaynak hiyerarşisi

1. **Arapça metin:** Tanzil Uthmani v1.1 (değiştirilmeden)
2. **Morfoloji / lemma / kök:** Quranic Arabic Corpus v0.4 + bağımsız kontroller
3. **Kök ve Türkçe karşılaştırma:** Açık Kuran
4. **Bizim türetilmiş indekslerimiz:** Yukarıdaki ham katmanlardan scriptlerle üretilecek ve ham kaynaklardan kesin biçimde ayrı tutulacak.

## Durum

Kaynak hiyerarşisi belirlendi. Sonraki adım Tanzil ham metninin lisans bildirimiyle birlikte alınması, hash'lenmesi ve ayet/sûre sayısının otomatik doğrulanmasıdır.
