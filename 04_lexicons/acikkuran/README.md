# Açık Kuran yardımcı kök katmanı

Bu klasör Açık Kuran'ı **ikincil çapraz kontrol** kaynağı olarak kullanmak için ayrılmıştır.

Kaynaklar:
- https://acikkuran.com
- https://github.com/acik-kuran/acikkuran-api

API projesi CC BY-NC-SA 4.0 lisans bildirimi taşır.

## Güncel erişim durumu

Eski `https://api.acikkuran.com` REST API alan adı artık çözülmüyor. Bu nedenle eski `/rootchars`, `/rootchar/{id}` ve `/root/latin/{latin}` API endpointlerine dayanan toplu snapshot akışı çekirdek bootstrap'tan çıkarılmıştır.

Açık Kuran'ın web sitesi ve kök sayfaları çalışmaya devam ediyor. Örnek:

- `https://acikkuran.com/root/Slw`
- `https://acikkuran.com/root/wqy`
- `https://acikkuran.com/root/Amn`

Bu sayfalar kökün Arapça/Latin anahtarını ve Türkçe anlam alanını gösterir. Site şu aşamada kök-bazlı filolojik çapraz kontrol için kullanılacaktır.

## Metodolojik rol

QAC kök occurrence konumlarını zaten verdiği için Açık Kuran'dan bütün ayet/meal verisini çoğaltmaya ihtiyacımız yoktur. Açık Kuran özellikle:

- kök anlam alanı için ikinci görüş,
- kritik köklerde anlam hipotezi üretme,
- QAC atamalarını insan-okunur bir kaynakla çapraz kontrol etme

için kullanılır.

Açık Kuran'daki kök anlamı tek başına nihai etimolojik veya semantik kanıt sayılmaz. Kaynak zinciri açık olmayan bir anlam, Kur'an içi dağılım ve karşılaştırmalı Sami verisinin önüne geçirilmez.

## Offline snapshot politikası

Yeni site veri yolu güvenilir ve lisansa uygun biçimde doğrulanana kadar toplu Açık Kuran snapshot'ı üretilmeyecektir. Kritik kökler gerektiğinde tek tek kayda alınabilir; her kayıtta kaynak URL'si ve erişim tarihi tutulur.
