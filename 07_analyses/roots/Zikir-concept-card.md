# KUR'AN KAVRAM ANALİZİ — ZİKİR (ẕ-k-r)

> **Statü ve kaynak notu (12 Ekim 2026).**
>
> - **Sürüm:** v1 — sohbet içinde altı bölümde yürütülmüş çalışma kaydı. Tanım ve üç düzeltmesi için ayrı bir açık onay kaydı yoktur; kullanıcı sonucun GitHub'a yüklenmesini istemiştir.
> - **Depoda yeniden üretilenler:** kök, lemma ve bab sayıları, deponun `python -m tezgah` aracıyla QAC v0.4 üzerinden yeniden çalıştırılmıştır (§3). Sayılar oturumdaki sayılarla aynı çıkmıştır.
> - **Depoda yeniden üretilmeyenler:** her kullanımın elle sınıflandırılması (nesne türleri, isim kullanımı, tezekkür tetikleyicileri), birlikte geçiş oranları (§8) ve kapalı örneklemin kodlaması oturumda **quran-morphology** birimleri ve oturum betikleriyle üretildi. Bunlar bu kayıtta QAC üzerinde yeniden çalıştırılmadı. Elle sınıflandırmalar yorum katmanıdır, sayım değil.
> - **İkincil katman yok:** Lane ve Sâmî katmanına oturumda erişilemedi (403). Hiçbir bulgu bu katmanlara dayanmaz ve bu boşluk uydurma veriyle doldurulmadı.
> - **Meal delil değildir.** Aşağıdaki Türkçe karşılıklar çalışma çevirisidir; terimler (zikir, salât, zekât, âyet…) korunmuş, kavramlar bağlamıyla açılmıştır.
> - **Okunuşlar** deponun `python -m tezgah okunus` çıktısından alınmıştır (Tanzil Uthmani, kurallı aktarım; delil değil).
>
> **Notasyon.** Kök, deponun harf tablosuna göre **ẕ-k-r** (ذ-ك-ر) yazılır; sohbette kısaca "z-k-r" denmişti. Zekât kökü **z-k-v** (ز-ك-و) ayrı köktür; 87:14'teki *tezekkâ* o köke aittir ve bu kayda girmez.

## 1. Araştırma sorusu

Kur'an'da ẕ-k-r ailesi (zikir, tezekkür ve türevleri) ne anlama gelir? Dille anmak mıdır, içten hatırlamak mı, yoksa bunların ötesinde bir şey mi? Neden istenir, kim yapar, karşıtı nedir ve kavramın metin içi tanımı nedir?

Okuma biçimi: kavramı bilmeyen ama dili bilen bir okuyucu gibi, yalnız Kur'an verisinden.

## 2. Sonuç (kısa)

**Çalışma tanımı.** Zikir, bir şeyi **bilince çıkarmak ve orada canlı tutmaktır.**

- **İç biçimleri:** hatırda tutmak, unutmamak, hesaba katmak.
- **Dış biçimleri:** söze dökmek, anlatmak, adını anmak.
- **Taşıyıcıları:** bilince çıkaran hatırlatıcı söz veya işaret (vahiy, âyet, olay) ve anılmak.
- **Normatif katman:** Allah, nimet, âyet ve âhiret söz konusu olduğunda, bilince getirilen şey kişinin yönelişini ve davranışını belirler.
- **Karşıtları:** unutmak, gaflet, oyalanmak ve yüz çevirmek. Karşıtı sessizlik değildir.

