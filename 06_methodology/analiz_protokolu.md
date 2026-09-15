# Kur'an Analiz Protokolü — v2.1

**Konumu:** `06_methodology/analiz_protokolu.md`  
**Kapsamı:** tek bir kavram, kök, ayet, pasaj veya tezin Kur'an merkezli ve denetlenebilir biçimde nasıl analiz edileceği.

Bu belge, çalışmanın **ana analiz protokolüdür**. Amaç bir anlamı baştan doğru kabul edip ona delil toplamak değil; Kur'an içi veriden hareketle anlamı kurmak, karşı örneklerle sınamak ve veri ile yorumu açıkça ayırmaktır.

**Sürüm notu (v2.1):** Protokol, `f-r-d` kökü üzerinde uçtan uca pilot olarak sınandı. Pilot sonucunda kapalı örneklemin hipotezden önce kilitlenmesi, aynı kök altında ayrı sözlüksel dalların mümkün olması ve “kanıtlayıcı örnek / yalnız uyumlu örnek” ayrımı açık kurala dönüştürüldü.

Arşiv, kavram kartı, versiyon defteri, hipotez defteri ve periyodik bakım bu belgenin konusu değildir. Tamamlanmış analizler `07_analyses/` altında durur. Ham veri, yorum ve yayımlanmış sonuç birbirine karıştırılmaz.

---

## 0. Ana ilkeler

1. **Kur'an içi kullanım birincil delildir.** Kök, morfoloji, sentaks, bağlam, dağılım, iç-tanım, karşıtlık ve kavram ağı birlikte değerlendirilir.
2. **Geleneksel anlam başlangıç varsayımı değildir.** Ne otomatik doğru ne otomatik yanlıştır; en güçlü biçimiyle ayrıca sınanır.
3. **Kesin veri ile yorum ayrılır.** Sayım, biçim ve cümle yapısı veri; bunlardan çıkarılan anlam hipotezdir.
4. **Karşı örnek anlamı daraltır.** Bir aykırı kullanım açıklanıp geçilmez; gerekirse tanım revize edilir.
5. **Dış dil verileri destekleyici kontroldür.** Lane, klasik sözlükler, İbranice ve Süryanice anlamı tayin etmez; yalnız hipotez üretir veya tarihsel olasılığı kontrol eder.
6. **Yokluk iddiası ağır bir iddiadır.** Tek kök taramasıyla "Kur'an'da yok" denmez.
7. **Anlam ile işlev ayrılır.** Bir kavramın sonucu, etkisi veya hükmü kelimenin sözlük anlamı yerine konmaz.
8. **Tek ayetten genel tanım kurulmaz.** Tanım bütün dağılımı karşılamalıdır.
9. **Sonuçtan önce kapsam yazılır.** Bir önerme hangi ayetler, hangi biçimler ve hangi bağlamlar için geçerliyse o sınır belirtilir.
10. **Analiz aşamalıdır.** Sohbet ortamında varsayılan çalışma biçimi her ana aşamanın sonunda durmak ve kullanıcıdan `devam` onayı almaktır. Kullanıcı açıkça kesintisiz çalışma isterse bu kural kaldırılır.

---

## 1. İki veri kaynağı

|  | depo (`quran-offline-corpus`) | beceri (`kuran-kok-analizi`) |
|---|---|---|
| morfoloji | QAC v0.4 (hash sabit) | `mustafa0x/quran-morphology` |
| segment | 128.219 | 130.030 |
| kelime konumu | 77.429 | 77.429 |
| benzersiz `ROOT` | 1.642 | 1.651 |
| kök yazımı | Buckwalter | Arapça |
| yan katman | Tanzil, Açık Kuran, İbranice indeks | Lane (47.919 madde), BDB + SEDRA |
| üretim | script + CI (`core-integrity.yml`) | her oturumda yeniden kurulur |

### 1a. Ölçülmüş ilişki

Aşağıdakiler protokol hazırlanırken iki dosya üzerinde fiilen hesaplanmıştır.

