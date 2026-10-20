# İMAN — Kur’an İçi Aşamalı Analiz

**Sürüm:** v1.2 — 2026-10-20. v2.4 analiz protokolüne göre Aşama 6–8 denetimleri ve onaylanmış sade nihai kartla uyum sağlandı. Biçim sayımı/semantik sayım ayrımı, tasdik–güven alternatifleri ve delil sınırları korunur.

## Kısa sonuç

İman, Kur’an’ın olumlu dinî çağrısında yalnızca “bir şeyin var olduğuna inanmak” ile açıklanamaz. Kök ailesi ile inanma kullanımları ayrılarak şu **kapsamı sınırlı sözlüksel çalışma tanımı** önerilir:

**İnanma bağlamlarında `āmana`: bir kişiyi, mercii, haberi veya bildirimi doğru ya da güvenilir kabul ederek ona inanmak.** Bazı bağlamlarda tasdik, bazılarında bir kişiye/merciye itimat öne çıkar. Hangisinin tüm kullanımlarda öncelikli olduğu gösterilmiş değildir.

**Olumlu dinî iman:** Allah’ı ve O’ndan gelen rehberliği doğru/güvenilir kabul edip bunu içten benimsemek. Kur’an bunun insanın kararlarında, yöneliminde ve davranışlarında karşılık bulmasını ister.

**Anlam–işlev ayrımı:** Güven, sadakat, tevekkül ve salih amel imanla ilişkili olabilir; fakat ilgili davranışların tamamı sırf bu yüzden `īmān` kelimesinin zorunlu sözlük anlamına dahil edilmez. Haber tasdikiyle güven okuması birbirini otomatik dışlamaz. 106:4'teki güvenlik sağlama anlamı yukarıdaki inanma tanımının dışında kalır.

---

## Kaynak ve yöntem

Bu çalışma öncelikle Kur’an’ın kendi kullanımına dayanır.

- Arapça ayet metni: repoda sabitlenmiş Tanzil Quran Text v1.1, Simple Clean dosyası. Ayet metinleri değiştirilmeden verilmiştir.
- Morfoloji, kök ve lemma verisi: Quranic Arabic Corpus v0.4.
- Sayımlar: repodaki ham QAC verisinden yeniden üretilebilir scriptlerle çıkarılmıştır.
- Türkçe çeviriler: bu çalışmaya ait sade/kavramsal çevirilerdir; yayımlanmış bir mealden kopyalanmamıştır.
- Yöntem: [analiz protokolü v2.4](../../06_methodology/analiz_protokolu.md); Kur’an içi kök/morfoloji/sentaks/bağlam → semantik kümeler → karşı örnekler ve kilitli hipotez sınaması → en güçlü tasdik alternatifi → İbn Fâris/Râgıb/Lane/Sâmî dış kaynak denetimi → delil dereceli sentez. Dış kaynakların taranması zorunludur; Kur’an içi anlamı kendiliğinden tayin ettikleri iddia edilmez.

Kaynak ve lisans ayrıntıları için: [SOURCES.md](../../SOURCES.md) ve [LICENSES.md](../../LICENSES.md).

---

# Aşama 1 — Kök ailesi ne söylüyor?

İman, ʾ-m-n (QAC Buckwalter: `Amn`) kök ailesindedir.

QAC v0.4 verisinde bu kök etiketi 879 kelime konumunda görülür; 723 ayete ve 77 sûreye dağılır. Başlıca biçimler arasında āman(a) fiil ailesi, īmān, muʾmin, amina, amīn, amn ve amāna türevleri vardır.

Kök ailesini incelemek için üç anlam alanı ayırt edilebilir; aşağıdaki biçim örnekleri tek anlamlı, birbirini dışlayan sınıflar değildir:

1. Doğru/güvenilir kabul etme, inanma ve bağlanma: āman(a), īmān, muʾmin kullanımları.
2. Güvenlik ve emniyet: amina, amn, āmin.
3. Güvenilirlik ve emanet: amīn, amāna.

Kök ailesi geniş bir **güven – güvenilirlik – güvenlik** alanına ilişkin hipotez üretir. Fakat aynı biçim farklı anlamlarda çalışabilir: 106:4’te IV. bâb *āmanahum* güvenlik sağlamayı anlatır. Kök ailesinin genişliği, *īmān* kelimesinin tek tek kullanımlarında haber tasdiki anlamını dışlamaz.

Bu aşama tek başına “iman = güven” sonucunu kanıtlamaz. Kök akrabalığı yalnız hipotez üretir. Hipotezin Kur’an’daki fiil kullanımlarıyla sınanması gerekir.

Teknik ayrıntı: [Amn — Aşama 1](Amn-quran-internal-stage1.md).

---

# Aşama 2 — Āmana fiili nasıl çalışıyor?

