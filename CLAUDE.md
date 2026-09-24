# Kur'an Çalışma Masası — Claude Code talimatı

Bu dosya `quran-offline-corpus` deposunun kökünde durur. Claude Code her oturumda önce bunu okur.

## 1. Amaç

Kavramları Kur'an'ın kendi verisinden tanımlamak için tek bir çalışma ortamı: tarama, okuma, kavram dosyası ve tez sınama. Hedef doğruyu bulmaktır. Geleneksel okumayı doğrulamak da çürütmek de hedef değildir; bulgular "lehine/aleyhine" diye çerçevelenmez.

Çalışma masası depoya **yeni bir katman** olarak eklenir, mevcut katmanlara dokunmaz:

```
09_calisma_masasi/
  tezgah/            Python paketi (tek giriş noktası: python -m tezgah)
    veri.py          yükleme, dizinler, kurulum denetimi
    tara.py          kök / lemma / etiket / kalıp sorguları, sayım, dağılım
    okuma.py         ayet görünümü (okunuş + kelime çözümlemesi + çalışma çevirisi)
    kavram.py        kavram dosyası işlemleri
    tez.py           tez sınama kaydı
    kayit.py         her sorgunun kaynak / birim / komut kaydı
    ikincil/         lane.py, sami.py — yalnız hipotez katmanı
  testler/           sağlama testleri (§6) — her değişiklikten sonra çalışır
  kavramlar/         ara çalışma dosyaları (olgunlaşınca 07_analyses'e taşınır)
  yerel/             .gitignore — lisansı doğrulanmamış veya dağıtılamaz veri
```

Kural: `01_raw`, `02_morphology`, `03_indices`, `04_lexicons` **salt okunur**. Çalışma masası bunlardan okur, bunlara yazmaz. Yeni türetilmiş veri gerekiyorsa `08_scripts` altında ayrı bir betikle üretilir.

## 2. Değişmez ilkeler

1. **Yalnız Kur'an verisi delildir.** Hadis, tefsir, meal, Lane ve Sâmî katmanı delil değildir; anılırlarsa ekranda ve raporda "hipotez / ikincil" etiketi taşırlar. Zincir tek yönlüdür: dış katman hipotez üretir, korpus sınar, sonuç korpus bulgusuyla yazılır.
2. **Hafızadan sayı ve ayet yazılmaz.** Her sayı ve her ayet referansı bir sorgunun çıktısıdır. Sorgu çalışmadıysa rapor bunu söyler.
3. **Her sayının birimi yazılır:** ayet / sûre / kelime konumu / segment. Farklı birimler ve farklı korpusların sayıları aynı tabloda toplanmaz.
4. **Boş çıktı yokluk delili değildir.** "Kur'an'da X yok" için eşanlamlı kökler ve kavramı kelimesiz kuran ayetler de taranmış olmalıdır; aksi hâlde "şu sorguyla bulunmadı" yazılır.
5. **Kavram daraltma yasağı.** İman, salât, zekât gibi kavramlar pasif zihinsel kabule veya ritüele otomatik indirgenmez. Önce kalıp çıkarılır, sonra anlam tartışılır. Meal karşılığı veri değildir.
6. **Sonuç iki eksende yazılır** (tez.py ve kavram.py bunu zorunlu alan yapar):
   - Mantıksal durum: Destekleniyor · Yalnız uyumlu · Destek gösterilemedi · Belirsiz · Çelişiyor
   - Delil derecesi: Sağlam · Muhtemel · Spekülatif
   "Yalnız uyumlu" asla "destekleniyor" diye yazılmaz.
7. **Kur'an dışı sınıflandırmalar varsayılan değildir.** Mekkî/Medenî ve nüzul sırası geleneksel veridir; kullanılırsa ayrı, etiketli filtre olarak.
8. **Sunum:** Arapça harf değil, Latin harfli okunuş + Türkçe anlam. Kök ayrık Latin yazılır (`s-l-v`). Komut satırında kök Arapça veya Buckwalter girilir; araç Latin girişi reddeder, boş sonuç üretmez.

## 3. Veri katmanları ve statüleri

