# İman–tevekkül karşılaştırması: mekanik QAC taraması

Betik sürümü: 1.0.0. Bu rapor `python 08_scripts/analyze_tawakkul_comparison.py` ile üretilir; elle düzenlenmez.

Anlam değerlendirmesi için [analiz dizinine](../../README.md) bakın. Sayım tek başına kavram tanımı değildir.

## Kök sayımları

| Kök | Kelime konumu | Segment | Ayet | Sûre |
|---|---:|---:|---:|---:|
| ʾ-m-n (`Amn`) | 879 | 879 | 723 | 77 |
| v-k-l (`wkl`) | 70 | 70 | 61 | 29 |
| f-v-ż (`fwD`) | 1 | 1 | 1 | 1 |

## Tam eşleşen alt sorgular

| Sorgu | Kelime konumu | Segment | Ayet | Sûre |
|---|---:|---:|---:|---:|
| `Amn_IV_fiil` | 537 | 537 | 478 | 73 |
| `Amn_IV_tum_turler` | 812 | 812 | 668 | 75 |
| `iman_isim_lemmasi` | 45 | 45 | 41 | 21 |
| `wkl_V_fiil` | 40 | 40 | 38 | 24 |
| `wkl_V_isim` | 4 | 4 | 4 | 4 |
| `wakil_isim_lemmasi` | 24 | 24 | 24 | 13 |
| `wkl_II_fiil` | 2 | 2 | 2 | 2 |
| `fwD_II_fiil` | 1 | 1 | 1 | 1 |

## Lemma, tür ve bap ayrımı

| Kök | Lemma | Tür | Bap | Kelime konumu |
|---|---|---|---|---:|
| ʾ-m-n | ʾâmana | V | IV | 537 |
| ʾ-m-n | ʾâmin | ADJ | işaretsiz | 2 |
| ʾ-m-n | ʾâmin | N | işaretsiz | 4 |
| ʾ-m-n | ʾâminat | N | işaretsiz | 1 |
| ʾ-m-n | ʾâminîn | N | işaretsiz | 10 |
| ʾ-m-n | ʾîmân | N | IV | 45 |
| ʾ-m-n | ʾamânât | N | işaretsiz | 4 |
| ʾ-m-n | ʾamânat | N | işaretsiz | 2 |
| ʾ-m-n | ʾamanat | N | işaretsiz | 2 |
| ʾ-m-n | ʾamina | V | I | 20 |
| ʾ-m-n | ʾamîn | ADJ | işaretsiz | 14 |
| ʾ-m-n | ʾamn | N | işaretsiz | 5 |
| ʾ-m-n | maʾman | N | işaretsiz | 1 |
| ʾ-m-n | maʾmûn | N | işaretsiz | 1 |
| ʾ-m-n | muʾmin | ADJ | IV | 7 |
| ʾ-m-n | muʾmin | N | IV | 195 |
| ʾ-m-n | muʾminât | ADJ | IV | 4 |
| ʾ-m-n | muʾminât | N | IV | 18 |
| ʾ-m-n | muʾminat | ADJ | IV | 4 |
| ʾ-m-n | muʾminat | N | IV | 2 |
| ʾ-m-n | uʾtumina | V | VIII | 1 |
| v-k-l | mutavakkilûn | N | V | 4 |
| v-k-l | tavakkal | V | V | 40 |
| v-k-l | vakîl | N | işaretsiz | 24 |
| v-k-l | vukkila | V | II | 2 |
| f-v-ż | ʾufavviżu | V | II | 1 |

## Aynı ayette birlikte geçiş

Pencere tam ayettir. Bu çıktı sözdizimi bağı, eşanlamlılık, nedensellik veya zorunlu aşama sırası kurmaz.