- **Kelime konumu düzeyinde iki kaynak birebir aynıdır: 77.429 / 77.429.** Ortak anahtar `(sûre:ayet:kelime)`. İki kaynak bu anahtarla birleştirilebilir.
- **Segment düzeyinde aynı değildir.** 130.030 ile 128.219 toplanamaz, biri diğerinin yerine kullanılamaz, oran paydası olarak karıştırılamaz.
- **Kök envanteri farklıdır.** Hemze yazımı nötrlendiğinde 1.638 kök ortaktır. Yalnız becerinin envanterinde olan 13 kök çoğunlukla dörtlü kök veya özel addır (`برزخ`, `لؤلؤ`, `نمرق`, `قرش`, `سبأ`, `طمأن`, `رمض`, `زرب`, `مرو`, `ندي`, `أدم`, `أون`, `هلم`). Yalnız QAC'ta olan 4 kök: `طمن`, `معن`, `ندو`, `نوس`.

### 1b. 1.651 sayısı — iki farklı sebep, aynı sayı

Deponun `root_count_policy.md` dosyası 1.651'i, QAC dosyasındaki CRLF satır sonu ve virgül-ayırıcı hatasının ürettiği bir sayım artefaktı olarak açıklar. Aynı dosyada kırılgan sayım yeniden üretildiğinde 1.651, sağlam parser'la 1.642 çıkar.

**Becerinin 1.651'i bu artefakt değildir.** Beceri kaynağında gerçekten birbirinden farklı 1.651 Arapça kök dizgisi bulunur. İki ayrı yoldan aynı sayıya varılması rastlantıdır.

Sonuç: **beceri kurulumunun "1.651 kök" denetim satırı, depo sayısını doğrulamaz.** İki ayrı kök envanteri vardır; hangisinin kullanıldığı her analizde yazılır.

### 1c. Kaynak kuralı

1. **Yayımlanan her sayı depodan gelir.** Depo hash sabitli, script ile yeniden üretilebilir ve CI ile denetlenir. `07_analyses/` altına yazılan bir rakamın dayanağı `08_scripts/` altındaki bir çalıştırma olmalıdır.
2. **Beceri hızlı çalışma katmanıdır.** Keşif, ilk döküm, Lane ve Sâmî sorgusu için kullanılır. Beceriden çıkan bir sayı yayımlanacaksa depoda yeniden üretilir.
3. **İkisinin uyuşması bağımsız doğrulama değildir.** Her ikisi de QAC soyundan gelir; uyuşma boru hattını doğrular, kök atamasını değil. Gerçek bağımsız katman QuranMorph'tur ve depoda henüz yoktur (`source_policy.md` §5). Tartışmalı bir kök ataması için "iki araç da aynı diyor" yazılmaz.
4. **Sayım birimi her tabloda yazılır:** kelime konumu / segment / ayet / sûre (`counting_units.md`). Birimsiz sayı kanıt değildir.
5. Tanzil ile QAC arasında **kelime düzeyinde doğrudan join yapılmaz**; ortak anahtar `(sûre:ayet)`tir, kelime eşlemesi için `tanzil_qac_alignment.csv` kullanılır.

---

## 2. Girdi türünü ve araştırma sorusunu ayır

| tür | işareti | işlem |
|---|---|---|
| **SORU** | "nedir", "aynı mı", soru işareti | Cevap aranır; doğru kavramı bulmak analistin işidir |
| **ARA CÜMLE** | "sanırım", "galiba", laf arası | Veri sayılmaz; gerekirse hipotez adayı olarak not edilir |
| **TEZ** | "şunu test et", açık formülasyon | Tez dondurulur ve §8'deki test akışı uygulanır |

Varsayılan **SORU**'dur. Soru işareti taşıyan cümle tez değildir.

**Sorunun kelimesi ile kastı ayrıdır.** Bir kelimeyi tarayıp "bu kavram metinde yok" demek cevap değil, cevabın reddidir. Kullanıcının kastını karşılayan Kur'an içi kavram veya yapı bulunmaya çalışılır.

Analize başlamadan önce tek cümlelik bir **araştırma sorusu** yazılır. Gerekirse ayrıca şu dört sınır kaydedilir:

- analiz birimi: kök / lemma / türev / ayet / pasaj / kavram / tez,
- kapsam: bütün Kur'an / belirli sûre / belirli pasaj,
- incelenecek karşı kavramlar,
- başlangıçta karantinaya alınacak dış varsayımlar.

**Karantina ilkesi:** Geleneksel terim, fıkıh kategorisi, tefsir kalıbı veya modern kavram başlangıçta yalnız aday açıklamadır. Kur'an içi veri onu doğrulayana kadar tanımın içine sokulmaz.

**Eksen denetimi:** Çelişki iddiası için iki önermenin aynı eksende olması şarttır. Tanımlayıcı ≠ normatif, oluşum ≠ sorumluluk, kapasite ≠ yükümlülük. Farklı eksendeki iki ifade çelişmez.

