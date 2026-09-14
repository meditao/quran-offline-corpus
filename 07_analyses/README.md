# 07_analyses — Okunabilir araştırma katmanı

Bu klasör artık aktiftir. Burada ham korpus değil; kök, kavram, ayet ve pasaj analizleri tutulur.

Amaç, dışarıdan gelen bir okuyucunun sonucu sadece kabul etmesi değil, sonuca hangi verilerle ve hangi ayetlerle ulaşıldığını adım adım görebilmesidir.

## Şu anda aktif çalışmalar

- [İman — ayrıntılı, aşamalı ana analiz](roots/Iman-analysis.md)
- [İman — kısa kavram kartı](roots/Amn-concept-card.md)
- [Mümin — kısa kavram kartı](roots/Mumin-concept-card.md)
- [Amn — Aşama 1](roots/Amn-quran-internal-stage1.md)
- [Amn — Aşama 2: sentaks](roots/Amn-quran-internal-stage2-syntax.md)
- [Amn — Aşama 3: bi- kullanımları](roots/Amn-quran-internal-stage3-bi.md)
- [Amn — Aşama 4: īmān isim kullanımı](roots/Amn-quran-internal-stage4-iman-noun.md)
- [Amn — Aşama 5: muʾmin profili](roots/Amn-quran-internal-stage5-mumin-profile.md)

Aynı klasördeki TSV/CSV türü dosyalar manuel kontrol, sınıflandırma ve falsifikasyon kayıtlarıdır. Bunlar teknik kanıt katmanıdır; nihai okuyucu metninin yerine geçmez.

## Standart analiz düzeni

Yeni ve tamamlanmış her kavram çalışması mümkün olduğunca şu yapıda tutulacaktır:

1. Kısa tanım ve araştırma sorusu.
2. Aşama 1 — kök, morfoloji, biçimler ve sayımlar.
3. Aşama 2 — sentaks ve kullanım kalıpları.
4. Aşama 3 — Kur'an içi bağlam ağı ve dağılım.
5. Kritik ayetler — ayet numarası, tam Arapça metin, sade/kavramsal Türkçe çeviri ve ayetin analize katkısı.
6. Karşı örnekler / falsifikasyon — alternatif açıklamalar ve onları doğrulayan veya bozan ayetler.
7. Varsa Sami dil karşılaştırması — yalnız destekleyici katman olarak.
8. Nihai sentez — verinin izin verdiği en dar ve en güçlü tanım.
9. Kavram kartı — kısa, kolay okunur sonuç.

## Yazım ilkesi

Analiz metni teknik olmayan bir okuyucunun da anlayabileceği Türkçe ile yazılır. Arapça terim ilk geçtiğinde açıklanır. Teknik transliterasyon ve script çıktıları ana anlatımı boğmaz.

Bir ayet merkezi kanıt olarak kullanılıyorsa yalnız referans verilmez; mümkün olduğunda tam Arapça ayet ve analizde kullanılan sade/kavramsal Türkçe karşılık da gösterilir. Böylece okuyucu sonucu metin üzerinden doğrudan denetleyebilir.

## Veri ile yorumun ayrılması

Sayım, morfoloji, lemma, kök, söz dizimi ve ayet dağılımı veri katmanıdır. “Bu kullanım bize ne anlatıyor?” bölümü yorum katmanıdır. İkisi açıkça ayrılır.

Sonuç kesin değilse “ara sonuç”, “çalışma hipotezi” veya “düşük/orta/yüksek güven” gibi işaretler kullanılır. Bir yorum karşı örnekle bozuluyorsa eski iddia korunmaz; tanım daraltılır.

## Sürüm ilkesi

Ara düşünceler doğrudan nihai analiz gibi sunulmaz. Sohbet/çalışma sırasında üretilen dağınık notlar önce temizlenir; sonra kanıt zinciri korunarak toparlanmış araştırma kaydına dönüştürülür.