- `Amn_koku_ve_wkl_koku`: **17 ayet** — 3:122, 3:160, 3:173, 4:171, 5:11, 5:23, 8:2, 9:51, 10:84, 14:11, 16:99, 17:68, 42:36, 58:10, 60:4, 64:13, 67:29.
- `iman_isim_lemmasi_ve_wkl_koku`: **2 ayet** — 3:173, 8:2.
- `Amn_koku_ve_wkl_V_fiil`: **14 ayet** — 3:122, 3:160, 5:11, 5:23, 8:2, 9:51, 10:84, 14:11, 16:99, 42:36, 58:10, 60:4, 64:13, 67:29.
- `iman_isim_lemmasi_ve_wkl_V_fiil`: **1 ayet** — 8:2.

Kök düzeyindeki kesişimde 17:68 de vardır; bu yüzden bütün kesişimleri iman–tevekkül bağı diye saymak yanlıştır.

## Kritik morfoloji denetimleri

- **106:4:5:2**: `'aAmana`, `TAG:V`, `(IV)`, `ROOT:Amn`; 537 IV. bap fiil sayımına dahildir. IV. bap tek bir anlama eşitlenemez.
- **12:17:14:2**: `mu&omin`, `TAG:N`, `ACT|PCPL|(IV)`, `ROOT:Amn`; fiil veya iman isim lemması değildir. 12:17:14:1 `bi` öneki, 12:17:15:1 `la` edatı ayrıca kayıttadır.
- **6:89:12; 32:11:6**: w-k-l II. bap fiilleri; V. bap tevekkül fiilleriyle birleştirilmez.
- **40:44:5:2**: `>ufaw~iDu`, `TAG:V`, `(II)`, `ROOT:fwD`; bu kök için taramada tek kelime konumu. Teknik tafvîż isim teriminin geçtiği sonucu çıkmaz.

## Bütün w-k-l geçişleri

Aşağıdaki liste tamdır. Ayetin tamamı, komşu ayet anahtarları ve aktarım belirsizlikleri `verse_lookup.csv` içindedir. Kelime biçimleri teknik Buckwalter verisidir; lemma okunuşu ayrıca gösterilir.

