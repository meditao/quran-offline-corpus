# Yûnus — sade meal okuma denemesi

Şimdilik yalnız Yûnus sûresinin 109 ayeti hazırlanır. Bütün ayetler tek sayfada alt alta gösterilir; ayet numarasına gitmek sayfa içinde kaydırır. Diğer sûrelerde boş hazırlık görünümü bulunur.

Ayetin üstünde mevcut tezgah motorunun Türkçe okunuşu, altında Mehmet Okuyan, Erhan Aktaş ve bizim tefsirli çevirimiz için ayrı alanlar bulunur. Arapça, morfoloji, kök araması ve terimleri koruyan çeviri bu denemenin ekranında gösterilmez. Tefsirli çevirimizdeki parantezli kavramlar kaynak dosyadan aynen korunur.

## Tek komutla açma

Deponun kökünde Python 3.10+ ile:

```sh
python 10_arastirma_web/serve.py
```

Windows'ta:

```powershell
.\10_arastirma_web\baslat.cmd
```

Başlatıcı py, python veya Codex'in bilgisayardaki Python ortamını bulur. Tarayıcıda http://127.0.0.1:8765/ açılır. Terminal açık kalır; Ctrl+C ile kapatılır. Port doluysa --port 8766; tarayıcı otomatik açılmasın istiyorsanız --no-browser ekleyin. Ek paket ve internet bağlantısı gerekmez.

## Mevcut içerik

Bizim tefsirli çevirimiz Yûnus 1–109 için 07_analyses/surahs/Yunus-001-109-meal-tefsir.md dosyasından alınır. Okunuşlar ve bu çeviri offline çalışır.

Mehmet Okuyan ve Erhan Aktaş'ın tam metinleri ve açıklamaları henüz pakete eklenmemiştir. Açık Kuran'ın yazılım lisansı, dış veritabanındaki yazar metinleri için açık yeniden kullanım izni olarak kabul edilmemiştir. Kaynak bağlantıları internet gerektirir. Boş meal alanına çeviri veya not uydurulmaz.

Doğrulanan kayıtlar Mehmet Okuyan (107) ve tam adı Erhan Aktaş olan sürümdür (105). Eski Baskı (50) ve 10. Baskı (115) alınmaz. Kaynaklar: [Açık Kuran](https://acikkuran.com/10), [API projesi](https://github.com/acik-kuran/acikkuran-api).

Kullanıcının sağladığı veya açık kullanım izni bulunan meal dosyaları yerel olarak alınabilir. Kaynak notlarının [1], [2] işaretleri ekranda yıldız düğmelerine dönüşür; ayeti ve yazarı korunur. Açıklama başka yazarın notuyla birleştirilmez.

## Kullanıcı meal dosyalarını içe aktarma

```sh
python 10_arastirma_web/import_meals.py --okuyan OKUYAN.json --aktas AKTAS.json --source "Kullanıcının sağladığı dosyalar"
python 10_arastirma_web/serve.py
```

Dosya biçimi Açık Kuran'ın data.verses listesi veya doğrudan ayet listesi olabilir. Her satırda verse_number (veya ayah) ve translation: {author: {id, name}, text, footnotes: [{id, number, text}]} bulunur. Her meal dosyası 109 Yûnus ayetini içermelidir; yanlış yazar/sürüm ve eksik dipnot reddedilir. İçe aktarım ağ kullanmaz. Yerel kayıt yerel/acikkuran-yunus.json altında tutulur ve Git'e eklenmez. Mevcut kayıt otomatik üzerine yazılmaz.

## Offline ve statik çıktı

Başlatma ve mevcut içerik yerel dosyalarla çalışır. Uzak API, CDN veya harici font yoktur. Tarayıcı offline kopyayı tamamladığında aynı adres destekleyen tarayıcılarda sunucu kapalıyken de açılır. Depolama temizlenirse sunucuyu tekrar çalıştırın. İlk açılışta file:// yerine yerel HTTP adresini kullanın.

```sh
python 10_arastirma_web/build.py
```

Dist dizininin tamamı statik hosta taşınabilir; göreli yollar ve hash tabanlı sûre/ayet adresleri alt dizinlerde çalışır. Bu komut kendi kendine yayın yapmaz. Dış meal metinlerinin yayın izni ayrıca doğrulanmalıdır.

Ana korpus ve araştırma kaynakları değişmez. Mevcut veri hazırlama ve kaynak bütünlüğü altyapısı korunur; sade ekran yalnız data/reader/ dosyalarını kullanır. Okunuş, metnin kurallı aktarımıdır; tefsirli çeviri yorum katmanıdır. Tanzil/QAC bildirimleri üretim çıktısında korunur. [Lisanslar](../LICENSES.md) ve [Kaynaklar](../SOURCES.md) geçerlidir.

## Kontroller

```sh
python -m unittest discover -s 10_arastirma_web/testler -v
```

Kontroller 109 ayeti, diğer sûrelerin boş durumunu, tefsir ve parantezli kavramların korunmasını, doğru yazar sürümlerini, dipnot eşleştirmesini ve offline kopyayı doğrular. Kullanıcı dosyası yoksa iki dış mealin açıkça eksik gösterilmesi de kontrol edilir.
