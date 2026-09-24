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
| 1 | Hurûf-ı mukattaa: harekesiz kelime harf adlarıyla okunur | hiç hareke yok | 2:1 `ʾalif lâm mîm`, 20:1 `ṭâ hâ` |
| 2 | Sûre başı besmelesi Tanzil'de ilk ayete önektir; ayrı gösterilir (QAC'ta yok). 95:1 ve 97:1'de önek şeddeyle yazılmıştır (بِّسْمِ) | ilk ayet, 1:1 metni | 2:1 |
| 3 | Vasl elifi ٱ ayet içinde okunmaz | ٱ | 1:1 `bismi llâhi` |
| 4 | **İbtidâ (istisna):** ayet başındaki ٱ, harf-i tariften önce `a`, diğer durumlarda 3. harf dammeliyse `u`, değilse `i` olarak okunur | ٱ (ünlü yazıda yok) | 2:3 `allaẕîna` |
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
