# İMAN — Kur’an İçi Aşamalı Analiz

## Kısa sonuç

İman, Kur’an’da yalnızca “bir şeyin var olduğuna inanmak” değildir. Amn kök ailesi, fiilin sentaksı, iman isim kullanımları, kalp bağlamları ve karşı örnekler birlikte değerlendirildiğinde en iyi çalışan anlam şudur:

**İman, bir şeyi veya bir mercii doğru ve güvenilir kabul ederek ona güven bağlamak ve bu güven doğrultusunda yönelim/sadakat geliştirmektir.**

Kur’an’ın olumlu iman çağrısında bu ilişkinin merkezi Allah ve O’ndan gelen rehberliktir. En sade ifadeyle:

**İman = Allah’a ve O’ndan gelen rehberliğe güven bağlamak.**

Bu sonuç tek bir sözlük anlamından değil, aşağıdaki aşamalı incelemeden çıkarılmıştır.

---

## Kaynak ve yöntem

Bu çalışma öncelikle Kur’an’ın kendi kullanımına dayanır.

- Arapça ayet metni: repoda sabitlenmiş Tanzil Quran Text v1.1, Simple Clean dosyası. Ayet metinleri değiştirilmeden verilmiştir.
- Morfoloji, kök ve lemma verisi: Quranic Arabic Corpus v0.4.
- Sayımlar: repodaki ham QAC verisinden yeniden üretilebilir scriptlerle çıkarılmıştır.
- Türkçe çeviriler: bu çalışmaya ait sade/kavramsal çevirilerdir; yayımlanmış bir mealden kopyalanmamıştır.
- Yöntem: kök ailesi → morfoloji/sentaks → Kur’an içi dağılım → kritik ayetler → karşı örnek/falsifikasyon → sentez.

Kaynak ve lisans ayrıntıları için: [SOURCES.md](../../SOURCES.md) ve [LICENSES.md](../../LICENSES.md).

---

# Aşama 1 — Kök ailesi ne söylüyor?

İman, Arapça أ م ن (Amn) kök ailesindedir.

QAC v0.4 verisinde bu kök etiketi 879 kelime konumunda görülür; 723 ayete ve 77 sûreye dağılır. Başlıca biçimler arasında āman(a) fiil ailesi, īmān, muʾmin, amina, amīn, amn ve amāna türevleri vardır.

Kök ailesinde üç ana damar görülür:

1. Birine/bir şeye güven bağlama: āman(a), īmān, muʾmin.
2. Güvenlik ve emniyet: amina, amn, āmin.
3. Güvenilirlik ve emanet: amīn, amāna.

Bu nedenle kök ailesinin ortak ekseni “salt zihinsel inanma” değil, daha geniş bir **güven – güvenilirlik – güvenlik** alanıdır.

Bu aşama tek başına “iman = güven” sonucunu kanıtlamaz. Kök akrabalığı yalnız hipotez üretir. Hipotezin Kur’an’daki fiil kullanımlarıyla sınanması gerekir.

Teknik ayrıntı: [Amn — Aşama 1](Amn-quran-internal-stage1.md).

---

# Aşama 2 — Āmana fiili nasıl çalışıyor?

QAC’ta āman(a) lemma ailesinin 537 fiil kullanımı vardır.

Yüzey taramasında fiilden hemen sonra 163 açık bi- adayı ve 18 li- adayı bulunmuştur. Li- adaylarının manuel kontrolünde 15 gerçek tamamlayıcı belirlenmiş; bunların 14’ünün kişi hedefli olduğu görülmüştür.

Bu veri, fiilin yalnız “bir önermeyi zihnen doğru saymak” anlamında çalışmadığını gösterir. İnsanların sözüne güvenme/itimat etme ilişkisi de açıkça vardır.

## Kritik ayet: Tevbe 9:61

ومنهم الذين يؤذون النبي ويقولون هو أذن قل أذن خير لكم يؤمن بالله ويؤمن للمؤمنين ورحمة للذين آمنوا منكم والذين يؤذون رسول الله لهم عذاب أليم

**Sade/kavramsal çeviri:** İçlerinden Nebi’yi inciten ve “O her söylenene kulak veriyor” diyenler vardır. De ki: “O sizin için hayra kulak verir; Allah’a iman eder ve müminlere güvenir; sizden iman edenler için bir rahmettir.” Allah’ın elçisini incitenler için acı bir azap vardır.

**Bu ayet neyi gösteriyor?** Aynı özne ve aynı fiil iki farklı yapıda kullanılıyor: “Allah’a iman eder” ve “müminlere güvenir.” İkinci kullanım, müminlerin var olduğuna zihinsel olarak inanmak değildir; bağlam açık biçimde onların sözünü güvenilir bulma/itimat etme ilişkisidir. Böylece āman(a) fiilinin güven boyutu Kur’an’ın kendi içinde görünür hale gelir.