| katman | kaynak | depoda | statü |
|---|---|---|---|
| Arapça metin | Tanzil Uthmani v1.1 | `01_raw/tanzil` | metin |
| morfoloji (**kanonik**) | QAC v0.4 | `02_morphology/qac`, `03_indices` | delil |
| morfoloji (ikinci annotation) | mustafa0x/quran-morphology | yok → §5 | çapraz kontrol |
| okunuş | fawazahmed0/quran-api `ara-quran-la` | yok → `yerel/` | aktarım, delil değil |
| kurumsal meal | aynı kaynak, `tur-diyanetisleri` | yok → `yerel/` | sınanan okuma, delil değil |
| çalışma çevirisi | kullanıcı | `kavramlar/` | kullanıcının yorumu |
| Lane | LexiconDatabase v1.0.9 | yok → `yerel/` | hipotez |
| İbranice | BDB index | `04_lexicons/generated` | hipotez |
| Süryanice | SEDRA 3 | yok → `yerel/` | hipotez |

**Meal görünümü:** Varsayılan kapalıdır. Açıldığında "kurumsal okuma — sınanan, delil değil" etiketiyle, çalışma çevirisinin **altında** gösterilir.

## 4. Kanonik korpus kararı

Kanonik korpus: **QAC v0.4** (depodaki denetimli veri).

- Kök/lemma sıklığında varsayılan birim **kelime konumu**dur (`06_methodology/counting_units.md`). Aynı kelimede tekrar eden kök bir kez sayılır.
- Segment düzeyi sorgular (ön ek, iyelik eki, bab etiketi) ayrıca desteklenir ve çıktıda "segment" diye işaretlenir.
- Tanzil ile QAC arasında kelime düzeyinde doğrudan eşleştirme yapılmaz; `tanzil_qac_alignment.csv` kullanılır.
- İyelik eki ayrı segmenttir. İsmin etiketlerinde zamir aranmaz, sonraki segmente bakılır.
- `--etiket` tam eşleşmedir. Alt-dize eşleşmesi (`VF:1` → `VF:10`, `DEF` → `INDEF` sızıntısı) yalnız açık bayrakla yapılır ve çıktıda uyarı basılır.
- Bab etiketi hem fiile hem türemiş isme yapışır; bab tablosunda "fiil" ve "isim" ayrı sütunlardır.

## 5. İkinci annotation katmanı (quran-morphology)

`counting_units.md` §6'daki açık konu (130.030 birim ↔ 128.219 segment) bu katmanla kapatılır:

- İki korpus kelime konumunda birebir aynıdır (77.429); segmentasyon ve kök envanteri farklıdır (1.651 ↔ 1.642).
- `08_scripts/crosscheck_qac_quranmorphology.py` konum bazında karşılaştırır ve `03_indices/audits/` altına rapor yazar.
- Çalışma masasında `--capraz` bayrağı bir kökün iki korpustaki sonucunu **yan yana**, ayrı tablolarda gösterir. İki sayının aynı çıkması doğrulama sayılmaz; kök atamasının farklı çıktığı yerler ayrıca listelenir.

## 6. Sağlama testleri

`testler/` altında. Kurulumdan ve her kod değişikliğinden sonra çalışır. Tutmazsa iş durur, rapor verilir.

QAC v0.4 (depodan ölçüldü, 24.09.2026):

| sorgu | beklenen |
|---|---|
| QAC dosyası sha256 | `a1d12923815341face765083805d2148ed2d9f5cc3f7d6665219d887675d8c46` |
| ayet / kelime konumu / segment | 6.236 / 77.429 / 128.219 |
| benzersiz kök | 1.642 |
| `Slw` (s-l-v) | 99 kelime konumu / 90 ayet / 37 sûre |
| `fTr` (f-t-r) | 20 / 19 / 17 |
| `rwH` (r-v-h) | 57 / 52 / 40 |
| `qdr` (q-d-r) | 132 / 121 / 58 |
| `gfr` (g-f-r) | 234 / 202 / 56 |
| `Amn` (e-m-n) | 879 / 723 / 77 |

Ayrıca: araç, `root_index.csv` ile kendi hesabının bütün kökler için aynı çıktığını doğrular.

## 7. Modüller ve kabul ölçütleri

**tara.py** — `sayim`, `dagilim` (tür / lemma / bab / iyelik / sûre), `kok`, `lemma`, `etiket`, `birlikte` (ortak geçiş), `kalip` (ardışık segment deseni), `kokler`. Kabul: §6 testleri geçer; her çıktının sonunda kayıt satırı (§8) vardır.

**okuma.py** — `ayet 2:3`: okunuş, kelime kelime kök/lemma/biçim, çalışma çevirisi, isteğe bağlı meal. Kabul: ayet referansı QAC ve Tanzil'de aynı ayete düşer.

