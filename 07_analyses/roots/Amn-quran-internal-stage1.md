# ʾ-m-n / Amn — Kur'an içi analiz, Aşama 1

**Durum:** Ön sonuç. Bu dosya nihai sözlük tanımı değildir.

**Sürüm:** v1.1 — 2026-10-11. Lemma gruplarının sayıları, anlam sınıflarının sayıları olarak okunmamalıdır.

Kaynak: sabit QAC v0.4 → `qac_word_annotations.csv` → otomatik `Amn` root profile.

## 1. Dağılım

QAC `Amn` kök etiketi:

- **879** kök taşıyan ortografik kelime konumu
- **723** ayet
- **77** sûre
- **558** fiil / **290** isim / **31** sıfat etiketi

Ana lemma dağılımı:

| lemma ailesi | kelime konumu | biçim / inceleme alanı |
|---|---:|---|
| `'aAmana` | 537 | IV. bâb āman(a) / yuʾminu fiil ailesi; 106:4 güvenlik sağlama kullanımı dahildir |
| `mu&omin` | 202 | muʾmin |
| `<iyma`n` | 45 | īmān |
| `m~u&omina`t` | 22 | muʾmināt |
| `>amina` | 20 | amina: güven içinde olmak / güvenmek |
| `>amiyn` | 14 | amīn: güvenilir |
| `'aAminiyn` | 10 | āminīn: güven içinde olanlar |
| `'aAmin` | 6 | āmin: güvenli / emniyetli |
| `m~u&ominap` | 6 | muʾmina |
| `>amon` | 5 | amn: güvenlik/emniyet |
| amāna / amānāt ve amana | 8 | emanet bildiren lemma biçimleri 6; `>amanap` güvenlik biçimi 2; tek anlam sınıfı değildir |
| diğer tekil türevler | 4 | maʾman, maʾmūn, utumina vb. |

Toplam = **879**.

## 2. Üç lemma grubu; anlam sayımı değil

Önceki sürümdeki **812 / 44 / 23**, lemma/biçim üyeliğine göre yapılmış analitik gruplamanın kelime konumu toplamlarıdır. Bunlar “güven bağlama / güvenlik / emanet” anlamlarının tek tek doğrulanmış sayıları değildir. Payda 879 kök kelime konumudur; yüzdeler yalnız bu biçim gruplarının payıdır. Gruplar QAC'ın semantik etiketleri değildir.

### A. `āman(a) / īmān / muʾmin` lemma grubu — 812 kelime konumu (%92,38)

Bu grup `āman(a)`, `muʾmin`, `īmān`, `muʾmināt`, `muʾmina` biçimlerini kapsar.

Bu biçimler çoğu bağlamda “inanmak / iman etmek / mümin / iman” diye çevrilir; fakat bu çeviriler grubun bütününü tek bir anlam sınıfına dönüştürmez. **106:4:5** *wa-āmanahum*, aynı IV. bâb fiil kümesinde olup korkuya karşı güvenlik sağlamayı anlatır. Dolayısıyla 537 IV. bâb fiilin tümü “iman etmek”, bu grubun 812 konumunun tümü “güven bağlama” diye sayılamaz. Yeni semantik toplam için her kullanımın bağlamı ayrıca kodlanmalıdır.

**12:17:14** *bi-muʾminin* bu grubun ism-i fâil kullanımıdır (`N`, IV. bâb); kardeşlerin anlattığına inanmakla ilgilidir. 537 çekimli fiile eklenmez ve tek başına dinî sadakat anlamını gerektirmez.

Önemli sentaktik örnekler:

- 2:3 — `yuʾminūna bi-l-ghayb`
- 2:4 — `yuʾminūna bi-mā unzila...`
- 2:8 — `āmannā bi-llāh...`
- 2:13 — `āminū kamā āmana al-nās`

Bu fiilin nesne/merci ile kurduğu ilişkinin daha sonra ayrıca `bi-`, `li-` ve çıplak kullanım açısından taranması gerekir.

