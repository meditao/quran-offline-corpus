# KUR’AN KAVRAM ANALİZİ — HİCRET (h-c-r)

**Sürüm:** v1 — ilk depo kaydı  
**Tarih:** 14 Ekim 2026  
**Durum:** Aşama 1–3 (veri, kullanımlar, kavram ağı) kullanıcı onayıyla ilerledi. Aşama 4 (anlam önerisi ve sınama) **ara sonuç** olarak kaydedilmiştir; kullanıcı incelemesi sürüyor.  
**Yöntem:** Tam kök taraması, lemma ve bab ayrımı, ayet ayet okuma, kavram ağı (ortak geçişler), iki öneriyi karşılaştırma, falsifikasyon, kapalı örneklem sınaması.  
**İşaretler:** [Y] doğrudan denetlenebilir veri · [O] dil ve bağlam çıkarımı · [İ] açık ihtimal · [S] dış çerçeve hipotezi (delil değil).

> **Kayıt notu (neyin yeniden üretildiği).** Bu karttaki bütün sayımlar ve ortak geçişler 14 Ekim 2026’da bu deponun kendi aracıyla, kanonik korpus **QAC v0.4** üzerinde yeniden üretilmiştir (sorgular §9’da). Çalışmanın ilk taraması ikinci annotation katmanıyla (mustafa0x/quran-morphology) yapılmıştı; kelime konumu, ayet ve sûre sayıları iki korpusta aynı çıktı (31 / 27 / 17). İki sonucun aynı çıkması bağımsız doğrulama sayılmaz (`CLAUDE.md` §5).  
> Okunuş, deponun Tanzil aktarımından alınmıştır (`python -m tezgah okunus`). Ayetlerin **Türkçe anlamları bu çalışmaya ait taslak çevirilerdir**: Claude tarafından yazılmıştır, kullanıcının çalışma çevirisi değildir, meal değildir ve delil sayılmaz. Gerekirse `tezgah ceviri` ile kullanıcı kendi çevirisini ekler.  
> **Beklenti kaydı:** Kullanıcı bu çalışma için kendi beklentisini yazmadı; sonucun bir beklentiyle karşılaştırması yapılmamıştır. Claude’un Aşama 2’de yazdığı beklenti de kayda geçmiştir: hicretin ağırlıklı olarak coğrafi göç çıkması (doğrulandı) ve “kötülüğü terk” anlamının III. babda da bulunması (**tutmadı**).  
> **Yapılmayanlar:** Lane ve Sâmî katmanları çalıştırılmadı. Hadis ve tefsir delil olarak kullanılmadı; anıldıkları yer “hipotez” etiketi taşır.

---

## 1. Çekirdek anlam ve kapsam

**Araştırma sorusu:** h-c-r kök ailesi Kur’an’da ne anlama geliyor ve “hicret” kelimesi bu ailenin neresinde duruyor?

**Ara sonuç (tanım önerisi):**

> **Hicret** (*hâcara*, III. bab), baskı altında kalan inananın **Allah’a yönelerek** yurdunu **fiilen bırakması** ve kendisini barındırıp destekleyen bir topluluğa katılmasıdır. Bu yeni aidiyet velâyet ve nikâh hükümlerini değiştirir, ama akrabalık bağını mirasta silmez. [O]

İki kalıp ayrı tutulmalıdır:

- **I. bab *hacara*:** “birini ya da bir şeyi terk etmek, ondan uzak durmak.” Geçişlidir; terk edilen hep söylenir, varılan yer söylenmez.
- **III. bab *hâcara*:** “hicret etmek.” Geçişsizdir; terk edilen nesne olarak söylenmez, onun yerine **yön** ve **alan** söylenir.

“Günahtan ya da kötülükten hicret” anlamı **III. babda yoktur**; “kötü şeyi terk” anlamı yalnız I. babda ve tek ayette (74:5) vardır. Bu, kelimeyle sınırlı bir bulgudur; içsel yöneliş fikrinin Kur’an’da başka kelimelerle kurulduğu §4 ve §6’da gösterilmiştir.

---

## 2. Morfolojik kimlik ve yeniden üretilen sayım

**Kök:** h-c-r (Buckwalter `hjr`). **Uyarı:** `Hjr` (ḥ-c-r) ayrı bir köktür; bu karta girmez.

**Toplam:** 31 kelime konumu · 27 ayet · 17 sûre. [Y]

