# İman, tevekkül, vekîl ve tafvîz — kapsamlı karşılaştırma kaydı

**Sürüm:** v1.0 — 11.10.2026. **Statü:** doğrulanmış biçim ve bağlam bulguları + kapsamı belirtilmiş semantik sentez. Bütün iman kullanımlarına tek karşılık veren yeni bir sözlük tanımı değildir.

**Araştırma sorusu:** İman, tevekkül, vekîl ve tafvîz hangi açılardan ilişkilidir; özellikle 3:159 insanın danışma, karar ve sorumluluğu hakkında neyi destekler?

```text
Kaynak      : depo QAC v0.4 + Tanzil Uthmani v1.1; tarihsel çerçeve için etiketli tefsir
Sayım birimi: kelime konumu / segment / ayet / sûre (ayrı ayrı)
Sorgu       : python 08_scripts/analyze_tawakkul_comparison.py
Durum       : çalıştırıldı
```

Tam sayım, kaynak hashleri, konumlar ve incelenen ayetler: [üretilmiş denetim raporu](../generated/tawakkul_comparison/report.md). Üretici: [analyze_tawakkul_comparison.py](../../08_scripts/analyze_tawakkul_comparison.py). Kanonik kaynak QAC'tır; becerinin 130.030 segmentlik korpusu bu sayılara karıştırılmaz.

## 1. Sade sonuç ve aktarım sınırı

3:159'da **danışmak, karar vermek ve Allah'a tevekkül etmek ayrı görevlerdir**. Tevekkül, bu bağlamda danışma ve kararın yerine geçmez. Ayet, karar verildiğinde Allah'a dayanmayı emreder; tevekkülün yalnız bütün düşünme ve eylem bittikten sonra başlayacağını söylemez.

İman için mevcut [ana analiz](Iman-analysis.md), doğru/güvenilir kabul etme, güven ve bağlılık alanlarını inceler. Buraya taşınan şey **anlam ihtimali ve ilişki kaydıdır**; imanın bütün anlamlarıyla tevekkülün eşit olduğu veya iman eden herkesin her durumda aynı psikolojik dayanmayı gösterdiği hükmü değildir.

Bu incelemedeki yerel ayrım:

| kavram / yapı | bu bağlamlarda görülen işlev | sınır |
|---|---|---|
| İman / ʾ-m-n ailesi | bir bildirimi/mercii doğru kabul etme, güven ve bağlanma; türeve göre güvenlik sağlama da vardır | bütün kök ailesi tek bir dinî anlam değildir; iman salt zihinsel kanaate indirgenmez |
| Tevekkül / V. bâb | Allah'a güvenip dayanma; tedbir, karar ve eylemle birlikte bulunabilir | yalnız hareket etmek, eylemsizlik veya yalnız iş bittikten sonra sonucu kabullenmek değildir |
| Vekîl / isim | kendisine dayanılan, işin gözetimi veya yürütülmesiyle ilişkili merci; anlamı özne ve bağlam belirler | her kullanımda modern hukukî avukat veya sorumluluk devri anlamına gelmez |
| Tafvîz / 40:44'te II. bâb fiil | konuşanın **işini** Allah'a havale etmesi | ayetin nesnesi “sonuç” değil “işim”dir; tevekkülle tam eşanlamlılık veya zorunlu mertebe sırası gösterilmiş değildir |

Bu tablo bir öğretici karşılaştırmadır. Kavramların mutlak olarak ayrık kümeler olduğunu veya birbirlerini zorunlu biçimde izlediklerini kanıtlamaz.

## 2. Morfoloji ve sayım düzeltmeleri

Kök gösterimi: QAC `Amn` = ʾ-m-n, `wkl` = uluslararası yazımla w-k-l, `fwD` = f-w-ḍ. Deponun [ortak Latin tablosunda](../../09_calisma_masasi/okunus_kurallari.md) vav `v`, dad `ż` yazılır; aynı kökler v-k-l ve f-v-ż görünür. Bunlar farklı kökler değildir.

