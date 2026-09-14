# أ م ن / Amn — Kur'an içi analiz, Aşama 2: `āman(a)` sentaksı

**Durum:** Ara sonuç. Nihai sözlük tanımı değildir.

Kaynak zinciri: sabit QAC v0.4 → ham morfoloji + `qac_word_annotations.csv` → `analyze_amn_verb_syntax.py` → manuel kritik-vaka kontrolü.

## 1. İncelenen fiil ailesi

QAC lemma `'aAmana` altında **537** fiil kullanımı vardır.

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

Bu kullanım kümesi yalnız 'bir önermenin doğruluğuna zihnen inanmak' şeklinde açıklanamaz. Fiil açıkça **bir kişiyi güvenilir/doğru kabul etme, onun sözüne güvenme/itimat etme** ilişkisine girebilmektedir.

## 3. En güçlü iç karşılaştırma: Tevbe 9:61

Aynı ayette, aynı özne ve aynı fiil iki farklı edatla kullanılır:

- `yuʾminu bi-llāh`
- `wa-yuʾminu li-l-muʾminīn`

İkinci ifade müminleri 'ilahî inanç nesnesi' yapmaz. Bağlamda elçinin insanlar hakkında söylenene kulak vermesi eleştirilmektedir; `yuʾminu li-l-muʾminīn` doğal olarak **müminlere güvenmesi / onların sözünü güvenilir bulması** alanındadır.

Bu ayet, `ʾ-m-n` fiil ailesinin ilişkisel **güven/itimat** bileşenini Kur'an'ın kendi içinde doğrudan görünür kılan en güçlü testlerden biridir.

Bu, `āmana bi-llāh` ifadesinin mekanik olarak yalnız 'Allah'a güvenmek' diye çevrilmesini tek başına ispatlamaz; `bi-` ile `li-` aynı sentaktik işlev değildir. Fakat fiilin çekirdeğinin salt 'zihinsel inanç' olmadığını güçlü biçimde gösterir.

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

Kur'an içi verinin şu aşamada izin verdiği en dar sonuç:

> `āmana` bir **güven / doğrulama / güvenilir kabul etme ilişkisi** kurar; bu ilişki kişiye, ilahî merciye, bildirime veya önermeye yönelebilir.

Dolayısıyla iki aşırı tanım da veriyi tam karşılamaz:

1. **'İman sadece zihinsel inanıştır.'** — kişi hedefli `li-` kullanımları bunu aşar.
2. **'İman sadece kişiye güvenmektir.'** — 10:90 gibi doğrudan önerme içeriği bunu aşar.

Daha uygun çalışma hipotezi:

> **Bir merciyi, kişiyi, bildirimi veya önermeyi güvenilir/doğru kabul ederek ona güven bağlamak.**

Bu hâlâ nihai sözlük tanımı değildir.

## 7. Sonraki falsifikasyon

Bir sonraki aşamada 163 `bi-` adayı çözülecek:

- Allah / Rabb
- resul / kişi
- kitap / ayet / vahiy
- gayb / ahiret
- `mā` ile başlayan bildirimler
- `bihi / bihā` zamirlerinin antecedentleri

Amaç, `bi-` ile kurulan bağın 'nesneye inanmak', 'sözü doğrulamak', 'güven bağlamak', 'bağlanmak' gibi seçeneklerden hangisini hangi bağlamlarda zorunlu kıldığını belirlemektir.