| Lemma | Kelime konumu | Tür | Bab (QAC) |
|---|---:|---|---|
| *hâcara* “hicret etmek” | 16 | fiil | III |
| *muhâcir* “hicret eden” | 7 | isim (ism-i fâil) | III |
| *muhâcirât* (60:10) | 1 | isim | işaretsiz |
| *uhcur* “terk et / uzak dur” | 5 | fiil | I |
| *mahcûr* “terk edilmiş” | 1 | isim (ism-i mef‘ûl) | işaretsiz |
| *hacr* (mastar) | 1 | isim | işaretsiz |
| **Toplam** | **31** | 21 fiil · 10 isim | |

**Bab sayımında dikkat:** QAC’ta I. bab işaretlenmez; fiilde işaretsiz gövde I. bab olarak raporlanır (5 fiil). **III. bab etiketi 23 segmentte** vardır (16 fiil + 7 isim). *Muhâcirât*, *mahcûr* ve *hacr* isimde işaretsizdir. Bu kartta “*hâcara* ailesi 24” sayısı, *muhâcirât*’ı (muhâcirenin çoğulu, III. bab ism-i fâilinden) ekleyerek yapılan **okuma kararıdır**; QAC’ın etiket sayısı 23’tür. “I. bab ailesi 7” de 5 fiil ile *mahcûr* ve *hacr* isimlerinin eklenmesiyle bulunur ve aynı nitelikte bir karardır. [Y/O]

**Kök sayımı anlam sayımı değildir:** 31 konumun 24’ü hicret, 7’si terk anlamına yakın bir kalıptadır; bunlar ayrı değerlendirilir.

---

## 3. Kur’an içi kullanımlar

### A. I. bab: *hacara* “terk etmek, uzak durmak” (7 konum, 6 ayet)

| Ayet | Kullanım | Terk edilen (nesne) | Bağlam |
|---|---|---|---|
| 4:34 | *vahcurûhunna fî lmażâciʿi* | eşler | “yataklarda onlardan uzak durun”: mekân değişmeden ilişkinin askıya alınması |
| 19:46 | *vahcurnî maliyyâ* | konuşan (İbrahim’in babası) | “benden uzun süre uzak dur” |
| 73:10 | *vahcurhum hacran camîlâ* | yalanlayanlar | “onlardan güzel bir uzaklaşmayla uzaklaş”; hemen önce *vaṣbir* (sabret) |
| 74:5 | *varrucza fahcur* | *rucz* | “*rucz*’u terk et”; önceki ayet 74:4 *s̱iyâbaka faṭahhir* |
| 25:30 | *ttaḫaẕû hâẕâ lqurʾâna mahcûrâ* | Kur’an | Resûl’ün şikâyeti; bağlam 25:27–29 (zalimin pişmanlığı) |
| 23:67 | *mustakbirîna bihî sâmiran tahcurûn* | **belirtilmemiş** | kalıba uymayan tek kullanım; anlam **belirsiz** (§7) |

[Y/O] 7 konumdan 6’sında terk edilenin kim ya da ne olduğu metinde söylenir (5 fiilin 4’ünde nesne vardır; *mahcûr* 25:30’da terk edileni, *hacr* 73:10’da terkin biçimini adlandırır). Yalnız 23:67 nesnesizdir. Hareketin yönü “bir şeyden uzağa”dır; varılan yer hiçbirinde söylenmez.

### B. III. bab: *hâcara* “hicret etmek” (24 konum, 21 ayet)

**Yön ve alan söylenir, terk edilen söylenmez:**

- Allah’a, Resûl’e: 4:100 *muhâciran ʾilâ llâhi varasûlihî*; 29:26 *muhâcirun ʾilâ rabbî*.
- Allah yolunda: *fî sabîli llâh* kalıbı 9 ayette (2:218, 3:195 [*fî sabîlî*], 4:89, 4:100, 8:72, 8:74, 9:20, 22:58, 24:22); 16:41’de *fî llâh*.
- Hicret edene doğru: 59:9 *man hâcara ʾilayhim*.
- Birlikte: 33:50 *hâcarna maʿaka* “seninle birlikte hicret eden”.

**Mekânsal harekettir:** 4:97 *takun ʾarżu llâhi vâsiʿatan fatuhâcirû fîhâ*; 4:100 *yaḫruc min baytihî muhâciran*; 3:195 ve 59:8’de yurtlarından çıkarılma. [Y/O]

**Sebep baskıdır:** 16:41 *mim baʿdi mâ ẓulimû* (zulme uğradıktan sonra); 16:110 *mim baʿdi mâ futinû* (fitneye uğratıldıktan sonra); 4:97 *mustażʿafîna* (ezilmiş); 4:98 çaresizler muaf. [Y]