---

## 3. Veri kaydı — her analizin başında

Analiz metninin başına dört satır yazılır. Eksiksiz doldurulamıyorsa analiz sayısal iddia taşıyamaz.

```text
Kaynak      : depo QAC v0.4 (hash a1d129…) | beceri | ikisi
Sayım birimi: kelime konumu | segment | ayet | sûre
Sorgu       : çalıştırılan tam komut veya script
Durum       : çalıştırıldı | önceki çıktı kullanıldı | çalıştırılmadı
```

**Durum satırı zorunludur ve gerçeği yazar.** Korpus kurulamadıysa, sorgu çalıştırılmadıysa veya sayı başka bir analizden hatırlandıysa öyle yazılır. Bir önceki sonucu hatırlamak doğrulama değildir. Hafızadan kök listesi, ayet numarası veya sayı yazılmaz.

---

## 4. Ana analiz akışı

Bu bölüm protokolün semantik omurgasıdır. Aşamalar sırayla ilerler; gerekirse önceki aşamaya dönülür.

### Aşama 0 — Ön tanım ve veri sınırı

- Araştırma sorusu tek cümleye indirilir.
- Analiz birimi belirlenir.
- Başlangıç varsayımları karantinaya alınır.
- Hangi verinin "kanıt", hangisinin "yardımcı kontrol" olacağı baştan yazılır.
- Tez varsa karşı örneğin ne sayılacağı taramadan önce belirlenir.

**Çıktı:** Ne araştırdığımız ve neyi henüz varsaymadığımız açık olmalıdır.

### Aşama 1 — Kök, lemma, morfoloji, sentaks ve tam dağılım

Önce ham yapı çıkarılır:

1. kök,
2. lemma/türev ailesi,
3. sözcük türü,
4. fiilse bab, zaman, kişi, çatı,
5. isimse sayı, cinsiyet, belirlik ve yapısal özellikler,
6. edat ve harf-i cer eşlikleri,
7. nesne/özne ve tamlama ilişkileri,
8. tekrar eden sentaktik kalıplar,
9. ayet ve sûre dağılımı.

Bu aşamada **anlam kararı verilmez**; mümkün olduğunca veri dökümü yapılır.

### Aşama 2 — Bağlam, pasaj ve Kur'an içi ağ

Her kritik kullanım için:

- konuşan,
- muhatap,
- zamir mercileri,
- şart ve istisnalar,
- önceki ve sonraki ayetlerle bağlantı,
- pasaj sınırı,
- paralel veya karşıt ayetler,
- aynı kavramın başka köklerle ifade edilip edilmediği

incelenir.

Pasaj sınırı dış konu başlığından değil, metnin kendi işaretlerinden çıkarılır: hitap değişimi, nidâ, zamir değişimi, bağlaç yapısı, fasıla ve konu geçişi.

**İç-tanım en güçlü katmandır.** Metin bir kavramı kendi içinde açıklıyor, karşıtını veriyor veya sonuçlarını yapısal olarak ayırıyorsa bu veri dış sözlükten önce gelir.

### Aşama 3 — Kullanım kümeleri, sözlüksel dal denetimi ve hipotez kilidi

Kullanımlar benzer morfoloji, sentaks ve bağlam özelliklerine göre kümelenir. Amaç, bütün kullanımları zorla tek Türkçe karşılığa indirmek değildir.

Şu sıra izlenir:

1. morfolojik ve sentaktik kümeler çıkarılır,
2. aynı kök altında ayrı **sözlüksel dallar** bulunup bulunmadığı sınanır,
3. kapalı örneklem yapılacaksa **anlam hipotezi kurulmadan önce** hangi kullanımların kapalı kalacağı kilitlenir,
4. açık örneklemden ortak semantik çekirdek adayı kurulur,
5. bağlama bağlı alt-anlamlar belirlenir,
6. mecaz/kurumsallaşmış kullanım varsa ayrıca işaretlenir,
7. tek bir tanım bütün örnekleri karşılamıyorsa anlam alanı dallandırılır.

**Aynı ROOT etiketi tek anlam garantisi değildir.** Aynı üç ünsüz dizgesi altında tarihsel olarak ayrışmış lemma veya sözlüksel dallar bulunabilir. Aykırı bir türev ana çekirdeğe zorla türetilmez; gerekirse ayrı dal olarak karantinaya alınır ve dış dil katmanında ayrıca sınanır.

