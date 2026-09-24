# Okunuş kuralları (Aşama 2a)

Kaynak metin: **Tanzil Uthmani v1.1** (`01_raw/tanzil/quran-uthmani.txt`, sha256 `bf4f57b968d0…`).
Kod: `tezgah/harf.py` (tablolar), `tezgah/okunus.py` (kurallar). Komut: `python -m tezgah okunus 2:3`.

Okunuş bir **aktarımdır, delil değildir**. Kelime sınırı Tanzil'in boşluk tokenıdır; QAC kelime konumu değildir.

**Temel ilke:** Yazıda işaretli olan uygulanır. Yazıda işareti olmayan telaffuz kuralları uygulanmaz.
Üç istisna vardır ve aşağıda açıkça listelenmiştir: ibtidâ ünlüsü, vakf ve lafzatullah.

## 1. Ünsüzler — kök gösterimiyle ortak tablo

Kök gösterimi (`Slw → ṣ-l-v`) ile okunuş aynı tabloyu kullanır. Tablonun tek kaynağı `harf.py`
dosyasıdır; `testler/test_okunus.py` bu belgedeki tablonun koddakiyle birebir aynı olduğunu denetler.
Eşleme ünsüzlerde kayıpsızdır: iki farklı harf aynı Latin karşılığa gitmez.

<!-- UNSUZ_TABLOSU_BASI -->
| Arapça | Latin | harf |
|---|---|---|
| ء | ʾ | hemze |
| ب | b | be |
| ت | t | te |
| ث | s̱ | se |
| ج | c | cim |
| ح | ḥ | ha |
| خ | ḫ | hı |
| د | d | dal |
| ذ | ẕ | zel |
| ر | r | ra |
| ز | z | ze |
| س | s | sin |
| ش | ş | şın |
| ص | ṣ | sad |
| ض | ż | dad |
| ط | ṭ | tı |
| ظ | ẓ | zı |
| ع | ʿ | ayn |
| غ | g | gayn |
| ف | f | fe |
| ق | q | kaf |
| ك | k | kef |
| ل | l | lam |
| م | m | mim |
| ن | n | nun |
| ه | h | he |
| و | v | vav |
| ي | y | ye |
<!-- UNSUZ_TABLOSU_SONU -->

Yazım varyantları: أ إ ؤ ئ ve tatvil üzerindeki hemze (ـٔ) → `ʾ` · ى (ünsüz olarak) → `y` · ة → `t` (vakfta `h`).
Hemze kelime başında da yazılır (`ʾinna`). Bunun sebebi vasl elifiyle (ٱ) başlayan kelimeden ayrımın korunmasıdır.

QAC kökünde hemze `A` harfiyle yazılır; kök gösteriminde de `ʾ` olur (`Amn → ʾ-m-n`).

## 2. Ünlüler

| işaret | Latin | not |
|---|---|---|
| ـَ fetha | a | Türkçe a/e uyumu uygulanmaz (bkz. §5) |
| ـِ kesre | i | |
| ـُ damme | u | |
| ـً ـٍ ـٌ tenvin | an · in · un | |
| fetha + ا / fetha + ى (harekesiz) | â | |
| kesre + ي / ى (harekesiz) | î | |
| damme + و (harekesiz) | û | |
| ـٰ hançerî elif (harf ya da و/ى taşıyıcı üzerinde) | â | صَلَوٰة → `ṣalât…`, عَلَىٰ → `ʿalâ` |
| ۥ küçük vav · ۦ küçük ye · ـۧ küçük üst ye | û · î · î | zamir sılası; vakfta düşer |
| fetha + يْ / وْ | ay · av | ünsüz y/v + sükûn |
| ـْ sükûn | ünlü yok | |
| ـّ şedde | ünsüz iki kez | `ṣṣalâta` |
| ـٓ medde | gösterilmez | uzunluk zaten harften gelir |

## 3. Bağlam kuralları (uygulama sırasıyla)