**Hükümlere bağlanır:** velâyet (4:89, 8:72, 8:75, 33:6) · nikâh (33:50, 60:10) · miras (8:75, 33:6) · fey/yardım (59:8, 24:22). [Y]

**İman ve cihadla dizilir:** *ʾâmanû … hâcarû … câhadû* 2:218, 8:72, 8:74, 8:75, 9:20’de. *Muhâcirûn* ile *anṣâr* birlikte 9:100 ve 9:117’de. [Y]

---

## 4. Kavram ağı (QAC üzerinde yeniden üretildi)

Hicret kelimesi tek başına durmaz; Kur’an onu bir **sahnenin halkası** olarak kurar. Her halka ayrı bir kökle anlatılır:

| Halka | İfade | Ayet |
|---|---|---|
| 1. Baskı | *ẓulimû, futinû*; *mustażʿaf*; *ʾuḫricû min diyârihim* | 16:41, 16:110, 4:75, 4:97, 8:26, 22:40, 3:195, 59:8 |
| 2. Ayrılış | *iʿtazala* | 19:48–49, 18:16 |
| 3. Yöneliş | *hâcara ʾilâ…*; *ẕâhibun ʾilâ rabbî* | 4:100, 29:26, 37:99 |
| 4. Mekân | *ʾarżu llâhi vâsiʿa* | 4:97, 29:56, 39:10 |
| 5. Karşılama | *ʾâvâ* + *naṣara* | 8:72, 8:74, 8:26, 59:9 |
| 6. Yeni aidiyet | velâyet, miras, nikâh | 8:72, 8:75, 33:6, 60:10 |

**Aynı ayette birlikte geçişler** (`tezgah birlikte hjr …`, ayet birimi): [Y]

| Kök çifti | Ayet sayısı | Ayetler |
|---|---:|---|
| h-c-r + v-l-y (velâyet) | 4 | 4:89, 8:72, 8:75, 33:6 |
| h-c-r + c-h-d (cihad) | 6 | 2:218, 8:72, 8:74, 8:75, 9:20, 16:110 |
| h-c-r + ʾ-m-n (iman) | 10 | 2:218, 8:72, 8:74, 8:75, 9:20, 29:26, 33:6, 33:50, 59:9, 60:10 |
| h-c-r + ʾ-v-y (barındırma/sığınak) | 3 | 4:97 (*maʾvâ* ismi), 8:72, 8:74 (*ʾâvâ* fiili) |
| h-c-r + n-ṣ-r (yardım) | 6 | 4:89, 8:72, 8:74, 9:100, 9:117, 59:8 |
| h-c-r + ḫ-r-c (çıkmak/çıkarılmak) | 3 | 3:195, 4:100, 59:8 |
| h-c-r + ẓ-l-m | 2 | 4:97, 16:41 |
| h-c-r + f-t-n | 1 | 16:110 |
| h-c-r + ż-ʿ-f | 1 | 4:97 |

**Sıklık bulgu değildir** (`CLAUDE.md` §2). Bu tablo bir birlikte-geçiş kaydıdır; tek başına anlam kanıtı değildir.

**Bu ağdan çıkan beş okuma:**

1. **Hicret ve çıkarılma aynı insanlar için yan yana kullanılır** (3:195 *hâcarû vaʾuḫricû*; 59:8). Zorla çıkarılma karşı tarafın eylemi, hicret inananın eylemidir; metin olayı iki taraftan anlatır. [Y/O]
2. **İbrahim’in ayrılışı üç ayrı fiille kurulur ve aynı ödülle biter:** 19:46 babası *vahcurnî* der; 19:48–49 İbrahim *iʿtazala* ile ayrılır ve İshak–Yakub armağan edilir; 29:26–27 *muhâcirun ʾilâ rabbî* der ve yine İshak–Yakub armağan edilir. İki anlatımdaki ortak unsurlar (ayrılış, Rabbe yöneliş, İshak–Yakub) iki ifadenin aynı olayı anlattığını güçlü biçimde düşündürür. [O] 29:26’da *qâla*’nın öznesi dilbilgisel olarak Lût ya da İbrahim olabilir; 29:24–25 ve 29:27 bağlamı İbrahim’i daha olası kılar. [O]
3. **Allah’a yöneliş mekânsız da kurulabilir, ama başka kökle:** 51:50 *fafirrû ʾilâ llâh*; 73:8 *vatabattal ʾilayhi tabtîlâ*; 9:118 (yeryüzü genişliğine rağmen dar gelir, Allah’tan başka sığınak yoktur). 18:16 hicret kökü olmadan ayrılış + yer değiştirme + sığınak kurar. [Y/O]
4. **“Allah’ın arzı geniş” üç ayette ve üç ayrı sonuca bağlıdır:** hicret (4:97), kulluk (29:56), sabır (39:10). [Y]
5. **Karşılayan taraf hicret edenle birlikte ve eşit ağırlıkla anılır:** 8:74 *ʾulâʾika humu lmuʾminûna ḥaqqâ* ifadesi hem hicret edenleri hem barındırıp yardım edenleri kapsar. 4:97’de hicret etmeyenin *maʾvâ*’sı cehennemdir; 8:72 ve 8:74’te *ʾâvâ* fiili barındıranlar için kullanılır. [Y/O]