**Hipotez kilidi:** Geçici çekirdek anlam tek cümleyle yazıldıktan sonra, falsifikasyon tamamlanana kadar sessizce değiştirilmez. Değişiklik gerekiyorsa eski hipotez, onu bozan veri ve yeni hipotez açıkça kaydedilir.

**Anlam ile işlev ayrılır.** "X, Y sonucunu doğurur" ile "X, Y demektir" aynı önerme değildir.

**Dört anlam katmanı karıştırılmaz:**
1. **lexical çekirdek** — kelimenin/türev ailesinin taşıdığı temel semantik alan,
2. **yapısal/sentaktik anlam** — edat, nesne, çatı ve kalıpla oluşan anlam,
3. **bağlamsal/normatif sonuç** — kullanımın o bağlamda doğurduğu yükümlülük, izin, yasak vb.,
4. **sonraki teknik terim** — fıkıh, kelâm veya başka bir kurumsal sistemde kazanılan özel kategori anlamı.

Bir üst katman otomatik olarak alt katmanın sözlük anlamı sayılmaz.

**Meal veri değildir.** Meal, analizden sonra karşılaştırılabilecek bir yorum katmanıdır.

### Aşama 4 — Semantik sınır testi

Bir kavram yalnız "ne olduğu" ile değil, "ne olmadığı" ile de sınanır.

#### 4a. Yakın kavram testi

Aynı veya benzer işlevde kullanılan başka Kur'an kelimeleri belirlenir. Örnek türü ilişkiler:

- `f-r-d` ↔ `k-t-b`,
- `ḥ-r-m` ↔ `j-n-b` / *ijtanibū*,
- `zakāt` ↔ `ṣadaqa` ↔ `infāq`,
- `nabī` ↔ `rasūl`.

Sorular:

- Kur'an neden burada X'i, başka yerde Y'yi seçiyor?
- İki kelime aynı nesneye uygulanabiliyor mu?
- Biri diğerinden daha dar/geniş mi?
- Sentaktik davranışları farklı mı?

#### 4b. Negatif semantik test

Her anlam önerisi için ayrıca şu soru sorulur:

> Bu kelime **ne anlama gelemez?**

Bir geleneksel veya modern karşılık bazı kullanımları karşılamıyor, yakın kavramla gereksiz eşanlamlılık yaratıyor veya başka bir Kur'an kalıbının işlevini üstleniyorsa bu, tanımı daraltan negatif delildir.

Her kritik kullanım ayrıca şu üç sınıftan biriyle etiketlenir:

- **kanıtlayıcı:** önerilen anlamı olumlu biçimde ayırt eder; rakip okumayı daraltır,
- **yalnız uyumlu:** önerilen anlamla çelişmez fakat tek başına onu öğretmez,
- **karşı / baskı noktası:** hipotezi zorlar, kapsam daraltma veya revizyon gerektirebilir.

“Uyuyor” ifadesi tek başına destek kanıtı sayılmaz.

#### 4c. Yokluk testi

"Kur'an'da X yok" denmeden önce:

- doğrudan kök,
- yakın/eşanlamlı kökler,
- aynı kavramı kelimesiz anlatan yapılar,
- karşıt kavramlar

taranır. Bunlar yapılmamışsa yalnız "şu kök/lemma taramasında bulunmadı" denir.

### Aşama 5 — Falsifikasyon ve kapalı örneklem

**Falsifikasyon her analizde zorunludur.** Ön-anlam hipotezi kurulunca sorulur:

> Bu hipotez doğru olsaydı hangi kullanım onu çürütürdü? Böyle bir kullanım var mı?

Aykırı kullanımda üç seçenek vardır:

- hipotez yanlıştır → revize edilir,
- kısmen doğrudur → kapsamı/alt-anlamı daraltılır,
- bağlam yeniden incelendiğinde uyuyordur → neden uyduğu açıkça gösterilir.

Karşı kanıtın açıklanıp geçilmesi yasaktır.

**Dışarıda bırakılan örneklem sınaması:** Tam dağılım ve biçim dökümü görüldükten sonra, fakat **çekirdek anlam hipotezi kurulmadan önce**, kullanımların bir bölümü kapalı örneklem olarak kilitlenir. Tercihen semantik açıdan en aykırı görünen biçimlerden örnek seçilir; hangi ayetlerin kapalı tutulduğu kaydedilir.

