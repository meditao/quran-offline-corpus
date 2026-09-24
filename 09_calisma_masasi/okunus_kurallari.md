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
üzerine yazılmaz. Kurulum komutu `python 08_scripts/fetch_tanzil_marks.py --i-agree-to-tanzil-terms`; kaynak
Tanzil'dir (`marks=true`). Betik dosyayı ancak şu koşulla yazar: durak işaretleri (U+06D6–06DC) çıkarılınca
6.236 ayetin hepsi taban dosyayla birebir aynı olmalı. Kaynak adresi, bayt sayısı ve sha256 `manifest.local.json`'a
işlenir. Yükleyici her açılışta sha256'yı manifest'le ve metni tabanla yeniden denetler.

**Okunuşta kullanım.**
- **Sekte:** Varsayılan olarak yalnız sekte kullanılır. Kelimeden sonra `[sekte]` yazılır. Sekteli kelimede vakf
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
| U+06DC | ۜ | sekte (ص üzerinde değilse) |

**Durum (24.09.2026):** Dosya kurulu değil. Oturumun ağ politikası `tanzil.net` adresini reddetti (403).
Kurulana kadar sekte gösterilmez. Gerçek dosyayı sınayan test (`test_durak.py`) atlanır. Mantık, sentetik
dosyayla sınanır.

**Sekteye bağlı ayetler.** Sekte yerleri olarak bilinen yerler 18:1, 36:52, 75:27 ve 83:14'tür. Taban dosyada
buralarda işaret yoktur.
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
| Sekte (18:1, 36:52, 75:27, 83:14) | Tanzil v1.1 dosyasında işareti yok (§3b) |
