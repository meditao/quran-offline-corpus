# أ م ن / Amn — Kur'an içi analiz, Aşama 3: `āman(a) bi-`

**Durum:** Ara sonuç. Nihai sözlük tanımı değildir.

**Sürüm:** v1.1 — 2026-10-11. Morfoloji, birlikte geçiş ve anlam önerisi sınırları güncellendi.

Kaynak zinciri: sabit QAC v0.4 → `analyze_amn_verb_syntax.py` → `analyze_amn_bi_targets.py` → manuel zamir ve sıra-dışı vaka kontrolü.

## 1. Otomatik tarama ne buldu?

537 adet IV. bâb `'aAmana` fiil kelime konumunun **163** tanesinde fiilden hemen sonra morfolojik olarak açık bir `bi-` yapısı gelir. **537 morfolojik toplamdır**; 106:4:5'teki güvenlik sağlama kullanımı da bu kümededir ve toplamın tamamı “inanma” anlamında sayılamaz.

İlk yüzey sınıfları:

- Allah: **64**
- zamirli (`bihi/bihā/bī...`): **37**
- relative/clause head (`bimā`, `bi-lladhī` vb.): **15**
- ahiret: **13**
- diğer açık lexical hedefler: **11**
- ayet: **9**
- Rabb: **9**
- resul: **2**
- kitap: **1**
- hesap günü: **1**
- gayb: **1**

Bu rakamlar yalnız **yüzey komşuluğu** gösterir. Manuel kontrol olmadan 163'ün tamamına 'semantik hedef' denemez.

## 2. Otomatik sayımın düzeltilmesi

11 'diğer' vakası tek tek kontrol edildi.

Üç önemli düzeltme:

1. **5:41 — `āmannā bi-afwāhihim`**: `bi-` burada hedef değil, biçim/araç bildirir — 'ağızlarıyla'. Aynı ayet hemen ardından `wa-lam tuʾmin qulūbuhum` diyerek ağız beyanı ile kalbin gerçek durumunu ayırır.
2. **16:72** — `wa-bi-niʿmati llāhi hum yakfurūn`: `bi-niʿmat` önceki `yuʾminūn`a değil, sonraki `yakfurūn`a bağlıdır.
3. **29:67** — aynı yapı: `bi-niʿmat` sonraki `yakfurūn`un tamamlayıcısıdır.

Dolayısıyla **163 = yüzeyde hemen sonraki bi- vakasıdır; 163 gerçek hedef değildir.**

Manuel sıra-dışı vaka kaydı: `Amn-bi-other-manual-review.tsv`.

## 3. Zamirli 37 kullanım

37 zamirli kullanım tek tek bağlam içinde çözüldü.

| antecedent sınıfı | sayı |
|---|---:|
| vahiy / kitap / mesaj / bildirim içeriği | **19** |
| Allah / ilahî merci | **6** |
| insan / elçi / çağırıcı | **4** |
| ayet / işaret | **3** |
| kıyamet / azap / gerçekleşecek olay | **3** |
| bilinçli olarak belirsiz bırakılan | **2** |

Belirsiz bırakılan iki vaka: **4:55** ve **7:123**. Bunlar nihai sayısal semantik sınıflamaya zorla sokulmadı.

Manuel zamir kaydı: `Amn-bi-pronoun-manual-review.tsv`.

## 4. `bi-` yalnız 'doktrin nesnesi' değildir

`bi-` ile hedeflenen alan çok geniştir:

### İlahi merci

- `āmana bi-llāh`
- `āmana bi-rabbihim`
- 67:29 — `al-Raḥmān; āmannā bihi wa-ʿalayhi tawakkalnā`

67:29, `āmannā bihi` ve `tawakkalnā ʿalayhi` ifadelerinde aynı ilahî merciye farklı fiiller ve tamlayıcılarla yönelir. Bu, inanma ve dayanma ilişkisini araştırmaya yarar; birlikte geçiş ve farklı edatlar tek başına ne eşanlamlılığı ne kesin anlam ayrılığını kanıtlar. Allah'a güven/bağlanma yorumu bağlamla değerlendirilir; tasdik okuması yalnız bu yapıya dayanılarak dışlanmaz.

