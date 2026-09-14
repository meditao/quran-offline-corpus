# Lisans Kayıtları

Bu depo üçüncü taraf veri içerir. Repo-geneli için tek bir lisans seçilmiş değildir; her veri katmanı kendi kaynak koşullarına tabidir. Aşağıdaki kayıtlar `SOURCES.md` ile birlikte okunmalıdır.

## 1. Tanzil Quran Text v1.1 — repo içindeki güncel ham metin

Dosyalar:
- `01_raw/tanzil/quran-uthmani.txt`
- `01_raw/tanzil/quran-simple-clean.txt`
- `01_raw/tanzil/quran-data.xml`

Kaynak: Tanzil Project, https://tanzil.net/

Tanzil'in güncel metin lisans bildirimi **Creative Commons Attribution 3.0** olarak yayımlanır. Buna ek olarak Tanzil'in kendi kullanım şartı, Kur'an metninin yalnız **verbatim** kopyalanıp dağıtılmasına izin verir ve metnin değiştirilmesini yasaklar. Kaynak atfı ve Tanzil'e bağlantı korunmalıdır.

Bu repodaki Tanzil ham metin dosyaları değiştirilmez. Normalizasyon veya karşılaştırma gerekiyorsa yeni bir türetilmiş çıktı üretilir; ham dosyanın yerine yazılmaz.

## 2. Quranic Arabic Corpus (QAC) v0.4

Dosya:
- `02_morphology/qac/quranic-corpus-morphology-0.4.txt`

Kaynak: Quranic Arabic Corpus / Kais Dukes, https://corpus.quran.com/download/

QAC v0.4 annotation dosyası **GNU General Public License** bildirimi taşır. Resmî indirme sayfasındaki ek kullanım bildirimi, dosyanın verbatim kopyalarında telif/lisans bloğunun korunmasını, kaynağın belirtilmesini ve QAC'a bağlantı verilmesini ister.

QAC dosyasının içinde ayrıca üzerine inşa edildiği eski **Tanzil Uthmani v1.0.2** metnine ait tarihsel bildirim bulunur. Bu gömülü tarihsel katman **CC BY-ND 3.0 Unported** olarak etiketlenmiştir. Bu, `01_raw/tanzil/` altındaki güncel Tanzil v1.1 dosyalarının lisans kaydıyla karıştırılmamalıdır.

`03_indices/generated/` altındaki kök/lemma/POS tabloları QAC annotationlarından script ile türetilmiştir. Bunlar bağımsız olarak yeniden lisanslanmış kabul edilmez; QAC/Tanzil kaynak atıfları korunur.

## 3. Open Scriptures Hebrew Lexicon

Türetilmiş çıktı:
- `04_lexicons/generated/hebrew_lexical_index.tsv`

Kaynak: Open Scriptures Hebrew Lexicon, sabit commit bilgisi `04_lexicons/semitic/VENDOR_LOCK.json` ve üretilmiş manifestte tutulur.

Lisans: **CC BY 4.0**. Kaynak atfı korunmalıdır. Brown–Driver–Briggs ve Strong sözlük metinlerinin public-domain durumu proje tarafından ayrıca belirtilmektedir; bu repo yine de türetilmiş indeksi Open Scriptures kaynak kaydıyla birlikte taşır.

## 4. Open Scriptures Hebrew Bible / morphhb

Şu anda kalıcı türetilmiş ana veri katmanı olarak kullanılmamaktadır; vendor kaynağı sabit commit ile tanımlanmıştır. Projenin lemma/morfoloji katmanı **CC BY 4.0**, WLC metni ise proje beyanına göre public domain'dir.

## 5. Açık Kuran

Açık Kuran API kaynak kodu **CC BY-NC-SA 4.0** olarak yayımlanmıştır. Ancak Açık Kuran'ın asıl veritabanı bu repoya alınmış değildir. Şu anda yalnız metodolojik/online yardımcı kaynak olarak kayıtlıdır; veri snapshot'ı yoktur.

## 6. QuranMorph

QuranMorph veri dosyası bu repoda **bulunmuyor**. Parser/validator altyapısı bulunması, veri setinin repoya dahil edildiği anlamına gelmez. Erişim ve yeniden dağıtım koşulları ayrıca doğrulanmadan veri eklenmeyecektir.

## Proje kodu ve belgeleri

Bu repo için henüz repo-geneli bir proje lisansı seçilmemiştir. Üçüncü taraf veri lisansları, kullanıcı tarafından yazılmış script/belge lisansından ayrı tutulmalıdır. Bir proje lisansı seçilene kadar üçüncü taraf veri üzerinde hak iddiasında bulunulmaz.

## Değişmez kurallar

1. Kaynağı/lisansı doğrulanmamış veri kalıcı ham kaynak olarak eklenmez.
2. Ham Tanzil ve QAC kaynak dosyaları yerinde değiştirilmez.
3. Türetilmiş dosyalarda kaynak/provenance bağı koparılmaz.
4. Bir klasör veya validator'ın varlığı, o veri katmanının dolu ya da bilimsel olarak doğrulanmış olduğu anlamına gelmez.