| # | kural | yazıdaki işaret | örnek (test ayetleri) |
|---|---|---|---|
| 1 | Hurûf-ı mukattaa: harekesiz kelime harf adlarıyla okunur (§3a) | hiç hareke yok | 2:1 `ʾalif lâm mîm`, 20:1 `ṭâ hâ` |
| 2 | Sûre başı besmelesi Tanzil'de ilk ayete önektir; ayrı gösterilir (QAC'ta yok). 95:1 ve 97:1'de önek şeddeyle yazılmıştır (بِّسْمِ) | ilk ayet, 1:1 metni | 2:1 |
| 3 | Vasl elifi ٱ ayet içinde okunmaz | ٱ | 1:1 `bismi llâhi` |
| 4 | **İbtidâ (istisna):** ayet başındaki ٱ şöyle okunur: harf-i tariften önce `a`; vasl elifli isimlerde (iskelet سم بن مر ثن: ٱسْم · ٱبْن, ٱبْنَة · ٱمْرُؤ, ٱمْرَأَة · ٱثْنَان, ٱثْنَتَا/ٱثْنَتَيْن) her zaman `i`; diğer durumlarda (fiil) 3. harf dammeliyse `u`, değilse `i` | ٱ (ünlü yazıda yok) | 2:3 `allaẕîna`, 1:6 `ihdinâ`, 96:1 `iqraʾ`, 16:125 `udʿu`, 4:50 `unẓur` |
| 5 | Kelime içi idgam: harekesiz ve sükûnsuz ünsüzden sonraki harf şeddeliyse, ilk ünsüz yazılmaz | işaretsiz harf + şedde | 1:1 `rraḥmâni`, 30:30 `liddîni`, 9:1 `ʿâhattum` |
| 6 | Harekesiz ve sükûnsuz, arkasından şeddeli harf gelmeyen ünsüz sükûnlu gibi okunur (ihfâ/izhar ayrımı gösterilmez) | işaretsiz harf | 2:3 `yunfiqûn` |
| 7 | Kelimeler arası idgam: kelime şeddeli harfle başlıyorsa önceki kelimenin tenvin n'si veya harekesiz son ünsüzü bu harfe dönüşür; baştaki harf tek yazılır | kelime başında şedde | 107:4 `favaylul lilmuṣallîn` |
| 8 | Ayet başında kelime şeddeli harfle başlıyorsa (önceki ayetle vasl yazımı) harf tek yazılır | ayet başında şedde | 2:245 `man`, 18:38 `lâkinna` |
| 9 | İklab: ۢ / ۭ küçük mim → n ve tenvin n'si `m` olur | ۢ ۭ | 2:33 `ʾambiʾhum`, 2:95 `ʾabadam` |
| 10 | Tenvinden sonraki elif ve ى okunmaz | ًا ًى | 30:30 `ḥanîfan` |
| 11 | ۟ ile işaretli harf hiç okunmaz | ۟ | 2:9 `ʾâmanû` |
| 12 | ۠ ile işaretli elif vaslda okunmaz, vakfta önceki ünlüyü uzatır | ۠ | 2:258 `ʾana`, 33:10 sonu `ẓẓunûnâ` |
| 13 | **Lafzatullah (sözlüksel istisna):** Tanzil Uthmani bu adda hançerî elifi yazmaz. Desen: iki lam (ikincisi şeddeli ve fethalı) + he + son hareke (+ مَّ). Bu desende lam ünlüsü `â` olur. `ٱللَّهْو`, `ٱللَّهَب`, `لَّهُم` eşleşmez | yazıda yok | 1:1 `llâhi` |
| 14 | **Vakf (istisna):** ayet sonunda son kısa ünlü ve tenvin (un/in) düşer, fetha tenvini `â` olur, ة `h` olur, sıla uzunluğu düşer | ayet sonu | 1:1 `rraḥîm`, 2:3 `yunfiqûn` |