### Vahiy / bildirim / önerme

Örnekler:

- 2:4 — `yuʾminūna bimā unzila ilayk`
- 2:85 — `a-fa-tuʾminūna bi-baʿḍi l-kitāb`
- 14:27 — `āmanū bi-l-qawli l-thābit`
- 18:6 — `bi-hādhā l-ḥadīth`
- 34:31 — `lan nuʾmina bi-hādhā l-Qurʾān`
- 72:2 — cinler Kur'an'ı duyup `fa-āmannā bihi` der.

Burada fiil, bir bildirimi/mesajı **doğru-güvenilir kabul edip ona bağlanma** alanına rahatça girer.

### Gayb / ahiret / kıyamet

- 2:3 — `yuʾminūna bi-l-ghayb`
- çok sayıda `bi-l-ākhirah`
- 20:16 / 42:18 — kıyamet saatine yönelen zamirli kullanımlar
- 10:51 — azabın/olayın gerçekleşmesinden sonra `āmantum bihi`

Bu örnekler fiilin yalnız 'bir kişiye güvenmek' olmadığını kesin biçimde gösterir. Gerçeklik/bildirim hakkında doğrulama ve güven ilişkisi de vardır.

## 5. `bi-` insanı da hedefleyebilir

Bu nokta önemlidir, çünkü Aşama 2'de `li-` kullanımlarının büyük kısmı insan hedefliydi. Fakat buradan 'insan = li-, Allah/bildirim = bi-' gibi katı bir kural çıkmaz.

Kur'an'da insan/elçi `bi-` ile de hedef olur:

- 5:12 — `āmantum bi-rusulī`
- 57:28 — `āminū bi-rasūlihi`
- 3:81 — `rasūlun muṣaddiqun ... la-tuʾminunna bihi wa-la-tanṣurunnahu`
- 7:157 — `āmanū bihi wa-ʿazzarūhu wa-naṣarūhu...`
- 46:31 — `ajībū dāʿiya llāhi wa-āminū bihi`

Bu örneklerde `bi-` insanı/elçiyi yalnız 'var olduğuna inanılan nesne' yapmaz. Fiil, elçiyi **doğru/güvenilir kabul etme ve onun getirdiği çağrıya bağlanma** ilişkisine girebilir. Özellikle 3:81 ve 7:157'de `āmana bihi` hemen destekleme/yardım etme fiilleriyle yan yana gelir.

## 6. En önemli falsifikasyon: yanlış hedefe de `āmana` denebilir

Kur'an fiili yalnız doğru/ilahî hedefler için kullanmaz:

- 4:51 — `yuʾminūna bi-l-jibti wa-l-ṭāghūt`
- 29:52 — `alladhīna āmanū bi-l-bāṭil wa-kafarū bi-llāh`

Bu iki ayet kritik bir sınama sağlar.

`āmana` fiilinin kendisi 'doğru şeye inanmak' veya 'hakikate iman etmek' anlamını **lexical olarak garanti etmez**. İnsan yanlış/boş/tağutî bir hedefe de `āmana bi-...` ilişkisi kurabilir.

Demek ki olumlu veya olumsuz değer, fiilin kökünde değil **güven/bağlanma ilişkisinin hangi hedefe yöneltildiğinde** ortaya çıkar.

Bu bulgu, 'îmân'ı baştan kutsal-teknik bir kategori olarak tanımlamanın metodolojik riskini gösterir.

## 7. Ağız–kalp karşılaştırması: 5:41

5:41 özel bir testtir:

`qālū āmannā bi-afwāhihim wa-lam tuʾmin qulūbuhum`

Yani ağızla 'āmannā' demek, kalbin `tuʾmin` etmesiyle aynı şey değildir.

Bu ayet şu sınırı koyar:

> `īmān/āmana` salt sözlü beyan değildir; içsel kabul/güven bağı kurulmadan kelimeyi söylemek gerçek `āmana` sayılmaz.