**kavram.py** — bir kavram için dosya açar ve `07_analyses/README.md`'deki standart düzeni izler: araştırma sorusu → Aşama 1 kök/morfoloji → Aşama 2 sentaks → Aşama 3 bağlam ağı → kritik ayetler → karşı örnekler/falsifikasyon → Sâmî (isteğe bağlı) → sentez → kavram kartı. Sayım bölümleri elle yazılmaz; sorgudan üretilir ve kaydıyla birlikte gömülür. Ayet başına çalışma çevirisi alanı vardır.

Anlam önerisi kaydedilirken şu alanlar boş bırakılamaz:
- iç-tanım var mı (metin terimi kendi içinde açıyor mu)
- falsifikasyon: "bu öneri doğru olsaydı hangi ayet onu çürütürdü" ve fiilen bulunan ayetler
- muhalif okumanın en güçlü hâli
- dışarıda bırakılan örneklem: öneri hangi kullanımlardan kuruldu, hangilerine sonradan uygulandı

**tez.py** — tez tek cümleyle dondurulur; tanımlar ve karşı örnek havuzu **taramadan önce** kaydedilir ve sonradan değiştirilemez (değişirse yeni sürüm açılır, eskisi silinmez). Her bulgu eksen etiketi taşır (tanımlayıcı/normatif, oluşum/sorumluluk vb.); farklı eksendeki bulgu "çelişen" rafına konamaz. Kullanıcının tez ifadesi kendiliğinden güçlendirilmez.

**ikincil/** — Lane ve Sâmî çıktıları her satırda "hipotez" etiketi taşır. Tek dilde kognat vuruşu tek başına raporlanmaz. Lane'in ك harfinden sonraki bölgesinde "Lane'de yok" argümanı üretilmez.

## 8. Kayıt satırı

Her sorgu çıktısının ve her kavram dosyası bölümünün sonunda:

```
Kaynak      : QAC v0.4 | + quran-morphology | + Lane | + Sâmî
Sayım birimi: kelime konumu | segment | ayet | sûre
Sorgu       : çalıştırılan tam komut
Veri izi    : kaynak dosyanın sha256'sının ilk 12 hanesi
Durum       : çalıştırıldı | çalıştırılmadı
```

## 9. Lisans kuralları

- Tanzil metni değiştirilmez; normalizasyon ayrı türetilmiş çıktıdır.
- QAC telif bloğu korunur.
- Okunuş ve meal katmanlarının lisansı doğrulanana kadar `yerel/` altında kalır ve depoya işlenmez. Depo herkese açıktır.
- SEDRA: değiştirilmiş dosya dağıtılmaz. Sonuç yayımlanırsa atıf eklenir.

## 10. Aşamalar

| aşama | içerik | durum |
|---|---|---|
| 0 | depo incelemesi, bu dosya | tamam |
| 1 | `veri.py` + `tara.py` + `kayit.py` + sağlama testleri | uygulandı — onay bekliyor |
| 2 | `okuma.py` + `kavram.py` (meal `yerel/`'e kurulur) — **açık konu:** okunuş fawazahmed0 yerine Tanzil Arapçasından Türkçe transliterasyon kurallarıyla üretilecek (İngilizce tarzı yazım "alssalata" gibi harf ayrımlarını kaybediyor; kendi kuralımız denetlenebilir ve lisans sorunu taşımaz). Tanzil işaretleri: U+064B–0654, 0670, 0671 (vasl elifi), 06DC–06ED (Osmanî özel işaretleri) | |
| 3 | `tez.py` | |
| 4 | ikinci annotation katmanı ve çapraz denetim raporu | |
| 5 | `ikincil/` (Lane, Sâmî) | |
| 6 | yerel web arayüzü (aynı paketin üstünde, ayrı mantık yok) | |

Her aşama sonunda: testler çalışır, sonuç kullanıcıya sayılarla raporlanır, bir sonraki aşama için onay alınır.

## 11. Claude Code çalışma kuralları

- Ham veri katmanlarına yazma. Silme gerekiyorsa önce kapsamı sor.
- Bir sayı raporlamadan önce onu üreten komutu çalıştır; önceki çıktıyı hatırlamak doğrulama değildir.
- Test kırılırsa testi değiştirerek geçirme. Önce sebebi bul ve raporla.
- Bulgu kullanıcının beklentisiyle çelişiyorsa yumuşatmadan yaz.
- Kod yorumları ve çıktılar Türkçe.