| QAC seçimi | kelime konumu | ayet | sûre |
|---|---:|---:|---:|
| `ROOT:Amn` | 879 | 723 | 77 |
| `ROOT:wkl` | 70 | 61 | 29 |
| `ROOT:fwD` | 1 | 1 | 1 |

`wkl` ailesindeki **70 kelime konumu**: 40 V. bâb fiil, 4 V. bâb ism-i fâil, 24 vekîl ismi, 2 II. bâb fiil. Bunların toplamı kök toplamıdır; “tevekkül fiili 70 kez” denmez. II. bâb örnekleri 6:89 ve 32:11'dir. `fwD` kökünün bu QAC taramasındaki tek konumu 40:44:5'tir; II. bâb fiildir. **Teknik isim olan “tafvîz”in bir kez geçtiği söylenmez:** bulunan, bu kökün fiilidir. Bu sayı tafvîz fikrinin başka ifadelerle anlatılmadığını göstermez.

### 106:4 — IV. bâb otomatik olarak “iman etmek” değildir

QAC 106:4:5'in kök taşıyan segmentini `V`, `(IV)`, `LEM:'aAmana`, `ROOT:Amn` olarak kaydeder. Bağlamda Allah'ın açlıktan doyurması ve korkudan güvene kavuşturması anlatılır. Dolayısıyla **537 IV. bâb fiil konumu morfolojik toplamdır; 537 dinî iman kullanımı değildir**. Tek aykırı anlam, morfolojik kümenin tek anlam olduğu iddiasını sınırlar.

Bu gözlem bütün diğer IV. bâb kullanımlarını “güvenlik sağlamak” diye çevirmeyi de haklı kılmaz. Öznenin kim olduğu, nesne ve tamamlayıcı yapısı ayrıca değerlendirilir. [QAC 106:4:5](https://corpus.quran.com/wordmorphology.jsp?location=(106:4:5))

### 12:17 — kişisel haber tasdiki; çekimli fiil değil

Kardeşlerin Yusuf hakkında anlattıkları sözün devamında `bi-muʾminin lanā` gelir: “doğru söylemiş olsak bile bize inanmayacaksın / bizi doğrulamayacaksın” anlam alanı. QAC 12:17:14'ün kök taşıyan segmentini **N, IV. bâb aktif ortaç / ism-i fâil** olarak kaydeder. Bu konum 537 çekimli fiile eklenmez.

Kişiler arası inanma/doğrulama örneği, bu biçimin her yerde dinî aidiyet bildirmediğini gösterir. Buna karşılık “bütün iman yalnız haber tasdikidir” sonucu da çıkmaz. Haber tasdiki ve itimat burada aynı veriyi açıklayabilir; “inanmak/tasdik” okuması sırf “güven” önerisi tercih edildi diye elenmez. [QAC 12:17](https://corpus.quran.com/wordbyword.jsp?chapter=12&verse=17)

## 3. Âl-i İmrân 3:159 — lafız, yorum ve tarihsel bağlam

**Çalışma çevirisi — tam ayet:** Allah'tan bir rahmet sayesinde onlara yumuşak davrandın. Kaba ve katı kalpli olsaydın çevrenden dağılıp giderlerdi. Öyleyse onları bağışla, onlar için bağışlanma dile ve iş konusunda onlarla danış. Kararını verdiğinde Allah'a tevekkül et. Allah tevekkül edenleri sever.

**Kritik yapının okunuşu:** `vaşâvirhum fî lʾamri faʾiẕâ ʿazamta fatavakkal ʿalâ llâh`. Okunuş bir aktarım katmanıdır; biçim denetimi QAC segmentlerinden, tam metin denetimi Tanzil'den yapılır.

| doğrudan gözlenen yapı | taşıyabileceği sonuç | taşımadığı ek iddia |
|---|---|---|
| `şâvirhum` — III. bâb emir + “onlar” zamiri | danışma emri muhatapları içerir | “her söylenen doğru kabul edilsin” veya “danışılan herkes yanılmazdır” |
| `fa-ʾiẕā ʿazamta` — karar/azim koşulu; tekil hitap | danışma ile karar aynı işlem değildir; kararın verilmesi ifade edilir | karar yönteminin bütün ayrıntıları, çoğunluk oylaması veya her kararın değiştirilemezliği |
| `fa-tawakkal ʿalā llāh` — V. bâb emir | karar verildiğinde Allah'a dayanma | “artık eylem yapma”, “sonuç kesin istediğin gibi olur” veya “tevekkül yalnız bu anda mümkündür” |
| `faʿfu ʿanhum` + bağışlanma dileme + danışma | bağışlama ve danışmayı sürdürme aynı ayette bulunur | toplumdaki herkesin aynı kusuru işlediği |

“Kararının arkasında dur” ifadesi azmi açıklayan bir yorum olabilir; ayette ayrı bir kelimesi kelimesine emir olarak gösterilmez. “Sonucu Allah'a bırak” ise tevekkülün bu bağlamdaki öğretici özetidir; `tawakkal` fiilinin tek ve bütün bağlamları tüketen sözlük karşılığı değildir. [QAC 3:159](https://corpus.quran.com/wordbyword.jsp?chapter=3&verse=159)

### Metnin kendi bağlamı

3:121 askerî mevzilendirmeyi anlatır. 3:152 gevşeme, iş hakkında anlaşmazlık, itaatsizlik ve bağışlanmayı; 3:155 çatışmada geri dönenlerin bağışlanmasını anlatır. 3:159 aynı savaş çevresinde yumuşaklık, bağışlama, bağışlanma dileme ve danışmayı birlikte korur. Bu bağlantı yalnız aynı köke dayanmaz: savaş, hata, bağışlama ve aynı topluluğa yönelen hitap birbirini izler.

Buradan **danışma, muhatabın yanılmazlığını varsaymak zorunda değildir** sonucu güçlü biçimde desteklenir. Bunun kapsamı hata ve bağışlanma bağlamında danışmanın sürdürülmesidir. “Uhud'da hata danışmanın kendisiydi” veya “danışılan her kişi hata yapmıştı” sonuçları bu veriyle kurulmaz.

3:160, yardımın Allah'a bağlı olduğunu ve müminlerin O'na tevekkül etmesini söyler. **İnsanın kararı ve tedbiri başarıyı mutlak olarak garanti etmez** çıkarımı bu bağlamla desteklenir. “İnsanın sonuç üzerinde hiçbir etkisi yoktur” iddiası ise daha geniş ve başka bir önermedir; burada kanıtlanmış sayılmaz.

### Uhud adı ve tarih katmanı

Bu ayetler **“Uhud” adını söylemez**. Pasajın Uhud'la ilişkilendirilmesi tefsir ve tarih aktarımıdır. Burada kullanılan açık kaynak, **İbn Kesîr'in kısaltılmış tefsirinin Quran.com'daki İngilizce sunumu**dur. 3:121 açıklaması pasajı Uhud'la ilişkilendirir; 3:159 açıklaması savaş öncesi danışmayı anlatır. [İbn Kesîr, 3:121](https://quran.com/ali-imran/121/tafsirs/en-tafisr-ibn-kathir), [İbn Kesîr, 3:159](https://quran.com/ali-imran/159/tafsirs/en-tafisr-ibn-kathir)

Bu kaynak, tefsirin ne anlattığının kaynağıdır; Kur'an lafzının veya bağımsız çağdaş tarih tanıklığının yerine geçmez. Okçuların sayısı, savaşın tarihi, tek tek kişilerin eylemleri ve danışmanın ayrıntıları bu analizin Kur'an içi kanıtına eklenmemiştir. Tarihsel çerçeve kullanılmasa da hata–bağışlama–danışma bağlantısı yukarıdaki ayetlerden değerlendirilebilir.

## 4. Tevekkül ile eylem: karşı örnekler ve kapsam

“Tevekkül ancak düşünme ve karar bittikten sonra gelir” cümlesi 3:159'un yerel sırasını bütün kullanımlara yayar; bu evrensel hüküm tek ayetten kurulamaz. **3:122**, aynı savaş çevresinde müminlerin Allah'a tevekkül etmesini söyler; fakat kararın öncesini/sonrasını belirtmediği için tek başına kronolojik karşı örnek değildir. **12:67–68** ise pratik talimatı, tevekkül beyanını ve talimatın sonradan uygulanmasını içerir. “Düşünme/karar sonrasında” ile “bütün eylem tamamlandıktan sonra” aynı iddia değildir.

**12:67 — çalışma çevirisi:** Dedi ki: “Oğullarım! Tek bir kapıdan girmeyin; farklı kapılardan girin. Allah'tan gelecek hiçbir şeyi sizden uzaklaştıramam. Hüküm yalnız Allah'ındır. O'na tevekkül ettim; tevekkül edenler de O'na tevekkül etsin.”

Bu ayet tedbiri gereksiz saymaz; verilen tedbirin Allah karşısında mutlak koruma sağlamadığını ifade eder. Tedbirin tarihsel gerekçesi ayetin açık lafzında değildir; bu gerekçe tanıma eklenmez. **Tedbir ve Allah'a dayanma birlikte bulunur; tevekkül beyanı eylem tamamlanmadan yapılır** sonucu sağlamdır: giriş eylemi 12:68'de anlatılır. “Tevekkül bütün eylemler/araçlar bittikten sonra başlayan son aşamadır” şeklindeki dışlayıcı genelleme bu örneği karşılamaz. Bu gözlem, tevekkülün her durumda düşünme veya karar öncesinde başladığını da göstermez.

8:2, 5:23, 10:84, 64:13 ve 67:29 imanla tevekkülü ilişkilendirir. Bunlar tevekkülün mümin davranışı olarak çağrıldığını destekler. “İman varsa her durumda tevekkül otomatik olarak gerçekleşir” veya “iman olmadan psikolojik dayanma mantıken imkânsızdır” hükümleri bu çağrılardan zorunlu olarak çıkmaz.

25:58 ölmeyen Diri'ye dayanmayı; 65:3 Allah'a tevekkül edene O'nun yeterli oluşunu söyler. “Yeterli oluş”, kişinin seçtiği her dünyevî sonucun aynı biçimde gerçekleşeceğinin garantisi olarak genişletilmez.

## 5. Vekîl: işin gözetimi ile ahlaki sorumluluk

Vekîl isminin **öznesi ve neyle ilişkilendirildiği** önemlidir. 3:173'te tehdit karşısında “Allah bize yeter; O ne güzel vekîldir” denir. 6:102 ve 39:62'de her şey üzerindeki vekîl oluş Allah'a bağlanır; 17:2'de Allah'tan başka vekîl edinmeme çağrısı vardır. Buradaki dayanma/gözetim alanı, her kullanımın modern vekâlet sözleşmesi olduğu anlamına gelmez.

10:108 ve 39:41'de hidayet/dalâletin kişiye dönmesi ile elçinin onların vekîli olmadığının söylenmesi birlikte bulunur. 6:107 ve 17:54 de elçinin insanlar üzerindeki vekîl konumunu sınırlar. Doğrudan görülen şey **kişinin yönelişinin kendisine dönmesi ve elçinin üzerlerindeki vekîl rolünün sınırlandırılmasıdır**. Ahlaki hesabın başkasına otomatik geçmediği sonucu, bu belirtilen bağlamlarla sınırlı bir çıkarımdır; vekîl kelimesinin bütün anlamlarının sözlük tanımı değildir. Bunlardan “insana hiçbir iş verilemez” şeklinde genel bir yasak çıkarılmaz.

Aynı kökün II. bâb fiilleri bu ayrımı açar:

- **6:89:** verilen kitabı, hükmü ve peygamberliği inkâr edenlere karşı, bunları inkâr etmeyen bir topluluğun bunlarla görevlendirilmesi anlatılır.
- **32:11:** ölüm meleği, muhataplarla ilgili görevlendirilmiş olarak anlatılır (`wukkila bikum`).

Görev verilmesi kök ailesinde vardır; 6:89 ve 32:11 doğrudan görev tahsisini örnekler, ahlaki hesabın devri hakkında ayrı bir hüküm söylemez. **Görevin yürütülmesi ile kişinin ahlaki hesabı ayrı sorulardır**; ilkine verilen cevap ikinciye otomatik taşınmaz. “Allah'a vekâlet vermek” ifadesi kullanılırsa bunun modern hukukî yetkilendirme veya Allah'a insanın üstünden verilen yetki olduğu izlenimi önlenmelidir. Metnin daha güvenli ifadesi: Allah'ı vekîl edinmek / O'na dayanmak.

## 6. Tafvîz — 40:44'ün kendi nesnesi

**40:44 — çalışma çevirisi:** “Size söylediklerimi hatırlayacaksınız. İşimi Allah'a havale ediyorum. Allah kulları görür.”

Kritik ifade `wa-ufawwiḍu amrī ilā llāh`: QAC'ta 40:44:5'in kök taşıyan segmenti **II. bâb, şimdiki/geniş zaman fiili**dir. Nesne `amrī`, “işim”dir. “Sonucu Allah'a bırakmak” yakın bir açıklama olabilir; “sonuç” ayetin nesnesiymiş gibi yazılmaz. [QAC 40:44](https://corpus.quran.com/wordbyword.jsp?chapter=40&verse=44)

40:28 ve 40:38–44 çevresinde konuşan kişi uyarır, gerekçe sunar ve doğru yola çağırır; 40:45'te kötülüklerden korunması anlatılır. Tafvîz beyanı, bu konuşma eylemi ve tutumla birlikte bulunur. Bu nedenle işini Allah'a havale etmenin burada ahlaki sorumluluğu bırakma veya susma olduğu sonucu desteklenmez.

Tevekkülün `ʿalā llāh` ile dayanmayı, tafvîzin `amrī ilā llāh` ile işi Allah'a havale etmeyi öne çıkarması **bu yapıların yerel ayrımıdır**. Farklı edatlar tek başına kesin sözlük sınırları kurmaz. Tek `fwD` geçişi bu cümlenin anlamını anlamlı biçimde destekleyebilir; tevekkül ile tafvîz arasında bütün bağlamları kapsayan kesin bir mertebe sırası kurmaya yetmez.

## 7. Birlikte geçişin kanıt gücü

Denetim raporu **Amn kökü + wkl kökü** ortak ayetlerini, **tam īmān isim lemması + wkl kökü** ortak ayetlerinden ayrı listeler. Kök düzeyindeki eşleşme, iman isminin geçtiği anlamına gelmez; mümin sıfatı, iman fiili veya başka bir türev eşleşmiş olabilir. Aynı ayette iki `wkl` kelimesi bulunması da ortak ayet sayısını iki yapmaz.

Köklerin ortak geçtiği **17 ayet** vardır; 17:68'deki ʾ-m-n fiili güvenlik bağlamındadır. Tam īmān isim lemması ile wkl kökü **2 ayette**, 3:173 ve 8:2'de buluşur. 3:173'teki wkl biçimi vekîl ismidir. Tam īmān ismi ile V. bâb tevekkül fiilinin ortak ayet sorgusu **yalnız 8:2'yi** verir. Bunlar farklı sorguların sonuçlarıdır; kavramsal ilişkinin yalnız bu ayetlerde bulunduğu iddiası değildir.

3:173'te iman artışı ve vekîl; 8:2'de iman artışı ve tevekkül bulunması **ilişki incelemek için bir başlangıçtır**. Ortak ayet sayısı veya yan yana geliş tek başına şu sonuçları kanıtlamaz:

- tam eşanlamlılık,
- iki kavramın mutlak olarak ayrılığı,
- birinin diğerinin zorunlu nedeni olması,
- her kullanımda zorunlu zaman sırası.

Ayrım, kelimelerin cümlede yaptıkları iş, tamamlayıcıları, özne ve bağlamlarıyla gerekçelendirilir. “İman ve tevekkül ayrı kelimeler; o halde aralarında kesin sınır var” çıkarımı da, “ikisine de güven deniyor; o halde aynılar” çıkarımı da yetersizdir.

## 8. Alternatif okuma, falsifikasyon ve dış tanıklar

**En güçlü alternatif:** İman birçok bağlamda inanma/tasdik ve dinî bağlılıkla; tevekkül ise Allah'a güvenip dayanmayla açıklanabilir. Bu okuma 12:17'nin haber tasdikini ve iman fiilinin önerme tamamlayıcılarını karşılar. “Güven bağı” sentezi bu karşılıkları dışlamak zorunda değildir. 3:159, rakip bir iman sözlüğü kurmaktan çok tevekkülün karar ve danışmayla ilişkisini aydınlatır.

| sınanan geniş iddia | baskı noktası | kayıt |
|---|---|---|
| IV. bâb āmana her yerde dinî iman demektir | 106:4 — güvenlik sağlama | çelişiyor; sağlam morfoloji + açık bağlam |
| muʾmin her yerde dinî kimliktir | 12:17 — kardeşlerin haberine inanma | kapsam daraltılmalı; sağlam yerel bağlam |
| tevekkül yalnız eylemin kendisidir | 3:159 — danışma, azim ve tevekkül ayrı görevler | eşitleme desteklenmiyor; eylemle ilişki korunur |
| tevekkül yalnız bütün eylemler bittikten sonra mümkündür | 12:67–68 | eylem tamamlanmadan beyan + sonradan uygulama; dışlayıcı genellemeyle çelişiyor |
| vekîl her yerde ahlaki hesabı devralır | 10:108, 39:41; görev fiilleri 6:89, 32:11 | bağlamların ayrılması gerekir |
| tafvîz, tevekkülden sonra zorunlu üst mertebedir | 40:44 ve wkl dağılımı | destek gösterilemedi; evrensel sıralama kurulmadı |

**İç-tanım durumu:** 3:159 ve 12:67 dayanmanın danışma/tedbirle ilişkisini açar; bir sözlük tanımı kalıbı değildir. **Kapalı örneklem durumu:** Kritik ayetler bu oturumun sorusunda ve önceki iman çalışmalarında zaten görülmüştür; hipotezden önce kilitlenmiş kapalı örneklem testi yapılmış gibi sunulmaz. Bu çalışma geriye dönük denetim ve kapsam düzeltmesidir.

**Kur'an öncesi ihtiyat:** Lane veya sonraki sözlüklerden bir karşılık bulmak, o karşılığın Kur'an öncesinde bu biçimle kullanıldığını kanıtlamaz. Tarihlenmiş, aidiyeti tartışılmış bağımsız şiir/yazıt/metin tanıkları gerekir. Sâmî kognatları eski bir anlam alanı için hipotez üretebilir; Kur'an öncesi Arapça kullanımın doğrudan tanığı veya Kur'an anlamının tayin edicisi değildir. Bu kayıtta yeni bir Kur'an öncesi tanık araştırması yapılmadı; “asıl/ilk anlam budur” iddiası kurulmadı.

## 9. Öğretici benzetmenin düzeltilmiş sınırı

Köprü örneğinde güvenilir görme, köprüye adım atma ve ağırlığını köprüye verme ayrı açılardan anlatılabilir. **Adım atma eylemi ile dayanma kavramsal olarak aynı şey değildir.** Fakat köprüye dayanmak yürüyüş sırasında sürer; bu örnek tevekkülü yalnız eylem sonrası bir evreye yerleştirmez.

“Mühendisliğinin kusursuz olduğundan emin olmak” iman için gereğinden güçlü bir açıklamadır; “güvenilir kabul etmek” daha ölçülüdür. Benzetme, imanın bütününü sadece zihne veya tevekkülü sadece bir fiziksel harekete indirgeyemez. Benzetme **anlatım aracıdır; ayet ve dilsel kanıt yerine kullanılmaz**.

## 10. Sonraki analizlere taşınacak kayıt

| önerme | mantıksal durum | delil derecesi ve kapsam |
|---|---|---|
| 3:159'da danışma ve karar tevekkülle birlikte korunur | Destekleniyor | Sağlam; ayetin açık yapısı |
| Hata yapmış toplulukla ilişki bağışlama ve danışmayla sürdürülür | Destekleniyor | Sağlam; 3:152, 155, 159 bağlam bağı; herkesin tek tek kusuru hakkında hüküm değil |
| Tedbir başarıyı mutlak biçimde garanti etmez; tevekkülle birlikte bulunabilir | Destekleniyor | Sağlam; 12:67 ve 3:160'ın belirtilen kapsamı |
| İncelenen iman, tevekkül, vekîl ve tafvîz yapıları arasında güven/dayanma ilişkisi vardır | Destekleniyor | Sağlam; belirtilen yerel bağlar. Bütün kullanımlar için ortak çekirdek bu incelemede belirlenmedi |
| Bu kavramlar her durumda kesin ayrık aşamalardır | Destek gösterilemedi | Spekülatif genel iddia; ortak geçiş veya benzetme bunu kanıtlamaz |
| İncelenen 3:121–160 ayetlerinde Uhud adı geçer | Çelişiyor | Sağlam metin denetimi; adlandırma tefsir/tarih katmanıdır |
| Kur'an öncesi ilk anlam bu oturumda belirlendi | Destek gösterilemedi | Spekülatif sonuç olarak benimsenmez; tarihsel tanık taraması yapılmadı |

**Kaynak hiyerarşisi:** Tanzil metni → QAC annotation ve yeniden sayım → sentaks/bağlam değerlendirmesi → kapsamlı fakat dereceli sentez. İbn Kesîr yalnız tarihsel/tefsirî çerçeve için kullanıldı. Dış kaynağın onaylaması bağımsız bir Kur'an içi kanıt değildir.

## 11. Sürüm ve köken notu

Bu kayıt, “Tevekkül-Vekil” sohbetinden çıkan sonuçları depoya aktarma talebi üzerine hazırlanmıştır. Aktarımda görülebilen kullanıcı metinleri ile kullanıcının belirttiği düzeltmeler araştırma gündemini oluşturdu. Eski asistan yanıtlarının tam metni bağlantıdan alınamadı; görünmeyen yanıtlar yeniden kurulmadı ve eksiksiz sohbet dökümü iddiası taşınmadı. Buradaki sonuçlar depo verisi ve açıkça gösterilen kaynaklardan yeniden doğrulandı.

**v1.0 — 11.10.2026:** QAC sayım birimleri ayrıldı; 106:4'ün IV. bâb güvenlik kullanımı ve 12:17'nin isim oluşu kaydedildi; 3:159'un yerel sırası genel zaman kuralından ayrıldı; Uhud tefsir katmanı etiketlendi; görev devri ile ahlaki sorumluluk ayrıldı; tafvîzin nesnesi düzeltildi; birlikte geçiş, benzetme ve Kur'an öncesi çıkarımların sınırları belirtildi. Mevcut iman dosyalarında aynı düzeltmelere kısa bağlantılar kondu; tam karşılaştırma burada tutulur.