Bu bulgu 'iman = yalnız fikir beyanı' okumasını zayıflatır.

## 8. `bi-` ile `li-` arasındaki fark için şimdiki sonuç

Aşama 2 ve 3 birlikte değerlendirildiğinde:

- `āmana li-X` özellikle insan/sözcü/hedefe yönelen **kişisel itimat / sözünü güvenilir bulma** işlevinde yoğunlaşır.
- `āmana bi-X` daha geniştir: Allah, elçi, vahiy, kitap, ayet, gayb, ahiret, olay, hatta bâtıl/jibt gibi hedeflerle **X'i doğru/güvenilir/geçerli kabul ederek ona bağlanma** ilişkisi kurabilir.
- Ancak bu ayrım mutlak değildir; `bi-` insan/elçiyle de kullanılabilir.

9:61 hâlâ en temiz iç karşılaştırmadır:

- `yuʾminu bi-llāh`
- `wa-yuʾminu li-l-muʾminīn`

Burada `li-` müminlerin sözünü doğru/güvenilir bulma okumasına açıktır. `Bi-` için bağlılık/doğrulama boyutları bağlamda değerlendirilebilir; bu karşılaştırma “li- tasdik olamaz” veya “bi- her zaman daha güçlü bağlılıktır” şeklinde genel bir kural vermez.

## 9. Çalışma tanımının güncellenmesi

Üç aşamanın sonunda, **inanma/tasdik bağlamlarıyla sınırlı** geçici anlam önerisi:

> **Bir merciyi, kişiyi, bildirimi veya gerçeklik iddiasını doğru/güvenilir kabul etmek; güven ve bağlılık boyutlarını bağlamın desteklediği ölçüde değerlendirmek.**

Bu tanımın avantajı:

- `amina` = güven içinde olmak / güvenmek,
- `amīn` = güvenilir,
- `amāna` = emanet/güven ilişkisi,
- `āmana li-` = kişiye/sözüne güvenme,
- `āmana bi-` = Allah'a, elçiye, vahye, ayete, ahirete veya başka bir hedefe güven/doğrulama bağı kurma,
- yanlış hedefe `āmana bi-l-bāṭil` gibi kullanımlar

aynı anlam ağı içinde araştırılabilir. Kök ortaklığı her biçime bütün anlamları yüklemez; 106:4'ün güvenlik sağlama anlamı yukarıdaki inanma alt anlamının dışındadır.

Bu hâlâ **nihai sözlük tanımı değildir**. **Durum: Destekleniyor, bu sınırlı kapsamda; derece: Muhtemel.** Haber tasdiki okumasının güçlü biçimleri elenmiş değildir.

## 10. Sonraki falsifikasyon

Bir sonraki aşamada `īmān` isim formunun 45 kullanımı ve `kufr` karşıtlıkları incelenecek.

Özellikle:

- `kufr ↔ īmān` değiş tokuşu,
- `baʿda īmānikum`,
- `zāda-hum īmānan`,
- `li-yazdādū īmānan`,
- 2:143'te `īmānakum`,
- kalp / şüphe / amel / itaat bağlantıları

üzerinden şu soru test edilecek:

**İman artışı bağlamlarında yeni bilgi, doğrulama, güven ve bağlılığın katkıları ayrılabiliyor mu?** Bunlar peşinen birbirini dışlayan seçenekler sayılmaz.

## v1.1 sınır düzeltmesi — 2026-10-11

537 toplamı anlam sayımı olmaktan ayrıldı; 67:29'daki birlikte geçiş eşanlamlılık/ayrılık kanıtı olarak kullanılmadı; çalışma tanımı inanma bağlamlarıyla sınırlandı ve tasdik alternatifi korundu. Kaynak ve denetim: [QAC 106:4:5](https://corpus.quran.com/wordmorphology.jsp?location=(106:4:5)), [karşılaştırma raporu](../generated/tawakkul_comparison/report.md), [Tevekkül–Vekîl analizi](Tawakkul-Wakil-analysis.md). Bu güncelleme bütün örneklerin semantik olarak yeniden kodlandığı anlamına gelmez.
