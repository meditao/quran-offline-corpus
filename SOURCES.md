# Kaynak Kayıtları

Bu dosya repoda gerçekten bulunan kaynaklarla yalnız aday/yardımcı kaynakları ayırır. Lisans ayrıntıları için `LICENSES.md` esas kayıttır.

## 1 — Tanzil Quran Text v1.1 — PRESENT

- Sağlayıcı: Tanzil Project
- Sürüm: 1.1, 12 Şubat 2021
- Kaynak: https://tanzil.net/download/
- Repo yolları: `01_raw/tanzil/`
- Rol: birincil Arapça metin
- Lisans bildirimi: CC BY 3.0 + Tanzil'in ek verbatim/değiştirmeme kullanım şartı
- Durum: ham dosyalar mevcut; SHA-256 değerleri validator içinde sabitlenmiş ve her push/PR'da doğrulanır.
- Uyarı: Tanzil Uthmani v1.1 kelime tokenizasyonu QAC v0.4 ile birebir aynı değildir. `tanzil_qac_alignment.csv` kullanılmalıdır.
- Durak işaretli sürüm (`01_raw/tanzil/quran-uthmani-durak.txt`, `marks=true`): ayrı ham dosya, `08_scripts/fetch_tanzil_marks.py` ile indirilir ve kaynak adresi + sha256 `manifest.local.json`'a işlenir. Çalışma masasında yalnız sekte için kullanılır; diğer durak işaretleri geleneksel — yorum içerebilir. Durum: kurulu (sha256 `7f30c647331a…`); oturumdan tanzil.net 403 döndüğü için kullanıcı yükledi, `--dosyadan` denetimleriyle kabul edildi (manifest `edinim` alanı).

## 2 — Quranic Arabic Corpus v0.4 — PRESENT

- Sağlayıcı: Quranic Arabic Corpus / Kais Dukes
- Kaynak: https://corpus.quran.com/download/
- Repo yolu: `02_morphology/qac/quranic-corpus-morphology-0.4.txt`
- Rol: birincil morfoloji / lemma / kök / segment annotation katmanı
- Lisans: QAC annotation bildirimi GNU GPL; verbatim/source-attribution şartları dosya ve resmî indirme sayfasında korunur.
- Tarihsel metin katmanı: QAC dosyası üzerine kurulduğu Tanzil Uthmani v1.0.2 için CC BY-ND 3.0 Unported bildirimi taşır. Bu, repodaki güncel Tanzil v1.1 dosyalarının lisans kaydı değildir.
- Sabit SHA-256: `a1d12923815341face765083805d2148ed2d9f5cc3f7d6665219d887675d8c46`
- Doğrulanan yapı: 128.219 segment / 77.429 kelime konumu / 6.236 ayet / 114 sûre
- Sağlam parser ile distinct ROOT: 1.642

## 3 — Open Scriptures Hebrew Lexicon — PRESENT AS DERIVED INDEX

- Repo: https://github.com/openscriptures/HebrewLexicon
- Sabit commit: `04_lexicons/semitic/VENDOR_LOCK.json`
- Lisans: CC BY 4.0
- Üretilmiş çıktı: `04_lexicons/generated/hebrew_lexical_index.tsv`
- Manifest: `04_lexicons/generated/hebrew_lexical_index.manifest.json`
- Rol: İbranice lexical/etimolojik araştırma indeksi
- Uyarı: Bu indeks otomatik olarak Kur'an kökleriyle kognat eşlemesi yapmaz.

## 4 — Open Scriptures Hebrew Bible / morphhb — PINNED CANDIDATE

- Repo: https://github.com/openscriptures/morphhb
- Sabit commit: `04_lexicons/semitic/VENDOR_LOCK.json`
- Rol: gerektiğinde İbranice metin içi lemma/morfoloji kontrolü
- Durum: ana türetilmiş analiz katmanı henüz üretilmiş değildir.