---

## 5. Kritik ayetler

Okunuş: Tanzil Uthmani’den kurallı aktarım (delil değil). Anlam: **taslak çeviri** (bu çalışmaya ait, delil değil). Tartışmalı terimler (*velâyet*, *cihad*) bağlamda açılana kadar korunur.

**Nisâ 4:89** — *vaddû lav takfurûna kamâ kafarû fatakûnûna savâʾan falâ tattaḫiẕû minhum ʾavliyâʾa ḥattâ yuhâcirû fî sabîli llâhi faʾin tavallav faḫuẕûhum vaqtulûhum ḥays̱u vacattumûhum valâ tattaḫiẕû minhum valiyyan valâ naṣîrâ**  
*Anlam (taslak):* Sizin de kâfir olmanızı, böylece onlarla bir olmanızı isterler. Allah yolunda hicret edinceye kadar onlardan dostlar (*evliyâ*) edinmeyin. Yüz çevirirlerse onları tutun, bulduğunuz yerde öldürün; onlardan ne dost ne yardımcı edinin.  
*Katkı:* Hicret burada bir **ölçüdür**: dostluğun (velâyetin) sürmesi hicret edilmesine bağlanmıştır. Bir ölçü olarak kullanılabilmesi için hicretin dışarıdan görülebilen bir eylem olması gerekir; bu, yalnız içsel bir yönelişin ölçü olamayacağını düşündürür. [O]

**Nisâ 4:97–98** — *ʾinna llaẕîna tavaffâhumu lmalâʾikatu ẓâlimî ʾanfusihim qâlû fîma kuntum qâlû kunnâ mustażʿafîna fî lʾarżi qâlû ʾalam takun ʾarżu llâhi vâsiʿatan fatuhâcirû fîhâ faʾulâʾika maʾvâhum cahannamu vasâʾat maṣîrâ. ʾillâ lmustażʿafîna mina rricâli vannisâʾi valvildâni lâ yastaṭîʿûna ḥîlatan valâ yahtadûna sabîlâ**  
*Anlam (taslak):* Melekler, kendilerine zulmederken canlarını alanlara “Ne durumdaydınız?” der. “Yeryüzünde ezilmiş kimselerdik” derler. “Allah’ın arzı geniş değil miydi ki onda hicret edesiniz?” denir. İşte bunların barınağı cehennemdir, ne kötü varış yeri! Ancak erkek, kadın ve çocuklardan ezilmiş olup bir çare bulamayanlar ve yol bilmeyenler (bunun dışındadır).  
*Katkı:* Gidebilecekken kalan kınanır; gerçekten çaresiz olan muaf tutulur. Hicret yalnız niyet değil, imkân ve yol gerektiren bir eylem olarak ele alınır. [Y/O]

**Nisâ 4:100** — *vaman yuhâcir fî sabîli llâhi yacid fî lʾarżi murâgaman kas̱îran vasaʿatan vaman yaḫruc mim baytihî muhâciran ʾilâ llâhi varasûlihî s̱umma yudrikhu lmavtu faqad vaqaʿa ʾacruhû ʿalâ llâhi*  
*Anlam (taslak):* Kim Allah yolunda hicret ederse yeryüzünde çok yer değiştirme imkânı (*murâğam*) ve genişlik bulur. Kim evinden Allah’a ve Resûlüne hicret ederek çıkar, sonra ölüm ona yetişirse, onun ecri Allah’a düşmüştür.  
*Katkı:* *Ev*’den çıkış ve *Allah’a ve Resûlüne* yönelişin aynı fiilde (*muhâciran*) birleştiği ayet. Yön ve fiilî çıkış birlikte hicretin içindedir. [Y]