Tanım yalnız açık örneklemden kurulur ve sonra kapalı örneklere uygulanır. Ek düzeltme gerektirmeden çalışıyorsa doğrulama gücü artar; her örnek için yeni istisna gerekiyorsa tanım zayıftır.

Kapalı örneklem daha önce anlam tartışmasında kullanılmışsa bu test sonradan varmış gibi gösterilmez. “Kapalı örneklem yapılamadı; tüm örnekler hipotez kurulurken görülmüştü” diye açıkça yazılır. Küçük örneklemde test anlamsızlaşacaksa neden yapılamadığı kaydedilir.

### Aşama 6 — En güçlü alternatif / geleneksel okuma

Yaygın veya geleneksel okumanın **en güçlü hali** kurulur; karikatürü kurulmaz.

Sonra iki okuma aynı veri üzerinde karşılaştırılır:

- hangisi daha fazla kullanımı açıklıyor,
- hangisi daha az istisna gerektiriyor,
- hangisi sentaksı daha iyi açıklıyor,
- hangisi yakın kavramları birbirinden daha iyi ayırıyor,
- hangisi karşı örneklerden sağ çıkıyor?

Bizim okuma muhalif okumayı kanıtla geçemiyorsa "geleneksel yorum yanlış" denmez. Sonuç "iki okuma rekabette" veya "mevcut veri karar vermeye yetmiyor" olabilir.

### Aşama 7 — Dış dil katmanı: Lane ve Sâmî diller

Bu aşama **Kur'an içi anlam hipotezi kurulduktan sonra** çalıştırılır.

- Lane ve klasik sözlükler: olası tarihsel anlam alanlarını ve klasik geleneğin kayıtlarını gösterir.
- İbranice, Aramice/Süryanice ve diğer Sâmî veriler: ortak köken veya eski semantik alan için kontrol sağlar.

Bunların hiçbiri tek başına Kur'an'daki anlamı belirlemez.

Tek yönlü kural:

> dış katman → hipotez üretir / tarihsel olasılığı kontrol eder → Kur'an korpusu sınar → sonuç Kur'an içi veriyle yazılır.

### Aşama 8 — Sentez

Sonuç üç katmanda yazılır:

1. **Kesin veri:** sayım, biçim, sentaks, açık bağlam ilişkileri.
2. **Güçlü çıkarım:** veriyi en az ek varsayımla açıklayan semantik sonuç.
3. **Açık ihtimal / spekülasyon:** mümkün fakat karar verdirici delili olmayan bağlantı.

Tanım mümkünse şu yapıda verilir:

> **Çekirdek anlam** → **bağlama bağlı alt-anlam(lar)** → **anlam sınırı** → **yakın kavramlardan farkı**.

### Aşama 9 — Sade anlatım ve nihai dosya

Teknik analiz bittikten sonra ayrıca dışarıdan birinin anlayabileceği sade anlatım hazırlanır. Bu sadeleştirme teknik sonucu değiştiremez.

Nihai dosya şunları içermelidir:

- araştırma sorusu,
- veri kaydı,
- tam dağılım özeti,
- kritik ayetler,
- morfoloji ve sentaks bulguları,
- bağlam kümeleri,
- çekirdek anlam önerisi,
- yakın kavram ve negatif semantik testleri,
- karşı örnekler ve falsifikasyon,
- en güçlü alternatif okuma,
- dış dil kontrolü,
- kesin veri / çıkarım / spekülasyon ayrımı,
- sade sonuç.

**Kritik ayetler eksik parça halinde değil, anlamı değerlendirmeye yetecek bağlamla ve gerektiğinde tam ayet olarak verilir.**

---

## 5. Tarama ve sayım disiplini

- **Kök ≠ lemma ≠ segment ≠ kelime konumu.** Bir kökün toplamı, aranan kelimenin toplamı değildir (`r-v-h` kökü 57 birim, *rûh* lemması 21; `f-t-r` kökü 20, *fıtrat* ismi 1).
- **Bab etiketi türemiş isimlere de yapışır.** `VF:1` toplamı fiil sayısı değildir; ism-i fâil, ism-i mef'ûl ve mastar kendi bablarının etiketini taşıyabilir.
- **Benzetme edatı ayıklanır.** `ke-` taşıyan kullanım o kavramın doğrudan örneği değildir; ham dökümde kalır, benzetme olarak etiketlenir.
- **Kök eşleşmesi konu eşleşmesi değildir.** Mekanik sonuç elenmeden kullanılmaz; elenenler gerekçeli listede görünür kalır.
- **Payda yazılır.** Alt sayıların toplamı kategoriyi aşıyorsa çift sayım vardır.
- **Etiket eksikliği bulgu değildir.** "Etiket yok" ile "özellik yok" ayrı şeylerdir.
- **Yokluk iddiası tek kökle kurulmaz.** Eşanlamlı kökler ve kavramı kelimesiz anlatan ayetler taranmadıysa "yok" denmez.
- **Boş komut çıktısı yokluk delili değildir.** Önce komut, kök yazımı ve etiket denetlenir.
- **Sıklık anlam değildir.** Çok tekrar bir tanımı otomatik olarak güçlendirmez; az tekrar da bir kullanımı otomatik olarak tali yapmaz.