Doğrulama (tüm korpus, `testler/test_okunus.py`):
- 6.236 ayetin hepsi bilinmeyen karakter ve belirsiz durum üretmeden okunur.
- Besmele öneki 112 ayette bulunur (114 − 1:1 − 9. sûre).
- Kural 13'ün deseni ayet ayet QAC'ın `{ll~ah` + `{ll~ahum~a` lemma sayısıyla aynıdır.
- İbtidâ (kural 4): ayet başında vasl elifiyle başlayan 54 kelimenin hepsinde araç, QAC'tan bağımsız türetilen ünlüyle aynı sonucu verir. QAC tarafında IMPV + I. bab için 2. kök harfinin gövde harekesi `u` ise `u`, diğer durumlarda (türemiş bab, PERF etken, isim) `i` alınır.
- Kural 4'ün bilinen sınırı: çoğul emirde 3. harfin dammesi çoğul ekinden geliyorsa (yâ ile biten fiiller: ٱمْشُوا۟, ٱقْضُوٓا۟) kural yanlış olarak `u` verir. Bu kelimeler korpusta ayet başında geçmez; ayet içinde vasl elifi okunmadığı için okunuşa etkileri yoktur.
- Mukattaa taraması (kural 1) ham QAC `INL` satırlarıyla ayet, kelime konumu ve harf dizisinde birebir aynıdır (§3a).

## 3a. Hurûf-ı mukattaa

Tanzil'de hiç hareke taşımayan token mukattaa sayılır; her harf adıyla okunur. Medde (ـٓ) gösterilmez.
Adların ilk ünsüzü §1 tablosundan gelir; elifin adı hemzeyle başlar. Kod: `okunus.MUKATTAA_TABLOSU`
(testler bu tabloyu kodla eşitler).

<!-- MUKATTAA_TABLOSU_BASI -->
| harf | ad |
|---|---|
| ا | ʾalif |
| ل | lâm |
| م | mîm |
| ص | ṣâd |
| ر | râ |
| ك | kâf |
| ه | hâ |
| ي | yâ |
| ع | ʿayn |
| ط | ṭâ |
| س | sîn |
| ح | ḥâ |
| ق | qâf |
| ن | nûn |
<!-- MUKATTAA_TABLOSU_SONU -->

Uygulanmayanlar (yazıda işaret yok):
- Harf adları arasındaki idgam ve ihfâ (ör. طسٓمٓ'de sîn'in nun'unun mîm'e idgamı).
- Mukattaanın sonraki ayete vaslı. Her ayet vakfla biter.

Tarama: `python -m tezgah okunus --mukattaa`. Doğrulama ham QAC'tan bağımsız yapılır
(`testler/test_okunus.py`): QAC'ta `INL` etiketli segmentler Tanzil taramasıyla ayet, kelime konumu ve harf
dizisinde birebir karşılaştırılır.

## 3b. Sekte ve durak işaretleri

**Taban dosyada sekte yok.** Tanzil Uthmani v1.1 taban dosyasında (`quran-uthmani.txt`) sekte işareti **yoktur**.
U+06DC (ۜ) orada yalnız 2:245 ve 7:69'da, ص üzerinde geçer ve "sin okunur" anlamındadır (§4). Dosyada U+06D6–06DB
durak işaretlerinin hiçbiri de yoktur.

**Durak işaretli sürüm.** Bu sürüm ayrı bir ham dosyadır: `01_raw/tanzil/quran-uthmani-durak.txt`, taban dosyanın
üzerine yazılmaz. Kaynak adresi:
`https://tanzil.net/pub/download/index.php?marks=true&sajdah=false&rub=false&tatweel=false&quranType=uthmani&outType=txt-2&agree=true`.
Kurulum komutu: `python 08_scripts/fetch_tanzil_marks.py --i-agree-to-tanzil-terms`.

Bu sürüm, parametreler kapalı olsa da rubʿ (U+06DE), secde (U+06E9) ve tatvil (U+0640) ekler.