**Enfâl 8:72** — *ʾinna llaẕîna ʾâmanû vahâcarû vacâhadû biʾamvâlihim vaʾanfusihim fî sabîli llâhi vallaẕîna ʾâvav vanaṣarû ʾulâʾika baʿżuhum ʾavliyâʾu baʿżin vallaẕîna ʾâmanû valam yuhâcirû mâ lakum min valâyatihim min şayʾin ḥattâ yuhâcirû vaʾini stanṣarûkum fî ddîni faʿalaykumu nnaṣru ʾillâ ʿalâ qavmim baynakum vabaynahum mîs̱âqun*  
*Anlam (taslak):* İman edip hicret edenler, mallarıyla canlarıyla Allah yolunda cihad edenler ve barındırıp yardım edenler: işte bunlar birbirinin velîleridir. İman edip de hicret etmeyenlerin velâyetinden, hicret edinceye kadar size ait bir şey yoktur. Dinde sizden yardım isterlerse, aranızda sözleşme bulunan bir topluluğa karşı olmadıkça yardım size düşer.  
*Katkı:* Hicret, **velâyetin kurucu şartıdır**. Aynı ayette hicret etmeyen müminin velâyet dışında kalması, hicretin fiilî ve toplumsal bir aidiyet değişikliği olduğunu gösterir. Sözleşme istisnası, aidiyetin başkalarıyla yapılan antlaşmaları geçersiz kılmadığını gösterir. [Y/O]

**Enfâl 8:74–75** — *vallaẕîna ʾâmanû vahâcarû vacâhadû fî sabîli llâhi vallaẕîna ʾâvav vanaṣarû ʾulâʾika humu lmuʾminûna ḥaqqâ … vallaẕîna ʾâmanû mim baʿdu vahâcarû vacâhadû maʿakum faʾulâʾika minkum vaʾulû lʾarḥâmi baʿżuhum ʾavlâ bibaʿżin fî kitâbi llâhi*  
*Anlam (taslak):* İman edip hicret eden, Allah yolunda cihad edenler ve barındırıp yardım edenler: gerçek müminler işte bunlardır. Sonradan iman edip hicret eden ve sizinle birlikte cihad edenler: işte onlar sizdendir. Allah’ın Kitabında akrabalık bağı olanlar birbirine daha yakındır.  
*Katkı:* Karşılayanlar hicret edenlerle **birlikte** *gerçek mümin* olarak anılır. 8:75, yeni aidiyetin **kapsam sınırını** koyar: akrabalık bağı mirasta öncelik taşır. [Y]

**Ankebût 29:26–27** — *faʾâmana lahû lûṭun vaqâla ʾinnî muhâcirun ʾilâ rabbî ʾinnahû huva lʿazîzu lḥakîm vavahabnâ lahû ʾisḥâqa vayaʿqûba vacaʿalnâ fî ẕurriyyatihi nnubuvvata valkitâba vaʾâtaynâhu ʾacrahû fî ddunyâ*  
*Anlam (taslak):* Lût ona iman etti ve dedi ki: “Ben Rabbime hicret edenim; O güçlüdür, hikmet sahibidir.” Ona İshak’ı ve Yakub’u armağan ettik, soyuna peygamberliği ve Kitab’ı koyduk, ecrini dünyada verdik.  
*Katkı:* Hicretin hedefi bir yer değil **Rabb**’dir (*ʾilâ rabbî*); kavramın “yön” bileşeni burada en çıplak hâlinde. [Y/O]

**Meryem 19:46, 19:48–49** — *qâla ʾarâgibun ʾanta ʿan ʾâlihatî yâʾibrâhîmu laʾil lam tantahi laʾarcumannaka vahcurnî maliyyâ … vaʾaʿtazilukum vamâ tadʿûna min dûni llâhi … falammâ ʿtazalahum vamâ yaʿbudûna min dûni llâhi vahabnâ lahû ʾisḥâqa vayaʿqûba*  
*Anlam (taslak):* “Ey İbrahim, sen benim ilâhlarımdan yüz mü çeviriyorsun? Vazgeçmezsen seni taşlarım; uzun bir süre benden uzak dur.” … “Sizden ve Allah’ın dışında yalvardıklarınızdan ayrılıyorum.” … Onlardan ve Allah’ın dışında kulluk ettiklerinden ayrılınca ona İshak’ı ve Yakub’u armağan ettik.  
*Katkı:* Aynı kopuş üç fiille: baskı yapan taraf I. babla (*uhcur*), ayrılan *iʿtazala* ile anlatır; 29:26 aynı olayı III. babla verir. [O]