---

## 6. Bağlam ve anlam kararı için özel kurallar

**Kavram daraltma yasağı:** Bir kelime, mealin verdiği kurumsal veya fıkhî karşılığa sınanmadan indirgenmez. Önce kalıp çıkarılır, sonra anlam tartışılır.

**İç açıklama önceliği:** Kur'an bir kavramı kendi cümlesinde açıklıyorsa dış sözlük bu açıklamayı geçersiz kılamaz.

**Aynı kök = aynı anlam değildir:** Türevler ortak semantik çekirdeği paylaşabilir; fakat sözcük türü, bab, sentaks, bağlam ve tarihsel sözlüksel dallanma farklı anlamlaşma üretebilir. Bir aykırı lemma sırf aynı `ROOT` etiketini taşıyor diye ana tanıma zorla sokulmaz.

**Aynı konu = aynı kavram değildir:** İki kelimenin aynı ibadet, hukuk veya ahlak bağlamında bulunması eşanlamlı olduklarını göstermez.

**Öz anlam ile kurumsal terim ayrılır:** Sonraki dönemlerde teknik bir terime dönüşen kelime, Kur'an'da aynı teknik sistemi zorunlu olarak taşımaz.

---

## 7. Kavramlar arası aktarım

Kullanılan bir kavram `07_analyses/` altında daha önce sonuçlandırılmışsa **o sonuç derecesiyle birlikte girdi alınır**; sonuçlandırılmamışsa yerel olarak analiz edilir ve bunun yerel analiz olduğu yazılır.

Bir kavramdan diğerine taşınan şey tek satırla belirtilir:

- anlam ihtimali,
- kapsam kaydı,
- ilişki,
- hüküm.

Ortak kök veya ortak tema tek başına aktarım gerekçesi değildir. Bir bağlantının kurulması iki kavramdaki bütün ayrıntıların karşılıklı taşınmasına izin vermez.

Sonraki analiz önceki sonuçla çelişirse çelişki açıkça yazılır; çözülmüyorsa iki olasılık birlikte taşınır. Yumuşatılıp gizlenmez.

---

## 8. Tez testi için özel akış

Kullanıcı açık bir tez verdiğinde:

1. tez tek cümleye dondurulur,
2. hangi bulgunun tezi destekleyeceği yazılır,
3. hangi bulgunun tezi çürüteceği yazılır,
4. neyin sayılacağı taramadan önce belirlenir,
5. karşı örnek havuzu önceden tanımlanır,
6. tarama yapılır,
7. eksen denetimi uygulanır,
8. destek ve karşı bulgu aynı özenle raporlanır.

Kullanıcının tez ifadesi kendiliğinden güçlendirilmez. Veri yalnız daha dar bir sonucu destekliyorsa sonuç o kapsamda bırakılır.

**Karşı bulgu rafı denetimi:** "Karşı bulgu" diye ayrılan her unsur için şu soru sorulur: Bu gerçekten tezi zorluyor mu, yoksa araştırma sorusunun cevabı mı? Cevapsa karşı bulgu rafında tutulmaz.

---

## 9. Sonucu iki ayrı eksende yaz

Bir şeyden çok emin olmak, onun belirli bir tezi desteklediği anlamına gelmez. Bu nedenle iki eksen ayrı tutulur.

### Eksen A — mantıksal durum

| durum | ne demek |
|---|---|
| **Destekleniyor** | Tez lehine olumlu metin içi delil var; desteklenen kapsam yazılır |
| **Yalnız uyumlu** | Tez metinle birlikte doğru olabilir; metin onu öğretmiyor |
| **Destek gösterilemedi** | Belirtilen taramada delil çıkmadı; bu tek başına tezin yanlışlığı değildir |
| **Belirsiz** | Açıklamalar arasında karar verecek delil yok |
| **Çelişiyor** | Aynı konu, kapsam ve şartta tezi dışlayan ifade var; karşı delil gösterilir |

