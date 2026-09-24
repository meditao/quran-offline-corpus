# Quran Offline Corpus

Bu depo, Kur'an merkezli dilsel ve kavramsal analizler için denetlenebilir, sürümlenebilir ve mümkün olduğunca offline çalışan açık bir araştırma arşividir.

Amaç yalnız veri depolamak değildir. Bir kavram hakkında ulaşılan sonucun hangi kök, morfoloji, ayet, bağlam ve karşı örneklerden çıkarıldığını dışarıdan bir okuyucunun adım adım takip edebilmesi hedeflenir.

## Buradan başlayın

Klasör listelerine erişemeyen tarayıcılar ve yapay zekâ araçları için önemli dosyalara doğrudan bağlantılar:

- [İman — ayrıntılı, aşamalı ana analiz](07_analyses/roots/Iman-analysis.md)
- [İman — kısa kavram kartı](07_analyses/roots/Amn-concept-card.md)
- [Mümin — kısa kavram kartı](07_analyses/roots/Mumin-concept-card.md)
- [Amn / أ م ن — Aşama 1: kök ve ilk Kur'an içi profil](07_analyses/roots/Amn-quran-internal-stage1.md)
- [Amn — Aşama 2: fiil sentaksı](07_analyses/roots/Amn-quran-internal-stage2-syntax.md)
- [Amn — Aşama 3: bi- kullanımları](07_analyses/roots/Amn-quran-internal-stage3-bi.md)
- [Amn — Aşama 4: īmān isim kullanımı](07_analyses/roots/Amn-quran-internal-stage4-iman-noun.md)
- [Amn — Aşama 5: muʾmin profili](07_analyses/roots/Amn-quran-internal-stage5-mumin-profile.md)
- [Analiz katmanı ve kayıt standardı](07_analyses/README.md)
- [Metodoloji](06_methodology/README.md)
- [Sayım birimleri](06_methodology/counting_units.md)
- [Kök sayım politikası](06_methodology/root_count_policy.md)
- [Kaynak politikası](06_methodology/source_policy.md)
- [Kaynak envanteri](SOURCES.md)
- [Lisanslar](LICENSES.md)

## Analizler nasıl yazılır?

Her nihai kavram kaydı, mümkün olduğunca aynı düzeni izler:

1. Kısa sonuç: kavramın sade tanımı.
2. Aşama 1 — kök, morfoloji ve biçimler.
3. Aşama 2 — sentaks ve temel kullanım kalıpları.
4. Aşama 3 — Kur'an içi bağlam ve kavram ağı.
5. Kritik ayetler — ayet numarası, tam Arapça metin, sade/kavramsal Türkçe çeviri ve ayetin neyi kanıtladığı.
6. Karşı örnekler ve falsifikasyon — yanlış veya fazla geniş yorumların ayetlerle sınanması.
7. Sonuç — kanıt zincirinden çıkan nihai tanım.
8. Kavram kartı — kısa, kolay okunur özet.

Ara veri, otomatik sayımlar ve TSV/CSV denetimleri araştırmanın kanıt katmanıdır; ana analiz metni ise teknik olmayan bir okuyucunun da anlayabileceği biçimde yazılır.

## Mevcut durum

Çekirdek veri katmanı hazırdır: Tanzil Uthmani v1.1, QAC v0.4 ve yeniden üretilebilir kök/lemma/POS indeksleri.

Analiz katmanı artık aktiftir. İlk ayrıntılı kamuya açık ana analiz İman kavramı için hazırlanmıştır. Amn kök ailesinin teknik aşamaları ve Mümin kavram kartı da bağlantılı kanıt katmanında tutulmaktadır.

İbranice lexical index mevcuttur. İncelenmiş Arapça↔Sami kognat eşlemeleri aşamalı olarak eklenmektedir. QuranMorph ve çeviri katmanları henüz tamamlanmış veri setleri değildir.

Kur'an çalışma masası (`09_calisma_masasi/`, `python -m tezgah`) tamamlanmıştır (Aşama 1–6: tarama, okunuş, ayet görünümü, kavram dosyası, tez sınama, quran-morphology çapraz kontrolü, Lane/Sâmî hipotez katmanı, yerel web arayüzü). Talimat ve ilkeler: [`CLAUDE.md`](CLAUDE.md); kullanım: [`09_calisma_masasi/README.md`](09_calisma_masasi/README.md). Testler Linux ve Windows'ta CI ile çalışır.

Opsiyonel yardımcı kaynak Açık Kuran'dır. Eski REST API çekirdek workflow'un parçası değildir.

## Temel ilke

Ham kaynak verisi, türetilmiş indeksler, sözlük katmanı ve yorum/analiz katmanı birbirinden ayrıdır. Kaynağı ve lisansı doğrulanmamış veri ham korpusa eklenmez. Yorum, ham veri gibi sunulmaz; çıkarımın dayandığı ayet ve veri açıkça gösterilir.

## Dizin yapısı

- `01_raw/` — doğrulanmış Tanzil metni ve metadata
- `02_morphology/` — QAC ve aday bağımsız annotation katmanları
- `03_indices/` — script ile üretilen kök/lemma/POS ve alignment indeksleri
- `04_lexicons/` — İbranice lexical index ve Sami kognat altyapısı
- `05_translations/` — planlanan yardımcı çeviri katmanı
- `06_methodology/` — kaynak, lisans, sayım ve alignment kuralları
- `07_analyses/` — okunabilir kavram/kök/ayet analizleri ve bunların denetim verileri
- `08_scripts/` — doğrulama, sayım, sorgu ve audit scriptleri
- `09_calisma_masasi/` — Kur'an çalışma masası (`tezgah` paketi, sağlama testleri, kavram ve tez kayıtları; lisansı doğrulanmamış veri `yerel/` altında, depoya işlenmez)

## Kaynak hiyerarşisi

1. Arapça metin: Tanzil Uthmani v1.1
2. Morfoloji / kök / lemma: Quranic Arabic Corpus v0.4
3. Kur'an içi dağılım: ham QAC'dan kendi scriptlerimizin ürettiği indeksler
4. Bağımsız kontroller: mevcutsa QuranMorph / Açık Kuran / sözlükler
5. Tarihsel anlam alanı: İbranice → Aramice/Süryanice → diğer Sami dilleri
6. Nihai yorum: yukarıdaki veri katmanlarından ayrı değerlendirilir

## Kritik tokenizasyon kuralı

Tanzil ile QAC aynı ayet anahtarlarını paylaşır fakat kelime tokenizasyonları birebir aynı değildir. `(sûre, ayet)` ortak referanstır; Tanzil↔QAC kelime düzeyi join için `03_indices/generated/tanzil_qac_alignment.csv` kullanılmalıdır. Ayrıntı: [counting_units.md](06_methodology/counting_units.md).

## Offline kök sorguları

```bash
python 08_scripts/query_qac.py --root Slw
python 08_scripts/query_root.py --root Amn
```

Her iki kök sorgu aracı da `--root` biçimini kullanır. `query_root.py` ayrıca varsa incelenmiş Sami kognat kayıtlarını gösterir; sıfır kayıt, “kognat yok” anlamına gelmez.

## Üretilen temel indeksler

`build_qac_indices.py` ham QAC dosyasından `qac_word_annotations.csv`, `root_index.csv`, `lemma_index.csv` ve `pos_index.csv` dosyalarını yeniden üretir. `build_tanzil_qac_alignment.py` ise Tanzil Uthmani v1.1 ile QAC arasındaki ayet-düzeyi kelime sayısı/alignment farklarını yeniden üretir.

## Otomatik bütünlük garantisi

`.github/workflows/core-integrity.yml` her push ve pull request'te Tanzil ve QAC dosyalarının sabit hash ve yapısal kontrollerini yapar, indeksleri yeniden üretir ve commit edilmiş çekirdek çıktıların yeniden üretilen dosyalarla aynı olmasını zorunlu kılar.

Sabitlenmiş QAC v0.4 annotation dosyasında sağlam parser ile 1.642 benzersiz ROOT etiketi vardır. Tarihsel 1.651 sonucu CRLF ve virgül-ayırıcı kaynaklı bir shell-pipeline artefaktı olarak yeniden üretilip belgelenmiştir. Bu sayı, “Kur'an ontolojik olarak tam 1.642 kökten oluşur” iddiası değildir; kullanılan annotation snapshot'ına bağlıdır.

## Lisans

Üçüncü taraf veri koşulları `LICENSES.md` ve `SOURCES.md` içinde ayrı ayrı kaydedilir. Repo-geneli için tek bir lisans seçilmiş değildir.