**Kehf 18:16** — *vaʾiẕi ʿtazaltumûhum vamâ yaʿbudûna ʾillâ llâha faʾvû ʾilâ lkahfi yanşur lakum rabbukum mir raḥmatihî*  
*Anlam (taslak):* Onlardan ve Allah’tan başkasına kulluk ettiklerinden ayrılıp uzaklaştığınıza göre mağaraya sığının; Rabbiniz size rahmetinden yayar.  
*Katkı:* Ayrılış + yer değiştirme + sığınak **h-c-r kökü olmadan** kurulur. Kavram, kelimeden geniştir (`CLAUDE.md` §2.4). [Y/O]

**Zâriyât 51:50 ve Müzzemmil 73:8** — *fafirrû ʾilâ llâhi ʾinnî lakum minhu naẕîrum mubîn* · *vaẕkuri sma rabbika vatabattal ʾilayhi tabtîlâ*  
*Anlam (taslak):* O hâlde Allah’a kaçın; ben sizin için O’ndan gelen açık bir uyarıcıyım. · Rabbinin adını an ve (her şeyden) kopup tam bir kopuşla O’na yönel.  
*Katkı:* **Mekânsız “Allah’a yöneliş”** Kur’an’da vardır, ama f-r-r ve b-t-l kökleriyle. [Y/O]

**Tevbe 9:118** — *vaʿalâ s̱s̱alâs̱ati llaẕîna ḫullifû ḥattâ ʾiẕâ żâqat ʿalayhimu lʾarżu bimâ raḥubat vażâqat ʿalayhim ʾanfusuhum vaẓannû ʾal lâ malcaʾa mina llâhi ʾillâ ʾilayhi s̱umma tâba ʿalayhim liyatûbû*  
*Anlam (taslak):* Geri bırakılan üç kişi: yeryüzü bütün genişliğine rağmen kendilerine dar gelmiş, canları da kendilerini sıkıştırmış ve Allah’tan başka sığınacak yer olmadığını anlamışlardı. Sonra onlara döndü ki onlar da dönsünler.  
*Katkı:* *ʾArżu llâhi vâsiʿa*’nın karşıtı: mekânın çözüm olmadığı yerde sığınak doğrudan Allah’tır. [Y/O]

**Mümtehine 60:10** — *yâʾayyuhâ llaẕîna ʾâmanû ʾiẕâ câʾakumu lmuʾminâtu muhâcirâtin famtaḥinûhunna llâhu ʾaʿlamu biʾîmânihinna faʾin ʿalimtumûhunna muʾminâtin falâ tarciʿûhunna ʾilâ lkuffâri*  
*Anlam (taslak):* Ey iman edenler, mümin kadınlar hicret ederek size geldiğinde onları sınayın; Allah onların imanını daha iyi bilir. Mümin olduklarını anlarsanız onları kâfirlere geri çevirmeyin.  
*Katkı:* Hicret tek başına imanın kanıtı sayılmaz; hicret edenler de sınanır. Hicret nikâh bağının hükmünü de değiştirir. [Y]

**Nahl 16:41, 16:110** — *vallaẕîna hâcarû fî llâhi mim baʿdi mâ ẓulimû lanubavviʾannahum fî ddunyâ ḥasanatan* · *lillaẕîna hâcarû mim baʿdi mâ futinû s̱umma câhadû vaṣabarû*  
*Anlam (taslak):* Zulme uğratıldıktan sonra Allah için hicret edenleri dünyada güzel bir yere yerleştireceğiz. · Fitneye uğratıldıktan sonra hicret eden, sonra cihad edip sabredenler.  
*Katkı:* Hicretin sebebi baskıdır; 16:110’da hicret, cihad ve sabırla **sıralı bir dizide** gelir. [Y]

**Haşr 59:8–9 ve Ahzâb 33:6** — *lilfuqarâʾi lmuhâcirîna llaẕîna ʾuḫricû min diyârihim vaʾamvâlihim* · *yuḥibbûna man hâcara ʾilayhim* · *ʾulû lʾarḥâmi baʿżuhum ʾavlâ bibaʿżin fî kitâbi llâhi mina lmuʾminîna valmuhâcirîna*  
*Anlam (taslak):* Yurtlarından ve mallarından çıkarılmış hicret eden yoksullar için. · Kendilerine hicret edeni severler. · Akrabalık bağı olanlar, Allah’ın Kitabında, müminlerden ve muhacirlerden birbirine daha yakındır.  
*Katkı:* Hicret maddi kayıp getirir; karşılayan tarafın duygusal ve ekonomik yükü de ayrıca anılır. 33:6, 8:75 ile aynı kapsam sınırını verir. [Y]

---

## 6. Karşı örnekler ve falsifikasyon (§12b)