### Eksen B — delil derecesi

- **Sağlam:** dil ve bağlam desteği açık, karşı deliller ele alınmış, aynı kapsamda eşit güçte rakip okuma kalmamış.
- **Muhtemel:** bir okuma daha iyi destekleniyor, fakat anlamlı bir alternatif sürüyor.
- **Spekülatif:** gösterilmemiş bağlantılara dayanıyor; sonuç olarak benimsenmez.

Tek geçiş otomatik olarak spekülatif değildir; çok tekrar otomatik olarak sağlam değildir.

---

## 10. Dış katmanlar için ayrıntılı kural

### Lane

Lane kendi gözlemini değil klasik Arap sözlüklerini derler; bu sözlükler de anlamı şiir, hadis ve tefsirle örneklendirebilir. Bu nedenle "Lane de böyle diyor" bağımsız doğrulama değildir.

Madde içinde `Bd`/`Jel` tefsir, "It is said in a trad." hadis kaynaklıdır; aktarılırsa kaynağı yazılır. Lane'in malzemesindeki boşluklardan yokluk argümanı kurulmaz.

### Sâmî katmanı

İşlevi bir kelimenin Kur'an'daki anlamını tayin etmek değil, önerilen anlamın dil-tarihsel olarak makul olup olmadığını ve olası eski semantik alanı kontrol etmektir.

Ortak ünsüz dizisi yalnız ortak köken **adayıdır**; ortak anlam değildir. Tek dildeki benzerlik tek başına delil sayılmaz. İbranice ile Süryanice de tamamen bağımsız iki tanık gibi sayılmaz.

Depo tarafında `04_lexicons/semitic/cognates.tsv` henüz filolojik olarak incelenmiş kayıtlarla dolu değilse bu durum açıkça yazılır.

SEDRA kullanılan yayımlanmış bir metinde atıf zorunludur (`sami-notlari.md`).

---

## 11. Sunum, sohbet ritmi ve depoya yazım

### 11a. Sunum

- Ayetler Latin harfli okunuş + Türkçe anlam olarak verilebilir; gerekli olduğunda Arapça özgün biçim de gösterilebilir.
- Kökler sunumda Latin harfle ve ayrık yazılır (`s-l-v`, `r-v-h`).
- Önce sayım ve dağılım, sonra kritik ayetler, sonra anlam yorumu gelir.
- Teknik bulgu ile sade açıklama birbirinden ayrılır.

### 11b. Sohbet ritmi

Varsayılan olarak analiz **aşama aşama** yürütülür. Her ana aşamanın sonunda:

- o aşamanın kesin bulguları,
- açık kalan noktalar,
- bir sonraki aşamada neyin sınanacağı

kısaca yazılır ve `devam` onayı beklenir.

Kullanıcı arada bir yorumu, ihtimali veya alternatif açıklamayı gündeme getirirse bu otomatik olarak "önceki analiz yanlıştı" şeklinde yorumlanmaz; ilgili aşamada test edilecek yeni hipotez olarak ele alınır.

### 11c. Depoya yazım

Tamamlanmış analiz `07_analyses/roots/<kok>/` veya `07_analyses/concepts/<kavram>.md` altına yazılır. Dosya başına §3'teki dört satırlık veri kaydı konur. Üretilen ham dökümler `07_analyses/generated/` altında, yorum metninden ayrı durur.

**Yorum ham veri alanına yazılmaz** (`01_raw`, `02_morphology`, `03_indices`).

**Sonuç kesinleşmeden ana analiz dosyası depoya yüklenmez.** Sohbet aşamasındaki geçici hipotezler veya yarım analizler yayımlanmış sonuç gibi kaydedilmez. Kullanıcı nihai analizi onayladıktan sonra depo sürümü hazırlanır.

**Basit istek, basit cevap.** Tek cümlelik soruya çok bölümlü protokol dokümanı üretilmez. Ancak soru ana analizin bir parçasıysa ilgili protokol aşamasına bağlanır.

---

## 12. Yapma

