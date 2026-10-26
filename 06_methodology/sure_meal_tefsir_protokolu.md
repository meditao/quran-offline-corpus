# Sûre Meal–Tefsir Bütünleşik Çalışma Protokolü — v1.2

**Tarih:** 2026-10-26 (v1.1: 2026-10-09)  
**Konum:** 06_methodology/sure_meal_tefsir_protokolu.md  
**Kapsam:** Bir sûrenin veya kendi içinde bağlantılı pasajın, tek çalışma talebiyle dilsel analizi, her ayet için iki bağımsız çevirisi (kavram merkezli ve anlam merkezli), her ayette bilimsel kontrolü, Kur'an içi ilişkileri ve bütünleşik tefsiri.

**Sürüm notu (v1.2):** "Tek ana çeviri + gerekirse tefsirli çeviri" düzeni kaldırıldı; yerine [kavramsal_ceviri_ilkesi.md](./kavramsal_ceviri_ilkesi.md) §1'deki iki bağımsız çeviri geldi. Bilimsel kontrol isteğe bağlı olmaktan çıktı, her ayette zorunlu oldu (`analiz_protokolu.md` Aşama 8a). Meal ve tefsir anlam kurulurken okunmaz; kendi çeviri yazıldıktan sonra karşılaştırma için açılabilir (§2.6).

Bu belge **uygulama protokolüdür**. Ana araştırma standardı olan [analiz_protokolu.md](./analiz_protokolu.md) ve [kavramsal_ceviri_ilkesi.md](./kavramsal_ceviri_ilkesi.md) yürürlükte kalır. Kaynak politikası, sayım birimleri, hipotez sınaması, falsifikasyon ve delil dereceleri bu belgelerden devralınır. Çatışmada kaynak/doğrulama disiplininden taviz verilmez; sûre çalışmasının **iş ritmi ve çıktı biçimi** için bu belge uygulanır.

## 1. Amaç ve tek çalışma döngüsü

Amaç geleneksel okumaya uymak veya ondan farklılaşmak değil, metnin söyleyebildiği anlamı dilsel ve Kur'an içi delillerle belirlemek; bunu anlaşılır Türkçeyle aktarmak; ayetlerin birbirini hangi gerekçeyle açıkladığını göstermek ve yorumu metnin izin verdiği sınırda tutmaktır.

**Tek aşamada çalışma = analizin tek adımla kestirilmesi değildir.** Bir istekle aşağıdaki denetim zinciri bütünüyle çalışır; her teknik aşamanın sonunda kullanıcıdan ayrıca «devam» istenmez. Uygulama, gerektiğinde önceki adıma geri döner. Kullanıcıya teknik ham döküm değil, denetlenmiş çeviri ve gerekli açıklamalar sunulur. Kullanıcı açıkça ayrıntılı analiz istediğinde teknik kayıt görünür kılınır.

Analiz edilecek kapsam ile kullanıcıya aynı mesajda sunulabilecek kapsam ayrılır: uzun sûrelerde çıktı doğal pasaj sınırlarında bölünebilir. **Henüz kontrol edilmeyen ayetler kontrol edilmiş gibi gösterilmez.** Bir sûre «tamamlandı» denmeden önce tüm ayetlerin ve sûrenin bütünlüğünün denetimi yapılır.

## 2. Kaynak hiyerarşisi ve doğrulama dürüstlüğü

