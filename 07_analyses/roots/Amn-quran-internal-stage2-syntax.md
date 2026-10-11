# ʾ-m-n / Amn — Kur'an içi analiz, Aşama 2: `āman(a)` sentaksı

**Durum:** Ara sonuç. Nihai sözlük tanımı değildir.

**Sürüm:** v1.1 — 2026-10-11. Morfolojik sayımın semantik karşılığı ve kişi hedefinden çıkarılan sonuçlar daraltıldı.

Kaynak zinciri: sabit QAC v0.4 → ham morfoloji + `qac_word_annotations.csv` → `analyze_amn_verb_syntax.py` → manuel kritik-vaka kontrolü.

## 1. İncelenen fiil ailesi

QAC lemma `'aAmana` altında **537 IV. bâb fiil kelime konumu** vardır. Bu, 537 “dinî inanma” örneği anlamına gelmez. **106:4:5** *wa-āmanahum* aynı kümede yer alır ve korkuya karşı güvenlik sağlamayı anlatır. Morfoloji ile semantik alt kümeler eşitlenemez. [QAC 106:4:5](https://corpus.quran.com/wordmorphology.jsp?location=(106:4:5))

Otomatik yüzey taraması, hemen sonraki kelimenin morfolojisini şu aday gruplara ayırdı:

- açık `bi-` komşuluğu: **163**
- açık `li-` komşuluğu: **18**
- `an/inna` biçimli komşuluk: **21**
- geri kalan: çıplak kullanım, koordinasyon, cümle sonu veya başka yüzey devamları

Bu rakamların tamamı doğrudan 'tam sentaktik bağ' demek değildir. Özellikle `li-` ve `an/inna` adayları elle denetlendi.

## 2. `āmana li-` — manuel doğrulama

18 yüzey adayının sonucu:

- **15 gerçek `āmana + li` tamamlayıcısı**
- **3 yalancı komşuluk**: 2:213, 24:19, 61:2

Gerçek 15 kullanımın:

- **14'ü kişi/insan hedefli**
- **1'i olay adı hedefli**: 17:93 `li-ruqiyyika` — 'senin yükselişine'

Makine-okunur manuel kayıt: `Amn-li-manual-review.tsv`.

### Kesin kişi hedefleri

Örnekler:

- 2:55 — `lan nuʾmina laka` — Musa'ya: 'sana ...'
- 2:75 — `an yuʾminū lakum` — 'size ...'
- 3:183 — `allā nuʾmina li-rasūlin` — 'bir elçiye ...'
- 7:134 — `la-nuʾminanna laka` — Musa'ya
- 9:94 — `lan nuʾmina lakum` — 'size ...'
- 10:83 — `āmana li-Mūsā` — Musa'ya
- 17:90 — `lan nuʾmina laka` — elçiye
- 20:71 / 26:49 — `āmantum lahu` — insan/pronominal hedef
- 23:47 — `a-nuʾminu li-basharayni mithlinā` — 'bizim gibi iki insana ...'
- 26:111 — `a-nuʾminu laka` — Nuh'a
- 29:26 — `fa-āmana lahu Lūṭ` — Lût özne; İbrahim pronominal hedef
- 44:21 — `wa-in lam tuʾminū lī` — insan konuşmacıya

Bu kullanım kümesi **bir kişiyi veya onun sözünü doğru/güvenilir kabul etme** bağlamlarına açıktır. Kişi hedefli tamlayıcı, o kişinin bildirimini tasdik etmeyi dışlamaz; tek başına “zihinsel tasdik mümkün değildir” sonucunu vermez. Güven/itimat yorumu ile sözün doğruluğunu kabul etme yorumu bazı bağlamlarda örtüşebilir.

### İsm-i fâil karşılaştırması: Yûsuf 12:17

*Bi-muʾminin lanā* kardeşlerin anlattığına inanılmasıyla ilgilidir; burada zorunlu olarak dinî bağlılık aranmaz. QAC 12:17:14'ü IV. bâbdan **ism-i fâil (`N`)** olarak etiketler. Aynı aileyi aydınlatan bir örnektir, fakat çekimli fiil değildir: **537 fiil konumuna ve 15 fiil + li- tamamlayıcısı sayısına eklenmez.** [QAC 12:17](https://corpus.quran.com/wordbyword.jsp?chapter=12&verse=17)

## 3. En güçlü iç karşılaştırma: Tevbe 9:61

Aynı ayette, aynı özne ve aynı fiil iki farklı edatla kullanılır:

- `yuʾminu bi-llāh`
- `wa-yuʾminu li-l-muʾminīn`

İkinci ifade müminleri 'ilahî inanç nesnesi' yapmaz. Bağlamda elçinin insanlar hakkında söylenene kulak vermesi eleştirilmektedir; `yuʾminu li-l-muʾminīn` doğal olarak **müminlere güvenmesi / onların sözünü güvenilir bulması** alanındadır.

Bu ayet, iki tamlayıcının aynı bağlamda karşılaştırılmasına imkân verir. Müminlerin sözünü tasdik etme ve onlara güvenme okumaları burada birbirini dışlayan açıklamalar değildir.

Bu, `āmana bi-llāh` ifadesinin mekanik olarak yalnız 'Allah'a güvenmek' diye çevrilmesini ispatlamaz. `Bi-` ile `li-` farklı yapılardır; farkın her bağlamda aynı anlam ayrımına karşılık geldiği ayrıca gösterilmelidir. 9:61'in kişi hedefi, “müminlerin var olduğunu kabul etmek” okumasını yetersiz bırakır; daha güçlü “onların sözünü doğru kabul etmek” okumasını elemez.

## 4. `bi-` adayları

Otomatik taramada fiilden hemen sonra **163** açık `bi-` adayı vardır.

İlk hedef dağılımında öne çıkanlar:

- Allah kökü (`Alh`): **64**
- ahiret/son (`Axr`): **13**
- `mā` relative/clausal hedef: **12**
- Rabb (`rbb`): **9**
- ayet (`Ayy`): **9**
- resul (`rsl`): en az **2** doğrudan komşu örnek
- gayb (`gyb`): doğrudan örnek
- kitap (`ktb`): doğrudan örnek

Ayrıca çok sayıda `bihi / bihā` zamirli kullanım vardır; bunların antecedentleri ayrıca çözülmeden hedef dağılımına kesin kategori verilemez.

Bu nedenle `bi-` katmanı bir sonraki aşamada **hedef türü + zamir çözümü** ile ayrıca incelenecektir.

## 5. `an / inna` adaylarının kontrolü

Otomatik komşuluk taraması **21** aday üretti; fakat bunların büyük çoğunluğu gerçek tamamlayıcı değildir. Örneğin:

- `alladhīna āmanū in...` ardından gelen şart cümlesi,
- `alladhīna āmanū inna...` ardından başlayan yeni açıklama,
- başka bir fiilin yönettiği `an` cümlesi

yalnızca yüzeyde `āmana` kelimesinden sonra gelir.

**10:90** ise açık bir doğrudan önerme örneğidir:

`āmantu annahu lā ilāha illā ...`

Yani `āmana` fiili yalnız kişi ilişkisi kurmaz; bir önermenin doğruluğunu kabul etme/ona güven bağlama içeriği de alabilir.

Bu karşı örnek önemlidir: 'iman yalnız kişiye güvenmektir' şeklindeki dar bir tanım da yanlış olur.

## 6. Şimdiki sentaktik sonuç

İnanma/tasdik bağlamlarıyla sınırlı çalışma sonucu:

> `Āmana` kullanımları kişiye, ilahî merciye, bildirime veya önermeye yönelebilir; **doğru/güvenilir kabul etme, inanma ve güven** okumalarının kapsamı bağlamla belirlenir. 106:4'teki güvenlik sağlama kullanımı bu alt anlamın dışında, aynı morfolojik kümenin içindedir.

Dolayısıyla şu daraltmaların sınırları vardır:

1. **'İman sadece bir şeyin var olduğunu kabul etmektir.'** — 9:61 ve 12:17'de sözün inanılır bulunması ayrıca açıklanmalıdır. Bu tespit, haber tasdikini dışlamaz.
2. **'İman sadece kişiye güvenmektir.'** — 10:90 gibi doğrudan önerme içeriği bunu aşar.
3. **'IV. bâbın bütün fiilleri inanmak demektir.'** — 106:4 güvenlik sağlama karşı örneğidir.

Daha uygun çalışma hipotezi:

> **İnanma bağlamlarında bir merciyi, kişiyi, bildirimi veya önermeyi doğru/güvenilir kabul etmek; güven ve bağlılık boyutlarını bağlamın desteklediği ölçüde değerlendirmek.**

Bu hâlâ nihai sözlük tanımı değildir. **Durum: Destekleniyor, bu sınırlı kapsamda; derece: Muhtemel.** Güven vurgusunun tasdik okumasını her örnekte geçtiği gösterilmiş değildir.

## 7. Sonraki falsifikasyon

Bir sonraki aşamada 163 `bi-` adayı çözülecek:

- Allah / Rabb
- resul / kişi
- kitap / ayet / vahiy
- gayb / ahiret
- `mā` ile başlayan bildirimler
- `bihi / bihā` zamirlerinin antecedentleri

Amaç, `bi-` ile kurulan bağın 'nesneye inanmak', 'sözü doğrulamak', 'güven bağlamak', 'bağlanmak' gibi seçeneklerden hangisini hangi bağlamlarda zorunlu kıldığını belirlemektir.

## 8. Kavramlar arası aktarım sınırı

İmanın tevekkülle aynı ayette yer alması, kelimelerin aynı veya kesinlikle ayrı anlamlara geldiğinin tek başına kanıtı değildir. Tamlayıcı, özne, fiil yapısı ve eylem bağlamı karşılaştırılmalıdır. 3:159 danışma ve kararı tevekkülle birlikte korur; bundan iman–eylem–tevekkül için zorunlu ve birbirini dışlayan zaman aşamaları çıkmaz. Ayrıntılı değerlendirme ve 40:44'teki tafvîz karşılaştırması [Tevekkül–Vekîl analizindedir](Tawakkul-Wakil-analysis.md).

## v1.1 düzeltme kaydı — 2026-10-11

- **537 inanma kullanımı → 537 IV. bâb fiil kelime konumu:** 106:4 morfoloji/anlam ayrımının karşı örneği olarak eklendi; doğrulanmamış semantik sayı verilmedi.
- **Kişi hedefi tasdiki çürütür → kişinin sözünü tasdik etmeyi dışlamaz:** 9:61'in iki güçlü okuması birlikte taşındı.
- **12:17 fiil gibi kullanılabilir → ism-i fâil karşılaştırması:** finite fiil ve fiil + li- sayılarına dahil edilmedi.
- **Genel güven tanımı → inanma bağlamlarıyla sınırlı hipotez:** güvenlik sağlama anlamı ayrı tutuldu; birlikte geçişten kesin anlam hükmü çıkarılmadı.

Denetim: [QAC karşılaştırma raporu](../generated/tawakkul_comparison/report.md). Bu sürüm yeni bir Kur’an öncesi veya Sâmî tarama içermez; bu katmanlardan sonuç taşınacaksa [Aşama 1'deki kaynak sınırları](Amn-quran-internal-stage1.md) geçerlidir. Eski sentaks tablosu bir **yüzey komşuluğu** taramasıdır; bu düzeltmeler bütün 537 örneğin semantik olarak yeniden etiketlendiği anlamına gelmez.