- Taramadan sayı verme; birim yazmadan sayı verme.
- Ayet referansını hafızadan kesin veri gibi yazma.
- Çalıştırılmamış bir sorguyu çalıştırılmış gibi raporlama.
- Beceri sayısıyla depo sayısını aynı tabloda toplamaya çalışma.
- 130.030 ile 128.219'u, 1.651 ile 1.642'yi eşitleme.
- İki aracın uyuşmasını bağımsız doğrulama sayma.
- Boş çıktıyı yokluk sayma.
- Kök toplamını lemma toplamı gibi sunma.
- Meal karşılığını kelimenin anlamı olarak baştan kabul etme.
- Kelimenin sonucunu veya işlevini doğrudan anlam yerine koyma.
- Karşı bulguyu açıklayıp geçme, yumuşatma veya sayısal çoğunlukla bastırma.
- Geleneksel okumayı hem tek otorite hem otomatik yanlış sayma.
- Tek ayetten genel kural çıkarma; kalıbı tam korpusta göstermeden genelleme yapma.
- Yakın iki kavramı yalnız aynı konuda kullanıldıkları için eşanlamlı sayma.
- Sâmî kognatı doğrudan Kur'an anlamı kabul etme.
- Kullanıcının vardığı sonucu, veri desteklemiyorken destekliyormuş gibi sunma.
- Nihai olmayan analizi kesin sonuç gibi depoya yazma.

---

## 13. Nihai kalite kontrol listesi

Bir analiz tamamlanmış sayılmadan önce şu soruların tamamı cevaplanır:

- [ ] Araştırma sorusu açık mı?
- [ ] Analiz birimi doğru mu?
- [ ] Kaynak, sayım birimi, sorgu ve durum yazıldı mı?
- [ ] Kök/lemma/segment/kelime ayrımı korundu mu?
- [ ] Bütün dağılım tarandı mı?
- [ ] Kritik sentaktik kalıplar çıkarıldı mı?
- [ ] Pasaj bağlamı incelendi mi?
- [ ] Kur'an içi tanım veya açıklamalar arandı mı?
- [ ] Kullanımlar semantik kümelere ayrıldı mı?
- [ ] Aynı kök altında ayrı sözlüksel dal ihtimali sınandı mı?
- [ ] Kapalı örneklem kullanılacaksa hipotezden önce kilitlendi mi?
- [ ] Geçici hipotez tek cümleyle donduruldu mu?
- [ ] Çekirdek anlam ile alt-anlamlar ayrıldı mı?
- [ ] Lexical çekirdek / sentaktik anlam / bağlamsal sonuç / sonraki teknik terim ayrıldı mı?
- [ ] Yakın kavramlarla fark testi yapıldı mı?
- [ ] "Ne anlama gelemez?" testi yapıldı mı?
- [ ] Kritik örnekler “kanıtlayıcı / yalnız uyumlu / karşı-baskı noktası” olarak ayrıldı mı?
- [ ] Yokluk iddiası varsa kavramsal tarama tamamlandı mı?
- [ ] Falsifikasyon sorusu açıkça cevaplandı mı?
- [ ] Kapalı örneklem testi yapıldı mı veya neden yapılamadığı yazıldı mı?
- [ ] En güçlü alternatif/geleneksel okuma sınandı mı?
- [ ] Lane ve Sâmî veriler yalnız yardımcı katman olarak kullanıldı mı?
- [ ] Veri / çıkarım / spekülasyon ayrımı yapıldı mı?
- [ ] Mantıksal durum ve delil derecesi ayrı yazıldı mı?
- [ ] Kritik ayetler değerlendirmeye yetecek biçimde verildi mi?
- [ ] Sade sonuç teknik sonuçla uyumlu mu?
- [ ] Kullanıcı nihai dosyayı onayladı mı?

Bu maddelerden kritik olan biri eksikse analiz "tamamlandı" diye işaretlenmez.

---

## Ek — korpus yapısına ilişkin mevcut denetimler

| ölçüm | sonuç |
|---|---|
| QAC v0.4, sağlam parser, benzersiz `ROOT` | 1.642 |
| QAC v0.4, 2019 kırılgan pipeline taklidi | 1.651 |
| QAC v0.4 segment / kelime konumu | 128.219 / 77.429 |
| `mustafa0x/quran-morphology` birim / kelime konumu | 130.030 / 77.429 |
| `mustafa0x` benzersiz `ROOT` (ham ve normalize) | 1.651 / 1.651 |
| iki envanterin kesişimi (hemze nötrlenmiş) | 1.638 ortak; 13 + 4 ayrık |

Durum: çalıştırıldı. Bu ölçümler korpus yapısına ilişkindir; bu belgede herhangi bir kavram taraması yapılmış sayılmaz.