Denklik kuralı (`okunus.denklik_tokenlari`; betik ve yükleyici aynı işlevi kullanır):
1. Tek başına duran işaret tokenları çıkarılır: U+06D6–06DC, U+06DE, U+06E9.
2. Kalan tokenlardan U+06D6–06DB, U+06DE, U+06E9 ve U+0640 çıkarılır.
3. Kelimeye bitişik U+06DC korunur (2:245 ve 7:69'da ص üzerinde, tabanda da vardır).

Bu işlemden sonra 6.236 ayetin 6.236'sı taban dosyayla aynı olmalıdır; olmazsa dosya yazılmaz ya da yüklenmez.
Manifest'e şunlar işlenir: kaynak adresi, bayt sayısı, sha256, kullanıcının ölçtüğü sha256 ve karşılaştırma
sonucu. Tanzil dosyayı dinamik üretebileceği için sha256 farkı rapor edilir, iş durdurulmaz. Yükleyici her
açılışta sha256'yı manifest'le, metni de tabanla yeniden denetler.

**Okunuşta kullanım.**
- **Sekte:** Varsayılan olarak yalnız sekte kullanılır. Sekte, yalnız **tek başına duran** U+06DC'dir. Kelimeden sonra `[sekte]` yazılır. Sekteli kelimede vakf
  kuralları uygulanır; o kelimeden sonrasına kelimeler arası idgam yapılmaz.
- **Diğer durak işaretleri:** Varsayılan olarak gösterilmez. `--durak` verilirse ayrı bir sütunda
  "geleneksel — yorum içerebilir" etiketiyle gösterilir. Durak işaretleri, metnin nasıl bölüneceğine dair
  geleneksel bir yorumdur ve veri değildir.

| kod | işaret | ad |
|---|---|---|
| U+06D6 | ۖ | ṣlâ (vasl evlâ) |
| U+06D7 | ۗ | qlâ (vakf evlâ) |
| U+06D8 | ۘ | mîm (vakf lâzım) |
| U+06D9 | ۙ | lâ (vakf yok) |
| U+06DA | ۚ | cîm (vakf câiz) |
| U+06DB | ۛ | muʿânaqa |
| U+06DC | ۜ | sekte (tek başına duruyorsa; kelimeye bitişikse ص üzerindeki sin işaretidir) |
| U+06DE | ۞ | rubʿ — kullanılmaz, gösterilmez |
| U+06E9 | ۩ | secde — kullanılmaz, gösterilmez |

**Durum (24.09.2026):** Kurulu. Bu oturumdan `tanzil.net` 403 döndürdüğü için dosyayı kullanıcı yükledi ve dosya
`--dosyadan` ile aynı denetimlerden geçirilerek kabul edildi. Manifest'teki `edinim` alanı bunu kaydeder.
- sha256 `7f30c647331a…`: kullanıcının ölçümüyle aynı.
- Denklik: 6.236 ayetin 6.236'sı taban dosyayla aynı.
- İşaret sayıları: U+06D6 1.682 · U+06D7 603 · U+06D8 22 · U+06D9 68 · U+06DA 1.972 · U+06DB 12 · U+06DC 7
  (5'i tek başına sekte, 2'si ص üzerinde) · U+06DE 199 · U+06E9 15.
- Eklenen tatvil: 6.036.

**Sekte yerleri.** Tek başına duran sekte beş yerde bulunur: 18:1, 36:52, 69:28, 75:27, 83:14. Gerçek dosyada ölçüldü ve
`test_durak.py` bunu denetler.
- **69:28** (`mâ ʾagnâ ʿannî mâliyah`, 69:29 `halaka` ile devam eder): Hafs'ta sekte burada **isteğe bağlıdır**.
  Ayetler birleştirilerek okunduğunda ya sekte yapılır ya da he harfi sonraki he'ye idgam edilir; iki okuyuş
  da geçerli sayılır (geleneksel okuma bilgisi — yorum içerebilir). Okunuş her ayeti vakfla bitirdiği için
  69:28'in harfleri değişmez; `[sekte]` yalnız durak işaretli sürümün işaretini gösterir.
- **75:27 ve 83:14** (`man râq`, `bal râna`): Tanzil sükûn yazar ve sonraki harfte şedde yoktur, bu yüzden
  idgam uygulanmaz. Bu sonuç sekte işaretinden değil yazımdan gelir.

## 4. Osmanî özel işaretler (U+06DC–06ED ve diğerleri)

| kod | işaret | işlem | örnek |
|---|---|---|---|
| U+0654 | ـٔ tatvil üstü hemze | `ʾ` + hareke | 2:4 `vabilʾâḫirati` |
| U+0640 | ـ tatvil | taşıyıcı; kendisi okunmaz | |
| U+06DC | ۜ küçük üst sin | ص harfi `s` okunur | 2:245 `vayabsuṭu` |
| U+06DF | ۟ yuvarlak sıfır | harf okunmaz | 2:9 `ʾâmanû` |
| U+06E0 | ۠ dikdörtgen sıfır | vaslda okunmaz, vakfta okunur | 2:258 `ʾana` |
| U+06E2 | ۢ küçük üst mim | iklab (n → m) | 2:33 `ʾambiʾhum` |
| U+06E3 | ۣ küçük alt sin | gösterilmez; ص okunur | 52:37 `lmuṣayṭirûn` |
| U+06E5 / 06E6 | ۥ ۦ | sıla: û / î | 9:1 `varasûlihî` |
| U+06E7 | ۧ küçük üst ye | î | 2:124 `ʾibrâhîma` |
| U+06E8 | ۨ küçük üst nun | ünsüz `n` | 21:88 `nuncî` |
| U+06EA | ۪ imâle | sonraki `â` → `ê` | 11:41 `macrêhâ` |
| U+06EB | ۫ işmam | gösterilmez (işitilmez) | 12:11 `taʾmannâ` |
| U+06EC | ۬ teshil | teshilli hemze `ʾa` yazılır | 41:44 `ʾaʾaʿcamiyyun` |
| U+06ED | ۭ küçük alt mim | iklab (tenvin n → m) | |

Bu dosyada bulunmayan bir karakter hata üretir; sessizce atlanmaz.

## 5. Bilinçli olarak uygulanmayan kurallar

| kural | neden |
|---|---|
| Türkçe a/e (kalın/ince) ünlü uyumu (`ellezîne`) | Harften kesin olarak türetilemez, istisnaları vardır. Fetha her yerde `a` yazılır, böylece denetlenebilir kalır |
| Vasl elifinden önce uzun ünlünün kısalması (`fî lʾarḍi` → `fi l-arḍ`) | Yazıda işareti yok; harf korunur |
| Tenvinden sonra vasl elifinde yardımcı kesre (`ḫayrun hbiṭû` → `ḫayruni hbiṭû`) | Yazıda işareti yok |
| İhfâ, ğunne, kalkale, med süreleri | Yazıda ayrı işareti yok ya da uzunluk derecesi Latin harfle gösterilmez |
| Harf-i tarif ile isim arasına tire (`l-qayyimu`) | Kelime Tanzil tokenı olarak bütün tutulur |
| Sûre ve ayet arası vasl (ayet sonunda durmadan okuma) | Her ayet vakfla biter |

## 6. Lemma okunuşu (bağlamsız okuma)

Tarama listelerinde iki okunuş sütunu vardır. İkisi aynı motoru ve aynı harf tablosunu (§1) kullanır:

| sütun | kaynak | nasıl üretilir |
|---|---|---|
| **biçim (ayet içinde okunuş)** | Tanzil Uthmani v1.1 + `tanzil_qac_alignment.csv` | Ayet bütün olarak okunur (§3: vasl, idgam, iklab, ayet sonu vakf). QAC kelime konumu hizalamayla Tanzil tokenına bağlanır; o tokenın okunuşu gösterilir (2:3:5 `ṣṣalâta`). Ayet görünümündeki okunuşla aynıdır. |
| **lemma (okunuş)** | QAC v0.4 lemma alanı (Buckwalter) | Lemma tek başına okunur (bu bölüm): `Salaw`p` → `ṣalât`. |

Hizalama farkı (§3 dışı, `okuma.hizala`): Tanzil↔QAC hizalaması bir kelimede farklıysa okunuşun yanına not düşülür: `[not: Tanzil↔QAC yazım farkı]`, `[not: 2 Tanzil tokenı = 1 QAC kelimesi]`, `[not: Tanzil↔QAC hizalanamadı]`. Tüm korpusta bu notu alan kelime konumu 7'dir (3 yazım farkı, 4 birleşik token); hizalanamayan yoktur. `etiket` ve `kalip` listelerinde okunuş segmentin değil, segmentin içinde geçtiği kelime konumunundur. Buckwalter biçim ve lemma yalnız `--bw` ile, ek sütun olarak gösterilir.

Lemma okunuşunun kuralları (`okunus.lemma_okunusu`):

| # | kural | örnek (QAC → okunuş) |
|---|---|---|
| 1 | **Bağlamsız:** komşu kelime yoktur. Kelimeler arası vasl ve idgam uygulanmaz; kelime ibtidâ ile başlar (§3 kural 4): vasl elifi ibtidâ ünlüsüyle okunur | `{som` → `ism`, `{l~a*iY` → `allaẕî` |
| 2 | **Yazıldığı harekelerle:** QAC lemması hangi harekeyi taşıyorsa o okunur; eksik hareke eklenmez. İsim lemmaları durum eki taşımaz, fiil lemmaları son ünlüsüyle yazılır | `kita`b` → `kitâb`, `qaAla` → `qâla`, `maE2` → `maʿ (2)` |
| 3 | **Vakf biçimi kullanılmaz:** ة `t` kalır. Vakftaki `h` sözlük başlığında kullanılmaz; ayet sonundaki biçim sütunu ise vakfla okunur (§3) | `Salaw`p` → `ṣalât` (`ṣalâh` değil) |
| 4 | **Tenvin durum ekidir, düşer:** zamme/kesre tenvini düşer; ى üzerindeki fetha tenvini vakftaki gibi `â` olur; ـًا sözcükseldir ve kalır. QAC'ta 4.832 lemmanın 24'ü tenvinlidir | `>abN` → `ʾab`, `hudFY` → `hudâ`, `<i*FA` → `ʾiẕan`, `>abadFA` → `ʾabadan` |
| 5 | **Kelime başı hemze yazılır** (§1: `ʾinna`). Vasl elifli lemmadan ayrım böyle korunur | `<insa`n` → `ʾinsân`, `{som` → `ism` |
| 6 | **Kelime başı آ:** QAC bunu "elif + medde" (`A^`) diye, Tanzil ise ءَا diye yazar. Lemma Tanzil yazımına çevrilir: `ʾâ` | `A^dam` → `ʾâdam` |
| 7 | **Lafzatullah** (§3 kuralının lemma karşılığı): QAC lemması harekesizdir; uzun â doğrudan verilir | `{ll~ah` → `allâh`, `{ll~ahum~a` → `allâhumma` |
| 8 | **Kelime başı şedde** (QAC idgamlı biçimi yazar): ayet başındaki gibi tek yazılır | `m~ula`quwA` → `mulâqû` |
| 9 | **Sondaki iklab işareti** (`[`) yok sayılır: iklab sonraki b'ye bağlıdır, bağlamsız okumada sonraki kelime yoktur. Kelime içindeki iklab uygulanır | `nasofaEF[` → `nasfaʿan`, `>an[ba>a` → `ʾambaʾa` |
| 10 | **Eşsesli lemma numarası** (QAC `EaSaA` / `EaSaA2`) okunuşa katılmaz, parantezle eklenir | `EaSaA2` → `ʿaṣâ (2)` |

QAC genişletilmiş Buckwalter işaretlerinin lemma karşılıkları (Tanzil'in aynı işaretleri; §4): `^` medde U+0653, `#` üst hemze U+0654, `[` küçük üst mim U+06E2, `,` küçük vav U+06E5, `.` küçük ye U+06E6, `@` yuvarlak sıfır U+06DF.

Belirsiz kalan (`okunus.lemma_okunusu(...).belirsiz`) 6 lemma vardır. Hepsinde çoğul vavından ya da ئ'den sonraki elif QAC lemmasında okunmaz işareti (`@`) olmadan yazılmıştır; motor bu elifi uzatma saymaz ve okunuş doğru çıkar: `naAkisuwA` → `nâkisû`, `miA}ap` → `miʾat`. Bilinmeyen karakter hata üretir; 4.832 lemmanın hepsi hatasız okunur (`testler/test_okunus_liste.py`).