| Kelime konumu | Lemma okunuşu | Kelime biçimi (BW) | Tür | Bap |
|---|---|---|---|---|
| [3:122:11](https://corpus.quran.com/wordmorphology.jsp?location=(3:122:11)) | tavakkal | `faloyatawak~ali` | V | V |
| [3:159:24](https://corpus.quran.com/wordmorphology.jsp?location=(3:159:24)) | tavakkal | `fatawak~alo` | V | V |
| [3:159:30](https://corpus.quran.com/wordmorphology.jsp?location=(3:159:30)) | mutavakkilûn | `{lomutawak~iliyna` | N | V |
| [3:160:17](https://corpus.quran.com/wordmorphology.jsp?location=(3:160:17)) | tavakkal | `faloyatawak~ali` | V | V |
| [3:173:17](https://corpus.quran.com/wordmorphology.jsp?location=(3:173:17)) | vakîl | `{lowakiylu` | N | işaretsiz |
| [4:81:19](https://corpus.quran.com/wordmorphology.jsp?location=(4:81:19)) | tavakkal | `watawak~alo` | V | V |
| [4:81:24](https://corpus.quran.com/wordmorphology.jsp?location=(4:81:24)) | vakîl | `wakiylFA` | N | işaretsiz |
| [4:109:18](https://corpus.quran.com/wordmorphology.jsp?location=(4:109:18)) | vakîl | `wakiylFA` | N | işaretsiz |
| [4:132:10](https://corpus.quran.com/wordmorphology.jsp?location=(4:132:10)) | vakîl | `wakiylFA` | N | işaretsiz |
| [4:171:53](https://corpus.quran.com/wordmorphology.jsp?location=(4:171:53)) | vakîl | `wakiylFA` | N | işaretsiz |
| [5:11:22](https://corpus.quran.com/wordmorphology.jsp?location=(5:11:22)) | tavakkal | `faloyatawak~ali` | V | V |
| [5:23:18](https://corpus.quran.com/wordmorphology.jsp?location=(5:23:18)) | tavakkal | `fatawak~aluw^A@` | V | V |
| [6:66:9](https://corpus.quran.com/wordmorphology.jsp?location=(6:66:9)) | vakîl | `biwakiylK` | N | işaretsiz |
| [6:89:12](https://corpus.quran.com/wordmorphology.jsp?location=(6:89:12)) | vukkila | `wak~alonaA` | V | II |
| [6:102:16](https://corpus.quran.com/wordmorphology.jsp?location=(6:102:16)) | vakîl | `wakiylN` | N | işaretsiz |
| [6:107:13](https://corpus.quran.com/wordmorphology.jsp?location=(6:107:13)) | vakîl | `biwakiylK` | N | işaretsiz |
| [7:89:33](https://corpus.quran.com/wordmorphology.jsp?location=(7:89:33)) | tavakkal | `tawak~alonaA` | V | V |
| [8:2:17](https://corpus.quran.com/wordmorphology.jsp?location=(8:2:17)) | tavakkal | `yatawak~aluwna` | V | V |
| [8:49:12](https://corpus.quran.com/wordmorphology.jsp?location=(8:49:12)) | tavakkal | `yatawak~alo` | V | V |
| [8:61:6](https://corpus.quran.com/wordmorphology.jsp?location=(8:61:6)) | tavakkal | `watawak~alo` | V | V |
| [9:51:13](https://corpus.quran.com/wordmorphology.jsp?location=(9:51:13)) | tavakkal | `faloyatawak~ali` | V | V |
| [9:129:11](https://corpus.quran.com/wordmorphology.jsp?location=(9:129:11)) | tavakkal | `tawak~alotu` | V | V |
| [10:71:19](https://corpus.quran.com/wordmorphology.jsp?location=(10:71:19)) | tavakkal | `tawak~alotu` | V | V |
| [10:84:9](https://corpus.quran.com/wordmorphology.jsp?location=(10:84:9)) | tavakkal | `tawak~aluw^A@` | V | V |
| [10:85:4](https://corpus.quran.com/wordmorphology.jsp?location=(10:85:4)) | tavakkal | `tawak~alonaA` | V | V |
| [10:108:22](https://corpus.quran.com/wordmorphology.jsp?location=(10:108:22)) | vakîl | `biwakiylK` | N | işaretsiz |
| [11:12:27](https://corpus.quran.com/wordmorphology.jsp?location=(11:12:27)) | vakîl | `wakiylN` | N | işaretsiz |
| [11:56:2](https://corpus.quran.com/wordmorphology.jsp?location=(11:56:2)) | tavakkal | `tawak~alotu` | V | V |
| [11:88:33](https://corpus.quran.com/wordmorphology.jsp?location=(11:88:33)) | tavakkal | `tawak~alotu` | V | V |
| [11:123:10](https://corpus.quran.com/wordmorphology.jsp?location=(11:123:10)) | tavakkal | `watawak~alo` | V | V |
| [12:66:24](https://corpus.quran.com/wordmorphology.jsp?location=(12:66:24)) | vakîl | `wakiylN` | N | işaretsiz |
| [12:67:24](https://corpus.quran.com/wordmorphology.jsp?location=(12:67:24)) | tavakkal | `tawak~alotu` | V | V |
| [12:67:26](https://corpus.quran.com/wordmorphology.jsp?location=(12:67:26)) | tavakkal | `faloyatawak~ali` | V | V |
| [12:67:27](https://corpus.quran.com/wordmorphology.jsp?location=(12:67:27)) | mutavakkilûn | `{lomutawak~iluwna` | N | V |
| [13:30:26](https://corpus.quran.com/wordmorphology.jsp?location=(13:30:26)) | tavakkal | `tawak~alotu` | V | V |
| [14:11:28](https://corpus.quran.com/wordmorphology.jsp?location=(14:11:28)) | tavakkal | `faloyatawak~ali` | V | V |
| [14:12:4](https://corpus.quran.com/wordmorphology.jsp?location=(14:12:4)) | tavakkal | `natawak~ala` | V | V |
| [14:12:16](https://corpus.quran.com/wordmorphology.jsp?location=(14:12:16)) | tavakkal | `faloyatawak~ali` | V | V |
| [14:12:17](https://corpus.quran.com/wordmorphology.jsp?location=(14:12:17)) | mutavakkilûn | `{lomutawak~iluwna` | N | V |
| [16:42:5](https://corpus.quran.com/wordmorphology.jsp?location=(16:42:5)) | tavakkal | `yatawak~aluwna` | V | V |
| [16:99:10](https://corpus.quran.com/wordmorphology.jsp?location=(16:99:10)) | tavakkal | `yatawak~aluwna` | V | V |
| [17:2:12](https://corpus.quran.com/wordmorphology.jsp?location=(17:2:12)) | vakîl | `wakiylFA` | N | işaretsiz |
| [17:54:14](https://corpus.quran.com/wordmorphology.jsp?location=(17:54:14)) | vakîl | `wakiylFA` | N | işaretsiz |
| [17:65:9](https://corpus.quran.com/wordmorphology.jsp?location=(17:65:9)) | vakîl | `wakiylFA` | N | işaretsiz |
| [17:68:15](https://corpus.quran.com/wordmorphology.jsp?location=(17:68:15)) | vakîl | `wakiylFA` | N | işaretsiz |
| [17:86:13](https://corpus.quran.com/wordmorphology.jsp?location=(17:86:13)) | vakîl | `wakiylFA` | N | işaretsiz |
| [25:43:9](https://corpus.quran.com/wordmorphology.jsp?location=(25:43:9)) | vakîl | `wakiylFA` | N | işaretsiz |
| [25:58:1](https://corpus.quran.com/wordmorphology.jsp?location=(25:58:1)) | tavakkal | `watawak~alo` | V | V |
| [26:217:1](https://corpus.quran.com/wordmorphology.jsp?location=(26:217:1)) | tavakkal | `watawak~alo` | V | V |
| [27:79:1](https://corpus.quran.com/wordmorphology.jsp?location=(27:79:1)) | tavakkal | `fatawak~alo` | V | V |
| [28:28:15](https://corpus.quran.com/wordmorphology.jsp?location=(28:28:15)) | vakîl | `wakiylN` | N | işaretsiz |
| [29:59:5](https://corpus.quran.com/wordmorphology.jsp?location=(29:59:5)) | tavakkal | `yatawak~aluwna` | V | V |
| [32:11:6](https://corpus.quran.com/wordmorphology.jsp?location=(32:11:6)) | vukkila | `wuk~ila` | V | II |
| [33:3:1](https://corpus.quran.com/wordmorphology.jsp?location=(33:3:1)) | tavakkal | `watawak~alo` | V | V |
| [33:3:6](https://corpus.quran.com/wordmorphology.jsp?location=(33:3:6)) | vakîl | `wakiylFA` | N | işaretsiz |
| [33:48:7](https://corpus.quran.com/wordmorphology.jsp?location=(33:48:7)) | tavakkal | `watawak~alo` | V | V |
| [33:48:12](https://corpus.quran.com/wordmorphology.jsp?location=(33:48:12)) | vakîl | `wakiylFA` | N | işaretsiz |
| [39:38:35](https://corpus.quran.com/wordmorphology.jsp?location=(39:38:35)) | tavakkal | `yatawak~alu` | V | V |
| [39:38:36](https://corpus.quran.com/wordmorphology.jsp?location=(39:38:36)) | mutavakkilûn | `{lomutawak~iluwna` | N | V |
| [39:41:18](https://corpus.quran.com/wordmorphology.jsp?location=(39:41:18)) | vakîl | `biwakiylK` | N | işaretsiz |
| [39:62:9](https://corpus.quran.com/wordmorphology.jsp?location=(39:62:9)) | vakîl | `wakiylN` | N | işaretsiz |
| [42:6:12](https://corpus.quran.com/wordmorphology.jsp?location=(42:6:12)) | vakîl | `biwakiylK` | N | işaretsiz |
| [42:10:13](https://corpus.quran.com/wordmorphology.jsp?location=(42:10:13)) | tavakkal | `tawak~alotu` | V | V |
| [42:36:17](https://corpus.quran.com/wordmorphology.jsp?location=(42:36:17)) | tavakkal | `yatawak~aluwna` | V | V |
| [58:10:16](https://corpus.quran.com/wordmorphology.jsp?location=(58:10:16)) | tavakkal | `faloyatawak~ali` | V | V |
| [60:4:48](https://corpus.quran.com/wordmorphology.jsp?location=(60:4:48)) | tavakkal | `tawak~alonaA` | V | V |
| [64:13:8](https://corpus.quran.com/wordmorphology.jsp?location=(64:13:8)) | tavakkal | `faloyatawak~ali` | V | V |
| [65:3:7](https://corpus.quran.com/wordmorphology.jsp?location=(65:3:7)) | tavakkal | `yatawak~alo` | V | V |
| [67:29:7](https://corpus.quran.com/wordmorphology.jsp?location=(67:29:7)) | tavakkal | `tawak~alonaA` | V | V |
| [73:9:9](https://corpus.quran.com/wordmorphology.jsp?location=(73:9:9)) | vakîl | `wakiylFA` | N | işaretsiz |

## Seçilmiş ayet görünümü

Latin aktarımı Tanzil ayetinden üretilir; bağımsız anlam delili değildir.

- **3:121**: vaʾiẕ gadavta min ʾahlika tubavviʾu lmuʾminîna maqâʿida lilqitâli vallâhu samîʿun ʿalîm
- **3:122**: ʾiẕ hammaṭ ṭâʾifatâni minkum ʾan tafşalâ vallâhu valiyyuhumâ vaʿalâ llâhi falyatavakkali lmuʾminûn
- **3:152**: valaqad ṣadaqakumu llâhu vaʿdahû ʾiẕ taḥussûnahum biʾiẕnihî ḥattâ ʾiẕâ faşiltum vatanâzaʿtum fî lʾamri vaʿaṣaytum mim baʿdi mâ ʾarâkum mâ tuḥibbûna minkum man yurîdu ddunyâ vaminkum man yurîdu lʾâḫirata s̱umma ṣarafakum ʿanhum liyabtaliyakum valaqad ʿafâ ʿankum vallâhu ẕû fażlin ʿalâ lmuʾminîn
- **3:153**: ʾiẕ tuṣʿidûna valâ talvûna ʿalâ ʾaḥadin varrasûlu yadʿûkum fî ʾuḫrâkum faʾas̱âbakum gammam bigammil likaylâ taḥzanû ʿalâ mâ fâtakum valâ mâ ʾaṣâbakum vallâhu ḫabîrum bimâ taʿmalûn
- **3:154**: s̱umma ʾanzala ʿalaykum mim baʿdi lgammi ʾamanatan nuʿâsan yagşâ ṭâʾifatam minkum vaṭâʾifatun qad ʾahammathum ʾanfusuhum yaẓunnûna billâhi gayra lḥaqqi ẓanna lcâhiliyyati yaqûlûna hal lanâ mina lʾamri min şayʾin qul ʾinna lʾamra kullahû lillâhi yuḫfûna fî ʾanfusihim mâ lâ yubdûna laka yaqûlûna lav kâna lanâ mina lʾamri şayʾum mâ qutilnâ hâhunâ qul lav kuntum fî buyûtikum labaraza llaẕîna kutiba ʿalayhimu lqatlu ʾilâ mażâciʿihim valiyabtaliya llâhu mâ fî ṣudûrikum valiyumaḥḥiṣa mâ fî qulûbikum vallâhu ʿalîmum biẕâti ṣṣudûr
- **3:155**: ʾinna llaẕîna tavallav minkum yavma ltaqâ lcamʿâni ʾinnamâ stazallahumu şşayṭânu bibaʿżi mâ kasabû valaqad ʿafâ llâhu ʿanhum ʾinna llâha gafûrun ḥalîm
- **3:159**: fabimâ raḥmatim mina llâhi linta lahum valav kunta faẓẓan galîẓa lqalbi lanfażżû min ḥavlika faʿfu ʿanhum vastagfir lahum vaşâvirhum fî lʾamri faʾiẕâ ʿazamta fatavakkal ʿalâ llâhi ʾinna llâha yuḥibbu lmutavakkilîn
- **3:160**: ʾin yanṣurkumu llâhu falâ gâliba lakum vaʾin yaḫẕulkum faman ẕâ llaẕî yanṣurukum mim baʿdihî vaʿalâ llâhi falyatavakkali lmuʾminûn
- **3:165**: ʾavalammâ ʾaṣâbatkum muṣîbatun qad ʾaṣabtum mis̱layhâ qultum ʾannâ hâẕâ qul huva min ʿindi ʾanfusikum ʾinna llâha ʿalâ kulli şayʾin qadîr
- **3:172**: allaẕîna stacâbû lillâhi varrasûli mim baʿdi mâ ʾaṣâbahumu lqarḥu lillaẕîna ʾaḥsanû minhum vattaqav ʾacrun ʿaẓîm
- **3:173**: allaẕîna qâla lahumu nnâsu ʾinna nnâsa qad camaʿû lakum faḫşavhum fazâdahum ʾîmânan vaqâlû ḥasbunâ llâhu vaniʿma lvakîl
- **5:23**: qâla raculâni mina llaẕîna yaḫâfûna ʾanʿama llâhu ʿalayhimâ dḫulû ʿalayhimu lbâba faʾiẕâ daḫaltumûhu faʾinnakum gâlibûna vaʿalâ llâhi fatavakkalû ʾin kuntum muʾminîn
- **6:66**: vakaẕẕaba bihî qavmuka vahuva lḥaqqu qul lastu ʿalaykum bivakîl
- **6:89**: ʾulâʾika llaẕîna ʾâtaynâhumu lkitâba valḥukma vannubuvvata faʾin yakfur bihâ hâʾulâʾi faqad vakkalnâ bihâ qavmal laysû bihâ bikâfirîn
- **6:102**: ẕâlikumu llâhu rabbukum lâ ʾilâha ʾillâ huva ḫâliqu kulli şayʾin faʿbudûhu vahuva ʿalâ kulli şayʾin vakîl
- **6:107**: valav şâʾa llâhu mâ ʾaşrakû vamâ caʿalnâka ʿalayhim ḥafîẓan vamâ ʾanta ʿalayhim bivakîl
- **8:2**: ʾinnamâ lmuʾminûna llaẕîna ʾiẕâ ẕukira llâhu vacilat qulûbuhum vaʾiẕâ tuliyat ʿalayhim ʾâyâtuhû zâdathum ʾîmânan vaʿalâ rabbihim yatavakkalûn
- **10:84**: vaqâla mûsâ yâqavmi ʾin kuntum ʾâmantum billâhi faʿalayhi tavakkalû ʾin kuntum muslimîn
- **10:108**: qul yâʾayyuhâ nnâsu qad câʾakumu lḥaqqu mir rabbikum famani htadâ faʾinnamâ yahtadî linafsihî vaman żalla faʾinnamâ yażillu ʿalayhâ vamâ ʾana ʿalaykum bivakîl
- **12:17**: qâlû yâʾabânâ ʾinnâ ẕahabnâ nastabiqu vataraknâ yûsufa ʿinda matâʿinâ faʾakalahu ẕẕiʾbu vamâ ʾanta bimuʾminil lanâ valav kunnâ ṣâdiqîn
- **12:66**: qâla lan ʾursilahû maʿakum ḥattâ tuʾtûni mavs̱iqam mina llâhi lataʾtunnanî bihî ʾillâ ʾan yuḥâṭa bikum falammâ ʾâtavhu mavs̱iqahum qâla llâhu ʿalâ mâ naqûlu vakîl
- **12:67**: vaqâla yâbaniyya lâ tadḫulû mim bâbin vâḥidin vadḫulû min ʾabvâbim mutafarriqatin vamâ ʾugnî ʿankum mina llâhi min şayʾin ʾini lḥukmu ʾillâ lillâhi ʿalayhi tavakkaltu vaʿalayhi falyatavakkali lmutavakkilûn
- **12:68**: valammâ daḫalû min ḥays̱u ʾamarahum ʾabûhum mâ kâna yugnî ʿanhum mina llâhi min şayʾin ʾillâ ḥâcatan fî nafsi yaʿqûba qażâhâ vaʾinnahû laẕû ʿilmil limâ ʿallamnâhu valâkinna ʾaks̱ara nnâsi lâ yaʿlamûn
- **14:12**: vamâ lanâ ʾallâ natavakkala ʿalâ llâhi vaqad hadânâ subulanâ valanaṣbiranna ʿalâ mâ ʾâẕaytumûnâ vaʿalâ llâhi falyatavakkali lmutavakkilûn
- **17:2**: vaʾâtaynâ mûsâ lkitâba vacaʿalnâhu hudal libanî ʾisrâʾîla ʾallâ tattaḫiẕû min dûnî vakîlâ
- **17:54**: rabbukum ʾaʿlamu bikum ʾin yaşaʾ yarḥamkum ʾav ʾin yaşaʾ yuʿaẕẕibkum vamâ ʾarsalnâka ʿalayhim vakîlâ
- **17:68**: ʾafaʾamintum ʾan yaḫsifa bikum câniba lbarri ʾav yursila ʿalaykum ḥâṣiban s̱umma lâ tacidû lakum vakîlâ
- **25:58**: vatavakkal ʿalâ lḥayyi llaẕî lâ yamûtu vasabbiḥ biḥamdihî vakafâ bihî biẕunûbi ʿibâdihî ḫabîrâ
- **32:11**: qul yatavaffâkum malaku lmavti llaẕî vukkila bikum s̱umma ʾilâ rabbikum turcaʿûn
- **33:3**: vatavakkal ʿalâ llâhi vakafâ billâhi vakîlâ
- **39:41**: ʾinnâ ʾanzalnâ ʿalayka lkitâba linnâsi bilḥaqqi famani htadâ falinafsihî vaman żalla faʾinnamâ yażillu ʿalayhâ vamâ ʾanta ʿalayhim bivakîl
- **39:62**: allâhu ḫâliqu kulli şayʾin vahuva ʿalâ kulli şayʾin vakîl
- **40:28**: vaqâla raculum muʾminum min ʾâli firʿavna yaktumu ʾîmânahû ʾataqtulûna raculan ʾan yaqûla rabbiya llâhu vaqad câʾakum bilbayyinâti mir rabbikum vaʾin yaku kâẕiban faʿalayhi kaẕibuhû vaʾin yaku ṣâdiqan yuṣibkum baʿżu llaẕî yaʿidukum ʾinna llâha lâ yahdî man huva musrifun kaẕẕâb
- **40:38**: vaqâla llaẕî ʾâmana yâqavmi ttabiʿûni ʾahdikum sabîla rraşâd
- **40:39**: yâqavmi ʾinnamâ hâẕihi lḥayâtu ddunyâ matâʿun vaʾinna lʾâḫirata hiya dâru lqarâr
- **40:40**: man ʿamila sayyiʾatan falâ yuczâ ʾillâ mis̱lahâ vaman ʿamila ṣâliḥam min ẕakarin ʾav ʾuns̱â vahuva muʾminun faʾulâʾika yadḫulûna lcannata yurzaqûna fîhâ bigayri ḥisâb
- **40:41**: vayâqavmi mâ lî ʾadʿûkum ʾilâ nnacâti vatadʿûnanî ʾilâ nnâr
- **40:42**: tadʿûnanî liʾakfura billâhi vaʾuşrika bihî mâ laysa lî bihî ʿilmun vaʾana ʾadʿûkum ʾilâ lʿazîzi lgaffâr
- **40:43**: lâ carama ʾannamâ tadʿûnanî ʾilayhi laysa lahû daʿvatun fî ddunyâ valâ fî lʾâḫirati vaʾanna maraddanâ ʾilâ llâhi vaʾanna lmusrifîna hum ʾaṣḥâbu nnâr
- **40:44**: fasataẕkurûna mâ ʾaqûlu lakum vaʾufavviżu ʾamrî ʾilâ llâhi ʾinna llâha baṣîrum bilʿibâd
- **40:45**: favaqâhu llâhu sayyiʾâti mâ makarû vaḥâqa biʾâli firʿavna sûʾu lʿaẕâb
- **64:13**: allâhu lâ ʾilâha ʾillâ huva vaʿalâ llâhi falyatavakkali lmuʾminûn
- **65:3**: vayarzuqhu min ḥays̱u lâ yaḥtasibu vaman yatavakkal ʿalâ llâhi fahuva ḥasbuhû ʾinna llâha bâligu ʾamrihî qad caʿala llâhu likulli şayʾin qadrâ
- **67:29**: qul huva rraḥmânu ʾâmannâ bihî vaʿalayhi tavakkalnâ fasataʿlamûna man huva fî żalâlim mubîn
- **73:9**: rabbu lmaşriqi valmagribi lâ ʾilâha ʾillâ huva fattaḫiẕhu vakîlâ
- **106:4**: allaẕî ʾaṭʿamahum min cûʿin vaʾâmanahum min ḫavf

## Sınırlar

- Kök ve lemma sayımı kelime konumunda tekilleştirilir; segment sayısı ayrıca verilir.
- Bap etiketi fiil ile türemiş isimde ayrı değerlendirilir; etiketler tam eşleştirilir.
- Ayet içi birlikte geçiş yalnız aday bulur; anlam özdeşliği, zorunlu sıra veya nedensellik ispatlamaz.
- Amn kökü bütün geçişlerinde teknik iman terimi değildir; 17:68 kök kesişiminde güvenlik bağlamını içerir.
- 106:4 IV. bap anotasyonunu, 12:17 IV. bap ism-i fâil anotasyonunu gösterir; anlam hükmü bağlam gerektirir.
- Tanzil ayetleri yalnız ayet anahtarıyla eşleştirilir; QAC kelime sırası Tanzil token sırası yerine kullanılmaz.
- Okunuş aktarımı yorum/delil değildir; belirsizlik alanları korunur.
- Bu tarama Uhud tarihini, Kur'an öncesi anlamı veya kavramsal yokluğu kanıtlamaz.

## Kaynak ve yeniden üretim

[Quranic Arabic Corpus](https://corpus.quran.com/download/), QAC v0.4, Copyright (C) 2011 Kais Dukes; özgün telif bloğu `source_notice.txt` içinde korunur.

[Tanzil](https://tanzil.net/docs/download), Uthmani v1.1; bu dosyada ayet metninin kurallı Latin aktarımı kullanılır. Kaynak metin değiştirilmez.

`summary.json`: kaynak ve üretim kodu hash'leri, tam sayımlar, her alt sorgunun bütün konumları.
`occurrences.csv`: üç kökün bütün kök taşıyan segmentleri ve ait oldukları kelimenin segmentleri.
`selected_segments.csv`: kritik ayetlerin tüm segmentleri; `verse_lookup.csv`: w-k-l ayetleri, komşuları ve 3:121–180 bağlamı.

Kaynak      : QAC v0.4 + Tanzil Uthmani v1.1 (yalnız aktarım)
Sayım birimi: kelime konumu | segment | ayet | sûre
Sorgu       : python 08_scripts/analyze_tawakkul_comparison.py
Veri izi    : a1d129238153
Durum       : çalıştırıldı