### B. `amina / āmin / amn` ve ilgili lemma grubu — 44 kelime konumu (%5,01)

Bu grup `amina` (20), `āminīn` (10), `āmin` (6), `amn` (5), `āmina` (1), `maʾman` (1) ve `maʾmūn` (1) kelime konumunu kapsar. Böylece 44 sayısının lemma üyeliği açıktır; anlam sınırları aynı listeden otomatik türetilmez.

Korpus örnekleri:

- 2:196 — `fa-idhā amintum`: güvenli duruma geldiğinizde
- 2:239 — `fa-idhā amintum`: güvene kavuştuğunuzda
- 2:283 — `fa-in amina baʿḍukum baʿḍan`: biriniz diğerine güvenirse
- 3:75 — `in taʾmanhu...`: ona ... emanet/güven verirsen
- 7:97 — `a-fa-amina ahlu l-qurā`: halk kendini güvende mi sandı?
- 2:126 — `baladan āminan`: güvenli bir belde
- 15:46 — `udkhulūhā ... āminīn`: güven içinde girin

Bu grupta güvenlik örnekleri yanında 2:283 ve 3:75 gibi kişiler arası güven/emanet bağlamları da vardır. “44 güvenlik kullanımı” sonucunu morfolojik üyelikten çıkarmak bu yüzden de geçersizdir. Kök ailesinin bu genişliği, tek bir türevin bağlama özgü tasdik anlamını dışlamaz.

### C. `amīn / amāna / amana / utumina` lemma grubu — 23 kelime konumu (%2,62)

Bu eski grup `amīn` (14), `amāna/amānāt` biçimleri (6), `>amanap` (2) ve `utumina` (1) kelime konumunu birleştirir. `>amanap` güvenlik alanındadır; bu nedenle 23 sayısını “emanet/güvenilirlik anlamı” toplamı diye okumak da yanlıştır. Gruplama burada önceki hesabın izini korur; yeni bir semantik tasnif önermez.

Korpus örnekleri:

- 7:68 — `nāṣiḥun amīn`: güvenilir bir öğütçü
- 12:54 — `makīnun amīn`: güvenilir
- 26:107 ve tekrarları — `rasūlun amīn`: güvenilir elçi
- 26:193 — `al-rūḥ al-amīn`: güvenilir ruh
- 2:283 bağlamı — güvenme ve emaneti yerine getirme aynı ayet ağı içinde buluşur

Bu örnekler güvenilirlik, güvenme ve emanet arasındaki anlam ilişkisini araştırmaya yarar; üç terimin özdeşliğini veya zorunlu bir zaman sırasını kanıtlamaz.

## 3. Şimdilik çıkan ortak çekirdek

Kök ailesi için incelenebilecek ortak anlam alanı hipotezi şudur:

> **güven / güvenilirlik / güvenlik ekseni**

Bir tarafın güvenilir görülmesi, ona güvenilmesi, güvenlik ve emanet ilişkileri arasında bağlantı aranabilir. Her biçimin bu bağlantıların tamamını içerdiği veya güvenmenin her durumda güvenlik doğurduğu ileri sürülmez.

“Kök ailesinin tamamı yalnız inanmak demektir” genellemesi 106:4 gibi güvenlik bağlamlarını karşılamaz. Fakat bundan “īmān tasdik anlamına gelemez” sonucu çıkmaz: kök ailesi ile tek bir kelimenin anlam kapsamı farklıdır. “Güven/güvenilir kabul etme” önerisi tasdik okumasının güçlü biçimleriyle birlikte sentaks ve bağlamda sınanmalıdır.

Fakat bu henüz nihai tanım değildir.

## 4. Falsifikasyon şartı

Hipotezi doğrulamış saymak için yalnız etimolojik/kök akrabalığı yeterli değildir. Özellikle şu sorular cevaplanmalıdır:

