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
- Kullanım rolü: **Birincil Arapça metin / kanonik metin katmanı**
- Durum: Doğrulandı; indirme ve doğrulama scriptleri hazır.
- Notlar: Quranic Arabic Corpus da kendi morfolojik katmanını bu doğrulanmış metin üzerine kurduğunu belirtir.

## Aday 2 — Quranic Arabic Corpus

- Kaynak adı: Quranic Arabic Corpus Morphological Data
- Sağlayıcı / proje: Quranic Arabic Corpus / Kais Dukes
- Sürüm: 0.4
- Orijinal URL: https://corpus.quran.com/download/
- Lisans / kullanım şartları: Resmî dosya GNU lisans bildirimi ve kaynak gösterme şartı taşır; dağıtılan annotation dosyasının değiştirilmemesi istenir. Dosya içindeki şartlar verbatim kopyaların dağıtılmasına izin verir.
- Kullanım rolü: **Birincil morfoloji, lemma, kök ve segment katmanı**
- Beklenen yapı: 128.219 segment / 77.429 benzersiz kelime konumu / 6.236 ayet / 114 sûre.
- Repo hedefi: `02_morphology/qac/quranic-corpus-morphology-0.4.txt`
- Durum: Kaynak doğrulandı. Resmî indirme sayfası e-posta adımı içerdiği için hash-pinned verbatim kamu kopyası için `08_scripts/fetch_qac.py` hazırlandı.
- Mirror doğrulaması: `bnjasim/quranic-corpus` ve `taziksh/quran-frequencies` içindeki v0.4 dosyaları aynı Git blob SHA-1 değerini taşır: `b91cec6e95d5e0306550b4aedacc7380dc71152a`.
- Güvenlik: `fetch_qac.py` indirilen baytların Git blob SHA'sını ve telif/sürüm bloğunu doğrular; içerik değişmişse dosyayı kabul etmez.
- Sonraki doğrulama: `08_scripts/validate_qac.py`.
- Notlar: Kritik kök/lemma sonuçları bağımsız kaynaklarla ayrıca sınanacaktır.

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
- Notlar: Kök sayfaları kavram analizlerinde değerli çapraz kontroldür; kaynağı açıklanmayan kök anlamı tek başına nihai filolojik delil sayılmaz.

## Aday 4 — QuranMorph

- Kaynak adı: QuranMorph: Morphologically Annotated Quranic Corpus
- Sağlayıcı / proje: SinaLab / Birzeit University
- Yayın: 2025
- Kaynak: https://sina.birzeit.edu/quran/
- Makale: https://arxiv.org/abs/2506.18148
- Kapsam: 77.429 kelime; lemma ve POS annotationları üç uzman dilbilimci tarafından manuel olarak hazırlanmış.
- Kullanım rolü: **QAC lemma/POS atamalarını bağımsız çapraz doğrulama**
- Erişim notu: Resmî indirme formu, Free Edition erişimini tanınan şirket/üniversite/kurum bağlantısı olan kullanıcılarla sınırlandırdığını ve kurumsal e-posta istediğini bildiriyor. Bu koşul aşılmayacaktır; otomatik indirme yapılmayacaktır.
- Lisans notu: Dağıtılmış kopyalarda CC BY 4.0 lisans belgesi raporlanmıştır; ancak erişim koşulları lisans metninden ayrı bir dağıtım kısıtı olarak ele alınacaktır.
- Ayet sayısı karantinası: Makale metni 6.235 ayet yazar; buna karşılık QAC/Tanzil 6.236 ayet kullanır. Kamuya açık bir bağımsız doğrulama QuranMorph dağıtımındaki 77.429 kelime konumunun 6.236 ayette QAC ile hizalandığını göstermektedir. Bu nedenle gerçek dosya geldiğinde `validate_quranmorph.py` ile anahtar kümesi bizzat hesaplanacaktır.
- Durum: Parser/validator hazır; veri dosyası erişim koşulları nedeniyle repoya otomatik çekilmiyor.
- Notlar: QAC'ın yerine geçmez; annotation uyuşmazlıklarını ortaya çıkarmak için ikinci korpus olarak kullanılır.

