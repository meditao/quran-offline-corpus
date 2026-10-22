# Kur'an Analiz Protokolü — v2.5

**Konumu:** `06_methodology/analiz_protokolu.md`  
**Kapsamı:** tek bir kavram, kök, ayet, pasaj veya tezin Kur'an merkezli ve denetlenebilir biçimde nasıl analiz edileceği; v2.5'ten itibaren ayrıca kavramların birbirine bağlandığı **kavram alanı** (§7A) ve kavram kartlarından kurulan **dünya görüşü önermeleri** (§7B).

Bu belge, çalışmanın **ana analiz protokolüdür**. Amaç bir anlamı baştan doğru kabul edip ona delil toplamak değil; Kur'an içi veriden hareketle anlamı kurmak, karşı örneklerle sınamak ve veri ile yorumu açıkça ayırmaktır.

**Sürüm notu (v2.5 — 22.10.2026):** Protokol, Izutsu'nun anlam katmanlarına (temel anlam → ilişkisel anlam → anlam alanı → dünya görüşü) göre dört düzeyli bir mimariye bağlandı (§0a). Izutsu'dan alınan, katman yapısıdır; câhiliye şiirine ve sonraki kelâm kullanımına dayanan verisi ve sonuçları delil sayılmaz (§0 ilke 5, Aşama 7c). Eklenenler: kavram alanı düzeyi (§7A) ve ortak ayet denetimi; dünya görüşü önerme defteri (§7B); kartlarda fiilen yapılıp protokolde adı olmayan üç işlemin adlandırılması — dinî olmayan kullanım tanığı (Aşama 1), çerçeve testi (4d), ikame testi (4e); karantina akıbeti (Aşama 0, Aşama 8); bilimsel çağrışım adımı (Aşama 8a); bağımsız tekrar (Aşama 9a). Terim ayrımı: "anlam alanı" bir kelimenin anlam yelpazesidir, "kavram alanı" birden çok kavramın oluşturduğu ağdır (§0a).

**Sürüm notu (v2.4 — 19.10.2026):** Kur'an içi kullanım birincil ölçüt olarak korunarak anlam önerisi kurulan kavram/kök analizlerinde İbn Fâris ve Râgıb'a ek olarak Lane çapraz denetimi ve Sâmî dil taraması zorunlu kılındı. Zorunlu tarama olumlu anlam eşleşmesi veya dış kaynağın hüküm üstünlüğü anlamına gelmez. Kur'an öncesi Arapça anlam iddiaları tarihlenebilir bağımsız Arapça tanık gerektirir. Kaynak bağımsızlığı, rivayet/tefsir ayrımı ve negatif tarama kayıtları Aşama 7, §10 ve kontrol listesinde açıklanır.

**Sürüm notu (v2.1):** Protokol, `f-r-d` kökü üzerinde uçtan uca pilot olarak sınandı. Pilot sonucunda kapalı örneklemin hipotezden önce kilitlenmesi, aynı kök altında ayrı sözlüksel dalların mümkün olması ve “kanıtlayıcı örnek / yalnız uyumlu örnek” ayrımı açık kurala dönüştürüldü.

**Sürüm notu (v2.3 — 14.10.2026):** İki klasik kök sözlüğü — İbn Fâris'in *Mekâyîs*'i ve Râgıb'ın *Müfredât*'ı — anlam önerisi kurulan her analizde zorunlu denetim adımı oldu (Aşama 7a, §10). Sözlüğe Kur'an içi hipotez kurulduktan sonra bakılır; hadis, şer'î ıstılah ve müfessir nakli taşıyan cümleler işaretlenir; sözlükçünün Kur'an kullanımı hakkındaki genellemeleri korpusla sayılır. Araç hem beceride (`kuran-kok-analizi` §12) hem çalışma masasında bulunur: `python -m tezgah kur klasik`, ardından `python -m tezgah klasik kok | asl | isaret | ayet | ara | kapsam | etiketler` (CLAUDE.md §7, §10 Aşama 7). Çalışma masasındaki sürüm girdiyi QAC envanterine karşı çözer ve her sorgunun kaydını §8 biçiminde yazar.

**Sürüm notu (v2.2 — 11.10.2026):** İman–tevekkül karşılaştırmasında biçim ile anlam kümesi, ortak geçişin kanıt sınırı, yerel sıra ile genel zaman kuralı, görev ile ahlaki sorumluluk, metinsel bağlam ile tarihsel çerçeve ve Kur'an öncesi tanıklık ayrımları somutlaştırıldı. Uygulama ve kaynaklar: [İman–tevekkül–vekîl–tafvîz kaydı](../07_analyses/roots/Tawakkul-Wakil-analysis.md).

Arşiv, kavram kartı, versiyon defteri, hipotez defteri ve periyodik bakım bu belgenin konusu değildir. Tamamlanmış analizler `07_analyses/` altında durur. Ham veri, yorum ve yayımlanmış sonuç birbirine karıştırılmaz.

---

## 0. Ana ilkeler