## 5 — Açık Kuran — OPTIONAL ONLINE CROSS-CHECK

- Site: https://acikkuran.com
- Kaynak kodu: https://github.com/acik-kuran/acikkuran-api
- API kod lisansı: CC BY-NC-SA 4.0
- Rol: kök sayfaları / Türkçe araştırma arayüzü / yardımcı kontrol
- Durum: asıl veri tabanı bu repoda yoktur; eski `api.acikkuran.com` REST endpoint'i çekirdek workflow'dan çıkarılmıştır.
- İlke: erişilebilir olduğunda yardımcı kontrol sağlar; çekirdek analiz için zorunlu değildir.

## 6a — mustafa0x/quran-morphology — LOCAL ONLY (yerel/)

- Kaynak: https://github.com/mustafa0x/quran-morphology, commit `8f38b39016824284f9ed16ae15069ff9102c4acf` (2018-06-19)
- Dosya: `quran-morphology.txt`, sha256 `742bfac59941b2cb09736d5b7aae694af50792261fb8450cbf6afafcc340645f`, LF satır sonu
- Niteliği: QAC v0.4 çatalı (Arapça harf, düzeltilmiş kök/lemma, farklı segmentasyon). 77.429 kelime konumu, 130.030 segment, 1.651 kök.
- Lisans: depoda lisans dosyası yok; QAC v0.4 kullanım şartı değiştirilmiş kopyayı yasaklar. Bu yüzden veri depoya işlenmez; `09_calisma_masasi/yerel/quran-morphology/` altına `python -m tezgah kur quran-morphology` ile kurulur (commit ve sha256 sabit).
- Rol: ikinci annotation katmanı — çapraz kontrol, delil değil. Rapor: `03_indices/audits/qac_quranmorphology.md`.
- SinaLab QuranMorph (§6) ile karıştırılmamalıdır.

## 6 — QuranMorph — INFRASTRUCTURE ONLY

- Proje: SinaLab / Birzeit University
- Makale: Akra, Hammouda & Jarrar (2025), *QuranMorph: Morphologically Annotated Quranic Corpus*
- Rol: gelecekte QAC lemma/POS annotationlarını bağımsız sınamak
- Durum: veri dosyası repoda yoktur. Yalnız validator/cross-check scriptleri vardır.
- İlke: izinli veri dosyası edinilmeden 'QuranMorph ile doğrulandı' denmez.

## 7 — Comprehensive Aramaic Lexicon (CAL) — ONLINE REFERENCE

- Site: https://cal.huc.edu/
- Rol: Aramice tarihsel kognat kontrolü
- Durum: toplu offline snapshot yok; yeniden dağıtım koşulları teyit edilmeden veri kopyalanmaz.

## 8 — SEDRA / Beth Mardutho — ONLINE REFERENCE

- Site: https://sedra.bethmardutho.org/
- Rol: Süryanice lexical/kognat kontrolü
- Durum: toplu offline snapshot yok; kaynak bazlı telif koşulları nedeniyle seçici referans.

## Veri olgunluğu özeti

- **Hazır ve CI ile korunuyor:** Tanzil v1.1, QAC v0.4, QAC türetilmiş indeksleri, Tanzil↔QAC alignment.
- **Mevcut yardımcı indeks:** Open Scriptures Hebrew Lexicon türevi İbranice indeks.
- **Şema var, veri yok:** `cognates.tsv` kognat kayıtları, QuranMorph, çeviri katmanı, analiz katmanı.
- **Online/opsiyonel:** Açık Kuran, CAL, SEDRA.

## Metodolojik sıra

Kur'an metni → QAC morfoloji/kök/lemma → kendi yeniden üretilebilir dağılım hesaplarımız → mevcutsa bağımsız annotation/sözlük kontrolü → filolojik olarak incelenmiş Sami kognatlar → yorum/sentez.