Ancak buradan “bi- her zaman şu, li- her zaman bu demektir” şeklinde mekanik bir kural çıkarılamaz. Bi- yapısı da insan, elçi, vahiy, ayet, gayb, ahiret ve başka hedeflerle kullanılabilir.

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

Bu ayetler önemlidir; çünkü iman sabit bir kimlik etiketi olsaydı “artması”nın ne anlama geldiğini açıklamak zorlaşır. Bağlamlara bakıldığında artan şey yeni “inanç maddelerinin sayısı” değil; güvenin, doğrulamanın ve bağlılığın güçlenmesiyle daha iyi açıklanır.

## Âl-i İmrân 3:173

الذين قال لهم الناس إن الناس قد جمعوا لكم فاخشوهم فزادهم إيمانا وقالوا حسبنا الله ونعم الوكيل

**Sade/kavramsal çeviri:** İnsanlar onlara, “İnsanlar size karşı toplandı; onlardan korkun” dediklerinde bu onların imanını artırdı ve “Allah bize yeter; O ne güzel vekildir” dediler.

**Gösterdiği şey:** Tehdit, iman sahibi kişiyi zorunlu olarak çökertecek yerde Allah’a güvenini güçlendirebiliyor. Ayetin hemen ardından “Allah bize yeter” ve vekil olarak Allah’a dayanma geliyor.

## Enfâl 8:2

إنما المؤمنون الذين إذا ذكر الله وجلت قلوبهم وإذا تليت عليهم آياته زادتهم إيمانا وعلى ربهم يتوكلون

**Sade/kavramsal çeviri:** Müminler, Allah anıldığında kalpleri duyarlılıkla ürperen; O’nun ayetleri kendilerine okunduğunda imanları artan ve Rablerine güvenip dayanan kimselerdir.

**Gösterdiği şey:** Ayetlerin okunması imanı artırıyor ve aynı cümlenin devamında tevekkül geliyor. İman ile güven/dayanma aynı kelime değildir; fakat aynı ilişkisel eksende birbirini destekler.

## Tevbe 9:124

وإذا ما أنزلت سورة فمنهم من يقول أيكم زادته هذه إيمانا فأما الذين آمنوا فزادتهم إيمانا وهم يستبشرون

**Sade/kavramsal çeviri:** Bir sûre indirildiğinde içlerinden bazıları, “Bu hanginizin imanını artırdı?” der. İman edenlere gelince, o sûre onların imanını artırır ve onlar sevinirler.

**Gösterdiği şey:** Yeni vahiy, mevcut iman ilişkisini güçlendirebilir.

## Ahzâb 33:22

ولما رأى المؤمنون الأحزاب قالوا هذا ما وعدنا الله ورسوله وصدق الله ورسوله وما زادهم إلا إيمانا وتسليما

**Sade/kavramsal çeviri:** Müminler birleşmiş düşman gruplarını gördüklerinde, “Bu, Allah’ın ve Elçisi’nin bize vaat ettiği şeydir; Allah ve Elçisi doğru söyledi” dediler. Bu durum onların yalnız imanını ve teslimiyetini artırdı.

**Gösterdiği şey:** Yaşanan olayın daha önce verilen sözü doğrulaması, iman artışıyla ilişkilendiriliyor. Burada “doğrulanma → güvenin güçlenmesi” zinciri açık biçimde görülüyor.

## Fetih 48:4

هو الذي أنزل السكينة في قلوب المؤمنين ليزدادوا إيمانا مع إيمانهم ولله جنود السماوات والأرض وكان الله عليما حكيما

**Sade/kavramsal çeviri:** Müminlerin kalplerine, mevcut imanlarının yanında imanlarını artırmaları için sekînet indiren O’dur. Göklerin ve yerin orduları Allah’ındır. Allah bilendir, hikmet sahibidir.

**Gösterdiği şey:** İman kalple ve sekînetle ilişkilidir; mevcut imanın üzerine daha fazla iman gelebilir.

## Müddessir 74:31

وما جعلنا أصحاب النار إلا ملائكة وما جعلنا عدتهم إلا فتنة للذين كفروا ليستيقن الذين أوتوا الكتاب ويزداد الذين آمنوا إيمانا ولا يرتاب الذين أوتوا الكتاب والمؤمنون وليقول الذين في قلوبهم مرض والكافرون ماذا أراد الله بهذا مثلا كذلك يضل الله من يشاء ويهدي من يشاء وما يعلم جنود ربك إلا هو وما هي إلا ذكرى للبشر