**Soru:** Öneri doğru olsaydı hangi ayet onu çürütürdü? Bu ayetler arandı.

1. **Yer değiştirme içermeyen bir III. bab kullanımı** → taranan 24 kullanımın hiçbirinde yok.
2. **Yerinde kalmanın hicret sayıldığı bir ayet** → yok.
3. **Yer değiştirmenin tek başına hicret sayıldığı bir ayet** → **ters yönde bulgu var:** 8:47 (*ḫaracû min diyârihim baṭaran*, böbürlenerek yurttan çıkanlar) ve 2:243 (*ḫaracû min diyârihim … ḥaẕara lmavti*, ölüm korkusuyla yurttan çıkanlar) yurttan çıkışı **h-c-r kökü olmadan** anlatır. Yön (Allah’a, Resûl’e, inananlara) bulunmadan göç hicret sayılmaz. [O]

**Kapsam kaydı (metnin kendisinden):** Hicret velâyet kurar (8:72), ama mirasta kan bağını geçmez (8:75, 33:6). İki ayrı ayette aynı ifade (*ʾulû lʾarḥâmi baʿżuhum ʾavlâ bibaʿżin fî kitâbi llâh*) kullanıldığı için bu, tek bir aykırı örneği kurtarmak için eklenmiş bir istisna değildir. [Y/O]

### Kapalı örneklem sınaması (§12d)

- **Kurma kümesi (8 ayet):** 3:195, 4:97, 4:100, 8:72, 16:41, 16:110, 29:26, 59:8.
- **Kapalı küme (13 ayet, 13 kelime konumu; III. bab):** 2:218, 4:89, 8:74, 8:75, 9:20, 9:100, 9:117, 22:58, 24:22, 33:6, 33:50, 59:9, 60:10.
- **Sonuç:** 13 kullanımın hepsi öneriye ek bir düzeltme yapılmadan uydu. Tek eklenen şey, metnin kendisinden gelen **kapsam kaydıdır** (8:75, 33:6).
- **Sınırlama (dürüstlük notu):** Kapalı küme, Aşama 2’de okunmuş ayetlerden oluşuyordu; yani sınama **kör değildir**. Doğrulama gücü bu yüzden sınırlıdır.
- **Düzeltme:** Çalışma sırasında önce “13 ayet / 14 kullanım” yazılmıştı; doğru sayı 13 ayet / 13 kelime konumudur (27 ayet − 6 I. bab ayeti − 8 kurma ayeti = 13; her biri tek konum).

---

## 7. Muhalif okumalar (§12c)

**İki okuma rekabette değildir; ikinci okuma kökte dayanak bulur ama III. babda bulmaz.**

**Dar tarihî okuma:** “Hicret, Mekke’den Medine’ye yapılan tek göçtür.” En güçlü hâli: *muhâcirûn/anṣâr* bir topluluk adı olarak geçer (9:100, 9:117), 59:8–9 belirli bir yoksul ve yurdundan çıkarılmış topluluğu anlatır, 33:6 ve 8:75 o topluluğun miras düzenine işaret eder. **Metin bu okumayı geçemez:** İbrahim de hicret eder (29:26); 4:97 genel bir ilke koyar; 29:56 ve 39:10 bu ilkeyi “inanan kullarım”a yöneltir. Hicret tarihî bir kurum olarak vardır, ama ona bağlı ilke genel geçerdir. [O]

**Geniş okuma (B):** “Hicret, Allah’a yöneliş için yapılan her kopuştur (içsel dahil); göç yalnız bir örnektir.” En güçlü hâli: 29:26’da hedef bir yer değil *rabbî*’dir; 74:5 kökte “kötüyü terk”i taşır; 51:50 ve 73:8 mekânsız yöneliş kurar. **Burada eksik olan III. babdaki dayanaktır:** B’yi taşıyan hiçbir III. bab kullanımı yoktur. B’nin sezgisi metinde karşılık bulur, ama **başka kelimelerle** (f-r-r, b-t-l, ʿ-z-l). [O]  
*Hipotez etiketi:* “Gerçek hicret günahları terk etmektir” biçimindeki yaygın geleneksel söz Kur’an dışı bir kaynağa aittir; burada **yalnız hipotez** olarak anılır, delil sayılmaz. [S]

---

## 8. Bilimsel çağrışımlar