1. **Kur'an içi kullanım birincil delildir.** Kök, morfoloji, sentaks, bağlam, dağılım, iç-tanım, karşıtlık ve kavram ağı birlikte değerlendirilir.
2. **Geleneksel anlam başlangıç varsayımı değildir.** Ne otomatik doğru ne otomatik yanlıştır; en güçlü biçimiyle ayrıca sınanır.
3. **Kesin veri ile yorum ayrılır.** Sayım, biçim ve cümle yapısı veri; bunlardan çıkarılan anlam hipotezdir.
4. **Karşı örnek anlamı daraltır.** Bir aykırı kullanım açıklanıp geçilmez; gerekirse tanım revize edilir.
5. **Kur'an içi kullanım birincil ölçüttür; dış kaynak denetimi zorunlu, hükmü yardımcıdır.** Anlam önerisi kurulan her kavram/kök analizinde İbn Fâris, Râgıb, Lane ve karşılaştırmalı Sâmî dil kaynakları taranır (Aşama 7, §10). Her anlam iddiası kaynağın türüne, tanığına ve bağımsızlığına göre değerlendirilir; tarihsel köken, sözlük anlamı, Kur'an bağlamı ve sonraki dinî yorum birbirine karıştırılmaz. Dış kaynaklar Kur'an'daki anlamı kendiliğinden tayin etmez; tarama zorunluluğu olumlu sonuç bulma zorunluluğu değildir. Kur'an öncesi Arapça anlam iddiası ayrıca tarihlenebilir bağımsız tanık gerektirir.
6. **Yokluk iddiası ağır bir iddiadır.** Tek kök taramasıyla "Kur'an'da yok" denmez.
7. **Anlam ile işlev ayrılır.** Bir kavramın sonucu, etkisi veya hükmü kelimenin sözlük anlamı yerine konmaz.
8. **Tek ayetten genel tanım kurulmaz.** Tanım bütün dağılımı karşılamalıdır.
9. **Sonuçtan önce kapsam yazılır.** Bir önerme hangi ayetler, hangi biçimler ve hangi bağlamlar için geçerliyse o sınır belirtilir.
10. **Analiz aşamalıdır.** Sohbet ortamında varsayılan çalışma biçimi her ana aşamanın sonunda durmak ve kullanıcıdan `devam` onayı almaktır. Kullanıcı açıkça kesintisiz çalışma isterse bu kural kaldırılır.

### 0a. Dört düzeyli mimari

Analiz dört düzeyde yürür. Her düzeyin bir çıktısı ve onu çürütecek önceden yazılmış bir koşulu vardır. Alt düzeyin sonucu üst düzeye **derecesiyle birlikte** girer (§7).

| düzey | Izutsu karşılığı | çıktı | neyle çürür | protokoldeki yeri |
|---|---|---|---|---|
| 1. Kelime | temel anlam | kelime profili | kapalı örneklemde çekirdeğin ek kayıt olmadan karşılayamadığı kullanım | Aşama 1–3, 5 |
| 2. Kavram | ilişkisel anlam, karşıtlık, yakın anlam | kavram kartı | aynı kapsamda dışlayan ayet; ikamede bozulan cümle; rakip okumanın daha az istisnayla açıklaması | Aşama 2–9 |
| 3. Kavram alanı | anlam alanı (semantic field) | alan haritası | ortak ayette kartlar arası çelişki; çerçevede karşılığı olmayan karşıtlık; metinsel bağı gösterilemeyen üye | §7A |
| 4. Dünya görüşü | Weltanschauung | önerme defteri | dayandığı kartlardan birinin revizyonu; aynı kapsamda karşı ayet | §7B |

Izutsu'nun diğer iki aşaması ayrı düzey değildir, her düzeyde çalışan denetimdir: **artzamanlı** aşama → karantina ve izdüşüm denetimi (Aşama 0, Aşama 3'teki "sonraki teknik terim" katmanı, Aşama 7c); **eşzamanlı** aşama → Mushaf tek bir eşzamanlı sistem olarak ele alınır, nüzul sırası ve Mekkî/Medenî ayrımı yalnız etiketli filtredir (CLAUDE.md §2 ilke 7). Kaynak ilkesi gereği artzamanlı aşama anlam üretmez; projeksiyonu yakalar.

**Düzeyler sıralı bir zincir gibi uygulanmaz.** Aynı ayet kelime, kavram ve alan düzeyinde ayrı ayrı "destek" diye sayılmaz; her ayet bir kez delil sayılır, diğer düzeylerde ona atıf yapılır. Dünya görüşü her kavramda değil, kartlar biriktikçe kurulur.

**Terimler:**

- **anlam alanı** — tek bir kelimenin veya kök ailesinin anlam yelpazesi (depodaki mevcut kullanım; ör. Dalâlet, Kitâb kartları),
- **kavram ağı** — tek bir kavramın Aşama 2'de çıkarılan bağlantıları,
- **kavram alanı** — bir odak kavram etrafında, tiplenmiş metinsel bağlarla birbirine bağlanmış kelimelerin oluşturduğu ağ (§7A). Izutsu'nun *semantic field* kavramının karşılığıdır.

**Sûre çevirisi özel kuralı:** Sûre ve bağlantılı pasajların meal–tefsirinde [sûre meal–tefsir bütünleşik protokolü](./sure_meal_tefsir_protokolu.md) uygulanır. Teknik aşamalar içeride eksiksiz işlenir; kullanıcıdan her aşama sonrası ayrı onay istenmez. Bu istisna analiz, karşı delil ve kaynak kontrollerini gevşetmez.

---

## 1. İki veri kaynağı