| # | Bulgu | Mantıksal durum | Delil derecesi |
|---|---|---|---|
| 1 | Çekirdek tanım (bilince çıkarmak ve canlı tutmak) | Destekleniyor | Sağlam |
| 2 | "Zikir yalnız dille anmaktır" ve "zikir yalnız içtir" okumaları ikisi de tutmaz | Destekleniyor | Sağlam |
| 3 | *Zikr* ismi vahyin işlevi olarak da kullanılır; önceki vahiyler dâhil | Destekleniyor | Sağlam |
| 4 | Bab işbölümü: II. bab "hatırlatmak", V. bab "hatırlatılanı kendine almak" | Destekleniyor | Sağlam |
| 5 | Kınanan unutma ve gaflet, kişiye ulaşmış bir konuyla ilgilidir | Destekleniyor | Sağlam (Ö1'in ayırt ediciliği düşüktür, §11) |
| 6 | Allah'ın zikir ve unutması "ilgi ve muamele" olarak okunur | Destekleniyor | Sağlam |
| 7 | Tezekkür = farkına varıp gereğine yönelmek ("öğüt almak" yetersiz) | Destekleniyor | Muhtemel |
| 8 | Zikir salâtı kapsar ama salâta indirgenmez | Destekleniyor | Muhtemel |
| 9 | *Zikrullâh* beş rekabetçi ayette (kalp, salât, yüz çevirme bağlamları) "eylem" mi "vahiy" mi | Belirsiz | Spekülatif |
| 10 | İnkâr ile unutmanın sırası sabit değildir | Belirsiz | Spekülatif |
| 11 | Davranış zikrin parçası mı, meyvesi mi | Belirsiz | Spekülatif |

*Mantıksal durum sütunu bu kayıt yazılırken oturumdaki delil derecelerinden türetilmiştir; oturumda yalnız delil dereceleri açıkça ilan edilmişti.*

## 3. Aşama 1 — kök, morfoloji, sayım

Kaynak: QAC v0.4. Sorgular: `python -m tezgah sayim --kok "ذكر"`, `dagilim --gore lemma`, `dagilim --gore bab`.

**Toplam:** 292 kelime konumu / 264 ayet / 71 sûre.

| Lemma (okunuş) | Kelime konumu | Not |
|---|---:|---|
| *ẕakara* (I. bab fiil) | 84 | |
| *ẕikr* | 76 | isim |
| *taẕakkara* (V. bab fiil) | 51 | |
| *ẕikrâ* | 23 | isim |
| *ẕakar* | 18 | **farklı sözcük: "erkek"; analiz dışı** (aşağıda) |
| *ẕukkira* (II. bab, edilgen) | 18 | |
| *taẕkirat* | 9 | |
| *muddakir* | 6 | VIII. bab ortacı |
| *ẕâkirîn* | 2 | |
| *ẕâkirât* | 1 | |
| *muẕakkir* | 1 | |
| *maẕkûr* | 1 | |
| *taẕkîr* | 1 | |
| *iddakara* (VIII. bab fiil) | 1 | |
| **Toplam** | **292** | |

**Eşadlı sözcük.** *Ẕakar* ("erkek") 18 kelime konumudur ve kullanıcı kararıyla analiz dışı tutulmuştur. On altısı *ʾunsâ* ile birlikte geçer; diğer ikisi 6:139 ve 26:165'tir. Geriye kalan **zikir ailesi 274 kelime konumu / 246 ayet / 67 sûredir** (154 fiil, 120 isim; oturumda quran-morphology birimleriyle sayıldı).

**Bab dağılımı (segment; QAC işaretlemesi):** I. bab fiil 84; II. bab fiil 18, isim 10; V. bab fiil 51; VIII. bab fiil 1, isim 6; işaretsiz isim 122.

*Not:* QAC *taẕkîr*'i işaretsiz bırakır; bu yüzden QAC'ta II. bab isim 10'dur (9 *taẕkira* + *muẕakkir*). Elle yapılan sınıflandırmada II. bab ailesi 29'dur: 18 fiil + 9 *tezkira* + *tezkîr* + *müzekkir*.

**Elle sınıflandırılmış birim toplamları (oturum, 274 birim):** I. bab fiil 84, *zikr* 76, *zâkir/zâkira* 3, *mezkûr* 1, II. bab ailesi 29, V. bab 51, VIII. bab 7 (1 fiil + 6 *müddekir*), *zikrâ* 23. Toplam 274.

**Emir kipi.**

- I. bab: 84 kullanımın 49'u emirdir (31 çoğul, 17 tekil, 1 dişil çoğul: 33:34).
- II. bab: 18 kullanımın 7'si emirdir ve hepsi bir elçiye söylenir (6:70, 14:5, 50:45, 51:55, 52:29, 87:9, 88:21).
- V. bab: 51 kullanımın 0'ı emirdir. VIII. bab: 0.
- **Tezekkür hiçbir yerde emredilmez;** emredilen zikirdir ve hatırlatmadır.

## 4. Aşama 2 — fiil I: nesne kalıbı ve iç–dış spektrumu

*Ẕakara* (I. bab, 84) nesne türüne göre (elle sınıflandırma):

| Nesne | Sayı |
|---|---:|
| Allah / Rab | 23 |
| Allah'ın ismi | 14 |
| nimet | 15 |
| geçmiş olay | 4 |
| vahiy içeriği | 5 |
| kişiler ("kitapta … zikret": 19:16–56) | 10 |
| diğer | 10 |
| nesnesiz | 2 |
| özne Allah (2:152) | 1 |

**İçten dışa spektrum.** Aynı fiil hem içte hem sözde kullanılır:

- **İç uç:** 18:24, 18:63, 19:67, 40:44.
- **Orta:** 7:205 (*fî nefsike*, ama "sesli olmayan söz"), 2:235.
- **Dış uç:** 12:42, 21:60, 19:16–56, 47:20.

**Zikir ayrı bir eylemdir.** Söz, tefekkür, tesbih, istiğfar ve salâttan ayrı sayılır (43:13, 3:191, 3:41, 3:135, 87:15).

**Zikir gündelik hayatın içinde istenir:** hacda (2:198, 2:200, 2:203), savaşta (8:45), salâttan sonra ve ticarette (62:10), hata sonrası (3:135), unutma anında (18:24), bineğe binerken (43:13).

**Salât sıralaması:** 4:103 ve 62:10'da zikir salâttan sonradır; 87:15'te önce gelir; 4:142'de salât tembelliği ve zikrin azlığı iki ayrı kusur olarak sayılır.

**Ölçü:** *kesîr* ("çok") 9 kez, *kalîl* ("az") 1 kez (4:142) geçer. Hiçbir yerde sayı veya kalıp verilmez.

**Zikrin içeriği bilgiye bağlıdır** (2:198, 2:239). 2:200'de ölçüt atalar anmadır.

**Edilgen kullanımlar:** 8:2, 22:35, 39:45, 17:46.

**İsmin anılması:** gıda ve kurban ayetlerinin sekizinin sekizinde ismin zikri "üzerine" yapılır.

**Nimet zikri:** 19 ayetin 13'ünde aynı ayette bir davranış istemi vardır.

**Zikir ve unutma karşılıklı bir çifttir** ve ilgi ile muamele olarak okunur (2:152, 9:67, 7:51, 20:126, 32:14, 45:34). Allah unutmaz (19:64, 20:52). 76:1'deki *mezkûr* "anılır" demektir.

## 5. Aşama 3a — isim *zikr* (76 kelime konumu)

| Kullanım | Sayı |
|---|---:|
| vahiy / mesaj | 37 |
| açık eylem (anma) | 12 |
| iki okumaya açık | 15 |
| alanda oluşan (20:113; 54. sûre ×4) | 5 |
| size / onlara ait | 3 |
| anlatı | 3 |
| anılma (94:4) | 1 |

- Harf-i tarifli *ez-zikr* 20 yerde geçer: 15 vahiy, 4'ü 54. sûrede, 1 belirsiz (25:18).
- *Zikrullâh* 11 yerde geçer: 4 eylem, 7 belirsiz; hiçbiri açıkça vahiy değildir.
- **İç-tanım (metnin kendi tanımı):** *in huve illâ zikrun li'l-âlemîn* (12:104, 38:87, 68:52, 81:27), 36:69 ve 6:90 (*zikrâ*). Zıt tutulanlar: ücret, şiir, delilik, şeytan sözü.
- Kelime önceki vahiyler için de kullanılır (7:63, 7:69, 21:24, 21:48, 21:105, 37:168; *ehle'z-zikr*: 16:43, 21:7).
- **On beş belirsiz ayet iki okuma olarak, rekabet hâlinde bırakılmıştır:** 13:28 (×2), 29:45, 39:22, 39:23, 57:16, 62:9, 18:28, 18:101, 21:36, 21:42, 43:36, 53:29, 72:17, 25:18. Üç bağlama toplanırlar: kalp, salât, yüz çevirme.

## 6. Aşama 3b — hatırlatmak ve karşılığı (II. ve V. bab)

**İşbölümü.** II. bab (*zekkera*) başkasına hatırlatmak, V. bab (*tezekkera*) hatırlatılanı kendine almaktır. 51 V. bab kullanımının 50'sinde nesne yoktur (79:35 istisnadır). 74:55'teki nesneli I. bab kullanımı bu işbölümüyle uyumludur: nesneli I. bab ile nesnesiz V. bab çelişmez, iş bölümü yapar (oturumda bu şekilde çözüldü).

**V. bab kullanımının tetikleyicileri** (elle; 51 kullanım):

| Tetikleyici | Sayı |
|---|---:|
| vahiy | 13 |
| tevhid sorgusu | 8 |
| yaratılış / nimet | 8 |
| benzetme | 5 |
| elçi sözü / ömür | 5 |
| hüküm (16:90, 6:152, 24:27, 2:221) | 4 |
| tarih | 3 |
| âhiret | 2 |
| vesvese | 1 |
| hikmet | 1 |
| ayrı: nesneli kullanım (79:35) | 1 |

**Elçinin araçları:** Kur'an (50:45, 6:70), Allah'ın günleri (14:5), âyetler (18:57, 25:73, 32:22, 10:71). Yaratılışın kendisi de hatırlatır (51:49, 16:13, 25:62, 56:62, 7:201). Elçi dışındaki tek II. bab örneği 2:282'dir: iki şahidin karşılıklı hatırlatması.

**Tezekkür bilmek demek değildir** (23:84–85, 56:62, 39:9).

**Yararlanan kişi niteliklerle anılır:** *ulu'l-elbâb* 9, dilemek 5, iman 4, haşyet 4, inâbe 2, takvâ 2, kalp 1. "Ancak" kısıtlamaları: 2:269, 3:7, 13:19, 39:9, 40:13.

**Yararlanmama:** unutmak (5:13, 5:14, 6:44, 7:165), "az şey" (7:3, 27:62, 40:58, 69:42), yüz çevirmek (18:57, 32:22, 74:49), nefret (17:41, 25:50), ağır gelme (10:71, 36:19), tevbe ve tezekkürün olmaması (9:126, 37:13).

**Unutmak bir bellek kaybı değil, tutumun bırakılmasıdır:** 5:13'te söz bozma ve tahrifle, 7:165'te kötülüğü yasaklamanın bırakılmasıyla birlikte anılır. (Kapsam notu: bu iki ayetten çıkan okumadır; §10 C5.)

**Zaman:** 35:37, 89:23–24, 44:13, 47:18. Âhirette tezekkür olur ama artık yarar sağlamaz. 54. sûrede *fe-hel min müddekir?* altı kez tekrarlanır.

**Çeviri notu.** "Tezekkür" için mealin "öğüt almak"ı yetersizdir. Daha uygun karşılık: **"farkına varıp gereğine yönelmek".**

## 7. Aşama 3c — karşıt ve komşu kavramlar

- **Unutturan etkenler:** şeytan (6:68, 12:42, 18:63, 58:19), refah (25:18, 6:44), alay (23:110).
- **Zincirler:** 18:57 (zikr ettirilmek → yüz çevirmek → unutmak → kalpte örtü → hidayetin kapanması) ve 20:124–126.
- **Oyalanma:** 24:37, 63:9, 21:2–3 ("zikri dinlerler ama oynarlar").
- **Gaflet:** 7:205, 18:28.
- **Kalp:** 7 açık ayet (8:2, 22:35, 13:28, 39:23, 57:16, 50:37, 24:37) ile 10 kapalı ayet.
- **Komşular:** tilâvet ve va'z araçtır; tesbih ve şükür meyvedir; tefekkür ve salât ayrı terimlerdir; haşyet alıcının hâlidir.

## 8. Birlikte geçiş (yalnız betimleyici)

Zikir ailesi 246 ayette geçer (6.236 ayetin %3,9'u). Oran = gerçek ortak ayet sayısı / beklenen (kök ayet sayısı × 246 / 6.236). **Oturumda quran-morphology birimleriyle hesaplandı; bu kayıtta QAC üzerinde yeniden çalıştırılmadı.**

| Kök | Oran |
|---|---:|
| n-s-y | 8,2 |
| ʿ-r-ḍ (IV) | 5,5 |
| l-h-v | 5,1 |
| k-l-b (isim) | 3,5 |
| ṣ-l-v | 3,4 |
| t-l-v | 3,3 |
| ḫ-ş-y | 3,2 |
| v-ʿ-ẓ | 3,2 |
| k-f-r | 0,4 |

**Oran anlam kanıtı değildir.** Yalnız hangi köklerin birlikte aranacağını gösterir. Çıkarımlar §4–§7'deki ayet okumalarına dayanır.

## 9. Kritik ayetler

Türkçe karşılıklar çalışma çevirisidir; terimler korunmuştur.

**2:152**
*faẕkurûnî ʾaẕkurkum vaşkurû lî valâ takfurûn*
"Öyleyse beni zikredin, ben de sizi zikredeyim; bana şükredin, (nimeti) örtüp inkâr etmeyin."
Özne Allah olduğunda zikir "ilgi ve muamele"dir; zikir şükürle yan yana, küfrün karşısındadır.

**18:24**
*ʾillâ ʾan yaşâʾa llâhu vaẕkur rabbaka ʾiẕâ nasîta vaqul ʿasâ ʾan yahdiyani rabbî liʾaqraba min hâẕâ raşadâ*
"… ancak 'Allah dilerse' (diyerek). Unuttuğunda Rabbini zikret ve de ki: 'Umulur ki Rabbim beni bundan daha doğruya yaklaştırır.'"
İç uç: zikir unutma anında hatırlayıp yeniden yönelmektir. Karşıt: *nasîta*.

**7:205**
*vaẕkur rabbaka fî nafsika tażarruʿan vaḫîfatan vadûna lcahri mina lqavli bilguduvvi valʾâṣâli valâ takum mina lgâfilîn*
"Rabbini içinden, yalvararak ve korkuyla, sözün yüksek olmayan (sesiyle), sabah akşam zikret; gafillerden olma."
Zikir hem içte hem sözde; karşıtı gaflet. Tek başına "yalnız iç" veya "yalnız dil" okumasını bozar.

**15:9**
*ʾinnâ naḥnu nazzalnâ ẕẕikra vaʾinnâ lahû laḥâfiẓûn*
"Zikri biz indirdik, onu koruyacak olan da elbette biziz."
*Zikr* burada indirilen vahiydir.

**13:28** *(belirsiz kullanım)*
*allaẕîna ʾâmanû vataṭmaʾinnu qulûbuhum biẕikri llâhi ʾalâ biẕikri llâhi taṭmaʾinnu lqulûb*
"Onlar iman edenlerdir; kalpleri Allah'ın zikriyle huzur bulur. Bilin ki kalpler ancak Allah'ın zikriyle huzur bulur."
*Zikrullâh* eylem mi vahiy mi, metin içinden çözülmez; iki okuma rekabette bırakılmıştır (§5).

**20:14**
*ʾinnanî ʾanâ llâhu lâ ʾilâha ʾillâ ʾana faʿbudnî vaʾaqimi ṣṣalâta liẕikrî*
"Ben Allah'ım; benden başka ilâh yoktur; bana kulluk et ve salâtı zikrim için ikâme et."
*Liẕikrî* "beni anman için" ya da "benim hatırlatmam için" okunabilir; salât ile zikir ilişkisi (§10 C2).

**29:45** *(belirsiz kullanım)*
*utlu mâ ʾûḥiya ʾilayka mina lkitâbi vaʾaqimi ṣṣalâta ʾinna ṣṣalâta tanhâ ʿani lfaḥşâʾi valmunkari valaẕikru llâhi ʾakbaru vallâhu yaʿlamu mâ taṣnaʿûn*
"Sana kitaptan vahyedileni oku ve salâtı ikâme et. Salât fahşâdan ve münkerden alıkoyar; Allah'ın zikri ise daha büyüktür. Allah ne yaptığınızı bilir."
Zikir salâttan ayrı ve onu aşan bir şeydir.

**4:103**
*faʾiẕâ qażaytumu ṣṣalâta faẕkurû llâha qiyâman vaquʿûdan vaʿalâ cunûbikum faʾiẕâ ṭmaʾnantum faʾaqîmû ṣṣalâta ʾinna ṣṣalâta kânat ʿalâ lmuʾminîna kitâbam mavqûtâ*
"Salâtı bitirince ayakta, oturarak ve yanlarınız üzerine (yatarken) Allah'ı zikredin. Güvene erince salâtı ikâme edin. Salât, müminler üzerine vakitleri belirli bir yazılı hükümdür."
Zikir salâtın bitiminden sonra da, her hâlde sürer.

**62:9–10**
*yâʾayyuhâ llaẕîna ʾâmanû ʾiẕâ nûdiya liṣṣalâti min yavmi lcumuʿati fasʿav ʾilâ ẕikri llâhi vaẕarû lbayʿa ẕâlikum ḫayrul lakum ʾin kuntum taʿlamûn*
"Ey iman edenler! Cuma günü salât için çağrıldığınızda Allah'ın zikrine koşun, alışverişi bırakın; bilirseniz bu sizin için daha hayırlıdır."
*faʾiẕâ qużiyati ṣṣalâtu fantaşirû fî lʾarżi vabtagû min fażli llâhi vaẕkurû llâha kas̱îral laʿallakum tufliḥûn*
"Salât bitince yeryüzüne dağılın, Allah'ın fazlından isteyin ve Allah'ı çok zikredin ki kurtuluşa eresiniz."
9'da *zikrullâh* salâtla kurulan belirsiz kullanımdır (§5); 10'da zikir ticaretin içinde istenir.

**3:191**
*allaẕîna yaẕkurûna llâha qiyâman vaquʿûdan vaʿalâ cunûbihim vayatafakkarûna fî ḫalqi ssamâvâti valʾarżi rabbanâ mâ ḫalaqta hâẕâ bâṭilan subḥânaka faqinâ ʿaẕâba nnâr*
"Onlar ayakta, oturarak ve yanları üzerine (yatarken) Allah'ı zikredenler ve göklerin ve yerin yaratılışı üzerine tefekkür edenlerdir: 'Rabbimiz, bunu boşuna yaratmadın; sübhânsın; bizi ateşin azabından koru.'"
Zikir ve tefekkür ayrı terimlerdir.

**4:142**
*ʾinna lmunâfiqîna yuḫâdiʿûna llâha vahuva ḫâdiʿuhum vaʾiẕâ qâmû ʾilâ ṣṣalâti qâmû kusâlâ yurâʾûna nnâsa valâ yaẕkurûna llâha ʾillâ qalîlâ*
"Münafıklar Allah'ı aldatmaya çalışırlar; oysa O onları aldatandır. Salâta kalktıklarında tembel tembel kalkarlar, insanlara gösteriş yaparlar ve Allah'ı ancak pek az zikrederler."
Salâta kalkmak ile zikir iki ayrı kusurdur.

**24:37**
*ricâlul lâ tulhîhim ticâratun valâ bayʿun ʿan ẕikri llâhi vaʾiqâmi ṣṣalâti vaʾîtâʾi zzakâti yaḫâfûna yavman tataqallabu fîhi lqulûbu valʾabṣâr*
"Kendilerini ne ticaretin ne alışverişin Allah'ın zikrinden, salâtı ikâmeden ve zekâtı vermekten oyalamadığı adamlar; kalplerin ve gözlerin ters döneceği bir günden korkarlar."
Karşıt kavram: oyalanmak (*lehv*). Zikir, salât ve zekâtla yan yana ama ayrı sayılır.

**18:57**
*vaman ʾaẓlamu mimman ẕukkira biʾâyâti rabbihî faʾaʿraża ʿanhâ vanasiya mâ qaddamat yadâhu ʾinnâ caʿalnâ ʿalâ qulûbihim ʾakinnatan ʾan yafqahûhu vafî ʾâẕânihim vaqran vaʾin tadʿuhum ʾilâ lhudâ falan yahtadû ʾiẕan ʾabadâ*
"Rabbinin âyetleriyle zikr ettirilip de onlardan yüz çeviren ve ellerinin önceden gönderdiğini unutandan daha zalim kim vardır? Biz onların kalpleri üzerine onu kavramalarına engel örtüler, kulaklarında da ağırlık kıldık. Onları hidayete çağırsan da o zaman asla yol bulamazlar."
Zincir: hatırlatılmak → yüz çevirmek → unutmak → kalpte örtü → yol bulamamak.

**20:124–126**
*vaman ʾaʿraża ʿan ẕikrî faʾinna lahû maʿîşatan żankan vanaḥşuruhû yavma lqiyâmati ʾaʿmâ*
"Kim zikrimden yüz çevirirse onun için dar bir geçim vardır ve onu kıyamet günü kör olarak haşrederiz."
*qâla rabbi lima ḥaşartanî ʾaʿmâ vaqad kuntu baṣîrâ*
"'Rabbim, beni neden kör haşrettin? Oysa görüyordum.' dedi."
*qâla kaẕâlika ʾatatka ʾâyâtunâ fanasîtahâ vakaẕâlika lyavma tunsâ*
"Dedi ki: 'İşte böyle; âyetlerimiz sana geldi de sen onları unuttun; bugün de öyle unutulursun.'"
Unutma ve unutulma karşılıklıdır; unutulan şey ulaşmış âyettir.

**54:17**
*valaqad yassarnâ lqurʾâna liẕẕikri fahal mim muddakir*
"Andolsun Kur'an'ı zikir (hatırlama ve hatırlatma) için kolaylaştırdık; hiç kendine getirip farkına varan var mı?"
VIII. bab ortacı (*müddekir*) hatırlatılanı kendi içine alan kişidir.

**87:15**
*vaẕakara sma rabbihî faṣallâ*
"Rabbinin ismini zikretti ve salât etti."
Zikir salâttan önce gelir ve ondan ayrı sayılır.

## 10. Karşı örnekler ve falsifikasyon

**Karşı örnek sınamaları (C1–C7)**

| # | İddia | Sonuç |
|---|---|---|
| C1 | Çekirdek tanım | Korundu |
| C2 | Zikir ve salât | **Düzeltildi** |
| C3 | Tezekkür | **Düzeltildi** |
| C4 | Yararlanma niteliğe bağlıdır | Korundu |
| C5 | Unutmak = tutumu bırakmak | Korundu, kapsam notuyla |
| C6 | İnkâr unutmadan sonra gelen geç aşamadır | **Düşürüldü, belirsiz** |
| C7 | Allah'ın zikir/unutması = ilgi | Korundu |

- **C2.** 2:238–239 ile 4:103 ve 62:9, salâtın zikrin bir biçimi olarak adlandırılabildiğini gösterir. Ama zikir salâta indirgenemez (4:103, 62:10, 20:14, 29:45, 5:91, 24:37, 4:142).
- **C3.** 24:27 ve 2:221 tezekkürün yalnız yeni öğrenilen değil, zaten bilinen ya da yeni bildirilen şeye de uygulandığını gösterir; bu yüzden tanım "farkına varıp gereğine yönelmek" olarak genişletildi.
- **C6.** 21:36, 41:41, 68:51 ve ayrıca 39:8 ile 16:106–108 zıt sırayla gelir; unutma ile inkârın sırası sabit değildir.

**En güçlü karşı okumalar**

- **M1 — "Zikir dille anmaktır."** Dayanakları: 7:205, 33:41–42, 3:41, 24:36, 14 isim kullanımı, edilgen kullanımlar, 2:200–201, 2:239, 62:9. **Açıklayamadıkları:** 18:24, 18:63, 19:67, 40:44, 2:235, 3:41, 43:13, 2:152, 4:142.
- **M2 — "Zikir tamamen içtir."** Dayanakları: 18:24, 19:67, 40:44, 7:205 (*fî nefsike*), 3:41. **Açıklayamadıkları:** 7:205'in ses düzeyi, 12:42, 21:60, 17:46, 8:2, isim kullanımları, 2:239.
- İki okuma da aynı kapsamdaki karşı örneklerde çöker. Tanım iki veri kümesini de kapsar.

## 11. Kapalı örneklem sınaması

**Tasarım.** Tanım ve tahminler sınamadan önce kaydedildi ([Zikir-onceden-kayit.md](Zikir-onceden-kayit.md)). Örneklem: ẕ-k-r ailesinden kelime içermeyen, n-s-y, ğ-f-l veya l-h-v köklü **69 ayet** (59'u daha önce okunmamış). Kodlama: [Zikir-kapali-orneklem.tsv](Zikir-kapali-orneklem.tsv). Ayet listesi ve kodlama oturum dosyalarından depoya aktarıldı; sayılar bu kayıtta aynı kodlamadan yeniden hesaplandı.

| Tahmin | Tüm örneklem | Daha önce görülmemiş alt küme |
|---|---|---|
| Ö1: kınanan konu kişiye ulaşmıştır | 31 / 31 | 24 / 24 |
| Ö2: ulaşmamış şeyden habersizlik kınanmaz | 4 / 4 (6:131, 6:156, 12:3, 36:6) | — |
| Ö3: bir tutum, eylem veya sonuç eşlik eder | 30 / 31 | 23 / 24 |

- Ö3'ün tek istisnası **10:92**'dir; bu yüzden ifade "neredeyse her zaman"dır.
- 69 ayetin sınıfları: kınama 31, özne Allah 15, nötr 13, tanımlayıcı 4, habersizlik 4, unutma uyarısı 2.

**Sınırlar (olumsuz ya da zayıf yönler açıkça yazılmıştır)**

- **Tek kodlayıcı, kör değil.** Kodlama aynı oturumu yürüten kişi tarafından, tahmin bilinirken yapıldı.
- **Komşu ayetle kodlama.** Kınama koduyla işaretlenen 8 ayette ("E-komşu") "ulaşmış" ve/veya "eylem" hükmü yanındaki ayetle verildi: 7:172, 15:3, 16:108, 21:1, 21:3, 31:6, 45:34, 80:10.
- **Ö1'in ayırt ediciliği düşüktür.** Kınama kavramı zaten bir konuya ulaşmış olmayı varsayar; 31/31 sonucu bu yüzden güçlü bir test sayılmamalıdır. Daha ayırt edici olan Ö3'tür (30/31) ve Ö2 (yalnız 4 ayet).
- **Örneklem kök seçimine bağlıdır.** Yalnız üç karşıt kök tarandı; başka karşıt köklerde sonuç sınanmadı.
- **Bu örneklem tanımın tamamını sınamaz.** Yalnız karşıt kavramların kınanma koşulunu sınar; zikir ismi, II/V bab işbölümü ve iç–dış spektrumu bu örneklemle sınanmadı.

## 12. Sözlük maddesi taslağı

*Depoda ayrı bir sözlük dosyası yok; bu madde taslak olarak kartta durur. Zekât (z-k-v) ve salât (ṣ-l-v) maddeleri bu depoda bulunamadı; sözlük dosyası kurulunca biçim onlarla uyumlandırılır.*

**ẕ-k-r (ذ-ك-ر) — 292 kelime konumu = 274 (zikir ailesi) + 18 (*ẕakar*, ayrı madde "erkek")**

| Biçim | Say | Türkçe karşılık (bağlamıyla) |
|---|---:|---|
| *ẕakara* (I) | 84 | zikretmek: hatırda tutmak (18:24, 19:67); anmak, söz etmek (12:42, 21:60); anlatmak (19:16); edilgen: anılmak |
| *ẕikr* | 76 | eylem (2:200, 33:41); hatırlatıcı söz / vahiy (15:9, 21:105: "âlemler için bir hatırlatma"); anılma (94:4) |
| *ẕâkir / ẕâkira* | 3 | zikredenler |
| *maẕkûr* | 1 | anılır (76:1) |
| *ẕakkara* (II) | 18 | zikr ettirmek, hatırlatmak |
| *taẕkira* | 9 | hatırlatıcı |
| *taẕkîr* | 1 | hatırlatma |
| *muẕakkir* | 1 | hatırlatıcı (88:21) |
| *taẕakkara* (V) | 51 | tezekkür etmek: hatırlatılanı kendine alıp farkına varmak ve gereğine yönelmek; "öğüt almak" değil |
| *iddakara* (VIII) | 1 | uzun zaman sonra hatırlamak |
| *muddakir* | 6 | hatırlatılanı kendine getiren |
| *ẕikrâ* | 23 | hatırlatma |

**Karşıtlar:** unutmak, gaflet, oyalanmak, yüz çevirmek. **Araçlar:** okumak (tilâvet), öğüt (va'z). **Meyveler:** şükür, tesbih.

**Yöntem önerisi:** İlk çeviride "zikir" terim olarak çevrilmeden bırakılır, birim bitince bağlamına göre karşılanır. Tezekkür hiçbir zaman "öğüt almak" diye çevrilmez.

## 13. Açık sorular ve sınırlar

- Beş rekabetçi *zikrullâh* ayetinde (§5) eylem/vahiy ayrımı metin içinden çözülmedi.
- İnkâr ile unutmanın sırası sabit değildir (§10 C6); başka bir sıra sınaması yapılmadı.
- Davranışın zikrin **parçası** mı, **meyvesi** mi olduğu açık: iki okuma da ayetlerle uyumludur.
- **Tezekkür ile hidayet ilişkisi** ayrı bir çalışmadır; bu kayıtta yalnız işaretlenmiştir (13:27, 76:30, 14:4). [Hidayet kartı](Hidayet-concept-card.md) ile birlikte sınanmalıdır; bu kayıtta sınanmadı.
- Kapalı örneklemin zayıf yönleri §11'de.
- Lane ve Sâmî katmanı yok (erişim 403); bu katmanlardan üretilecek hipotezler henüz sınanmadı.
- Birlikte geçiş oranlarının (§8) ve elle sınıflandırmaların QAC üzerinde yeniden üretilmesi açık iştir.

## 14. Kayıt satırı

```
Kaynak      : QAC v0.4 (kök / lemma / bab sayımı, okunuş) + oturumda quran-morphology (elle sınıflandırma, birlikte geçiş, kapalı örneklem); Lane/Sâmî kurulamadı (403)
Sayım birimi: kelime konumu (292, 274) | segment (bab tablosu) | ayet (264, 246, kapalı örneklem 69) | sûre (71, 67)
Sorgu       : python -m tezgah sayim --kok "ذكر"; python -m tezgah dagilim --kok "ذكر" --gore lemma; python -m tezgah dagilim --kok "ذكر" --gore bab; python -m tezgah etiket "(II)" "ROOT:*kr" TAG:N; python -m tezgah okunus <ayetler>
Veri izi    : a1d129238153 (QAC v0.4)
Durum       : kısmen çalıştırıldı (QAC sayımları çalıştırıldı; elle sınıflandırmalar, birlikte geçiş oranları ve kapalı örneklem bu depoda yeniden çalıştırılmadı)
```