- **Göç araştırmalarında itme–çekme çerçevesi** (Ravenstein, 1885; Lee, 1966) Kur’an’ın kavram ağıyla yapısal olarak örtüşür: itici etken zulüm ve fitne (16:41, 16:110); çekici etken barındırma ve yardım (8:72, 4:100); aradaki engeller, “çare bulamayan, yol bilmeyen” çaresizler (4:98). Lee modelindeki “araya giren engeller” öğesi 4:98’de neredeyse birebir karşılığını bulur. **Bu bir çağrışımdır, delil değildir:** model genel göç davranışını betimler; Kur’an aynı davranış üzerine ahlaki ve hukuki bir yükümlülük kurar. [S]
- **51:47 *ʾinnâ lamûsiʿûn* (“genişleticiyiz”)** yaygın olarak genişleyen evren bulgusuyla ilişkilendirilir. Bu bağ hicret kavramına **anlam olarak değil**, yalnızca aynı kökün (v-s-ʿ) ve aynı pasajın yakınlığıyla dayanır. *Mûsiʿ*, 2:236’da “imkânı geniş olan” anlamında da geçer; 51:47 için “genişleten” ya da “gücü geniş” okumaları arasında karar verecek metin içi delil bu çalışmada gösterilmedi. **Belirsiz.** [İ/S]

---

## 9. Sonuç, delil dereceleri (§13)

| Önerme | Mantıksal durum | Delil derecesi |
|---|---|---|
| I. bab *hacara*: “bağı kesip uzak durmak” (nesneli) | Destekleniyor (6/7) | Sağlam |
| III. bab *hâcara*: yön + fiilî yer değiştirme + yeni aidiyet | Destekleniyor (24/24) | Sağlam |
| Kapsam kaydı: yeni aidiyet mirasta kan bağını geçmez | Destekleniyor (8:75, 33:6) | Sağlam |
| Yön bileşeni zorunlu (yönsüz göç hicret değil) | Destekleniyor (8:47, 2:243 karşıtlığı) | Muhtemel (dayanak, h-c-r kullanılmamasından çıkarılıyor) |
| B: hicret kelimesi içsel kopuşu da kapsar | **Destek gösterilemedi** | Spekülatif |
| Mekânsız “Allah’a yöneliş” Kur’an’da vardır | Destekleniyor (51:50, 73:8, 9:118) | Sağlam, ama **başka kökle** |
| 23:67 *tahcurûn* | Belirsiz | Açık kalıyor |

**Kavram kartı (kısa):**

> Kur’an’da h-c-r iki kalıba ayrılır. *Hacara* (7 konum), “birini ya da bir şeyi terk etmek, ondan uzak durmak”tır. *Hâcara* (24 konum), bildiğimiz hicrettir: baskı altındaki inananın Allah’a yönelerek yurdunu gerçekten bırakması ve onu barındıran bir topluluğa katılması. Bu yeni aidiyet velâyet ve nikâh hükümlerini değiştirir, ama mirasta akrabalığı silmez. Yönsüz göç hicret sayılmaz (8:47, 2:243). Karşılayanlar, hicret edenlerle birlikte “gerçek mümin” diye anılır (8:74). Kur’an mekânsız bir “Allah’a yöneliş” de bilir, ama onu h-c-r köküyle değil, “Allah’a kaçın” (51:50) ve “O’na yönel” (73:8) gibi başka kelimelerle anlatır.

**Açık noktalar:** 23:67 (*tahcurûn*) anlamı belirsiz. Kapalı örneklem kör değil. Lane ve Sâmî katmanları çalıştırılmadı. Türkçe anlamlar taslaktır. Kullanıcı beklentisi kaydedilmedi.

---

## 10. Kayıt (`CLAUDE.md` §8)

```
Kaynak      : QAC v0.4
Sayım birimi: kelime konumu | ayet | sûre (birlikte geçişte: ayet)
Veri izi    : a1d129238153 (QAC); okunuş: bf4f57b968d0 | 7f30c647331a (Tanzil)
Durum       : çalıştırıldı (14 Ekim 2026)
Sorgular    :
  python -m tezgah dagilim --kok hjr --gore tur
  python -m tezgah dagilim --kok hjr --gore lemma
  python -m tezgah dagilim --kok hjr --gore bab
  python -m tezgah birlikte hjr wly | jhd | Amn | Awy | nSr | xrj | Zlm | ftn | sbl | DEf
  python -m tezgah sayim --kok Ezl | Awy | nSr | wsE | bwA | frr | btl | nwb | DEf
  python -m tezgah okunus <sûre:ayet>   (alıntılanan her ayet için)
```

**Not:** Bu karttaki Türkçe taslak anlamlar, Aşama 2–4 ayet okumaları ve yorum cümleleri sorgu çıktısı değildir; yorum katmanıdır ([O], [İ], [S] işaretleriyle ayrılmıştır).
