# Kaynak Politikası

Bu depo için amaç yalnızca çok sayıda kaynak toplamak değil, hangi verinin hangi iddiayı taşıyabileceğini açıkça ayırmaktır.

## 1. Kanonik Arapça metin

Birincil metin katmanı Tanzil Uthmani v1.1'dir. Dosya kaynaktan alındığı biçimiyle korunur; Arapça karakterlerde, işaretlerde veya ayet metninde elle değişiklik yapılmaz. Normalize edilmiş sürüm gerekiyorsa ayrı türetilmiş çıktı/script üretir.

## 2. Morfoloji ve sözdizimi

Quranic Arabic Corpus v0.4 morfolojik annotation, lemma, kök ve sözdizimsel analiz için ana referans katmanıdır. Bu veri Kur'an metninin kendisi değil, insan yapımı dilsel annotation'dır; hata ve editoryal karar ihtimali taşır.

## 3. Tanzil ↔ QAC hizalama sınırı

Tanzil v1.1 ile QAC v0.4 aynı ayet numaralandırmasını paylaşır, fakat aynı kelime tokenizasyonunu paylaşmak zorunda değildir. Bu nedenle:

- `(sûre,ayet)` güvenli ortak referans anahtarıdır.
- `(sûre,ayet,kelime)` QAC içinde güvenli anahtardır.
- Tanzil ile QAC arasında kelime düzeyi join doğrudan yapılmaz.
- `03_indices/generated/tanzil_qac_alignment.csv` ve ilgili audit raporu kullanılmalıdır.

Özellikle sûre başı besmeleleri ve sürümler arasındaki split/merge farkları kelime pozisyonlarını kaydırabilir.

## 4. Açık Kuran

Açık Kuran kök sayfaları ve Türkçe araştırma arayüzü **opsiyonel yardımcı çapraz kontrol** kaynağıdır. Eski API endpoint'i kullanılabilir bir offline veri kaynağı değildir ve asıl veri tabanı bu repoda yoktur.

Açık Kuran'a erişilememesi veya snapshot bulunmaması çekirdek analizi durdurmaz. Kök anlamı cümleleri tek başına nihai etimolojik delil sayılmaz.

## 5. QuranMorph

QuranMorph için parser/validator altyapısı vardır, fakat veri dosyası bu repoda yoktur. Bu nedenle mevcut durumda QAC'a karşı aktif bağımsız morfoloji kontrolü sağlıyor gibi sunulmaz. Veri izinli kanaldan edinilirse ikinci annotation korpusu olarak devreye alınacaktır.

## 6. Sami dil katmanı

İbranice offline lexical index mevcuttur; ancak `04_lexicons/semitic/cognates.tsv` şu anda filolojik olarak incelenmiş kognat kayıtlarıyla doldurulmuş değildir. Dolayısıyla Sami katmanı bugün için **altyapı + kaynak indeksi** düzeyindedir, tamamlanmış kognat veri tabanı değildir.

Kognat eşlemesi otomatik biçim benzerliğiyle yapılmaz; düzenli ses denklikleri, tarihsel ilişki ve semantik süreklilik aranır.

## 7. Ham veri ve yorum ayrımı

- `01_raw`: dış kaynaktan aynen alınmış metin/veri
- `02_morphology`: dış annotation veya belgelenmiş kopya
- `03_indices`: script ile hesaplanan sonuçlar
- `04_lexicons`: sözlük/kognat kaynakları
- `07_analyses`: yorum ve sentez

Bir yorum hiçbir zaman ham veri alanına yazılmaz.

## 8. İddia sınıfları

- **Doğrudan veri:** ayette bulunan biçim, kök/lemma etiketi, frekans, dağılım
- **Türetilmiş bulgu:** script ile hesaplanan eşdizim, oran, ağ, bağlam kümesi
- **Dilbilimsel yorum:** sentaks, semantik alan, olası kök anlamı
- **Tefsir/sentez:** Kur'an içi ağdan çıkarılan kavramsal sonuç

## 9. Çapraz doğrulama

Kritik bir kavram için çekirdek akış:

1. Tanzil üzerinden ayet metnini sabitle.
2. QAC üzerinden kök/lemma/morfoloji adaylarını çıkar.
3. Kendi scriptlerimizle dağılımı yeniden hesapla.
4. Mevcutsa bağımsız kaynaklarla (QuranMorph, Açık Kuran, sözlükler) çapraz kontrol yap.
5. Uyuşmazlığı karantinaya al ve elle incele.
6. Sonucu kanıt gücünü belirterek raporla.

Bağımsız yardımcı kaynağın bulunmaması, QAC'tan gelen bir annotationı otomatik olarak 'kesin' yapmaz; yalnızca çapraz doğrulama yapılmadığı açıkça belirtilir.

## 10. Tekrarlanabilirlik

Her sayısal çekirdek iddia script tarafından yeniden üretilebilir olmalıdır. `.github/workflows/core-integrity.yml` her push ve pull request'te sabit kaynak hashlerini doğrular, QAC indekslerini ve Tanzil↔QAC alignment raporunu yeniden üretir ve commit'li sonuçlarla byte düzeyinde karşılaştırır.
