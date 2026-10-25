# KUR'AN KAVRAM ANALİZİ — ÂLİM (Ankebût 29:43 *el-ʿâlimûn*)

**Sürüm:** v1 — nihai kart  
**Kayıt tarihi:** 25 Ekim 2026  
**Durum:** Kullanıcının "nihai sonucu kaydet" talimatıyla hazırlandı; birleştirme (merge) kullanıcı incelemesine bağlıdır.  
**Yöntem:** [Kur'an Analiz Protokolü v2.4](../../06_methodology/analiz_protokolu.md). Kullanıcının verdiği "Genişletilmiş Izutsu Temelli Kur'an Semantik Analiz Protokolü v0.1" taslağından iddia etiketleri ve lafzî/açıklamalı çift çeviri ödünç alındı (§11); derecelendirme v2.4'ün iki eksenli sistemiyle yapıldı.  
**Kapsam:** *ʿâlim* lemmasının bütün geçişleri, 29:43'teki kullanımı ve onu tanımlayan bağlam. ʿ-l-m kökünün tamamı (854 kelime konumu) sınıflandırılmadı; bu kart bir "ilim" kavram kartı değildir.  
**Mekanik döküm:** [generated/alim_29_43/report.md](../generated/alim_29_43/report.md) — `python 08_scripts/analyze_alim_29_43.py`

```text
Kaynak      : depo QAC v0.4 (hash a1d129…) + Tanzil Uthmani v1.1 (yalnız ayet metni ve okunuş aktarımı)
Sayım birimi: kelime konumu | ayet | sûre
Sorgu       : python 08_scripts/analyze_alim_29_43.py; python -m tezgah sayim --kok Elm; python -m tezgah sayim --kok Eql; python -m tezgah dagilim --kok Elm --gore lemma --bw; python -m tezgah dagilim --kok Eql --gore tur
Klasik      : asl + isaret + ayet çalıştırıldı (Elm, Eql), anlam→dayanak tablosu yazıldı (§8); Lane kok Elm, Eql; Sâmî kok Elm, Eql
Durum       : çalıştırıldı
```

**İddia etiketleri:** [M] metin verisi · [D] dilsel çıkarım · [T] tarihsel sözlük (hipotez) · [Y] yorum · [B] bilimsel çağrışım · [R] rivayet/sonraki gelenek.

---

## 1. Araştırma sorusu

Ankebût 29:43 *ve mâ yaʿqiluhâ ʾillâ lʿâlimûn* ("onları bilenlerden başkası kavramaz") cümlesindeki "bilenler" kimdir ve neyi bilirler? Bu bir zümre adı (din âlimleri, bilim insanları) mıdır, yoksa bir nitelik mi?

**Karantina varsayımları:**
- K1 — Kullanıcı sûre adını yazmadı; "43. ayet" Ankebût 43 olarak alındı (önceki çalışma Ankebût 10 idi; *ʿâlim* kelimesi 29:43'te geçiyor). → bağlamla kabul edildi.
- K2 — 30:22'nin "bilenler" (*ʿâlimîn*) okunuşu. → **açık** (§3.4); sonuç ona dayanmıyor.

## 2. Aşama 1 — kök, lemma ve sayımlar [M]

| sorgu | kelime konumu | ayet | sûre |
|---|---:|---:|---:|
| ʿ-l-m kökü (`Elm`) | 854 | 728 | 85 |
| ʿ-q-l kökü (`Eql`) | 49 | 49 | 30 |

ʿ-l-m lemma dağılımı (kelime konumu): *ʿalima* 382 · *ʿalîm* 163 · *ʿilm* 105 · *ʿâlamîn* 73 · *ʾaʿlam* 49 · *ʿallama* 41 · **ʿâlim 18** · *maʿlûm* 11 · *ʿallâm* 4 · *ʾaʿlâm* 2 · *maʿlûmât* 2 · *yataʿallamu* 2 · *ʿalâmât* 1 · *muʿallam* 1. Kök toplamı aranan kelimenin sayısı değildir.

### 2.1 *ʿâlim* (ism-i fâil, "bilme işini taşıyan") — 18 kelime konumu

| atıf (elle inceleme) | kelime konumu | yerler |
|---|---:|---|
| Allah | 15 | 13'ü *ʿâlimu'l-gayb(i ve'ş-şehâde)*: 6:73, 9:94, 9:105, 13:9, 23:92, 32:6, 34:3, 35:38, 39:46, 59:22, 62:8, 64:18, 72:26; ayrıca 21:51, 21:81 (*kunnâ … ʿâlimîn*) |
| insan | 3 | 12:44 (nesneli, olumsuz), 29:43 (nesnesiz), 30:22 (nesnesiz; okunuş açık, §3.4) |

### 2.2 İnsan için *ʿalîm* ve *ʿulemâʾ*

QAC *ʿulemâʾ* çoğulunu *ʿalîm* lemmasına bağlar: 26:197 (*ʿulamâʾu banî ʾisrâʾîl*), 35:28. Elle incelenen insan kullanımları: "bilgin sihirbaz" 7:109, 7:112, 10:79, 26:34, 26:37; Yûsuf'un kendisi 12:55 (*ḥafîẓun ʿalîm*); oğul müjdesi 15:53, 51:28; *ʿulemâʾ* 26:197, 35:28. 12:76 (*vafavqa kulli ẕî ʿilmin ʿalîm*) tartışmalıdır (insan mı Allah mı); ayrı tutuldu.

### 2.3 ʿ-q-l

49 kelime konumunun 49'u fiildir (48 muzâri, 1 mâzî); kökün isim biçimi QAC'ta yoktur [M]. Açık nesne zamiri taşıyan yalnız iki fiil vardır: **2:75** *ʿaqalûhu* ("onu kavradılar") ve **29:43** *yaʿqiluhâ* ("onları kavrar").

## 3. Aşama 2 — sentaks ve kalıplar [M]

### 3.1 29:43'ün yapısı

- *tilka lʾams̱âlu*: uzak işaret + belirli çoğul "o misaller". Aynı açılış Kur'an'da iki yerde: **29:43, 59:21**. 59:21'de tek bir misalden (dağ) sonra gelir; çoğul *ams̱âl* burada Kur'an'ın misallerini genel olarak gösterebilir [D].
- *nażribuhâ linnâsi*: "insanlar için ortaya koyarız" — muzâri (süreklilik), muhatap bütün insanlar. Mesel + ḍ-r-b + nâs aynı ayette **9 ayette** geçer: 13:17, 14:25, 22:73, 24:35, 29:43, 30:58, 39:27, 47:3, 59:21. Amaç cümleleri: 14:25, 39:27 *laʿallahum yataẕakkarûn*; 59:21 *laʿallahum yatafakkarûn*. Sınırlama (*mâ … ʾillâ*) yalnız 29:43'te.
- *vamâ yaʿqiluhâ ʾillâ lʿâlimûn*: *mâ … ʾillâ* sınırlama kalıbı = "yalnızca". Mantığı tek yönlüdür: kavrayan herkes bilenlerdendir; her bilenin kavradığı söylenmez [D].
- *lʿâlimûn*: belirli, çoğul, nesnesiz ism-i fâil. Neyi bildiği bağlamdan belirlenmelidir.

### 3.2 Ankebût'ta aynı kalıp

*mâ … ʾillâ* + belirli çoğul ism-i fâil sûrede üç kez: **29:43** (*ʾillâ lʿâlimûn*), **29:47** (*vamâ yacḥadu biʾâyâtinâ ʾillâ lkâfirûn*), **29:49** (*… ʾillâ ẓẓâlimûn*). 29:47 ve 29:49'da kalıp bir kurumu değil bir insan tipini adlandırır; aynı yapıdaki *lʿâlimûn* için en doğal okuma da tip okumasıdır [D].

### 3.3 Nesneli ve nesnesiz kullanım

İnsan için *ʿâlim*'in tek nesneli kullanımı 12:44: *vamâ naḥnu bitaʾvîli lʾaḥlâmi biʿâlimîn* — "biz rüya yorumunu bilenler değiliz" (konuşan: hükümdarın meclisi; muhatap: hükümdar). Bilginin alanı açıkça yazılmıştır. Nesnesiz insan kullanımları (29:43, 30:22) bağlamla doldurulur.

### 3.4 30:22 ve ünsüz iskeleti

*ʿâlimîn* (bilenler) ile *ʿâlamîn* (âlemler) aynı ünsüz iskeletini (`Elmyn`) taşır: iskelet *ʿâlim*'in 4 kelime konumunda (12:44, 21:51, 21:81, 30:22) ve *ʿâlamîn*'in 73 kelime konumunda ortaktır [M]. 12:44, 21:51 ve 21:81'de sentaks "bilen" okunuşunu zorlar; 30:22'de (*laʾâyâtin lilʿâlimîn*) iki okunuş da anlamlıdır. QAC ve Tanzil Hafs okunuşunu izler. Kurtubî kesreli okunuşu ("bilenler için") Hafs'a nispet eder [R; [Kurtubî, Rûm 30:22](https://quran.ksu.edu.sa/tafseer/qortobi/sura30-aya22.html)]; öteki okuyuşların ayrıntısı bu çalışmada doğrulanmadı. Bu yüzden 30:22 destek verisi olarak düşük ağırlıklıdır.

## 4. Aşama 3 — bağlam ve Kur'an içi ağ

### 4.1 Birim: 29:41–44

Sınır gerekçesi [D]: 29:40 helak edilen kavimlerin anlatısını *fakullan ʾaḫaẕnâ biẕanbihî* ile kapatır; 29:41 onların ortak hatasını bir misalle toplar; 29:45 Peygamber'e doğrudan emirle (*utlu*) yeni birim açar.

### 4.2 Bağlam "bilenler"i tanımlıyor

1. **29:41 *lav kânû yaʿlamûn* ("bir bilselerdi").** 43'teki bilenlerin karşı tipi burada. Bu kişiler örümcek ağının çürük olduğunu bilir; bilmedikleri, kendi dayanaklarının da öyle olduğudur. Misali kavratan bilgi imge hakkında değil, hedef (Allah'tan başka dayanaklar) hakkındadır [D].
2. **Kalıbın bütün geçişleri.** *lav kânû yaʿlamûn* ayet sonunda, nesnesiz **7 ayette** geçer: 2:102, 2:103, 16:41, 29:41, 29:64, 39:26, 68:33 [M]. Yedisinde de eksik bilgi bir şeyin gerçek değeridir: 2:102 *labiʾsa mâ şarav* (ne kötü sattılar), 2:103 *ḫayr*, 16:41 ve 39:26 ve 68:33 *ʾakbar*, 29:41 *ʾavhan*, 29:64 *lahiya lḥayavân* [D]. **Sınır:** bu bir kalıptır; doğal olarak değer cümlelerinin ardından gelir. 7/7 oranı yedi bağımsız tanık gibi okunmaz; kalıbın içeriğini gösterir.
3. **Bilgiye sahip olmak ≠ bilmek.** 2:102 aynı ayette *valaqad ʿalimû* ("andolsun bildiler") ve *lav kânû yaʿlamûn* ("bir bilselerdi") der [M]. 29:63'te müşrikler yağmuru indirenin Allah olduğunu söyler; ayet *bal ʾaks̱aruhum lâ yaʿqilûn* ile biter [M].
4. **Sûre içinde şirk bir bilgi hatası olarak:** 29:8 *mâ laysa laka bihî ʿilm* ("hakkında bilgin olmayan şey"); 29:41 velî edinmeyi bilgi eksikliğiyle bitirir [M + D].
5. **Üç işaret, üç muhatap:** 29:35 (Lût kavminin kalıntısı) *liqavmin yaʿqilûn*; 29:43 (misaller) *lʿâlimûn*; 29:44 (hak ile yaratılış) *lilmuʾminîn* [M]. Rûm 30:21–24'te de işaretler farklı muhataplara bağlanır: *yatafakkarûn* (30:21), *ʿâlimîn* (30:22), *yasmaʿûn* (30:23), *yaʿqilûn* (30:24).
6. **ʿilm ↔ ẓann:** ʿilm ismi ile ẓ-n-n kökü **4 ayette** birlikte: 4:157, 6:148, 45:24, 53:28; çerçeve "onların bu konuda bilgisi yok, yalnız zanna uyarlar" [M].
7. ***ellezîne ʾûtû lʿilm* ("kendilerine ilim verilenler"):** **9 ayet** — 16:27, 17:107, 22:54, 28:80, 29:49, 30:56, 34:6, 47:16, 58:11 [M]. Dokuzunda da bu kişiler gerçeği tanıyan taraftadır.

## 5. Kritik ayetler

Etiketler protokol Aşama 4b'ye göredir: **kanıtlayıcı** · **yalnız uyumlu** · **karşı/baskı noktası**. Okunuş, depo okunuş motorunun Tanzil'den ürettiği aktarımdır.

**29:41 — kanıtlayıcı** (bilenlerin neyi bildiğini belirler)  
مَثَلُ ٱلَّذِينَ ٱتَّخَذُوا۟ مِن دُونِ ٱللَّهِ أَوْلِيَآءَ كَمَثَلِ ٱلْعَنكَبُوتِ ٱتَّخَذَتْ بَيْتًا وَإِنَّ أَوْهَنَ ٱلْبُيُوتِ لَبَيْتُ ٱلْعَنكَبُوتِ لَوْ كَانُوا۟ يَعْلَمُونَ  
*mas̱alu llaẕîna ttaḫaẕû min dûni llâhi ʾavliyâʾa kamas̱ali lʿankabûti ttaḫaẕat baytan vaʾinna ʾavhana lbuyûti labaytu lʿankabûti lav kânû yaʿlamûn*  
"Allah'ın berisinden velîler (dayanak, koruyucu) edinenlerin durumu, bir ev edinen örümceğin durumu gibidir. Evlerin en çürüğü şüphesiz örümceğin evidir — bir bilselerdi."

**29:42 — yalnız uyumlu**  
إِنَّ ٱللَّهَ يَعْلَمُ مَا يَدْعُونَ مِن دُونِهِۦ مِن شَىْءٍ وَهُوَ ٱلْعَزِيزُ ٱلْحَكِيمُ  
*ʾinna llâha yaʿlamu mâ yadʿûna min dûnihî min şayʾin vahuva lʿazîzu lḥakîm*  
"Allah, O'nun berisinden çağırdıkları her ne varsa bilir; O azîzdir, hakîmdir."

**29:43 — incelenen ayet**  
وَتِلْكَ ٱلْأَمْثَٰلُ نَضْرِبُهَا لِلنَّاسِ وَمَا يَعْقِلُهَآ إِلَّا ٱلْعَٰلِمُونَ  
*vatilka lʾams̱âlu nażribuhâ linnâsi vamâ yaʿqiluhâ ʾillâ lʿâlimûn*  
"İşte o misaller; onları insanlar için ortaya koyarız. Onları bilenlerden başkası kavramaz."

**29:44 — yalnız uyumlu** (ayrı muhatap: mü'minler)  
خَلَقَ ٱللَّهُ ٱلسَّمَٰوَٰتِ وَٱلْأَرْضَ بِٱلْحَقِّ إِنَّ فِى ذَٰلِكَ لَـَٔايَةً لِّلْمُؤْمِنِينَ  
*ḫalaqa llâhu ssamâvâti valʾarża bilḥaqqi ʾinna fî ẕâlika laʾâyatal lilmuʾminîn*  
"Allah gökleri ve yeri hak ile yarattı; bunda mü'minler (güvenip bağlananlar) için bir işaret vardır."

**29:64 — kanıtlayıcı** (aynı sûrede ikinci "bir bilselerdi": değer tartısı)  
وَمَا هَٰذِهِ ٱلْحَيَوٰةُ ٱلدُّنْيَآ إِلَّا لَهْوٌ وَلَعِبٌ وَإِنَّ ٱلدَّارَ ٱلْـَٔاخِرَةَ لَهِىَ ٱلْحَيَوَانُ لَوْ كَانُوا۟ يَعْلَمُونَ  
*vamâ hâẕihi lḥayâtu ddunyâ ʾillâ lahvun valaʿibun vaʾinna ddâra lʾâḫirata lahiya lḥayavânu lav kânû yaʿlamûn*  
"Bu dünya hayatı oyun ve eğlenceden başka bir şey değildir; ahiret yurdu ise asıl hayattır — bir bilselerdi."

**29:63 — kanıtlayıcı** (bilgiyi söylemek ≠ akletmek)  
وَلَئِن سَأَلْتَهُم مَّن نَّزَّلَ مِنَ ٱلسَّمَآءِ مَآءً فَأَحْيَا بِهِ ٱلْأَرْضَ مِنۢ بَعْدِ مَوْتِهَا لَيَقُولُنَّ ٱللَّهُ قُلِ ٱلْحَمْدُ لِلَّهِ بَلْ أَكْثَرُهُمْ لَا يَعْقِلُونَ  
*valaʾin saʾaltahum man nazzala mina ssamâʾi mâʾan faʾaḥyâ bihi lʾarża mim baʿdi mavtihâ layaqûlunna llâhu quli lḥamdu lillâhi bal ʾaks̱aruhum lâ yaʿqilûn*  
"Onlara 'gökten su indirip onunla ölümünden sonra yeri dirilten kim?' diye sorsan 'Allah' derler. De ki: hamd Allah'a. Ama çoğu akletmez."

**2:102 (son kısmı) — kanıtlayıcı** (iki düzeyli bilme)  
… وَلَقَدْ عَلِمُوا۟ لَمَنِ ٱشْتَرَىٰهُ مَا لَهُۥ فِى ٱلْـَٔاخِرَةِ مِنْ خَلَٰقٍ وَلَبِئْسَ مَا شَرَوْا۟ بِهِۦٓ أَنفُسَهُمْ لَوْ كَانُوا۟ يَعْلَمُونَ  
*… valaqad ʿalimû lamani ştarâhu mâ lahû fî lʾâḫirati min ḫalâqin valabiʾsa mâ şarav bihî ʾanfusahum lav kânû yaʿlamûn*  
"… Andolsun, onu satın alanın ahirette bir payı olmadığını bildiler; karşılığında kendilerini sattıkları şey ne kötüdür — bir bilselerdi." (Tam ayet: mekanik dökümde `verse_lookup.csv`.)

**2:75 — karşı/baskı noktası** (kavrayış doğru davranışı garanti etmez)  
أَفَتَطْمَعُونَ أَن يُؤْمِنُوا۟ لَكُمْ وَقَدْ كَانَ فَرِيقٌ مِّنْهُمْ يَسْمَعُونَ كَلَٰمَ ٱللَّهِ ثُمَّ يُحَرِّفُونَهُۥ مِنۢ بَعْدِ مَا عَقَلُوهُ وَهُمْ يَعْلَمُونَ  
*ʾafataṭmaʿûna ʾan yuʾminû lakum vaqad kâna farîqum minhum yasmaʿûna kalâma llâhi s̱umma yuḥarrifûnahû mim baʿdi mâ ʿaqalûhu vahum yaʿlamûn*  
"Size inanacaklarını mı umuyorsunuz? Oysa içlerinden bir grup Allah'ın sözünü dinler, sonra onu kavradıktan sonra bile bile çarpıtırdı."

**12:44 — kanıtlayıcı** (kelime düzeyi: alan uzmanlığı; dinî olmayan kullanım tanığı)  
قَالُوٓا۟ أَضْغَٰثُ أَحْلَٰمٍ وَمَا نَحْنُ بِتَأْوِيلِ ٱلْأَحْلَٰمِ بِعَٰلِمِينَ  
*qâlû ʾażgâs̱u ʾaḥlâmin vamâ naḥnu bitaʾvîli lʾaḥlâmi biʿâlimîn*  
"Karışık düşler, dediler; biz düşlerin yorumunu bilenler değiliz."

**30:7 — karşı/baskı noktası** (bilim-zümresi okumasına sınır)  
يَعْلَمُونَ ظَٰهِرًا مِّنَ ٱلْحَيَوٰةِ ٱلدُّنْيَا وَهُمْ عَنِ ٱلْـَٔاخِرَةِ هُمْ غَٰفِلُونَ  
*yaʿlamûna ẓâhiram mina lḥayâti ddunyâ vahum ʿani lʾâḫirati hum gâfilûn*  
"Dünya hayatının görünen yüzünü bilirler; ahiretten ise gafildirler."

**30:22 — yalnız uyumlu** (okunuş açık, §3.4)  
وَمِنْ ءَايَٰتِهِۦ خَلْقُ ٱلسَّمَٰوَٰتِ وَٱلْأَرْضِ وَٱخْتِلَٰفُ أَلْسِنَتِكُمْ وَأَلْوَٰنِكُمْ إِنَّ فِى ذَٰلِكَ لَـَٔايَٰتٍ لِّلْعَٰلِمِينَ  
*vamin ʾâyâtihî ḫalqu ssamâvâti valʾarżi vaḫtilâfu ʾalsinatikum vaʾalvânikum ʾinna fî ẕâlika laʾâyâtil lilʿâlimîn*  
"Göklerin ve yerin yaratılışı, dillerinizin ve renklerinizin farklılığı O'nun işaretlerindendir; bunda bilenler için işaretler vardır."

**35:28 — yalnız uyumlu** (doğa çeşitliliği → bilenlerin haşyeti; 35:27 ile birlikte okunur)  
وَمِنَ ٱلنَّاسِ وَٱلدَّوَآبِّ وَٱلْأَنْعَٰمِ مُخْتَلِفٌ أَلْوَٰنُهُۥ كَذَٰلِكَ إِنَّمَا يَخْشَى ٱللَّهَ مِنْ عِبَادِهِ ٱلْعُلَمَٰٓؤُا۟ إِنَّ ٱللَّهَ عَزِيزٌ غَفُورٌ  
*vamina nnâsi vaddavâbbi valʾanʿâmi muḫtalifun ʾalvânuhû kaẕâlika ʾinnamâ yaḫşâ llâha min ʿibâdihi lʿulamâʾu ʾinna llâha ʿazîzun gafûr*  
"İnsanlardan, canlılardan ve hayvanlardan da renkleri farklı olanlar vardır. Allah'tan, kulları arasında ancak bilenler haşyet duyar."

**26:197 — karşı/baskı noktası** (Kur'an bir topluluğun bilginlerini de adlandırır)  
أَوَلَمْ يَكُن لَّهُمْ ءَايَةً أَن يَعْلَمَهُۥ عُلَمَٰٓؤُا۟ بَنِىٓ إِسْرَٰٓءِيلَ  
*ʾavalam yakul lahum ʾâyatan ʾan yaʿlamahû ʿulamâʾu banî ʾisrâʾîl*  
"İsrâiloğullarının bilginlerinin onu bilmesi onlar için bir işaret değil mi?"

**39:9 — yalnız uyumlu** (bilenler, gece secde eden kişiyle paralel kurulur)  
أَمَّنْ هُوَ قَٰنِتٌ ءَانَآءَ ٱلَّيْلِ سَاجِدًا وَقَآئِمًا يَحْذَرُ ٱلْـَٔاخِرَةَ وَيَرْجُوا۟ رَحْمَةَ رَبِّهِۦ قُلْ هَلْ يَسْتَوِى ٱلَّذِينَ يَعْلَمُونَ وَٱلَّذِينَ لَا يَعْلَمُونَ إِنَّمَا يَتَذَكَّرُ أُو۟لُوا۟ ٱلْأَلْبَٰبِ  
*ʾamman huva qânitun ʾânâʾa llayli sâcidan vaqâʾiman yaḥẕaru lʾâḫirata vayarcû raḥmata rabbihî qul hal yastavî llaẕîna yaʿlamûna vallaẕîna lâ yaʿlamûna ʾinnamâ yataẕakkaru ʾulû lʾalbâb*  
"Gece saatlerinde secde ederek ve ayakta durarak gönülden boyun eğen, ahiretten sakınan, Rabbinin rahmetini uman kimse (öteki gibi) midir? De ki: bilenlerle bilmeyenler bir olur mu? Ancak öz akıl sahipleri öğüt alır."

**28:80 — kanıtlayıcı** (ilim verilenler doğru tartar; Kârûn bağlamı, 28:79)  
وَقَالَ ٱلَّذِينَ أُوتُوا۟ ٱلْعِلْمَ وَيْلَكُمْ ثَوَابُ ٱللَّهِ خَيْرٌ لِّمَنْ ءَامَنَ وَعَمِلَ صَٰلِحًا وَلَا يُلَقَّىٰهَآ إِلَّا ٱلصَّٰبِرُونَ  
*vaqâla llaẕîna ʾûtû lʿilma vaylakum s̱avâbu llâhi ḫayrul liman ʾâmana vaʿamila ṣâliḥan valâ yulaqqâhâ ʾillâ ṣṣâbirûn*  
"Kendilerine ilim verilenler dedi ki: yazık size! İman edip salih iş yapan için Allah'ın karşılığı daha hayırlıdır; ona ancak sabredenler kavuşturulur."

**59:21 — kanıtlayıcı** (aynı açılış; amaç herkesin düşünmesi)  
لَوْ أَنزَلْنَا هَٰذَا ٱلْقُرْءَانَ عَلَىٰ جَبَلٍ لَّرَأَيْتَهُۥ خَٰشِعًا مُّتَصَدِّعًا مِّنْ خَشْيَةِ ٱللَّهِ وَتِلْكَ ٱلْأَمْثَٰلُ نَضْرِبُهَا لِلنَّاسِ لَعَلَّهُمْ يَتَفَكَّرُونَ  
*lav ʾanzalnâ hâẕâ lqurʾâna ʿalâ cabalil laraʾaytahû ḫâşiʿam mutaṣaddiʿam min ḫaşyati llâhi vatilka lʾams̱âlu nażribuhâ linnâsi laʿallahum yatafakkarûn*  
"Bu Kur'an'ı bir dağa indirseydik, onu Allah'ın haşyetinden boyun eğmiş, parçalanmış görürdün. İşte o misaller; onları insanlar düşünsünler diye ortaya koyarız."

**9:31 — yalnız uyumlu** (bilginlerin dayanak edinilmesi)  
ٱتَّخَذُوٓا۟ أَحْبَارَهُمْ وَرُهْبَٰنَهُمْ أَرْبَابًا مِّن دُونِ ٱللَّهِ وَٱلْمَسِيحَ ٱبْنَ مَرْيَمَ وَمَآ أُمِرُوٓا۟ إِلَّا لِيَعْبُدُوٓا۟ إِلَٰهًا وَٰحِدًا لَّآ إِلَٰهَ إِلَّا هُوَ سُبْحَٰنَهُۥ عَمَّا يُشْرِكُونَ  
*ittaḫaẕû ʾaḥbârahum varuhbânahum ʾarbâbam min dûni llâhi valmasîḥa bna maryama vamâ ʾumirû ʾillâ liyaʿbudû ʾilâhan vâḥidal lâ ʾilâha ʾillâ huva subḥânahû ʿammâ yuşrikûn*  
"Allah'ın berisinden hahamlarını ve rahiplerini, Meryem oğlu Mesih'i de rabler edindiler; oysa yalnız tek ilâha kulluk etmekle emrolunmuşlardı." Not: aynı fiil (*ittaḫaẕû*) 29:41'de de geçer; fiil olağan olduğu için bu benzerlik tek başına delil sayılmaz (§7.4).

**16:43 — yalnız uyumlu** (bilene sormak; bağlamdaki soru belirlidir)  
وَمَآ أَرْسَلْنَا مِن قَبْلِكَ إِلَّا رِجَالًا نُّوحِىٓ إِلَيْهِمْ فَسْـَٔلُوٓا۟ أَهْلَ ٱلذِّكْرِ إِن كُنتُمْ لَا تَعْلَمُونَ  
*vamâ ʾarsalnâ min qablika ʾillâ ricâlan nûḥî ʾilayhim fasʾalû ʾahla ẕẕikri ʾin kuntum lâ taʿlamûn*  
"Senden önce de ancak kendilerine vahyettiğimiz adamlar gönderdik. Bilmiyorsanız zikir ehline sorun." (Aynı cümle 21:7'de.)

**12:76 (son kısmı) — yalnız uyumlu** (insanlar arasında bilgi görelidir; insan/Allah okuması tartışmalı)  
*… vafavqa kulli ẕî ʿilmin ʿalîm* — "… her bilgi sahibinin üstünde bir bilen vardır."

## 6. Aşama 4 — semantik sınır testleri

### 6.1 Yakın kavram testi

| kavram | nerede | fark |
|---|---|---|
| *ʿâlimûn* | 29:43, 30:22 | misali/işareti kavramanın şartı olarak bilgi |
| *qavmun yaʿqilûn* | 29:35, 30:24 | işaretten sonuca geçme işi (fiil) |
| *muʾminîn* | 29:44 | güvenip bağlanma; ikame testi: 29:43'e konsa anlama şartı aidiyete kayar (*anlam kayar*) |
| *qavmun yatafakkarûn / yasmaʿûn* | 30:21, 30:23 | farklı işaretlere farklı zihinsel işler |
| *ʾulû lʾalbâb* | 39:9 | bilenlerle bilmeyenler sorusundan sonra öğüt alanlar |

### 6.2 Negatif semantik test — *ʿâlim* ne anlama gelemez?

- **Bir zümre ya da makam adı olamaz:** 29:43'te topluluk eki yok; aynı kalıbın 29:47/49'daki eşleri tip adlandırır; misaller bütün insanlar için. Kur'an bir topluluğun bilginlerini ancak tamlamayla adlandırır (26:197).
- **Kendiliğinden övgü/erdem olamaz:** sihirbaz için *ʿalîm* (7:109 vd.), bilgisine rağmen sapma (45:23), kavrayıp çarpıtma (2:75).
- **29:43'te "her türlü malumat sahibi" olamaz:** örümcek ağının çürüklüğünü herkes bilir; 29:41 yine de "bilmiyorlar" der. Bu okuma cümleyi boşaltır.
- **Doğa bilgisiyle sınırlanamaz:** 30:7 dünyanın görünen yüzünü bilmeyi yeterli saymaz.

## 7. Aşama 5–6 — falsifikasyon, kapalı örneklem ve rakip okumalar

### 7.1 Geçici hipotez (kilit)

H0: "29:43'teki *lʿâlimûn*, şeylerin gerçek ağırlığını (neyin gerçekten dayanak, neyin gerçekten hayat olduğunu) bilenlerdir."

**Falsifikasyon sorusu:** Bu doğru olsaydı hangi kullanım onu çürütürdü? — İnsan için nesnesiz, övgülü *ʿâlim/ʿulemâʾ/ellezîne yaʿlamûn* kullanımlarından birinin değer tartısı içermeyen salt teknik bilgiyi göstermesi. Bulunan: 12:44 teknik uzmanlıktır ama **nesneli ve olumsuzdur**; Allah için 15 kullanım değer tartısı içermez. **Sonuç: revizyon (kısmen doğru → alt-anlamla sınırlandı).** H0 kelimenin değil, 29:43 bağlamının anlamıdır. Kelime düzeyindeki çekirdek yalnız "bilen"dir.

### 7.2 Kapalı örneklem

**Kapalı örneklem geçerli sayılmaz.** Hipotez sohbette yalnız Ankebût verisinden kurulmuş, sonra öteki *lav kânû yaʿlamûn* ayetlerine (5/5 uydu) ve *ellezîne ʾûtû lʿilm* ayetlerine (9/9 gerçeği tanıyan tarafta; 28:79–80 değer tartısı) uygulanmıştır. Ancak bu ayetlerin bir kısmı hipotez kurulmadan önce biliniyordu ve kullanımlar önceden kilitlenmedi. Bu uygulamalar protokol Aşama 5 uyarınca **sonradan uygulama** olarak raporlanır, doğrulama gücü iddia edilmez.

### 7.3 Rakip okumalar

| okuma | en güçlü hâli | sınama | sonuç |
|---|---|---|---|
| R1 — *ʿâlim* = din âlimleri sınıfı; misalleri halk değil onlar anlar | anlamak bilgiye bağlıysa bilgiyi meslek edinen önce gelir; 26:197 bir topluluğun bilginlerini anar; *ʾûtû lʿilm* 9 ayet | 29:43'te topluluk eki/makam yok; misaller *linnâs*; 59:21 amaç *yatafakkarûn*; 29:47/49 tip adlandırır; "onlara uyun" sonucu ayette yok; 9:31 bilginlerin rab edinilmesini kınar | Bilginler bilenlerin içinde olabilir: yalnız uyumlu. "Sınıf adı" okuması: **Destek gösterilemedi · Spekülatif** |
| R2a — ılımlı: doğa bilgisi "bilmek"in alanına girer | insanlar için nesnesiz "bilenler"in öteki iki yeri doğa/insan çeşitliliği (30:22, 35:27–28) | 30:22 okunuşu açık; 35:28 sağlam | Kur'an geneli için **Destekleniyor · Muhtemel**; 29:43 için yalnız uyumlu |
| R2b — güçlü: *ʿâlimûn* = bilim insanları; misali yalnız onlar anlar | örümcek misalinin biyolojiyle örtüşen noktaları (§9) | 29:41 misalin anlamını kendisi verir; *lav kânû yaʿlamûn* kalıbı değer tartısıdır; 30:7 | **Destek gösterilemedi · Spekülatif** |
| R3 — herhangi bir malumata sahip olan | kelime düzeyinde doğru (12:44) | 29:41/29:63 malumatı olanı "bilmeyen/akletmeyen" sayar; 29:43'ü boşaltır | **Yalnız uyumlu** |
| R4 — gizli/iç bilgiye erenler (bâtınî) | misalin derin anlamı olabilir | anlam 29:41'de açıkça verilmiş; hitap herkese; 59:21 | **Destek gösterilemedi · Spekülatif** |

### 7.4 Sohbet sürecinde geri alınan hükümler (kayıt)

- Örümceğin evini kendi bedeninden üretmesiyle velîlerin "kendinden üretilmesi" arasında kurulan bağ ilk aşamada "en güçlü çağrışım" diye sunulmuştu. Korpus denetiminde *ittaḫaẕa*'nın ev/mesken edinmek için de olağan fiil olduğu görüldü (*ittaḫaẕa* + *bayt* aynı ayette: 2:125, 7:74, 16:68, 29:41; 7:74'te Semûd *tattaḫiẕûna … quṣûran*). Fiil tekrarı dilin doğal sonucudur; "kendinden" lafızda yoktur. Hüküm **yalnız uyumlu / yorum**a indirildi.
- "Dişi örümcek" okuması ilk aşamada yalnız kanıt olarak sınanıp reddedilmiş, en güçlü hâli kurulmamıştı. Düzeltilmiş hüküm §9'dadır.

## 8. Aşama 7 — dış dil katmanı (hipotez, delil değil)

### 8.1 Anlam → dayanak tablosu

| kaynak | anlam | dayanak (araç statüsü) | korpus sınavı | not |
|---|---|---|---|---|
| İbn Fâris, ʿ-l-m (4/108) | asl: "bir şeyin üzerinde onu başkasından ayırt eden iz" (*ʿalâme*) | tanıksız açıklama [ASL] | Ankebût'ta Allah'ın bilmesi iki kez ayırma çiftiyle gelir (29:3 doğrular/yalancılar; 29:11 inananlar/münafıklar); 29:41 sağlam/çürük dayanak | **yalnız uyumlu**; kök anlamı kelimeye giydirilmedi. *ʿalâmât* lemması 1 kelime konumu (16:16), ayrı lemma |
| İbn Fâris, ʿ-l-m | ʿilm = cehlin zıddı, *ʿalâme* ile aynı kıyas | araç: YALNIZ rivayetle tanıklı [HADİS] | ʿilm ↔ ẓann çerçevesi 4 ayet (§4.2) | araçtan sapma: anlam dil beyanıdır; işaret, tanık olarak anılan kıraat/yorumdan (*innehû leʿilmun li's-sâʿa*) gelir |
| Râgıb, ʿ-l-m (1/579) | ʿilm = "şeyi hakikatiyle idrak" | tanıksız açıklama | 2:102 iki düzeyli bilme ile uyumlu | yalnız uyumlu |
| Râgıb, ʿ-l-m | ilim nazarî/amelî ikiye ayrılır | tanıksız açıklama | korpusta böyle bir sınıflama terimi yok | sözlükçünün sistematiği; taşınmadı |
| Râgıb, ʿ-l-m | 12:76 *ʿalîm* insan da olabilir, Allah da | sözlükçünün ayet okuması [KUR] | §2.2'de tartışmalı tutuldu | uyumlu |
| İbn Fâris, ʿ-q-l (4/68) | asl: "bir şeyde tutma/alıkoyma"; akıl kötü söz ve işten alıkoyan | tanıksız açıklama [ASL] | 2:44 (dediğini yapmamak = akletmemek) uyumlu; 2:75 (kavrayıp çarpıtmak) sınır koyar | **kısmen uyumlu** |
| Râgıb, ʿ-q-l (1/576) | 29:43'teki akıl "kazanılmış akıl"dır | araç: dil-içi tanıklı (+ rivayet) [KUR][HADİS][NAKİL][ŞİİR] | — | **[R]**: 29:43 yorumu bir hadis ve bir şiirle (Hz. Ali'ye nispet edilen) temellendirilmiş; delil sayılmadı |

Sözlüklerin ayet atıfları: Râgıb'ın ʿ-q-l maddesi kökün 49 ayetinden 1'ini (29:43) anar; ʿ-l-m kökünün 728 ayetinden İbn Fâris 1'ini, Râgıb 20'sini anar (birim: ayet; `klasik ayet`). Kalan kullanımlar sözlükte anılmayan kullanımlardır. İbn Fâris, Râgıb ve Lane aynı geleneğin kayıtlarıdır; birleşmeleri bağımsız doğrulama değildir.

### 8.2 Lane

ʿ-l-m: 40 madde (s. 2138 vd.). *ʿalimahu* "bildi, tanıdı (*ʿarafahu*)"; bazı kaynaklara göre "gerçekten/kesin bildi"; *ʿilm* = *yaqîn* (Msb). Madde 1 hadis ve Kur'an atfı taşır (araç: dairesellik riski). ʿ-q-l: 30 madde (s. 2112 vd.); *ʿaql* "alıkoyma, tutma (*manʿ*)", Lane'in köşeli parantezle "muhtemelen asıl anlam" kaydıyla. İbn Fâris'in asl'ıyla örtüşür; bağımsız değildir. Kur'an öncesi anlam iddiası kurulmadı; 7c tanık araması gerekmedi.

### 8.3 Sâmî katman

- ʿ-l-m: yalnız İbranicede tek aday (gürültü payı ≈ %35,4); tek dil vuruşu tek başına raporlanmaz. "Bilmek" anlamında doğrulanmış karşılık bulunamadı.
- ʿ-q-l: iki dilde aday (gürültü payı ≈ %20,9): İbranice *ʿāqal* "eğmek", Süryanice "çarpık". Arapçadaki "bağlamak/alıkoymak" anlamıyla ilişkisi gösterilemedi; kullanılmadı.
- `04_lexicons/semitic/cognates.tsv` bu kökler için incelenmiş kayıt içermiyor; tarama dizin düzeyindedir.

SEDRA atfı: This work makes use of the Syriac Electronic Data Retrieval Archive (SEDRA) by George A. Kiraz, distributed by the Syriac Computing Institute. — G. Kiraz, "Automatic Concordance Generation of Syriac Texts", VI Symposium Syriacum 1992, OCA 247, Roma 1994.

## 9. Bilimsel çağrışım katmanı [B] — delil değil

Bilim kelimenin anlamını belirlemez; sonuçlar en fazla **yalnız uyumlu** olabilir. Çağrışımları kendi içinde derecelendirmek için kullanıcıyla tartışılan dört soru kullanıldı (protokole henüz eklenmedi, öneri):
1. metinde seçim var mı (dil zorunlu kılıyorsa bilgi taşımaz);
2. dönemin gözlemiyle bilinebilir miydi (ayrıca kaynak gerektirir; bu kartta araştırılmadı);
3. kaç bağımsız noktada örtüşüyor;
4. daha basit bir açıklama var mı.

| çağrışım | seçim | daha basit açıklama | değerlendirme |
|---|---|---|---|
| **İplik güçlü, ev çürük.** Örümcek ipeği ağırlığına göre çok dayanıklı bir malzemedir (Gosline ve ark., *J. Exp. Biol.* 202:3295, 1999; Vollrath ve Knight, *Nature* 410:541, 2001); ayet ipliği değil evi (*bayt*) "en çürük" (*ʾavhan*) der | var | kısmen: ağın sığınak olarak zayıflığı gözle görülür | orta — yalnız uyumlu |
| **Evi kuran dişi.** Fiil dişil (*ittaḫaẕat*); arıda da dişil (16:68 *ittaḫiẕî*). Biyolojide kalıcı ağı kuran ve onda yaşayan esas olarak ergin dişidir; erkek çoğunlukla erginleşince ağ örmeyi bırakır (genel bilgi; bkz. Foelix, *Biology of Spiders*, 3. bs., 2011) | yok: Lane'e göre *ʿankabût* çoğunlukla dişil kullanılır [T] | var: dilbilgisi | zayıf — örtüşme gerçek, metin bilgi taşımaz |
| **Kendinden üretilmiş sığınak.** Örümcek evini kendi ipek bezlerinden üretir | lafızda yok | var: fiil olağan (§7.4) | zayıf — yorum [Y] |
| **Benzetmeyi kavramak bilgiye bağlı.** Benzetme ilişki eşleme ile anlaşılır (Gentner, *Cognitive Science* 7(2), 1983); bilgi arttıkça yorum yüzeyden ilişkiye kayar (Gentner, *Child Development* 59(1):47–59, 1988) | — | — | yalnız uyumlu: 29:43'ün "kavrama bilgiye bağlı" önermesiyle örtüşür |
| **Uzman–acemi farkı.** Uzmanlar problemleri derin ilkelere, acemiler yüzey özelliklerine göre sınıflar (Chi, Feltovich ve Glaser, *Cognitive Science* 5(2):121–152, 1981) | — | — | yalnız uyumlu: 30:7 "görünen yüz" ile işaret okuyan bilenler ayrımına benzer |

Künye durumu: Gentner 1988, Chi ve ark. 1981, Gosline ve ark. 1999, Vollrath ve Knight 2001 web aramasıyla varlık düzeyinde doğrulandı; Gentner 1983 ve Foelix 2011 doğrulanmadı (genel bilgi).

**v0.1 ayet başı çağrı satırı:** 29:41 — Bu ayette doğrudan bilimsel çağrı yok (doğa nesnesi misal yapılıyor; gözlem dolaylı). 29:42 — Bu ayette doğrudan bilimsel çağrı yok. 29:43 — Bu ayette doğrudan bilimsel çağrı yok (anlamayı bilgiye bağlaması dolaylı yönlendirme [D]). 29:44 — Bu ayette doğrudan bilimsel çağrı yok (yaratılışı işaret olarak sunuyor).

## 10. Aşama 8 — sentez

**Çekirdek anlam (kelime):** *ʿâlim* = bir şeyi/alanı bilen. Kendiliğinden övgü, erdem ya da makam taşımaz (12:44, 7:109 vd.).

**Bağlama bağlı alt-anlam (29:43):** nesnesiz ve tip bildiren *lʿâlimûn*, misalin hedefini bilenlerdir: Allah'ın berisinden edinilen dayanakların çürüklüğünü, dünya hayatının değerini — kısaca şeylerin gerçek ağırlığını (29:41, 29:64; *lav kânû yaʿlamûn* kalıbı).

**Anlam sınırı:** bilmek kavramanın şartıdır, yeterli şartı değildir; kavrayış da doğru davranışı garanti etmez (2:75; 45:23).

**Yakın kavramlardan farkı:** mü'min (aidiyet/güven, 29:44), akleden topluluk (işaretten sonuca geçme işi, 29:35), *ʾulû lʾalbâb* (öğüt alma, 39:9).

| bulgu | katman | mantıksal durum | derece |
|---|---|---|---|
| *ʿâlim* = "bilen"; 18 kelime konumunun 15'i Allah, 3'ü insan; kendiliğinden övgü/sınıf taşımaz | kesin veri + çıkarım | Destekleniyor | Sağlam |
| 29:43'te nesnesiz, tip bildiren kullanım; kim olduğu bağlamdan belirlenir | kesin veri + çıkarım | Destekleniyor | Sağlam |
| Bilinen şey: şeylerin gerçek ağırlığı | güçlü çıkarım | Destekleniyor | Muhtemel |
| Anlama şartı aidiyet değil bilgidir | güçlü çıkarım | Destekleniyor | Muhtemel |
| Bilmek kendiliğinden erdem değil; doğru tartmanın şartı | güçlü çıkarım | Destekleniyor | Muhtemel |
| Doğa bilgisi "bilmek"in alanına girer (Kur'an geneli) | güçlü çıkarım | Destekleniyor | Muhtemel |
| Sûre düzeyi: Ankebût'ta yanlış tartma teması (29:10 baskı = azap; 29:41 çürük dayanak = ev; 29:64 oyun = hayat) | açık ihtimal | Yalnız uyumlu | Muhtemel — 29:10 sonucu depoda olmayan önceki yerel analizden "anlam ihtimali" olarak taşındı (protokol §7) |

**İnsanları değerlendirme ölçütü (kullanıcı sorusuna cevap):** Kur'an'ın kullanımına göre bir bilim insanı ya da din bilgini **alanının âlimidir** (12:44, 12:55). 29:43'teki bilenlerden olmak için ise ayrıca bilginin işaret ettiğine geçmek (30:22, 35:28), şeyleri doğru tartmak (29:41–43) gerekir; bilginin davranışa dönmemesi ise mümkündür (2:75, 45:23). Bilene sormak meşrudur (16:43); bilgini sorgulanmaz dayanak edinmek uyarılır (9:31). Bu ölçüt bütün meslek gruplarına aynen uygulanır.

## 11. Çeviri

- **Lafzî:** "İşte o misaller; onları insanlar için ortaya koyarız (lafzen: vururuz). Onları bilenlerden başkası kavramaz (akletmez)."
- **Açıklamalı:** "Örümcek evi gibi misalleri bütün insanlar için veriyoruz; ama neyi gösterdiklerini yalnız bilenler kavrar: neyin gerçekten dayanak, neyin yalnızca dayanak gibi göründüğünü bilenler."
- **Korunacak sınır:** lafza "âlimler" diye bir sınıf adı eklenmez; "gerçek ağırlık" içeriği açıklamada kalır.

**Kısa tefsir (29:41–44):** Yıkılan kavimlerin ortak hatası bir imgeyle verilir: Allah'tan başka dayanak edinmek örümceğin evine sığınmak gibidir. İmgeyi herkes görür; imgenin kendi hayatındaki karşılığını görmek şeylerin gerçek ağırlığını bilmeyi gerektirir. Bilenler bir zümre değil, bu tartıyı doğru yapanlardır.

**Meal karşılaştırması (sonuçlandırma sonrası, delil değil):** Diyanet 29:41'de "dişi örümcek" der; "dişi"nin lafızda ayrı karşılığı yoktur, fiilin dilbilgisel dişilliğinden çıkarılmıştır. 29:43'te "anlayabilir", lafzın bildirme kipine (kavramaz) yeterlik anlamı katar.

## 12. Kavram kartı

> **Âlim (Ankebût 29:43):** Kelime olarak "bir alanı bilen" demektir; Kur'an aynı kelimeyi Allah için, rüya yorumcuları ve sihirbazlar için de kullanır, yani kendiliğinden övgü ya da unvan değildir. 29:43'te misali kavrayan "bilenler", bir önceki ayetin "bir bilselerdi" dediği bilgiye sahip olanlardır: Allah'tan başka dayanakların örümcek ağı kadar çürük olduğunu, kısaca şeylerin gerçek ağırlığını bilenler. Bu bir meslek zümresi değil, herkese açık bir niteliktir; ama bilmek tek başına doğru davranışı garanti etmez.

## 13. Sade sonuç

29:43 "Bu misalleri herkes için veriyoruz, ama onları ancak bilenler kavrar" der. "Bilenler" ne yalnız din âlimleri ne yalnız bilim insanlarıdır. Bir konuya hâkim olan herkes Kur'an'ın dilinde o konunun âlimidir; ama misali kavrayan bilenler, bilgisi şeylerin gerçek değerine ulaşanlardır. Bu ölçü her mesleğe aynen uygulanır.

## 14. Açık konular

- Bağımsız tekrar yapılmadı (başka model ailesi ya da kişi).
- Kapalı örneklem geçerli sayılmadı (§7.2).
- 30:22 okunuş farkı ayrıntılı doğrulanmadı (K2 açık).
- ʿ-l-m kökünün tam sınıflandırması ("ilim" kavram kartı) yapılmadı.
- Bilimsel çağrışımlar için "dönemin gözlemiyle bilinebilirlik" sorusu araştırılmadı.
- Bilimsel çağrışım derecelendirme ölçütü (dört soru) protokole eklenmedi; kullanıcı kararı bekliyor.

## 15. Kalite kontrol listesi (protokol §13)

| madde | durum |
|---|---|
| araştırma sorusu, analiz birimi, veri kaydı | evet |
| kök/lemma/kelime ayrımı; tam dağılım (*ʿâlim* lemması) | evet; kök tamamı sınıflandırılmadı (kapsam dışı) |
| sentaktik kalıplar, pasaj bağlamı, iç-tanım | evet (bağlamsal iç-tanım: 29:41 ↔ 29:43) |
| sözlüksel dal denetimi | *ʿâlim* / *ʿâlamîn* ayrı lemma; iskelet ortaklığı kaydedildi |
| kapalı örneklem | yapılamadı; gerekçesi yazıldı |
| hipotez donduruldu; revizyon kaydedildi | evet (§7.1) |
| çekirdek/alt-anlam; dört anlam katmanı | evet (sonraki teknik terim "âlim = din bilgini" ayrı tutuldu) |
| yakın kavram, negatif semantik, kanıtlayıcı/uyumlu/karşı | evet |
| falsifikasyon, en güçlü alternatif | evet |
| İbn Fâris, Râgıb (anlam→dayanak), Lane, Sâmî | evet |
| Kur'an öncesi anlam iddiası | yok |
| iki eksen; sade sonuç teknik sonuçla uyumlu | evet |
| kullanıcı onayı | kayıt talimatı verildi; PR incelemesi bekliyor |

## 16. Değişiklik günlüğü

- v1 (25.10.2026): ilk kayıt. Sohbet sırasında "dişi örümcek" hükmü düzeltildi; *ittaḫaẕû/ittaḫaẕat* bağının "en güçlü" nitelemesi geri alındı (§7.4). Sayımlar depo QAC v0.4 üzerinde yeniden üretildi (sohbetteki ilk sayımlar beceri korpusundandı; kelime konumu sayıları birebir aynı çıktı).

```text
Kaynak      : QAC v0.4 + klasik + Lane + Sâmî
Sayım birimi: kelime konumu | ayet | sûre | madde | anlam birimi | atıf geçişi
Sorgu       : python 08_scripts/analyze_alim_29_43.py; python -m tezgah klasik asl|isaret|ayet Elm|Eql; python -m tezgah lane kok Elm|Eql; python -m tezgah sami kok Elm|Eql
Veri izi    : a1d129238153 | klasik c32e695538da | Lane a16651d5381b | Sâmî 2c16606447f2, f90fbf51a3de
Durum       : çalıştırıldı
```
