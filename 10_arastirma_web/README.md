# Kur'an Araştırma Masası

Türkçe, tamamen offline çalışan okuma ve araştırma uygulaması. Ana depo kaynak/veri arşividir; uygulama ayrı bir sunum katmanıdır. Araştırma dosyalarını, Tanzil metnini ve QAC verisini değiştirmez.

## Tek komutla başlatma

Gereksinim: **Python 3.10 veya üstü**. Ek paket, npm, framework veya internet bağlantısı gerekmez. Önce deponun tamamını bilgisayara indirin; yalnız bu klasörü indirmek veri kaynakları için yeterli değildir.

Deponun kök dizininde:

```sh
python 10_arastirma_web/serve.py
```

Windows'ta hazır başlatıcı da kullanılabilir:

```powershell
.\10_arastirma_web\baslat.cmd
```

Başlatıcı `py`, `python` veya Codex'in bu bilgisayardaki Python çalışma ortamını bulur. Python komutu `py` olarak kurulmuşsa doğrudan `py -3 10_arastirma_web/serve.py` de kullanılabilir. Komut yerel kaynakları doğrular, statik uygulamayı üretir ve tarayıcıda **http://127.0.0.1:8765/** adresini açar. Terminal açık kalmalıdır. Kapatmak için Ctrl+C kullanın. Port doluysa `--port 8766`; tarayıcı açılmasın istiyorsanız `--no-browser` ekleyin. Üretimi tekrar etmeden açmak için `--no-build` kullanılabilir; kaynak dosyaları değiştiğinde normal komutla yeniden üretin.

## Kullanım

- Sol taraftan sûre seçin; sûre listesinde isim veya numara ile filtreleyin. Ayet numarası ve önceki/sonraki düğmeleriyle gezin.
- Arapça kelimeye tıklayın: QAC kelime konumu, kök, lemma, ön ek/gövde/son ek segmentleri ve ham morfoloji etiketleri açılır. Kök veya lemma bağlantısı bütün korpusta arama yapar.
- Aramada kök, lemma, kelime, metin veya ayet referansı seçin. Örneğin kök `Amn`, `أ م ن`; ayet `2:3`. Buckwalter büyük/küçük harf duyarlıdır: `Slw` ve `slw` ayrı köklerdir.
- Çevirilerde iki ayrı yorum bölümü bulunur: **Terimleri koruyan çeviri** ve **Tefsirli çeviri**. Mevcut kapsam Bakara **2:2–117** ve Yûnus **10:1–109**. Başka ayetlerde çeviri uydurulmaz; kaydın bulunmadığı belirtilir.
- Kavram ve analiz dosyaları uygulama içinden okunur. Âsr analizi, İman/Mümin kartları, Amn aşamaları, mevcut türetilmiş raporlar ve yöntem dosyaları yerel olarak bulunur.

## Veri, aktarım ve yorum

**Veri:** Tanzil Uthmani v1.1 Arapça metni ve QAC v0.4 morfoloji annotationları. Arapça metin aynen korunur. Morfoloji etiketleri bir annotation kaynağıdır; kelimenin Türkçe anlamı olarak sunulmaz.

**Aktarım:** Okunuş mevcut `tezgah.okunus` motorundan üretilir. Kuralları ve belirsizlikleri kaynak okunuş belgesine dayanır; ses kaydı veya bağımsız bir meal değildir.

**Yorum/tefsir:** Depodaki Markdown çeviriler ve araştırma kayıtları. Çeviri, kök veya sayısal veri yerine geçmez. Her kaydın kaynak dosyası uygulamada görünür.

Tanzil ve QAC tokenizasyonu her ayette birebir değildir. Uygulama `tezgah.okuma.hizala` ve mevcut hizalama tablosunu kullanır. Besmele öneki ve çoklu Tanzil tokenları dikkate alınır; eşleşmeyen tokenlara sahte kök atanmaz. Hizalama/yazım farkları kelime ayrıntısında belirtilir. Kök araması sayım birimi **QAC kelime konumu**dur; ayet ve sûre sayıları ayrıca gösterilir.

## Offline çalışma ve statik taşıma

Başlatma, okuma, arama ve analiz görüntüleme yerel dosyalarla çalışır; uzak API, CDN, harici font veya paket indirme yoktur. İlk sayfa açılışında tarayıcı uygulamanın tüm dosyalarını offline önbelleğine alır. Durum göstergesi tamamlandığında aynı adres, yerel sunucu kapalıyken de destekleyen tarayıcılarda açılabilir. Tarayıcı depolamayı temizler/boşaltırsa veya service worker desteklenmiyorsa sunucuyu yeniden çalıştırın. İlk açılışı `file://` ile yapmayın; JSON yükleme ve service worker için yerel HTTP adresini kullanın.

Yalnız statik çıktı üretmek için:

```sh
python 10_arastirma_web/build.py
```

Çıktı `10_arastirma_web/dist/` altındadır; Git'e eklenmez. Bu dizinin **tamamı** GitHub Pages veya başka bir statik hosta taşınabilir. Sunucuda Python/API gerekmez. Dosya adresleri göreli, ayet/analiz adresleri hash tabanlıdır; `/quran-offline-corpus/` gibi bir alt dizinde de çalışır. Başka çıktı dizini için `python 10_arastirma_web/build.py --output YOL` kullanın. Bu komut burada belirtilen taşıma çıktısını hazırlar; kendiliğinden yayın yapmaz.

## Mimari ve kaynaklar

- `build.py`: salt okunur kaynaklardan JSON, arama indeksi ve kaynak belgeleri üretimi; `09_calisma_masasi/tezgah` yeniden kullanılır.
- `static/`: bağımlılıksız HTML/CSS/JavaScript arayüzü, arama worker'ı, offline service worker.
- `serve.py`: Python standart kütüphanesiyle yalnız `127.0.0.1` üzerinde statik sunucu.
- `testler/`: tam metin, kapsam, hizalama, kök sayımı ve kaynak bütünlüğü kontrolleri.
- `dist/`: yeniden üretilebilir dağıtım çıktısı; kaynak arşivinin yerine geçmez.

Lisans ve atıflar kaynak bazındadır: [Lisanslar](../LICENSES.md), [Kaynaklar](../SOURCES.md). Tanzil ve QAC'ın özgün bildirimleri dağıtımda korunur. Repo için tek bir genel lisans varsayılmaz. Çekirdek üretim lisansı belirsiz `yerel/` katmanlarını, üçüncü taraf meal veya sözlükleri içermez.

## Testler

Deponun kökünde:

```sh
python -m unittest discover -s 10_arastirma_web/testler -v
python -m unittest discover -s 09_calisma_masasi/testler -v
```

Tarayıcıda Arapça kelime tıklama, Amn/Slw araması, Bakara/Yûnus kapsam uçları, analiz bağlantıları, mobil görünüm ve offline önbellek ayrıca doğrulanmalıdır.