1. `āman(a)` fiilinin bütün sentaktik kalıpları güven ilişkisiyle açıklanabiliyor mu?
2. `āmana bi-` ile `āmana li-` arasında işlevsel fark var mı?
3. İnsanlara yönelen kullanımlarda kişinin sözünü doğru kabul etme ile güvenme ayrılabiliyor mu; 9:61 ve 12:17 iki okumadan birini gerçekten dışlıyor mu?
4. `īmān` ile `kufr` karşıtlığında güven açıklaması bağlamların tümünde çalışıyor mu?
5. “İman artması” ayetlerinde artan şey zihinsel kanaat mi, güven bağı mı, yoksa daha geniş bir bağlılık durumu mu?
6. Güven hipotezini bozan açık bir ayet var mı?
7. IV. bâbın 106:4’teki güvenlik sağlama anlamı, önerinin hangi biçimlere ve hangi anlam alt kümesine uygulanacağını nasıl sınırlar?

Bu sorular çözülmeden nihai sözlük tanımı yazılmayacaktır.

## 5. Sami katmanının rolü

Sâmî karşılaştırma yalnız **ikincil hipotez katmanıdır**. İbranice ve Aramice/Süryanice benzerlikleri bağımsız anlam doğrulaması sayılamaz; ortak dil geçmişi ve kognatın zaman içinde anlam değiştirebilmesi hesaba katılmalıdır. Bu sürüm yeni bir kognat taraması veya Kur’an öncesi Arapça tanık incelemesi yapmaz. Kur’an öncesi anlam ya da Kur’an’la gerçekleştiği öne sürülen anlam değişimi için tarihlenmiş, aidiyeti ve aktarımı incelenmiş tanık gerekir; sonraki sözlük/Lane tanımı tek başına yeterli değildir.

## Sonraki aşama

`āman(a)` fiilinin **sentaks taraması**:

- `āmana bi-`
- `āmana li-`
- çıplak / nesnesiz kullanım
- insan, Allah, ayet/kitap, gayb, resul vb. hedef türleri
- özellikle “güvenmek” ile “bir önermeyi doğru kabul etmek” okumalarının ayrıldığı test ayetleri

## v1.1 düzeltme kaydı — 2026-10-11

- **812 / 44 / 23 semantik sınıf → lemma/biçim grubu:** eski sayıların yeni bir anlam sayımı olmadığı açıklandı; bunların yerine doğrulanmamış başka semantik sayılar konmadı.
- **8 emanet türevi → 6 amāna/amānāt + 2 `>amanap`:** eski toplamdaki biçimler ayrıldı; güvenlik biçiminin emanet anlamına otomatik dahil edilmesi kaldırıldı.
- **IV. bâb = inanmak → biçim ile anlam ayrı:** 106:4 güvenlik sağlama karşı örneği eklendi.
- **12:17 iman fiili örneği → IV. bâb ism-i fâil:** fiil sayımına eklenmemesi belirtildi.
- **Kök genişliği tasdiki dışlar → kök/kelime kapsamları ayrı:** güven hipotezi, haber tasdiki okumasını peşinen elemez.
- **Sâmî destekleyici kontrol → ikincil hipotez:** bağımsızlık ve Kur’an öncesi tanıklık sınırları kaydedildi.

Kaynaklar: [QAC 106:4:5](https://corpus.quran.com/wordmorphology.jsp?location=(106:4:5)), [QAC 12:17](https://corpus.quran.com/wordbyword.jsp?chapter=12&verse=17), [yeniden üretilebilir karşılaştırma raporu](../generated/tawakkul_comparison/report.md). Morfolojik tespitler annotation bulgusudur; ortak anlam çekirdeği **muhtemel bir çalışma hipotezidir**, bütün kullanımlar için doğrulanmış tanım değildir. İman–tevekkül karşılaştırması: [Tevekkül–Vekîl](Tawakkul-Wakil-analysis.md).