1. **Metin:** Depodaki Tanzil Uthmani v1.1 (çalışmanın esas aldığı Hafs metin düzeni). Metin değiştirilmez; önemli kıraat farkı biliniyor ve sonucu etkiliyorsa ayrıca not edilir. Kapsamlı kıraat taraması yapılmadıysa yapıldığı söylenmez.
2. **Dilsel çözümleme:** QAC v0.4 kök, lemma ve morfoloji için kanonik yardımcı anotasyondur. Bu anotasyon **Arapça metnin kendisi değil, yanılabilen insan çözümlemesidir**. Tartışmalı sentaks ve kelime çözümlemesi ayrıca sorgulanır.
3. **Korpus içi karşılaştırma:** Aynı lemma, kalıp, sentaks, deyim, yakın/karşı kavramlar ve ilgili pasajlar araştırılır. Sayılar ancak fiilen çalıştırılmış sorgu ve sayım birimiyle verilir. Kök ≠ lemma ≠ kelime konumu ≠ segment.
4. **Çapraz kontrol:** İkinci QAC kökenli morfoloji katmanı bağımsız doğrulama sayılmaz. Bağımsız bir kaynak yoksa yokluğu belirtilir; kaynaklar arasında ihtilaf elle değerlendirilir.
5. **Dış dil bilgisi:** Arapça sözlük ve tarihsel kullanım, Lane, diğer Sâmî diller, gerektiğinde tarihsel bağlam, dilsel olasılıkları aydınlatan veya hipotez üreten **yardımcı** katmandır. Dinî hüküm otoritesi değildir. Sözlük yok sayılmaz; kök etimolojisi bağlamda geçerli anlam yerine konmaz.
6. **Mealler, hadisler, mezhebî ve tefsir gelenekleri:** İlk anlamın delili veya hüküm kaynağı yapılmaz. **Anlam kurulurken okunmaz;** başka bir meal (ör. karşılaştırma meali) ancak iki çeviri yazıldıktan sonra açılır ve açıldığı kayda geçer. Alternatif/geleneksel okumalar ancak Arapça dil ve metin içi verilerle karşılaştırılmak üzere, gerektiğinde ayrı değerlendirilir; kullanıcı sormadıkça "geleneksel" diye adlandırılmaz ve kaynağı yazılmaz (`analiz_protokolu.md` Aşama 6).

Kaynak erişimi yoksa «tam tarama», «bağımsız doğrulandı», «korpusla kanıtlandı» gibi ifadeler kullanılmaz. Çalışma kaydı: kaynak sürümü; kullanılan ayet aralığı; sorgu/komut; sayım birimi; çalıştırıldı/önceki çıktı/çalıştırılmadı. Sayısal iddia gerekiyorsa ana protokolün kayıt ve yeniden üretim kuralları geçerlidir.

## 3. Tek döngünün sıralı iç işlemleri

### A. Sûrenin önce bütün olarak okunması

- Sûrenin ayet sırası, seslenişleri, konuşan/muhatap değişimleri, zamir zincirleri, konu sürekliliği, soru-cevap, şart/istisna, tekrar ve karşıtlıklar haritalanır.
- Çalışılacak **pasaj birimleri**, dışarıdan hazır bölüm adlarıyla değil; hitap, konu, bağlaç, zamir, gerekçe-sonuç ve geçiş işaretleriyle belirlenir. Gerekirse sınırlar sonraki incelemeyle düzeltilir.
- Metnin kendi içindeki zaman, hafifletme, değişiklik, istisna ve hüküm ilişkileri korunur. İniş sırası veya tarihsel olay uydurulmaz.
- Sûrenin beklenen ana fikri **kesin yorum olarak önden kilitlenmez**; araştırmanın geçici okuma sorusu olarak kalır.

### B. Ayetlerin tek tek dilsel çözümlemesi

**Pasaj birlikte, ayetler ayrı analiz edilir.** Her ayetin bütün kelimeleri okunur; sonucu etkileyen kelime ve yapılar derinlemesine incelenir:

- Metin, kelime biçimi, kök ve lemma; fiil babı/kip/çatı/kişi, isim hâli/belirliliği ve bağlı edatları;
- özne-yüklem-nesne, tamlama, hâl, sıfat, atıf, şart, olumsuzluk, istisna ve gönderim zinciri;
- cümlenin doğal Arapça dizimi, deyim ve kalıplar, ellipsis/takdir ihtimali;
- sözlük çekirdeği → sentaktik anlam → bu cümledeki bağlamsal karşılık; **sonradan oluşmuş teknik anlam** bunlardan ayrılır;
- gerçekten mümkün rakip dilsel çözümlemeler ve metnin zorunlu kılmadığı yorumlar.