# Karşılaştırmalı Sami dil kaynakları

## Aday 5 — Open Scriptures Hebrew Lexicon

- Proje: Open Scriptures Hebrew Bible
- Repo: https://github.com/openscriptures/HebrewLexicon
- Lisans: CC BY 4.0
- Veri: BDB, Strong ve lexical index XML katmanları.
- Kullanım rolü: **İbranice kognat/anlam alanı kontrolü**
- Durum: Offline kullanıma uygun aday; commit pinleme kaydı tutulur.

## Aday 6 — Open Scriptures Hebrew Bible (morphhb)

- Repo: https://github.com/openscriptures/morphhb
- Lisans: lemma/morfoloji CC BY 4.0; proje WLC metnini public domain olarak belirtir.
- Kullanım rolü: **İbranice kognatların gerçek metin içi dağılımı ve morfolojisi**
- Durum: Offline kullanıma uygun aday; commit pinleme kaydı tutulur.

## Aday 7 — ETCBC BHSA

- Repo: https://github.com/ETCBC/bhsa
- Lisans: CC BY-NC 4.0
- Kullanım rolü: **İleri İbranice morfoloji/sentaks çapraz kontrolü**
- Durum: Gerektiğinde ikinci İbranice annotation kaynağı.

## Aday 8 — Comprehensive Aramaic Lexicon (CAL)

- Site: https://cal.huc.edu/
- Kapsam: MÖ 9. yy'dan MS 13. yy'a kadar çok sayıda Aramice lehçe; milyonlarca lexically parsed kelime ve 40.000+ headword.
- Kullanım rolü: **Aramice tarihsel kognat kontrolü**
- Durum: Online referans. Tüm veri için açık yeniden dağıtım lisansı teyit edilmeden repo içine toplu kopya alınmayacak.

## Aday 9 — SEDRA / Beth Mardutho

- Site: https://sedra.bethmardutho.org/
- Kapsam: Süryanice kök, lexeme, sözlük ve morfoloji verileri.
- Kullanım rolü: **Süryanice kognat kontrolü**
- Durum: Online referans / lisansa göre seçici offline kullanım. Site ve sözlük bileşenlerinin telif koşulları aynı değildir; toplu kopyalama yapılmayacak.

## Kaynak hiyerarşisi

1. **Arapça metin:** Tanzil Uthmani v1.1 — değiştirilmeden.
2. **Kur'an morfolojisi / kök / lemma:** QAC v0.4.
3. **Bağımsız morfoloji kontrolü:** QuranMorph + Açık Kuran.
4. **Kur'an içi dağılım:** Kendi scriptlerimizin ham veriden ürettiği indeksler.
5. **Sami karşılaştırması:** İbranice → Aramice/Süryanice → gerektiğinde diğer Sami dilleri.
6. **Yorum:** Bütün ham ve türetilmiş veri katmanlarından ayrı tutulur.

## Metodolojik sınır

Sami kognat verisi Kur'an içi bağlamın önüne geçirilmez. Benzer biçimler otomatik olarak eş anlamlı kabul edilmez; düzenli ses denklikleri, tarihsel ilişki ve semantik süreklilik aranır. Kognat verisi esas olarak kökün eski anlam alanını desteklemek, sınırlamak veya mevcut hipotezi falsifiye etmek için kullanılır.

## Durum

Kanonik metin, QAC morfoloji, bağımsız QuranMorph kontrolü ve Sami karşılaştırma mimarisi belirlendi. QAC için hash-pinned indirme + doğrulama + indeks üretim zinciri hazırdır; QuranMorph için erişim koşulları aşılmadan doğrulama ve çapraz-korpus araçları hazır tutulmaktadır.