|  | depo (`quran-offline-corpus`) | beceri (`kuran-kok-analizi`) |
|---|---|---|
| morfoloji | QAC v0.4 (hash sabit) | `mustafa0x/quran-morphology` |
| segment | 128.219 | 130.030 |
| kelime konumu | 77.429 | 77.429 |
| benzersiz `ROOT` | 1.642 | 1.651 |
| kök yazımı | Buckwalter | Arapça |
| yan katman | Tanzil, Açık Kuran, İbranice indeks | İbn Fâris (4.649 madde) + Râgıb (1.662 madde), Lane (47.919 madde), BDB + SEDRA |
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
2. **Beceri hızlı çalışma katmanıdır.** Keşif, ilk döküm, klasik sözlük, Lane ve Sâmî sorgusu için kullanılır. Beceriden çıkan bir sayı yayımlanacaksa depoda yeniden üretilir.
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
Klasik      : asl + isaret + ayet çalıştırıldı, anlam→dayanak tablosu yazıldı | çalıştırılmadı (gerekçe) | salt sayım, gerekmez
Durum       : çalıştırıldı | önceki çıktı kullanıldı | çalıştırılmadı
```

`Klasik` satırı anlam önerisi kurulan her analizde doldurulur (Aşama 7a).

**Durum satırı zorunludur ve gerçeği yazar.** Korpus kurulamadıysa, sorgu çalıştırılmadıysa veya sayı başka bir analizden hatırlandıysa öyle yazılır. Bir önceki sonucu hatırlamak doğrulama değildir. Hafızadan kök listesi, ayet numarası veya sayı yazılmaz.

---

## 4. Ana analiz akışı

Bu bölüm protokolün semantik omurgasıdır. Aşamalar sırayla ilerler; gerekirse önceki aşamaya dönülür.

### Aşama 0 — Ön tanım ve veri sınırı

- Araştırma sorusu tek cümleye indirilir.
- Analiz birimi belirlenir.
- Başlangıç varsayımları karantinaya alınır. Karantina listesi **numaralanır** (K1, K2 …); her madde Aşama 8'de akıbetiyle kapatılır (karantina akıbeti).
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
9. ayet ve sûre dağılımı,
10. **dinî olmayan kullanım tanıkları.**

Bu aşamada **anlam kararı verilmez**; mümkün olduğunca veri dökümü yapılır.

**Dinî olmayan kullanım tanığı.** Kelimenin Kur'an içinde dinî-terimsel bağlam dışında geçtiği yerler ayrı listelenir. İki türü vardır:

- **gündelik kullanım:** alışveriş, borç, emanet, yolculuk, aile içi ilişki gibi bağlamlar (ör. 2:283 *faʾin ʾamina baʿżukum baʿżan* — "biriniz diğerine güvenirse"),
- **aktarılan söz:** Kur'an'ın başka konuşanlardan aktardığı sözler (ör. 12:17 *vamâ ʾanta bimuʾminil lanâ* — Yûsuf'un kardeşleri: "sen bize inanmazsın"). Konuşan ve muhatap Aşama 2'deki gibi kaydedilir.

İşlevi: Izutsu'nun câhiliye şiirinden aldığı "temel anlam" tanığının Kur'an içindeki karşılığıdır. **Sınırı:** dinî bağlam dışındaki kullanımı gösterir; "ilk anlam" veya "Kur'an öncesi anlam" iddiası kurmaz (o iddia Aşama 7c'nin tanığını ister). Böyle bir kullanım yoksa "dinî olmayan kullanım bulunmadı" diye yazılır; bu, kelimenin anlamı hakkında tek başına bir bulgu değildir.

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

#### 4d. Çerçeve testi — karşıtlık hangi çerçevede?

Karşıtlık kelime çiftine değil **çerçeveye** bağlanır. Çerçeve: kelimenin cümlede aldığı edat, nesne, özne ve kalıp düzeni. Her karşıtlık iddiası için şu tablo yazılır:

| X | Y | çerçeve (edat / nesne / kalıp) | ayetler | not |
|---|---|---|---|---|

Kurallar:

- Bir kelimenin birden fazla karşıtı olabilir; her biri ayrı çerçevede kaydedilir. "X, Y'nin karşıtıdır" cümlesi çerçeve belirtilmeden tam tanım olarak yazılmaz.
- Kelimenin değeri nesnesine bağlı olabilir; olumlu ve olumsuz kullanımlar ayrı satırda tutulur.
- Kök düzeyindeki ortak geçiş karşıtlık delili değildir; her satır lemma düzeyinde denetlenir.

> **Örnek (yöntem gösterimi, kavram sonucu değil):** "Küfür imanın karşıtıdır" önermesi tam tanım olarak sınandı. QAC v0.4'te k-f-r ile ş-k-r 7 ayette birlikte geçer; 5:89'daki kelime *kaffâra*dır (başka lemma). Kalan 6 ayette (2:152, 14:7, 27:40, 31:12, 39:7, 76:3) küfür şükrün karşısındadır — 14:7 *laʾin şakartum laʾazîdannakum valaʾin kafartum ʾinna ʿaẕâbî laşadîd*. 2:256 *faman yakfur biṭṭâgûti vayuʾmim billâhi* ve 60:4 *kafarnâ bikum* küfrün olumlu nesneyle de kullanıldığını gösterir. Sonuç: küfrün en az iki karşıtı vardır (iman, şükür), değeri nesnesine bağlıdır; önerme tam tanım olarak çürür. Bu, "Kur'an'da küfrün şükür ekseni vardır" demeye izin verir; "ilk anlamı nankörlüktür" demeye izin vermez (Aşama 7c).

Kartlarda örnek uygulama: Dalâlet kartı, karşıtlığı "bütün kök ailesinde değil, dinî yol ve rehberlik bağlamında" sınırlar.

#### 4e. İkame testi — biri ötekinin yerine geçebiliyor mu?

Yakın kavram testi (4a) şu işlemle somutlaştırılır:

1. X ve Y'nin geçtiği bütün konumlar listelenir.
2. Önerilen ortak anlam (veya Y) X'in her konumuna, X de Y'ninkine konur.
3. Her konum için sonuç kaydedilir: **yerine geçer · anlam kayar · cümle bozulur.**
4. X ile Y'nin aynı ayette yan yana geldiği yerler ayrıca işaretlenir; tam eşanlamlılık bu yerlerde ifadeyi tekrar veya vurgu hâline getirir. Hangisinin olduğu bağlamdan gerekçelendirilir; ortak geçiş tek başına karar vermez (§5).

Test soruyu kurar, cevabı kendisi vermez: "anlam kayar" sonuçları ayrımın nerede olduğunu gösteren adaylardır ve Aşama 5'te sınanır.

> **Örnek malzeme:** ʿ-d-l ile q-s-ṭ QAC v0.4'te 6 ayette birlikte geçer (2:282, 4:3, 4:135, 5:8, 6:152, 49:9). 49:9 *faʾaṣliḥû baynahumâ bilʿadli vaʾaqsiṭû* iki kelimeyi aynı cümlede kullanır; 4:3'te *tuqsiṭû* yetimler hakkında, *taʿdilû* evlenilen kadınlar arasında geçer. Kartlarda örnek uygulama: Sırât–Sebîl kartı, 6:153'te iki kelimenin aynı ilahî yol için kullanıldığını gösterir.

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

### Aşama 7 — Dış dil katmanı: klasik sözlükler, Lane ve Sâmî diller

Bu aşama **Kur'an içi anlam hipotezi kurulduktan sonra** çalıştırılır. Önce bakılırsa çapa etkisi yapar: ayetler sözlüğün verdiği anlamla okunur ve sözlüğün görmediği kullanımlar görünmez olur.

#### 7a. Klasik kök sözlükleri — zorunlu

Anlam önerisi kurulan her kavram/kök analizinde iki sözlüğe bakılır; Lane ve Sâmî dil katmanları da 7b uyarınca zorunlu taranır:

- **İbn Fâris, *Mu'cemü Mekâyîsi'l-luga*** — kökün *asl*ı: bütün türevlerin dayandığı bir-üç çekirdek anlam. Kelime kelime ilerlerken kaybolan kök ailesi damarını denetler.
- **Râgıb el-İsfahânî, *el-Müfredât*** — kelimenin Kur'an kullanımları ve yakın anlamlılar arası ayrım. Sayımın hiç göstermediği komşu kavram sınırını denetler.

Sonra üçlü karşılaştırma yazılır:

1. Kur'an içi hipotezle örtüşen,
2. sözlükte olup korpusta desteği olmayan,
3. korpusta olup sözlükte eksik kalan.

**Gelenek-içi anlamın ayrılması — birim cümle değil, anlamdır.** Soru "bu cümlede hadis var mı" değil, "bu anlam neye dayanıyor"dur. Sözlük maddesi anlam birimlerine bölünür (bir anlam beyanı + ona getirilen tanıklar) ve her birim dayanağına göre bir statü alır: Arap kullanımı ve şiir **dil-içi**; Peygamber'e açıkça nisbet edilen söz (**hadis**) ile sahibi yazılmamış rivayet ("el-hadîs", "ruviye": **rivayet**) ayrı tutulur, ikisi de **gelenek-içi**; şer'î ıstılah ("şeriatın getirdiği", "mahsus ibadet") ve sahabe/müfessir nakli **gelenek-içi**; hiçbir tanık göstermeyen birim **tanıksız**. Yalnız rivayetle tanıklı ya da şer'î bir anlam dil anlamı diye aktarılmaz.

Araç ayırır, karar analizde verilir: biçimsel işaret bir birimde iki anlamı birlikte bırakabilir (Râgıb'ın virgül zincirleri) ve "yukâl" kelimesi her zaman gerçek bir kullanım örneği değildir. Bu yüzden her analizde araç çıktısından sonra Türkçe bir **anlam → dayanak** tablosu yazılır (anlam · dayanak · statü · araçtan sapma notu); her satır tek anlamdır. Tanık göstermeden tefsirden alınmış (örtük) anlam işaretle yakalanamaz; ona üç sınav uygulanır:

- **asl sınavı:** sözlükçünün kendi verdiği asldan türetilebiliyor mu?
- **tanık sınavı:** dil-içi tanığı var mı; yoksa Sâmî katmanı ve Lane'in şiir tanıkları aranır;
- **korpus sınavı:** sözlükçünün anmadığı ayetlerde de tutuyor mu? Anılmayan ayetler Aşama 5'in kapalı örneklemidir.

**Genelleme denetimi.** Sözlükçünün Kur'an kullanımı hakkındaki "hep / hiç / yalnız" hükümleri sayılabilir iddialardır; aktarılmadan önce korpusta sayılır. Örnek: Râgıb, övgü yerinde hep *ikâme* lafzının geldiğini, *el-musallîn*'in yalnız münafıklar için kullanıldığını söyler. *Musallîn* 3 ayette geçer (70:22, 74:43, 107:4); 70:22 *illâ'l-musallîn* övgü bağlamıdır (70:23-34 nitelikleri sayar, 70:35 ödülü bildirir). Genelleme bu kapsamda çelişiyor.

Aynı sertlik, Kur'an içi hipotezi destekler görünen sözlük cümlesine de uygulanır. "İbn Fâris de Râgıb da Lane de böyle diyor" üç bağımsız tanık değildir; aynı geleneğin birbirinden nakleden kayıtlarıdır.

#### 7b. Lane ve karşılaştırmalı Sâmî diller — zorunlu denetim

Anlam önerisi kurulan her kavram/kök analizinde şu taramalar yapılır:

- **Lane — zorunlu çapraz denetim:** ilgili madde, önceki klasik sözlüklerde bulunmayan açıklamalar, aktarılan Arapça kullanımlar/şiir tanıkları ve Lane'in kaynakları incelenir. Lane çoğunlukla klasik geleneği derlediği için onun teyidi otomatik bağımsız kanıt sayılmaz.
- **Sâmî dil karşılaştırması — zorunlu tarama:** önce İbranice ile Aramice/Süryanice güvenilir sözlükler ve ulaşılabiliyorsa tarihlenebilir dil tanıkları incelenir. Araştırma sorusu veya bulunan veri gerektiriyorsa Ugaritçe, Akadca ve diğer Sâmî dillere genişletilir. Yalnız ortak ünsüzler eş kök ispatlamaz; ses denklikleri, biçim, anlam, tarih ve kaynak bağımsızlığı ayrıca denetlenir.
- **Eksik veya olumsuz bulgular raporlanır:** doğrulanmış eş kök ya da tanık yoksa 'doğrulanmış karşılık bulunamadı'; kaynak erişimi mümkün değilse 'denetlenemedi' ve nedeni yazılır. Yapılmayan tarama 'tamamlandı' olarak işaretlenmez.

**7c. Kur'an öncesi Arapça tanık koşulu:** 'Bu biçim Kur'an öncesinde şu anlama geliyordu' veya 'anlam sonradan değişti' iddiası ileri sürüldüğünde tarihlenebilir ve aidiyeti değerlendirilebilen bağımsız Arapça şiir, yazıt ya da metin tanığı aranması zorunludur. Tanık yoksa bu tarihsel iddia kesin hüküm olarak yazılamaz. Tarihsel iddia yoksa tanık aramasına ihtiyaç olup olmadığı açıkça kaydedilir.

**Kanıt hiyerarşisi:** Kur'an içi kullanım birincil ölçüttür. İbn Fâris, Râgıb, Lane ve Sâmî diller farklı soruları aydınlatır; kaynak aktarımı, Arapça dil tanığı, eş kök, hadis/rivayet, tefsir ve sonraki teknik anlam ayrı tutulur. Taramak zorunludur; kaynakta belirli bir anlamı bulmak ya da benimsemek zorunlu değildir.

Tek yönlü kural:

> dış katman → hipotez üretir / tarihsel olasılığı kontrol eder → Kur'an korpusu sınar → sonuç Kur'an içi veriyle yazılır.

### Aşama 8 — Sentez

Sonuç üç katmanda yazılır:

1. **Kesin veri:** sayım, biçim, sentaks, açık bağlam ilişkileri.
2. **Güçlü çıkarım:** veriyi en az ek varsayımla açıklayan semantik sonuç.
3. **Açık ihtimal / spekülasyon:** mümkün fakat karar verdirici delili olmayan bağlantı.

Tanım mümkünse şu yapıda verilir:

> **Çekirdek anlam** → **bağlama bağlı alt-anlam(lar)** → **anlam sınırı** → **yakın kavramlardan farkı**.

**Karantina akıbeti.** Aşama 0'da numaralanan her karantina maddesi burada kapatılır:

| madde | varsayım | akıbet | dayanak |
|---|---|---|---|
| K1 | … | doğrulandı / reddedildi / açık | ayetler, aşama |

"Açık" kalan madde sonuçta varsayım olarak kullanılmaz.

### Aşama 8a — Bilimsel çağrışım adımı

Anlam Kur'an içinden kurulduktan sonra (Aşama 8) **zorunlu olarak** çalıştırılır; atlanmaz. Ayetin veya kavramın anlattığı olgunun (doğa, biyoloji, insan davranışı, toplum) bilimdeki karşılığı aranır ve gösterilir.

Kurallar:

1. **Yön:** bilim kelimenin anlamını belirlemez. Modern bilimsel kavram Aşama 0'da karantinadadır; sıra tersine dönerse modern terim de, fıkıh terimi gibi metne geri taşınır.
2. **Mantıksal durum** §9'daki Eksen A ile yazılır. Çoğu durumda doğru etiket **"yalnız uyumlu"**dur. "Metin bunu söylüyor" (destekleniyor) ancak kelimenin Kur'an içi kullanımı o okumayı ek varsayım olmadan taşıyorsa yazılır.
3. Bilimsel kaynak künyesiyle verilir; tartışmalı bilimsel bulgu kesin bilgi gibi sunulmaz.
4. Anlamlı bir çağrışım yoksa "belirgin bir bilimsel çağrışım bulunmadı" yazılır; çağrışım kota doldurmak için zorlanmaz.

### Aşama 9 — Sade anlatım ve nihai dosya

Teknik analiz bittikten sonra ayrıca dışarıdan birinin anlayabileceği sade anlatım hazırlanır. Bu sadeleştirme teknik sonucu değiştiremez.

Nihai dosya şunları içermelidir:

- araştırma sorusu,
- veri kaydı,
- tam dağılım özeti,
- kritik ayetler,
- morfoloji ve sentaks bulguları,
- dinî olmayan kullanım tanıkları,
- bağlam kümeleri,
- çekirdek anlam önerisi,
- yakın kavram, negatif semantik, çerçeve ve ikame testleri,
- karşı örnekler ve falsifikasyon,
- en güçlü alternatif okuma,
- dış dil kontrolü,
- kesin veri / çıkarım / spekülasyon ayrımı,
- karantina akıbeti tablosu,
- bilimsel çağrışım adımı,
- bağımsız tekrar kaydı (Aşama 9a),
- ortak ayet denetimi kaydı (§7A),
- sade sonuç.

**Kritik ayetler eksik parça halinde değil, anlamı değerlendirmeye yetecek bağlamla ve gerektiğinde tam ayet olarak verilir.**

### Aşama 9a — Bağımsız tekrar

Kavram kartının ilk onayından önce aynı araştırma sorusu, ilk sonucu görmeyen ikinci bir uygulayıcıya (başka bir model ailesi ya da bir kişi) aynı protokol ve aynı veriyle verilir. Karşılaştırılan üç şey:

1. kullanım sınıflandırmaları (kümeler, kanıtlayıcı / yalnız uyumlu / karşı etiketleri),
2. çekirdek anlam önerisi,
3. bulunan karşı örnekler.

Uyuşmayan her karar **karar kaydına** gerekçesiyle yazılır ve çözülür ya da açık bırakılır. İki uygulayıcının uyuşması doğrulamanın kendisi değildir (aynı soydan modeller bağımsız sayılmaz); işlevi, tek uygulayıcının fark etmediği kararları görünür kılmaktır. Tekrar yapılmadıysa kartta "bağımsız tekrar yapılmadı" yazılır.

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

**Morfolojik küme semantik küme değildir.** QAC'ta 106:4'ün `āmana` biçimi IV. bâb fiildir, fakat bağlamda güvenlik sağlama anlatır. Bu nedenle “IV. bâb fiil toplamı” doğrudan “dinî iman kullanımı toplamı” diye adlandırılamaz. 12:17'deki `muʾmin` IV. bâb ism-i fâildir; çekimli fiil toplamına eklenmez. Anlam sınıflaması yapılacaksa her konum gerekçeli semantik etiketiyle ayrıca incelenir; biçim gruplarına sonradan anlam adı vererek sayısal sonuç üretilmez. İlgili tam sorgular ve kaynak hashleri [denetim raporunda](../07_analyses/generated/tawakkul_comparison/report.md) bulunur.

**Birlikte geçiş yalnız aday ilişki bulur.** Pencere (aynı ayet / komşu ayet / pasaj), kök veya tam lemma seçimi ve sayım birimi yazılır. Birlikte geçiş, tek başına eşanlamlılık, mutlak kavramsal ayrılık, nedensellik veya zorunlu aşama sırası kanıtı değildir. Kök düzeyindeki ʾ-m-n + w-k-l kesişiminde 17:68'in güvenlik kullanımı da vardır; bütün sonuçlar “iman–tevekkül ilişkisi” diye etiketlenemez. Ayrı kelimeler olduklarını görmek de kesin bir semantik sınır kurmaya yetmez; sentaks ve bağlam ayırıcı olmalıdır.

---

## 6. Bağlam ve anlam kararı için özel kurallar

**Kavram daraltma yasağı:** Bir kelime, mealin verdiği kurumsal veya fıkhî karşılığa sınanmadan indirgenmez. Önce kalıp çıkarılır, sonra anlam tartışılır.

**İç açıklama önceliği:** Kur'an bir kavramı kendi cümlesinde açıklıyorsa dış sözlük bu açıklamayı geçersiz kılamaz.

**Aynı kök = aynı anlam değildir:** Türevler ortak semantik çekirdeği paylaşabilir; fakat sözcük türü, bab, sentaks, bağlam ve tarihsel sözlüksel dallanma farklı anlamlaşma üretebilir. Bir aykırı lemma sırf aynı `ROOT` etiketini taşıyor diye ana tanıma zorla sokulmaz.

**Aynı konu = aynı kavram değildir:** İki kelimenin aynı ibadet, hukuk veya ahlak bağlamında bulunması eşanlamlı olduklarını göstermez.

**Öz anlam ile kurumsal terim ayrılır:** Sonraki dönemlerde teknik bir terime dönüşen kelime, Kur'an'da aynı teknik sistemi zorunlu olarak taşımaz.

**Yerel sıra ile genel zaman kuralı ayrılır:** 3:159'daki danışma → karar → tevekkül düzeni bu cümlenin yapısıdır. “Tevekkül yalnız bütün düşünme ve eylem bittikten sonra başlar” genellemesi için başka kullanımlar da sınanır; 12:67 tedbir ve tevekkülü birlikte içerir. Bir emir, davranışın normatif olarak beklendiğini gösterebilir; her kişide otomatik gerçekleşen psikolojik bir yasa olduğunu göstermez.

**Görev devri ile ahlaki sorumluluk ayrılır:** `wkl` ailesinin görevlendirme fiilleri (6:89, 32:11), vekîl ismi ve tevekkül fiili aynı anlamda sayılmaz. Bir işi yürütmek üzere görevlendirilme, başka kişinin tercihinin hesabını üstlenme ve Allah'a dayanma ayrı ilişkiler olarak incelenir. 10:108 ve 39:41'deki sorumluluk sınırı her türlü pratik görevlendirmeye genel yasak olarak taşınmaz. 40:44'te “işim” nesnesi “sonuç” diye değiştirilmez; “sonucu Allah'a bırakmak” açıklayıcı özet olarak etiketlenir.

**Metinsel bağlam ile tarihsel çerçeve ayrılır:** Bir pasajın kendi içindeki savaş, hata, bağışlama ve hitap bağları doğrudan metinden incelenir. “Bu Uhud'dur” gibi tarihsel adlandırma kullanılırsa tefsir/tarih kaynağı ayrıca gösterilir; metinde geçmeyen ad, tarih, sayı veya ayrıntı ayetin lafzına eklenmez. Tarihsel çerçeve olmadan hangi çıkarımın sürdüğü açıkça yazılır.

**Benzetme kanıt değildir:** Bir kavramı açıklamak için kullanılan köprü, yolculuk vb. örnekler öğretici araç olarak etiketlenir. Benzetmenin gerektirdiği kusursuzluk, mutlak kesinlik veya zorunlu zaman sırası, ayetlerin ve kullanım dağılımının gerektirdiği anlam gibi kaydedilmez.

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

## 7A. Kavram alanı — Düzey 3

Bir kavram tek başına tam tanımlanamaz; alandaki yeri tanımının parçasıdır. Bu düzey, kavram kartlarını birbirine bağlayan ağı açık, denetlenebilir bir dosyada kurar.

### 7A-1. Alan dosyası

Konumu: `07_analyses/fields/<alan>.md`. İçeriği:

1. **odak kavram** — alanı düzenleyen kavram (bir alanda birden fazla olabilir),
2. **üyelik ölçütü** — taramadan önce yazılır,
3. **üye listesi** — her üye **kelime (lemma + kalıp)** düzeyinde; kök düzeyinde üye yazılmaz,
4. **bağ tablosu** — her bağ türüyle, ayetiyle ve derecesiyle,
5. **dayandığı kartlar** — kart adı ve sürümü,
6. **ortak ayet denetimi kaydı**,
7. kayıt satırı (§3).

### 7A-2. Üyelik

Bir kelime alana ancak **en az bir ayette gösterilmiş, türü belli bir metinsel bağla** girer. Birlikte geçiş yalnız aday üretir (§5). Bir kelime birden çok alana girebilir (ör. küfür hem iman hem şükür alanında; 4d).

**Kök ≠ üye.** Aynı kök iki zıt kutbu taşıyabilir: q-s-ṭ kökünün 25 kelime konumundan 2'si *qâsiṭûn*dur (72:14–15, *vaminnâ lqâsiṭûna* — müslimlerin karşısında), *muqsiṭîn* ise övülür (49:9). Bu yüzden "adalet alanına q-s-ṭ girer" değil, "*qisṭ* ve *muqsiṭ* adalet kutbuna, *qâsiṭ* karşı kutba girer" yazılır.

### 7A-3. Bağ türleri

| tür | ne demek | örnek |
|---|---|---|
| karşıtlık | aynı çerçevede zıt kutup (4d) | 14:7 şükür ↔ küfür |
| paralel yuva | aynı cümle yapısında karşılıklı yerleri dolduran kelimeler | 47:3 *kafarû ttabaʿû lbâṭila* / *ʾâmanû ttabaʿû lḥaqqa* |
| iç-tanım | metnin bir terimi kendi içinde açması | 2:177 *valâkinna lbirra man ʾâmana billâhi …* |
| şart–sonuç | bir kavramın ötekinin koşulu veya gereği olarak kurulması | 10:84 *ʾin kuntum ʾâmantum billâhi faʿalayhi tavakkalû* |
| ikame | aynı göndergeye iki kelime (4e) | 6:153 *ṣirâṭ* / *sabîl* |
| birlikte geçiş | yalnız aday; tür belirlenmeden bağ sayılmaz | — |

Her bağın derecesi §9 Eksen B ile yazılır. Bağın varlığı, iki kavramdaki bütün ayrıntıların karşılıklı taşınmasına izin vermez (§7).

### 7A-4. Ortak ayet denetimi

Bir kavram kartı onaylandığında veya sürümü değiştiğinde:

1. kartta anılan ayetlerden, başka kartlarda da anılanlar listelenir,
2. her ortak ayet için kartların okuması yan yana konur,
3. sonuç kaydedilir: **uyumlu · farklı yönler (çelişki yok) · çelişki,**
4. çelişki ya çözülür ya da **iki kartta da** açıkça yazılır; sessizce bırakılmaz.

Durum (22.10.2026): `07_analyses/roots` altındaki kavram dosyalarında otomatik atıf taramasıyla 242 farklı ayet bulundu; en az 35'i birden fazla kavramda geçiyor (aralık içleri sayılmadı). 37:23, 42:52 ve 27:14 elle denetlendi: farklı yönler, çelişki yok. Bu denetim için çalışma masasında henüz komut yoktur; araç eklenene kadar elle yapılır ve "elle yapıldı" diye kaydedilir.

### 7A-5. Alan neyle çürür

- ortak ayette kartlar arası çözülmemiş çelişki,
- çerçeve tablosunda karşılığı gösterilemeyen bir karşıtlık,
- metinsel bağı gösterilemeyen üye,
- yeni bir kartın alana ancak alanın tanımını değiştirerek sığması (bu durumda alan revize edilir, eski hâli sürüm defterinde kalır).

---

## 7B. Dünya görüşü — Düzey 4

Kavram kartlarından ve alan dosyalarından Kur'an'ın insan, Allah, sorumluluk, hayat ve ahlak hakkındaki önermeleri kurulur. Bu düzey bütün olarak yanlışlanamaz; **halkaları** yanlışlanır. Bu yüzden her önerme bağımlılıklarıyla birlikte kaydedilir.

### 7B-1. Önerme kaydı

Konumu: `07_analyses/worldview/` (önerme defteri; çalışma masasında `tez.py`'nin sürümlü, zincirli defter yapısı kullanılabilir). Her önerme:

1. **tek cümle** ifade,
2. **kapsam** — hangi ayet kümeleri, hangi bağlamlar,
3. **bağımlılıklar** — dayandığı kart ve alan bağları, **sürüm numaralarıyla**,
4. **doğrudan dayanak** — önermeyi söyleyen ayet; yoksa önerme **"çıkarım"** etiketi taşır,
5. **karşı ayet taraması** — §8'deki tez akışıyla,
6. **mantıksal durum ve derece** (§9).

### 7B-2. Kurallar

- **En zayıf halka kuralı:** önermenin derecesi, bağımlılıklarının en düşük derecesini aşamaz. Üç sağlam kart ve bir muhtemel bağ, en fazla muhtemel bir önerme verir.
- **Otomatik yeniden bakış:** bağımlı olduğu bir kartın veya bağın sürümü değişen önerme "yeniden bak" işareti alır; gözden geçirilene kadar kesin sonuç gibi kullanılmaz.
- **Yerel dayanak:** tam kartı olmayan kavrama dayanan önerme **"yerel"** etiketi taşır ve kapsamı o yerel analizle sınırlı yazılır (§7). Böylece her kavramı ayrıntılı işlemeden de ilerlenebilir; bedeli görünür kalır.
- Aynı ayet, önermenin dayandığı kartta zaten delil sayıldıysa önerme düzeyinde ikinci kez bağımsız delil sayılmaz (§0a).

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

### Lane — zorunlu çapraz denetim

Lane kendi gözlemini değil klasik Arap sözlüklerini derler; bu sözlükler de anlamı şiir, hadis ve tefsirle örneklendirebilir. Bu nedenle "Lane de böyle diyor" bağımsız doğrulama değildir.

Madde içinde `Bd`/`Jel` tefsir, "It is said in a trad." hadis kaynaklıdır; aktarılırsa kaynağı yazılır. Lane'in malzemesindeki boşluklardan yokluk argümanı kurulmaz.

### Sâmî katmanı — zorunlu tarama

İşlevi bir kelimenin Kur'an'daki anlamını tayin etmek değil, önerilen anlamın dil-tarihsel olarak makul olup olmadığını ve olası eski semantik alanı kontrol etmektir.

Ortak ünsüz dizisi yalnız ortak köken **adayıdır**; ortak anlam değildir. Tek dildeki benzerlik tek başına delil sayılmaz. İbranice ile Süryanice de tamamen bağımsız iki tanık gibi sayılmaz. İbranice ile Aramice/Süryanice asgari taraması ve bulunan adayların ses/biçim/anlam denetimi kaydedilir. Gerekirse başka Sâmî dillere genişletilir. Eş kök bulunamaması 'kökte böyle anlam yok' kanıtı değildir; veri ve erişim yetersizliği açıkça raporlanır.

### Klasik kök sözlükleri

Kaynak: OpenITI külliyatı (CC BY-NC-SA 4.0), commit'e sabit iki dosya — *Mekâyîs* Hârûn tahkiki (`0395IbnFarisQazwini.MucjamMaqayis.Shamela0021710-ara1`), *Müfredât* Dâvûdî tahkiki (`0502RaghibIsbahani.Mufradat.Shamela0023636-ara1`). Künye, sağlama toplamı ve ayrıştırma kuralları becerinin `references/klasik-notlari.md` dosyasındadır.

- **Kapsam (QAC v0.4, 1.642 kök; birim: kök):** İbn Fâris 1.560 kesin + 33 zayıf eşleşme, 49 kök yok (49.968 kelime konumunun 141'i). Râgıb 1.522 kesin + 16 zayıf, 104 kök yok (935 kelime konumu). Beceri envanterine göre ölçülen sayılar bunlarla aynı tabloda toplanmaz.
- **"Sözlükte yok" bulgu değildir.** İbn Fâris'te yok olanların çoğu dörtlü kök veya alıntı kelimedir; birkaç üçlü kökün maddesi dijital metinde bulunamadı. Râgıb bütün kökleri işlemez, bazılarını başka maddede anar (*mâl* → *m-y-l*).
- **Zayıf eşleşme elle denetlenir.** Zayıf kural yanlış madde de bulabilir (`ʿ-v-n` → İbn Fâris `(عن)`).
- **Aynı madde birden çok kökü kapsayabilir.** Râgıb'ın *salâ* maddesi hem `ṣ-l-v` (salât) hem `ṣ-l-y` (ateşe girmek) köklerini anar; korpusta bunlar ayrı köktür.
- **Dijital metnin kusuru.** Râgıb'ın OpenITI metninde madde başlıkları kaymıştır; madde, başlıktan değil tanım satırından başlatılır (1.662 maddenin 120'si). Kaymış maddenin ilk ve son satırı ayrıca okunur.
- **İşaret biçimseldir.** `[HADİS]` (Peygamber'e açık nisbet), `[RİVAYET]` (sahibi yazılmamış), `[ŞER]`, `[NAKİL]` bir anlamın dayandığı tanığı gösterir, anlamın doğruluğunu değil. Kararı analizdeki anlam → dayanak tablosu verir.

### Kur'an öncesi kullanım iddiası

“Kur'an öncesinde bu biçim şu anlama geliyordu” iddiası, tarihlenmiş ve aidiyeti tartışılmış bağımsız metin, şiir veya yazıt tanığı gerektirir. Sonraki sözlüklerin bir anlam kaydetmesi veya Sâmî dillerde benzer bir kök bulunması tek başına Kur'an öncesi Arapça tanıklık değildir. Tanık gösterilmiyorsa “ilk/asıl anlam” diye kesin hüküm kurulmaz; tarihsel ihtimal veya araştırılmamış konu olarak yazılır. Sonraki teknik terim, Kur'an'daki aynı köklü fiilin nesne ve bağlamından ayrı incelenir.

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
- Karşıtlığı çerçevesini yazmadan tam tanım olarak sunma (4d).
- Kavram alanına kök düzeyinde üye yazma (§7A-2).
- Aynı ayeti kelime, kavram, alan ve önerme düzeyinde ayrı ayrı bağımsız delil sayma (§0a).
- Dünya görüşü önermesinin derecesini en zayıf bağımlılığının üstünde yazma (§7B-2).
- Bilimsel bulguyu kelimenin anlamını belirleyen delil olarak kullanma (Aşama 8a).
- "Dinî olmayan kullanım"dan "ilk anlam" veya "Kur'an öncesi anlam" sonucu çıkarma (Aşama 1).

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
- [ ] İbn Fâris ve Râgıb maddeleri taranıp anlam → dayanak ayrımı yapıldı mı?
- [ ] Lane maddesi ve dayandığı klasik kaynaklar çapraz denetlendi mi?
- [ ] İbranice ve Aramice/Süryanice için güvenilir Sâmî taraması yapıldı mı; bulunamayan/doğrulanamayan eş kökler açıkça kaydedildi mi?
- [ ] Kur'an öncesi Arapça anlam veya değişim iddiası varsa tarihlenebilir bağımsız tanık gösterildi mi; yoksa kesinlik iddiası sınırlandı mı?
- [ ] Dış kaynak bağımsızlığı, dil tanığı / rivayet / tefsir ayrımı ve Kur'an içi birincillik ilkesi korundu mu?
- [ ] Dinî olmayan kullanım tanıkları listelendi mi veya bulunmadığı yazıldı mı?
- [ ] Karşıtlıklar çerçeve tablosuyla (4d) yazıldı mı?
- [ ] Yakın kavramlar için ikame testi (4e) yapıldı mı?
- [ ] Karantina maddelerinin her biri akıbetiyle kapatıldı mı?
- [ ] Bilimsel çağrışım adımı (8a) çalıştırıldı ve Eksen A ile etiketlendi mi?
- [ ] Bağımsız tekrar yapıldı mı veya yapılmadığı kartta yazıldı mı?
- [ ] Ortak ayet denetimi (§7A-4) yapıldı ve sonucu kaydedildi mi?
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