Kök bilgisi tek başına karşılık seçtirmez. Aynı kök tek anlam zorunluluğu taşımaz; aynı konuya ait iki kelime de otomatik eşanlamlı değildir. Sözcüğün hükmü, işlevi, davranışsal sonucu onun sözlük anlamı diye sunulmaz.

### C. Üç ölçekli bağlam ve Kur'an içi bağlantı

1. **Yakın bağlam:** Önceki/sonraki ayet, konuşan, muhatap, referanslar, istisna ve gerekçeler.
2. **Sûre bağlamı:** Aynı sûredeki ilgili pasajlar, tekrarlar, karşıtlıklar, ilerleyen anlatı ve sonuç.
3. **Kur'an bütünü:** Gerçekten aynı ifadeyi, yapıyı, kavramı veya durumu açıklayan diğer kullanımlar; ayrıca aykırı ve sınırlayıcı örnekler.

Bir ayetin ötekini açıklaması **kanıtlanması gereken bağlantı iddiasıdır**. Aynı kökün geçmesi veya düşünsel çağrışım yetmez. İç bağlantılar şu sınıflarla kaydedilir:

- **Doğrudan/açık:** Açık atıf, açıklama, tanım, aynı olayın devamı veya belirtilmiş gerekçe.
- **Güçlü yapısal paralel:** Ayırt edici kalıp/benzer şart-muhatap-nesne ve anlamı netleştiren tamamlayıcı ifade.
- **Tematik paralel:** Konu benzer, fakat anlamı tek başına belirlemez; yardımcıdır.
- **Serbest çağrışım:** Açıklayıcı delil değildir; gerektiğinde yalnız nottur.

Önemli her bağlantı için **bağlantı fişi** tutulur: iki ayet, paylaşılan somut ifade/yapı, konuşan-muhatap ve şart farkı, bağın türü, hangi anlam sonucuna izin verdiği, hangi sonuca **izin vermediği**, güven düzeyi. Farklı konular veya şartlar altında söylenen iki ifade zorla birleştirilmez.

### D. Aday anlam, karşı delil ve karar