**Sade/kavramsal çeviri:** Ateşin görevlilerini yalnız melekler yaptık; sayılarını da inkâr edenler için bir sınama yaptık ki kendilerine Kitap verilenler kesinlik kazansın, iman edenlerin imanı artsın, Kitap verilenler ve müminler kuşkuya düşmesin; kalplerinde hastalık bulunanlar ve kâfirler ise “Allah bununla ne demek istedi?” desinler. Allah dileyeni böylece sapmada bırakır, dileyeni rehberliğe yöneltir. Rabbinin ordularını O’ndan başkası bilmez. Bu, insanlar için bir hatırlatmadan başka bir şey değildir.

**Gösterdiği şey:** Kesinlik kazanma, kuşkunun azalması ve imanın artması aynı bağlamda bulunur. Bu da imanın bilgiyle ilişkili olduğunu, fakat salt bilgi olmadığını gösterir: yeni bilgi/gösterge mevcut güven bağını güçlendirebilir.

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
- kalpte güven/sekînet oluşturabilir,
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

# Aşama 7 — Sami dilleri karşılaştırması

Kur’an içi analizden bağımsız bir kontrol olarak, aynı Sami kök ailesinin İbranice, Aramice ve Süryanice karşılıklarında da sağlamlık, güvenilirlik, doğrulama ve güvenme alanları görülür.

Bu veri sonucu belirlemez. Yöntem gereği önce Kur’an içindeki amina / amīn / amāna / amn / āman(a) ağı incelenmiş, Sami karşılaştırması daha sonra destekleyici kontrol olarak kullanılmıştır.

Bu yüzden “İbranice böyle, o halde Kur’an’da da mutlaka böyledir” denmemektedir. Söylenebilecek daha dar şey şudur: Kur’an içinde bulunan güven/güvenilirlik ekseni tarihsel Sami karşılaştırmasıyla çelişmemekte, tersine onunla uyum göstermektedir.

---

# Falsifikasyon özeti

Bu analiz sırasında aşağıdaki dar tanımlar sınandı:

### “İman = yalnızca bir şeyin var olduğuna inanmak.”

Yetersizdir. 9:61’de fiil kişiler arası güven ilişkisi kurar; 49:14 ve 5:41’de sözlü beyan ile kalpteki iman ayrılır.

### “Āmana fiili her zaman hakikati kabul etmek demektir.”

Yanlıştır. 29:52 açıkça bâtıla iman etmekten söz eder.

### “İman = yalnız kalpteki duygu.”

Yetersizdir. 2:143 ve 6:158 iman ile fiilî sadakat/hayır arasında ilişki kurar.

### “İman = yalnız amel.”

Yetersizdir. 16:106 ve 49:14 kalpteki iman durumunu açıkça ayırır.

### “İman = namaz.”

Sözlük eşitliği olarak desteklenmez. 2:143, kıble/uyma davranışını iman kapsamında değerlendirir; iman kelimesini salâtın eş anlamlısı yapmaz.

### “İman artmaz; kişi ya inanır ya inanmaz.”

Yanlıştır. 3:173, 8:2, 9:124, 33:22, 48:4 ve 74:31 imanın arttığını açıkça söyler.

---

# Nihai sentez

Bütün katmanlar birlikte değerlendirildiğinde üç boyut birbirinden koparılamaz:

1. **Doğrulama:** Bir mercii, bildirimi veya gerçeklik iddiasını doğru/güvenilir/geçerli kabul etmek.
2. **Güven:** Ona içsel güven bağlamak; kuşku ve tehdit karşısında bu bağın güçlenebilmesi.
3. **Sadakat/yönelim:** Kurulan güven doğrultusunda yönelmek ve davranış geliştirmek.

Bu nedenle çalışma sonucunda ulaşılan en kapsayıcı tanım şudur:

**İman, bir şeyi veya bir mercii doğru ve güvenilir kabul ederek ona güven bağlamak ve bu güven doğrultusunda sadakat/yönelim geliştirmektir.**

Kur’an’ın olumlu iman çağrısında bunun merkezi Allah ve O’ndan gelen rehberliktir:

**İman = Allah’a ve O’ndan gelen rehberliğe güven bağlamak; bu güveni kişinin temel yönelimi haline getirmek.**

Bu tanım “inanmak” kelimesini tamamen reddetmez; fakat Türkçedeki “zihnen var saymak/doğru saymak” anlamının Kur’an’daki kullanım alanını tek başına karşılamadığını söyler.

---

# Kısa kavram kartı

**İman:** Allah’a ve O’ndan gelen rehberliğe güven bağlamak.

Daha açık hali:

**Doğru/güvenilir kabul et → güven bağla → bu güvene sadakat göster.**

İman yalnız söz değildir; 5:41 ve 49:14.

İman yalnız bilgi değildir; yanlış hedefe de iman ilişkisi kurulabilir; 29:52.

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