QAC’ta āman(a) lemma ailesinin IV. bâb **537 fiil kelime konumu** vardır. Bu morfolojik toplam, “537 dinî inanma kullanımı” değildir: 106:4:5’te *wa-āmanahum* korkuya karşı güvenlik sağlamadır. Biçimin IV. bâb olması anlamı otomatik belirlemez. [QAC 106:4:5](https://corpus.quran.com/wordmorphology.jsp?location=(106:4:5))

Yüzey taramasında fiilden hemen sonra 163 açık bi- adayı ve 18 li- adayı bulunmuştur. Li- adaylarının manuel kontrolünde 15 gerçek tamamlayıcı belirlenmiş; bunların 14’ünün kişi hedefli olduğu görülmüştür.

Bu veri, fiilin kişi ve bildirimlerle kurduğu ilişkiyi incelemeye yarar. Bir kişinin sözünü doğru kabul etme (tasdik) ile ona itimat etme burada rakip olmak zorunda değildir; kişi hedefli tamamlayıcı tek başına bilişsel tasdik okumasını çürütmez.

## Kritik ayet: Tevbe 9:61

ومنهم الذين يؤذون النبي ويقولون هو أذن قل أذن خير لكم يؤمن بالله ويؤمن للمؤمنين ورحمة للذين آمنوا منكم والذين يؤذون رسول الله لهم عذاب أليم

**Sade/kavramsal çeviri:** İçlerinden Nebi’yi inciten ve “O her söylenene kulak veriyor” diyenler vardır. De ki: “O sizin için hayra kulak verir; Allah’a iman eder ve müminlere güvenir; sizden iman edenler için bir rahmettir.” Allah’ın elçisini incitenler için acı bir azap vardır.

**Bu ayet neyi gösteriyor?** Aynı özne ve aynı fiil iki farklı yapıda kullanılıyor: “Allah’a iman eder” ve “müminlere güvenir.” İkinci kullanım, müminlerin var olduğuna zihinsel olarak inanmak değildir; bağlam açık biçimde onların sözünü güvenilir bulma/itimat etme ilişkisidir. Böylece āman(a) fiilinin güven boyutu Kur’an’ın kendi içinde görünür hale gelir.

Ancak buradan “bi- her zaman şu, li- her zaman bu demektir” şeklinde mekanik bir kural çıkarılamaz. Bi- yapısı da insan, elçi, vahiy, ayet, gayb, ahiret ve başka hedeflerle kullanılabilir.

Yûsuf 12:17’de *bi-muʾminin lanā* kardeşlerin anlatısına inanılmasıyla ilgilidir. Bu, dinî bağlılığın bütün kullanımlara yüklenemeyeceği bir karşı örnektir. QAC 12:17:14’ü IV. bâbdan **ism-i fâil (`N`)** olarak işaretler; bu kelime yukarıdaki 537 çekimli fiile eklenmez. [QAC 12:17](https://corpus.quran.com/wordbyword.jsp?chapter=12&verse=17)

Teknik ayrıntı: [Amn — Aşama 2: sentaks](Amn-quran-internal-stage2-syntax.md).

---

# Aşama 3 — “İman etmek” fiili kendi başına hakikat garantisi taşıyor mu?

Hayır. Kur’an, āman(a) fiilini yanlış hedefler için de kullanır. Bu, kavramı anlamak için en güçlü karşı örneklerden biridir.

## Ankebût 29:52

قل كفى بالله بيني وبينكم شهيدا يعلم ما في السماوات والأرض والذين آمنوا بالباطل وكفروا بالله أولئك هم الخاسرون

**Sade/kavramsal çeviri:** De ki: “Benimle sizin aranızda tanık olarak Allah yeter. O, göklerde ve yerde olanı bilir.” Bâtıla iman eden ve Allah’ı inkâr edenler, işte kaybedenler onlardır.

**Bu ayet neyi gösteriyor?** Kur’an açıkça “bâtıla iman etmek” ifadesini kullanıyor. Demek ki āman(a) fiilinin sözlük yapısı kendi başına “hakikati kabul etmek” anlamını garanti etmiyor. İnsan yanlış bir hedefi de doğru/güvenilir kabul edip ona bağlanabilir. Değer, güven ilişkisinin hangi hedefe yöneltildiğine bağlıdır.

Bu nedenle “iman” kelimesini daha baştan yalnız kutsal-teknik bir etiket olarak tanımlamak yeterli değildir; fiilin kurduğu ilişkinin yapısına bakmak gerekir.

## Mâide 5:41 — sözlü beyan yeterli mi?

يا أيها الرسول لا يحزنك الذين يسارعون في الكفر من الذين قالوا آمنا بأفواههم ولم تؤمن قلوبهم ومن الذين هادوا سماعون للكذب سماعون لقوم آخرين لم يأتوك يحرفون الكلم من بعد مواضعه يقولون إن أوتيتم هذا فخذوه وإن لم تؤتوه فاحذروا ومن يرد الله فتنته فلن تملك له من الله شيئا أولئك الذين لم يرد الله أن يطهر قلوبهم لهم في الدنيا خزي ولهم في الآخرة عذاب عظيم

**Sade/kavramsal çeviri:** Ey Elçi! Küfre koşanlar seni üzmesin: ağızlarıyla “İman ettik” dedikleri halde kalpleri iman etmemiş olanlar ve Yahudilerden yalana kulak verenler, sana gelmemiş başka bir topluluğa kulak verenler... Sözleri yerlerinden kaydırırlar; “Size bu verilirse alın, verilmezse sakının” derler. Allah kimin sınanmasını/sapmasını dilerse onun için Allah’a karşı hiçbir şeye güç yetiremezsin. Bunlar Allah’ın kalplerini arındırmayı istemediği kimselerdir. Dünyada onlar için rezillik, ahirette büyük bir azap vardır.

**Bu ayet neyi gösteriyor?** “Ağızlarıyla iman ettik” demek ile “kalplerinin iman etmesi” aynı şey değildir. İman salt sözlü kimlik beyanı değildir.

Teknik ayrıntı: [Amn — Aşama 3: bi- kullanımları](Amn-quran-internal-stage3-bi.md).

---

# Aşama 4 — İman artabilir mi?

Evet. QAC’ta īmān isim lemması 45 kez geçer. Manuel kontrolde 6 ayette 7 açık “iman artışı” ifadesi bulunur.

Bu ayetler, imanın artışla nitelenebildiğini gösterir. Artışı güvenin, doğrulamanın ve bağlılığın güçlenmesi olarak okumak bağlamla desteklenen bir yorumdur; her bağlamda artan boyutun aynı olduğu veya yeni öğrenilen içeriğin hiçbir katkısı olmadığı sonucu çıkmaz.

## Âl-i İmrân 3:173

الذين قال لهم الناس إن الناس قد جمعوا لكم فاخشوهم فزادهم إيمانا وقالوا حسبنا الله ونعم الوكيل

**Sade/kavramsal çeviri:** İnsanlar onlara, “İnsanlar size karşı toplandı; onlardan korkun” dediklerinde bu onların imanını artırdı ve “Allah bize yeter; O ne güzel vekildir” dediler.

**Gösterdiği şey:** Tehdit haberi karşısında imanın artması ve “Allah bize yeter; O ne güzel vekîldir” cevabı birlikte anlatılır. Bunu güvenin güçlenmesi olarak okumak bağlamsal bir yorumdur; birlikte geçiş *īmān* ile *vekîl* kelimelerinin eşanlamlı olduğunu göstermez.

## Enfâl 8:2

إنما المؤمنون الذين إذا ذكر الله وجلت قلوبهم وإذا تليت عليهم آياته زادتهم إيمانا وعلى ربهم يتوكلون

**Sade/kavramsal çeviri:** Müminler, Allah anıldığında kalpleri duyarlılıkla ürperen; O’nun ayetleri kendilerine okunduğunda imanları artan ve Rablerine güvenip dayanan kimselerdir.

**Gösterdiği şey:** Ayetlerin okunmasıyla iman artışı ve Rabbe tevekkül aynı müminlerin özellikleri olarak sıralanır. Birlikte geçiş anlam ilişkisini araştırmaya yarar; tek başına eşanlamlılık, kesin anlam ayrılığı veya nedensellik kanıtı değildir. Ayrım için ayrıca fiilin tamlayıcısı ve eylem bağlamı incelenir.

## Tevbe 9:124

وإذا ما أنزلت سورة فمنهم من يقول أيكم زادته هذه إيمانا فأما الذين آمنوا فزادتهم إيمانا وهم يستبشرون

**Sade/kavramsal çeviri:** Bir sûre indirildiğinde içlerinden bazıları, “Bu hanginizin imanını artırdı?” der. İman edenlere gelince, o sûre onların imanını artırır ve onlar sevinirler.

**Gösterdiği şey:** Yeni vahiy, mevcut iman ilişkisini güçlendirebilir.

## Ahzâb 33:22

ولما رأى المؤمنون الأحزاب قالوا هذا ما وعدنا الله ورسوله وصدق الله ورسوله وما زادهم إلا إيمانا وتسليما

**Sade/kavramsal çeviri:** Müminler birleşmiş düşman gruplarını gördüklerinde, “Bu, Allah’ın ve Elçisi’nin bize vaat ettiği şeydir; Allah ve Elçisi doğru söyledi” dediler. Bu durum onların yalnız imanını ve teslimiyetini artırdı.

**Gösterdiği şey:** Yaşanan olayın daha önce verilen sözü doğrulaması, iman artışıyla ilişkilendiriliyor. Bunu “doğrulanmayla güvenin güçlenmesi” diye açıklamak bağlamsal yorumdur; ayet bütün iman kullanımlarını tanımlayan bir sözlük eşitliği kurmaz.

## Fetih 48:4

هو الذي أنزل السكينة في قلوب المؤمنين ليزدادوا إيمانا مع إيمانهم ولله جنود السماوات والأرض وكان الله عليما حكيما

**Sade/kavramsal çeviri:** Müminlerin kalplerine, mevcut imanlarının yanında imanlarını artırmaları için sekînet indiren O’dur. Göklerin ve yerin orduları Allah’ındır. Allah bilendir, hikmet sahibidir.

**Gösterdiği şey:** İman kalple ve sekînetle ilişkilidir; mevcut imanın üzerine daha fazla iman gelebilir.

## Müddessir 74:31

وما جعلنا أصحاب النار إلا ملائكة وما جعلنا عدتهم إلا فتنة للذين كفروا ليستيقن الذين أوتوا الكتاب ويزداد الذين آمنوا إيمانا ولا يرتاب الذين أوتوا الكتاب والمؤمنون وليقول الذين في قلوبهم مرض والكافرون ماذا أراد الله بهذا مثلا كذلك يضل الله من يشاء ويهدي من يشاء وما يعلم جنود ربك إلا هو وما هي إلا ذكرى للبشر

**Sade/kavramsal çeviri:** Ateşin görevlilerini yalnız melekler yaptık; sayılarını da inkâr edenler için bir sınama yaptık ki kendilerine Kitap verilenler kesinlik kazansın, iman edenlerin imanı artsın, Kitap verilenler ve müminler kuşkuya düşmesin; kalplerinde hastalık bulunanlar ve kâfirler ise “Allah bununla ne demek istedi?” desinler. Allah dileyeni böylece sapmada bırakır, dileyeni rehberliğe yöneltir. Rabbinin ordularını O’ndan başkası bilmez. Bu, insanlar için bir hatırlatmadan başka bir şey değildir.

**Gösterdiği şey:** Kesinlik kazanma, kuşkunun azalması ve imanın artması aynı bağlamda bulunur. Bu, bilgi/kesinlik ile iman arasındaki ilişkinin incelenmesini destekler; birlikte sıralanma tek başına bunların tam eşanlamlı veya kesinlikle ayrı olduğunu kanıtlamaz. Yeni bilgi/göstergenin güven bağını güçlendirmesi mümkün bir açıklamadır.

### Ara sonuç

Bu altı ayet birlikte değerlendirildiğinde iman artışı şu bağlamlarda gerçekleşir:

- vahyin okunması ve yeni vahiy,
- ilahî vaadin olaylarla doğrulanması,
- tehdit karşısında Allah’a güvenin korunması,
- kalbe sekînet gelmesi,
- kesinliğin artması ve kuşkunun azalması.

Bunları tek çatı altında en iyi açıklayan hipotez, **güven/doğrulama/bağlılık ilişkisinin güçlenmesidir.**

Teknik ayrıntı: [Amn — Aşama 4: īmān isim kullanımı](Amn-quran-internal-stage4-iman-noun.md).

---

# Aşama 5 — İman kalpte midir, davranışta mıdır?

Kur’an’ın cevabı “yalnız biri” değildir. İman kalple ilişkilidir; fakat davranıştan bütünüyle kopuk bir iç duygu da değildir.

## Nahl 16:106 — dış baskı ile iç yönelim ayrımı

من كفر بالله من بعد إيمانه إلا من أكره وقلبه مطمئن بالإيمان ولكن من شرح بالكفر صدرا فعليهم غضب من الله ولهم عذاب عظيم

**Sade/kavramsal çeviri:** İmanından sonra Allah’ı inkâr eden kimse — zorlandığı halde kalbi imanla güven içinde olan hariç — fakat kim göğsünü küfre açarsa, onların üzerine Allah’tan bir öfke vardır ve onlar için büyük bir azap vardır.

**Gösterdiği şey:** Zorla yaptırılan dış beyan ile kişinin iç yönelimi aynı değildir. Kalbin “imanla mutmain” kalması özel olarak korunuyor. Bu, imanın içsel güven/bağlılık boyutunun en açık göstergelerindendir.

## Hucurât 49:14 — “iman ettik” demek yeterli mi?

قالت الأعراب آمنا قل لم تؤمنوا ولكن قولوا أسلمنا ولما يدخل الإيمان في قلوبكم وإن تطيعوا الله ورسوله لا يلتكم من أعمالكم شيئا إن الله غفور رحيم

**Sade/kavramsal çeviri:** Bedeviler, “İman ettik” dediler. De ki: “Henüz iman etmediniz; ‘teslim olduk’ deyin. Çünkü iman henüz kalplerinize girmedi. Eğer Allah’a ve Elçisi’ne itaat ederseniz, yaptıklarınızdan hiçbir şeyi eksiltmez. Allah bağışlayandır, merhametlidir.”

**Gösterdiği şey:** Sözlü iman iddiası ile kalbe yerleşmiş iman aynı değildir. Ayet aynı zamanda teslimiyet davranışının başlamasıyla imanın içselleşmesinin tek bir mekanik aşama olmadığını gösterir.

## Bakara 2:143 — iman davranışla ilişkisiz mi?

وكذلك جعلناكم أمة وسطا لتكونوا شهداء على الناس ويكون الرسول عليكم شهيدا وما جعلنا القبلة التي كنت عليها إلا لنعلم من يتبع الرسول ممن ينقلب على عقبيه وإن كانت لكبيرة إلا على الذين هدى الله وما كان الله ليضيع إيمانكم إن الله بالناس لرءوف رحيم

**Sade/kavramsal çeviri:** Böylece sizi dengeli/orta bir topluluk yaptık ki insanlar üzerine tanık olasınız, Elçi de sizin üzerinize tanık olsun. Daha önce yöneldiğin kıbleyi, Elçi’ye uyan ile gerisin geri döneni ortaya çıkarmak için belirlemiştik. Bu, Allah’ın rehberlik ettikleri dışında ağır geldi. Allah sizin imanınızı boşa çıkaracak değildir. Allah insanlara karşı çok şefkatli ve merhametlidir.

**Gösterdiği şey:** Ayetin bağlamı kıble ve Elçi’ye fiilen uyma sınamasıdır; buna rağmen “imanınızı boşa çıkarmaz” denir. Buradan “iman = namaz” diye sözlük eşitliği çıkarılamaz. Daha güvenli sonuç şudur: Allah’ın yönlendirmesine güvenerek gösterilen sadık uyum iman kapsamında değerlendirilebilir.

## En‘âm 6:158 — iman ve hayır kazanmak

هل ينظرون إلا أن تأتيهم الملائكة أو يأتي ربك أو يأتي بعض آيات ربك يوم يأتي بعض آيات ربك لا ينفع نفسا إيمانها لم تكن آمنت من قبل أو كسبت في إيمانها خيرا قل انتظروا إنا منتظرون

**Sade/kavramsal çeviri:** Onlar meleklerin gelmesini, Rabbinin gelmesini veya Rabbinin bazı ayetlerinin gelmesini mi bekliyorlar? Rabbinin bazı ayetleri geldiği gün, daha önce iman etmemiş veya imanı içinde bir hayır kazanmamış kişiye o anda iman etmesi yarar sağlamaz. De ki: “Bekleyin; biz de bekliyoruz.”

**Gösterdiği şey:** Ayet, daha önce iman etmiş olmak ile “imanı içinde hayır kazanmak” arasında ilişki kurar. İman davranışın eş anlamlısı değildir; fakat davranıştan kopuk, sonuçsuz bir etiket de değildir.

## Şûrâ 42:52 — vahiy ve imanın içeriği

وكذلك أوحينا إليك روحا من أمرنا ما كنت تدري ما الكتاب ولا الإيمان ولكن جعلناه نورا نهدي به من نشاء من عبادنا وإنك لتهدي إلى صراط مستقيم

**Sade/kavramsal çeviri:** İşte böyle, emrimizden bir ruhu sana vahyettik. Sen Kitab’ın ne olduğunu da bu imanın ne olduğunu da bilmiyordun. Fakat onu, kullarımızdan dilediğimizi kendisiyle yönlendirdiğimiz bir nur yaptık. Sen de gerçekten dosdoğru bir yola yöneltiyorsun.

**Gösterdiği şey:** İmanın vahiy tarafından biçimlenen/bilinen bir içeriği vardır. Ayetten “Nebi daha önce Allah’ın varlığına inanmıyordu” sonucu çıkarmak zorunlu değildir. Daha dar ve güvenli sonuç: Kitab’ın ve vahyin tanımladığı iman yolu/içeriği vahiy ile açıklanmıştır.

### Ara sonuç

Kur’an içindeki iman:

- kalpte yerleşebilir,
- kalpteki sekînetle artışı birlikte anlatılabilir,
- sözlü iddiadan farklı olabilir,
- davranış ve sadakat üretebilir,
- vahiy ile güçlenebilir ve içerik kazanabilir.

Bu nedenle “iman yalnız iç duygudur” ve “iman yalnız ameldir” tanımlarının ikisi de yetersizdir.

---

# Aşama 6 — İman sabit ve geri döndürülemez bir kimlik midir?

Hayır. Kur’an iman ile küfür arasında yön değişimini açıkça anlatabilir.

## Âl-i İmrân 3:90

إن الذين كفروا بعد إيمانهم ثم ازدادوا كفرا لن تقبل توبتهم وأولئك هم الضالون

**Sade/kavramsal çeviri:** İmanlarından sonra küfre yönelen, ardından küfürlerini artıranların tövbeleri kabul edilmeyecektir; işte onlar sapmış olanlardır.

**Bu ayet neyi gösteriyor?** İman da küfür de güçlenebilen yönelimler olarak anlatılabilir. Bu ayette artan şey iman değil küfürdür. Dolayısıyla “bir kere iman etiketi aldıktan sonra ilişkinin niteliği artık değişmez” anlayışı Kur’an’ın diline uymaz.

16:106 ile birlikte düşünüldüğünde sınır daha da belirginleşir: dış baskı altında söylenen söz otomatik olarak iman bağını koparmaz; buna karşılık kişinin iç yönelimini küfre açması farklı bir durumdur.

---

# Aşama 7 — Klasik sözlükler, Lane ve Sâmî dil denetimi (v2.4)

Bu kaynaklar **zorunlu taranır**, fakat anlam kararında Kur’an içi metin birincildir. Her madde dil-içi kullanım, hadis/rivayet, tefsir, sonraki teknik terim ve bağımsız tarihsel tanık bakımından ayrılır.

| Kaynak | Kaydedilen anlam alanı / katkı | Kanıt sınırı |
|---|---|---|
| **İbn Fâris, Mekâyîs, e-m-n** | Emanet/güvenilirlik ile tasdik için iki yakın asıl anlam; 12:17'nin sözün doğru bulunması bağlamı | Dilsel açıklama; bütün `īmān` kullanımlarını tek başına belirlemez |
| **Râgıb, Müfredât, e-m-n** | Emniyet, tasdik, güven bağlantısı; 106:4 ve 12:17 örnekleri | Kalp–dil–amel şeklindeki dinî tarifin hadis/rivayet ve şer'î yorumla desteklenen kısımları doğrudan sözlük kanıtı yapılmaz |
| **Lane, Arabic-English Lexicon, ʾ-m-n** | Güvende olma, güvenme, güvenilirlik, güvenlik sağlama, tasdik ve inanma; `bi-`/`li-` kullanımlarını çapraz kontrol | Klasik Arap sözlüklerini derler; aynı geleneğin üçüncü bağımsız tanığı sayılmaz |
| **İbranice ʾ-m-n (BDB)** | Sağlamlık, doğrulanmışlık/güvenilirlik, güvenme ve inanma | Akraba dil karşılığı; Kur’an öncesi Arapça anlam sırasını ispatlamaz |
| **Aramice/Süryanice hymn / hayman- (CAL, SEDRA)** | İnanma, güvenme, güvenilirlik; Süryanice dinî iman terminolojisi | Yüzey biçim farklılıkları ve tarihsel morfoloji ihtiyatla ele alınır; iki dil tam bağımsız kanıt değildir |

Kaynaklar: [İbn Fâris ve Râgıb için protokolün kaynak notları](../../06_methodology/analiz_protokolu.md), [Lane](https://www.arabic-english-dictionary.com/content/01_a/135_amn), [BDB ʾ-m-n](https://biblehub.com/hebrew/539.htm), [CAL hymn](https://cal.huc.edu/JLAentry.php?cits=all&lemma=hymn+V), [Sâmî kognat pilotu](../../04_lexicons/semitic/reviews/Amn.md).

**Üçlü kontrol:**
1. **Örtüşme:** Güven/güvenilirlik, inanma ve tasdik arasındaki ilişki Kur’an kullanımları ve sözlüklerde görülür.
2. **Sözlükte olup bağımsız Kur’an tanımı olmayan:** Bütün iman kullanımlarında güvenin zorunlu olması; dinî iman için kalp–dil–amelin üçünün birlikte kelimenin sözlüksel anlamı sayılması; 2:143'teki `īmān`ın genel sözlükte doğrudan salât olması.
3. **Kur’an'ın özel olarak gösterdiği:** 106:4 IV. bâb güvenlik sağlama; 29:52 bâtıla iman; 49:14 beyan/kalp ayrımı; 9:61 `bi-`/`li-` karşılaştırması; 8:2 iman artışı.

**Tarihsel sınır:** Kur’an öncesi Arapça için tarihlenebilir bağımsız şiir/yazıt/metin üzerinden bu analizde tam ayrı tanık doğrulaması yapılmadı. Bu yüzden kökün kesin ilk anlamı veya anlamların kesin tarihsel gelişim sırası ileri sürülmez. İbranice ve Aramice/Süryanice benzerlikleri destekleyici dil tarihi verisidir; Arapça için doğrudan tarih belgesi değildir.

---

# Aşama 6'nın tamamlayıcı denetimi — Tasdik görüşünün güçlü biçimi

Rakip okuma yalnız “Allah vardır” düşüncesi değildir. Güçlü **kalbî tasdik** yaklaşımı, haberin ve haber veren merciin doğruluğunu içten benimsemeyi ifade eder; sözlü iddia ile gerçek kabulü ayırabilir. 12:17, 9:61, 10:90, 29:52 ve 49:14 gibi bağlamlarda tasdik görüşü doğrudan veya uyumlu açıklama sunar. 8:2, 3:173 gibi iman artışı kullanımlarında da tasdikin kesinliğinin/kuvvetinin artması bir yorum seçeneğidir.

**Rekabet hükmü:** Güçlü tasdik görüşü çürütülemedi. Güven merkezli okuma da elenmedi. Birçok bağlamda örtüşürler; hangi boyutun tarihsel/lexical olarak öncelikli olduğu gösterilemedi. Güçlü tasdik görüşü doğrudan sözlük karşılığı ile imanın ahlaki sonucunu ayrı tutarak daha az ilave unsur gerektirebilir. Buna karşılık güven bağlantısı kök ailesi ve kişiler arası kullanımlarda belirgindir.

---

# Falsifikasyon özeti

Bu analiz sırasında aşağıdaki dar tanımlar sınandı:

### “İman = yalnızca bir şeyin var olduğuna inanmak.”

Yetersizdir. 9:61’de fiil kişiler arası güven ilişkisi kurar; 49:14 ve 5:41’de sözlü beyan ile kalpteki iman ayrılır.

### “Āmana fiili her zaman hakikati kabul etmek demektir.”

Nesnel hakikat garantisi anlamında yanlıştır: 29:52 bâtıla iman etmekten söz eder. Kişinin yanlış bir bildirimi doğru **sayması** anlamındaki tasdik okuması bu karşı örnekle çürütülmez. Ayrıca 106:4, IV. bâbın bütün örneklerinin inanma anlamında olduğunu dışlar.

### “İnsan hedefli iman kullanımı tasdik olamaz.”

Desteklenmez. 9:61 ve 12:17 kişinin sözünü doğru/güvenilir kabul etme okumalarına açıktır. İmanı salt varlık kabulüne indirgememek, haber tasdikini anlam alanından çıkarmayı gerektirmez.

### “İman = yalnız kalpteki duygu.”

Yetersizdir. 2:143 ve 6:158 iman ile fiilî sadakat/hayır arasında ilişki kurar.

### “İman = yalnız amel.”

Yetersizdir. 16:106 ve 49:14 kalpteki iman durumunu açıkça ayırır.

### “İman = namaz.”

Sözlük eşitliği olarak desteklenmez. 2:143, kıble/uyma davranışını iman kapsamında değerlendirir; iman kelimesini salâtın eş anlamlısı yapmaz.

### “İman artmaz; kişi ya inanır ya inanmaz.”

Yanlıştır. 3:173, 8:2, 9:124, 33:22, 48:4 ve 74:31 imanın arttığını açıkça söyler.

---

# Aşama 8 — Kapsamı sınırlı sentez

**Kesin morfolojik/veri düzeyi:** QAC v0.4'te e-m-n kökü 879 kelime konumunda, 723 ayette ve 77 sûrede görünür; IV. bâb çekimli `āmana` fiili 537, `īmān` ismi 45, `muʾmin` biçim ailesi 230 kelime konumundadır. Bunlar **anlam sayısı değildir**. 106:4'te IV. bâb güvenlik sağlama; 12:17'de `muʾmin` dinî olmayan haber kabulü bağlamındadır.

**Güçlü çıkarım — inanma kullanımının sözlüksel çalışma tanımı:** Bir kişiyi, mercii, haberi veya bildirimi **doğru ya da güvenilir kabul ederek ona inanmak**. Tasdik ve güven bazı bağlamlarda örtüşür; birini bütün kullanımlarda diğerinden önceleyen karar verici delil yoktur.

**Kur’an'ın olumlu dinî iman anlatımı:** Allah'ı ve O'ndan gelen rehberliği doğru/güvenilir kabul ederek içten benimsemek. 49:14 ve 16:106 içsel gerçekliği sözlü beyana indirgememeyi gerektirir. 8:2–4, 49:15, 2:143 ve 3:81 gibi pasajlar güven, tevekkül, yönelim ve davranışı imanla ilişkilendirir; bu, sözlük eşitliği değildir.

**Açık ihtimaller:** İmanın tarihsel olarak önce “güven”, sonra “tasdik” veya tersi yönde geliştiği gösterilmedi. Güvenin her inanma kullanımının zorunlu sözlük bileşeni olduğu, sadakat/itaatin doğrudan `īmān` kelimesine dahil olduğu kanıtlanmadı.

**Karşı örnekler ve yöntem sınırı:** 29:52 yanlış hedefe iman etmeyi gösterir. 67:29 iman ve tevekkülü ayrı sözcüklerle kullanır. 48:25 dışarıdan tanınmayan müminleri anlatır; mümin olmanın daima dışarıdan görünür olduğu iddiası desteklenmez. İncelenen 16 örnek bağımsız kör test değildir; bütün 879 konum tek tek semantik etiketlenmiş değildir. Ayrıca `analyze_amn_verb_syntax.py` betiğinde `POS:P` alt dizesinin `POS:PRO` vb. etiketlerde yanlış eşleşmesi nedeniyle otomatik 'other_prep' sınıfında 31 sahte kayıt bulunmuştur; **kök/lemma toplamları etkilenmez**, bu alt sentaks raporunun düzeltilmesi ayrı teknik iştir.

**Delil hükmü:** Kur’an içi bağlamlarda “salt varlık kabulü” tanımı yetersizdir. Güçlü kalbî tasdik ile doğru/güvenilir kabul-güven okuması rekabette kalmaktadır; nihai tarihsel üstünlük iddiası **belirsiz**. Sınırlı sözlüksel çalışma tanımı **muhtemel**; sayım, biçim ve açık ayet ilişkileri **sağlam veri** niteliğindedir.

## İman, eylem ve tevekkül ilişkisi

3:159’da danışma ve karar verme, Allah’a tevekkülle birlikte korunur. Tevekkül bu eylemlerin yerine geçmez; fakat “önce iman tamamen biter, sonra eylem, en son tevekkül başlar” şeklinde zorunlu zaman dilimleri de metinden çıkmaz. 3:122 tevekkülü mücadele bağlamında gösterir; ayet sırası tek başına psikolojik veya tarihsel zaman çizelgesi değildir. 12:67–68'de tevekkül beyanı ile daha sonra uygulanan kapı talimatı, tevekkül için eylemin bütünüyle bitmiş olmasının gerekmediğini destekler; düşünmenin veya kararın henüz tamamlanmadığını ayrıca kanıtlamaz. İman, eylem ve tevekkül kavramsal olarak ayrıştırılabilir; aralarındaki ilişki mekanik bir aşama şeması değildir.

“Sonucu Allah’a bırakmak” yararlı bir açıklama olabilir; 3:159’un kelimesi kelimesine tercümesi veya tevekkülün bütün anlamını tüketen tanım değildir. Sorumluluk, vekîl ve 40:44’teki tafvîz ilişkisi için [Tevekkül–Vekîl karşılaştırması](Tawakkul-Wakil-analysis.md) esas alınır; bu dosyaya bütün ayrıntıları taşınmaz.

---

# Kısa kavram kartı

**Sözlüksel çalışma tanımı (inanma kullanımları):** Bir kişi, merci, haber veya bildirimi doğru ya da güvenilir kabul ederek ona inanmak.

**Olumlu dinî iman:** Allah’ı ve O’ndan gelen rehberliği doğru/güvenilir kabul edip içten benimsemek; Kur’an bu kabulün kararlar ve davranışlarda karşılık bulmasını ister.

**Anlam–işlev sınırı:** Tasdik ve güven birbirini dışlamak zorunda değildir. Tevekkül, itaate yönelme ve salih amel ilişkilidir; zorunlu eşanlamlılar değildir. Güvenin tasdik karşısında tarihsel önceliği kanıtlanmış değildir.

İman yalnız söz değildir; 5:41 ve 49:14.

İnanma fiili, kabul edilen hedefin nesnel hakikatini garanti etmez; 29:52.

İman artabilir; 3:173, 8:2, 9:124, 33:22, 48:4, 74:31.

İman kalple ilişkilidir ama davranıştan kopuk değildir; 16:106, 2:143, 6:158.

Kısa kartın ayrı dosyası: [İman — Kavram Kartı](Amn-concept-card.md).

---

# Teknik iz ve yeniden üretilebilirlik

Bu kamuya açık ana analiz, aşağıdaki teknik/ara denetim dosyalarının sonuçlarını toparlar:

- [Aşama 1 — kök profili](Amn-quran-internal-stage1.md)
- [Aşama 2 — fiil sentaksı](Amn-quran-internal-stage2-syntax.md)
- [Aşama 3 — bi- hedefleri](Amn-quran-internal-stage3-bi.md)
- [Aşama 4 — īmān isim kullanımı](Amn-quran-internal-stage4-iman-noun.md)
- [li- manuel denetimi](Amn-li-manual-review.tsv)
- [bi- zamir manuel denetimi](Amn-bi-pronoun-manual-review.tsv)
- [bi- sıra dışı vakalar](Amn-bi-other-manual-review.tsv)
- [iman artışı manuel denetimi](Amn-iman-increase-manual-review.tsv)

Bu dosyalar, ana metindeki sayısal ve sentaktik sonuçların nasıl üretildiğini denetlemek isteyen okuyucu içindir.

## v1.1 düzeltme kaydı — 2026-10-11

- **537 “iman etme” kullanımı → 537 IV. bâb fiil kelime konumu:** 106:4’ün güvenlik sağlama anlamı morfolojik kümenin içindedir; yeni bir semantik toplam ileri sürülmedi.
- **Kişi hedefi tasdiki dışlar → sözün tasdiki ve güven birlikte mümkün:** 12:17’nin ism-i fâil olduğu, çekimli fiil olmadığı açıklandı.
- **Kök/biçimden genel tanım → bağlamla sınırlı anlam önerisi:** olumlu dinî çağrı ile kök ailesinin tamamı ayrıldı.
- **Birlikte geçişten anlam/nedensellik → ilişkiyi araştırma işareti:** 3:173 ve 8:2 üzerinden iman–tevekkül özdeşliği ya da kesin ayrılığı ispatlanmadığı belirtildi.
- **Sâmî bağımsız kontrol → ikincil hipotez:** Kur’an öncesi kullanım hakkında tarihlenmiş tanık bulunmadan sonuç kurulmayacağı kaydedildi.

**v1.2 değişiklik kaydı — 2026-10-20:** Aşama 6'nın en güçlü tasdik okuması, v2.4 zorunlu Lane/Sâmî karşılaştırması ve Aşama 8'in kesin veri/güçlü çıkarım/açık ihtimal ayrımı ana metne işlendi. Eski “güven bağlamak ve sadakat geliştirmek” tüm bileşenleriyle sözlüksel eşitlik iddiası daraltıldı. Teknik sentaks sınıflandırmasındaki `POS:P` alt dizesi hatası not edildi; betik değiştirilmedi. Nihai sade kart [Amn-concept-card.md](Amn-concept-card.md) ile uyumlu tutuldu.

Yeni sayım ve ayet denetimi: [QAC karşılaştırma raporu](../generated/tawakkul_comparison/report.md). Morfoloji gözlemleri ile semantik yorumun derecesi ayrıdır; bu dosya bütün 879 kullanımın bağımsız, konum konum semantik sınıflandırmasını içermez.