- Her kritik ifade için en az iki makul aday varsa ikisi de belirlenir; adayın gramer ve bağlam dayanağı açıkça sınanır.
- Dışarıdan ödünç alınmış yaygın okuma ile bizim önerdiğimiz okuma aynı ölçütlerden geçirilir. Sırf geleneksel diye reddedilmez; sırf yeni diye seçilmez.
- Metindeki karşı örnek, negatif semantik sınır ve alternatif zamir/sentaks okuması aranır. **Yalnız uyumlu** örnek, **kanıtlayıcı** sayılmaz.
- Kavramın genel anlamına ilişkin yeni tez kuruluyorsa ana protokolün hipotez kilidi ve uygun olduğunda önceden ayrılmış kapalı örneklem ilkeleri uygulanır; tüm örnekler görülmüşse sonradan kör test yapılmış gibi davranılmaz.
- Delil yetersizse tek anlama zorlama yapılmaz. Birden fazla makul karşılık **gerçekten** kalıyorsa çeviride ikisini temsil etme (örneğin «Kur'an/okuyuş») veya kısa notla alternatif belirtme mümkündür. Buna karşılık kararı mümkün olan yerde gereksiz ikileme yapılmaz.
- Karar kaydı: tercih edilen karşılık; elenen/rakip karşılık; hangi dilsel ve iç bağlamsal kanıt; açık karşı delil; sonucun sağlam/muhtemel/spekülatif derecesi. Açık ihtimal kesin tefsire dönüştürülmez.

### E. Çeviri: her ayette iki bağımsız çeviri

Tanımlar [kavramsal_ceviri_ilkesi.md](./kavramsal_ceviri_ilkesi.md) §1'dedir. İki çeviri birleştirilmez; biri ötekinin açıklaması değildir.

**1 — Kavram merkezli çeviri (her ayette)**

- Terimler Kur'an içi ilişki ağından çıkar; karşılıklar D'deki karar kaydına ve sûrenin **kavram tablosuna** dayanır (kavram · karşılık · dayanak · derece).
- Bağlamdan gelen her ekleme **[ ]** içinde yazılır; köşeli ayraç dışındaki her kelimenin karşılığı ayette vardır. Yazarın çıkarımı ayetin ağzından kesin bilgi diye söyletilmez.
- Geniş anlamlı veya tartışmalı kavram tablodaki karşılıkla verilir; **özgün Arapça kavramın Türkçe okunuşu gerektiğinde ilgili ifadenin sonunda parantez içinde** gösterilir. Bir terimi aynen korumak ancak Türkçe karşılık önemli anlam ihtimallerini yok ediyorsa tercih edilir; gerekçe tabloda tutulur.
- Ayetler farklı görünse de paralel ifadelerde terim tutarlılığı denetlenir; bağlamın gerçekten gerekçelendirdiği değişken karşılıklar korunur. Tekdüzelik uğruna anlam bozulmaz.

**2 — Anlam merkezli çeviri (her ayette)**

- Birim cümle ve iletidir. Sade, açık, akıcı, **doğal Türkçe** kullanılır. Mekanik kelime sırası ve Türkçede anlaşılmayan harfî deyim kullanılmaz; deyim anlamıyla verilir.
- Kavram tablosuna bağlı değildir; kendi ölçütüyle kurulur.
- Açıklanmayan yeni olay, muhatap, kesin sonuç, tarih ve hüküm eklenmez. Açıklama ayrı bir çıkarımsa çeviriye gizlice sokulmaz; pasaj sonu tefsirinde delil seviyesiyle verilir.

**Her iki çeviride:** bir ayetin şartı, olumsuzluğu, istisnası ve kapsamı mutlaka görünür kalır. İki çeviri her ayette yan yana denetlenir: atlanan, fazladan eklenen, kapsamı daraltılan veya genişletilen unsurlar gözden geçirilir. Anlam merkezli çevirinin kavram kararlarından ayrılması hata değildir; ayetin söylemediği bir hükmü söylemesi hatadır. Sadece dilsel alternatifleri karşılaştırmak gerekiyorsa bunlar kısa **dikkat noktasında** gösterilir.

**3 — Bilimsel kontrol (her ayette)**

Ayetin anlattığı olgunun bilimdeki karşılığı aranır ve ayrı satırda verilir: ilişkinin türü (çağrışım / modern paralellik / açıklama ihtimali), bilimsel tarafın derecesi (yerleşik / tartışmalı / öncü-spekülatif) ve gerçekten bulunmuş künye. Bilim kelimenin anlamını belirlemez; çevirinin içine karıştırılmaz. Çağrışım yoksa "belirgin bir bilimsel çağrışım bulunmadı" yazılır (`analiz_protokolu.md` Aşama 8a).

### F. Bağlantılı pasajın tek bütünleşik tefsiri

- Ayetler arasındaki bağlam birimi tamamlanınca, **her ayetin altına dağınık yorum yazmak yerine** bir defa, kısa ve bütünleşik bir açıklama sunulur.
- Tefsir «önceki ayet ne koydu → sonraki ayet nasıl geliştirdi/sınırladı → pasajın çıkarımı ne» ilişkisini açıkça kurar.
- Yorumun dayanağı bağlantı fişidir. Açık ifade, güçlü çıkarım ve açık ihtimal birbirinden ayrılır.
- Çevirilerin uzun tekrarı yapılmaz. Metinde olmayan tarihsel hikâye, zorlama sembol, psikolojik/nörobilimsel spekülasyon veya mezhebî hüküm tefsire eklenmez. Bilimsel bağlantı tefsirin içine karıştırılmaz; E.3'teki bilimsel kontrol satırında, statüsüyle durur.

### G. Çift yönlü yeniden denetim

- **Ayet → sûre:** Tek tek seçilen karşılıklar pasajı ve sûrenin gelişen anlamını bozuyor mu?
- **Sûre → ayet:** Sûre hakkındaki genel ön yorum, açık ayet lafzını bastırıyor mu? Bastırıyorsa önce genel yorum düzeltilir; ayet zorlanmaz.
- Sûre genelinde tekrar eden kavramlar, zamirler, hikâye kronolojisi, benzer emir/istisnalar, hüküm kapsamı ve üslup tek tek kontrol edilir. Çelişki iddiası aynı muhatap, şart, zaman ve önerme düzleminde sınanır.
- Bağımsız ikinci bir okuma yapılabiliyorsa tercih nedenleri gizlenmeden kaydedilir. Teknik sorun çözülmüyorsa «geçici / belirsiz» yazılır.

## 4. Kullanıcıya varsayılan sunum

**Sûre başında:** Gerekirse yalnız kısa bir «okuma anahtarları» paragrafı. Uzun kavram sözlükleri tekrar edilmez.

**Her doğal pasajda:**

1. Ayet numaraları korunur; her ayet şu sırayla verilir: **okunuş → kavram merkezli çeviri → anlam merkezli çeviri → bilimsel kontrol.** Sûrenin kavram tablosu sûre başında ya da ilk geçtiği pasajda bir kez verilir; sonraki ayetlerde yalnız değişen karar gösterilir.
2. Pasaj sonunda yalnız bir **kısa bütünleşik tefsir** verilir. Gerçek anlam farkı yaratan tartışmalı kelime/bağlantı için ayrıca **dikkat noktası** eklenebilir.
3. İstenmediği sürece tüm morfoloji tabloları, kök frekansları ve karar fişleri ana sunuma dökülmez. Ancak kritik çeviri tercihi kullanıcıca sorgulanınca delili ve alternatifleri denetlenebilir biçimde açıklanır.

**Sûre sonunda:** Ayet atlaması, pasaj bütünlüğü ve terim uyumu kontrol edilir; sûrenin ana düşüncesi kısa ve **delil sınırını aşmayan** bir sentezle yazılır. İstenirse iki çevirinin her biri ayrı ayrı tek yerde toplanabilir; iki çeviri o zaman da birleştirilmez.

**Özel istek önceliği:** Kullanıcı yalnız çeviri, okunuş, ayrıntılı analiz veya sırf devam istediğinde görünür çıktı buna göre uyarlanır; **iç kontrol disiplini değişmez**.

## 5. Zorunlu kalite kapısı — yayımlamadan önce

Aşağıdaki kontrollerden biri kritik düzeyde başarısızsa ilgili ayet/pasaj «nihai» sayılamaz; düzeltme veya **dürüst belirsizlik kaydı** gerekir:

- [ ] Arapça esas metin, ayet referansı ve kıraat/metin kapsamı sabit mi?
- [ ] Her ayet ve özellikle kritik kelimeler ayrı dilsel çözümlemeden geçti mi?
- [ ] Kökten mekanik anlam türetme, lemma/kök veya biçim/sözlük karışıklığı var mı?
- [ ] Cümle öğeleri, zamir mercileri, deyim, şart, olumsuzluk ve istisna doğru korundu mu?
- [ ] Pasaj sınırı ve yakın/sûre/Kur'an bütünü bağlamı gerekçeli mi?
- [ ] «Bu ayet ötekini açıklar» iddiası salt benzerlikten değil, **somut metinsel ilişkiden** mi çıktı?
- [ ] Karşı örnek ve rakip okuma sınandı; «uyumlu» ile «kanıtlayıcı» ayrıldı mı?
- [ ] Birden fazla ciddi anlam kalıyorsa çeviri bunları dürüstçe temsil ediyor mu?
- [ ] Kavram merkezli çeviride her ekleme [ ] içinde mi; ayetin söylemediği yorum kesin söz olarak eklendi mi?
- [ ] Kavram tablosundaki her karşılığın dayanağı ve derecesi yazıldı mı?
- [ ] Anlam merkezli çeviri doğal Türkçe mi; ayetin söylemediği bir hüküm, olay veya muhatap ekliyor mu?
- [ ] İki çeviri ayrı mı tutuldu, birleştirilmedi mi; bütün önemli ifadeler çevrilmiş mi?
- [ ] Her ayette bilimsel kontrol yapıldı mı; ilişki türü, bilimsel tarafın derecesi ve künye yazıldı mı ya da "bulunmadı" denildi mi?
- [ ] Meal veya tefsir iki çeviri yazılmadan önce açıldı mı; açıldıysa kayda geçti mi?
- [ ] Sentezde veri, dilsel çözümleme, çıkarım ve spekülasyon karıştırıldı mı?
- [ ] Yapılmamış sorgu, tüm korpus taraması veya bağımsız doğrulama yapılmış gibi sunuldu mu?
- [ ] Sûrenin bütünü işlendi deniyorsa her ayet ve sûre çapında tutarlılık son kontrolden geçti mi?

## 6. Kayıt, sürüm ve depoya yazma

- **Ham veri salt okunurdur:** 01_raw/, 02_morphology/, 03_indices/, 04_lexicons/ katmanına yorum yazılmaz.
- Teknik çalışma izi ve kritik tercih gerekçeleri, yayımlanan sade metinden ayrılır. Bir iddiayı taşıyan ayet ve gerekçe gerektiğinde gösterilebilir olmalıdır.
- Tamamlanan sûre/pasaj çalışması, kullanıcı onayından sonra 07_analyses/surahs/ altında sürümlenir. Ara çalışma, nihai delil diye kaydedilmez.
- Değişen bir çeviri için eski ifade, yeni ifade ve değişiklik nedeni kayıt altına alınır. Önceki incelemede çözülmemiş tartışma gizlice kapanmış sayılmaz.
- Mevcut ana kavram analizi protokolünün «her ana aşamada dur» varsayılanı **sûre çeviri iş akışı için geçerli değildir**; burada tek talep üzerine kesintisiz iç işlem zinciri esastır. Kavram/tez araştırmalarında ana protokolün kendi ritmi korunur.

## 7. Kısa uygulama komutu

> «[Sûre adı] sûresini bütünleşik sûre meal–tefsir protokolüyle incele. Metni ve pasaj sınırlarını önce bütün olarak değerlendir; her ayeti ayrı dilsel çözümle; gerektiğinde bütün Kur'an'daki ilgili kullanımları, alternatifleri ve karşı delilleri denetle. Bir istek içinde tüm iç aşamaları yürüt. Her ayet için okunuşu, kavram merkezli çeviriyi (eklemeler [ ] içinde, kavram tablosuyla) ve anlam merkezli çeviriyi (doğal Türkçe, tabloya bağlı değil) ayrı ayrı ver; ikisini birleştirme. Her ayette bilimsel kontrol yap; çağrışım yoksa "bulunmadı" yaz. Meal veya tefsiri iki çeviriyi yazmadan açma. Tartışmalı kelimeleri gerektiğinde dikkat noktalarında delille ele al; pasaj bağlamı tamamlandığında kısa, tek bir bütünleşik tefsir yaz. Kritik belirsizlikleri gerekçelendir; yorumları lafız gibi sunma. Ulaşamadığın kaynak veya incelemediğin kapsamı açıkça belirt.»
