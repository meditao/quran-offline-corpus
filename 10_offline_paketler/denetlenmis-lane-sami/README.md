# Denetlenmiş Lane–Sâmî çevrimdışı paket kaydı

Bu kayıt, `kuran-kok-analizi-offline-DENETLENMIS-LANE-SAMI.zip` arşivinin
kimliğini ve depoyla ilişkisini belgeler. Arşiv ve üçüncü taraf veri dosyaları
bu dizine dahil değildir. İnceleme tarihi: 18 Ekim 2026.

## Paket kimliği

- Boyut: 102.168.413 bayt (97,44 MiB).
- Dosya sayısı: 427; açılmış toplam boyut: 190.236.193 bayt.
- SHA-256: `b433682212ca92b59a6a08192eb5533c98c29e2955ae23c8d9e9c25a41b33026`.
- Paket içi `DOSYA-SHA256.json` listesindeki 426 dosya doğrulandı; listenin kendi dosyası bu sayıya dahil değildir.
- Veri manifestindeki 402 dosya doğrulandı. Bu 402 dosya, 426 dosyanın içindedir; ayrı bir toplam değildir.
- `lane.sqlite` ve `sami.sqlite` salt okunur bütünlük kontrolleri başarılı.

## GitHub karşılaştırması

Bağlı hesapta erişilebilen `meditao/quran-offline-corpus` deposu incelendi.
Karşılaştırılan `main` commit'i: `a65d2d98baf1e5aab8146fa418349b460044319b`.
9 uzak dalın erişilebilir 199 commit'lik geçmişinde ZIP'in kendisi, paket adı
ve arşivdeki 427 dosyanın byte düzeyinde aynı Git blob'ları bulunmadı.
İnceleme anında yayımlanmış GitHub Release yoktu; indirilen Git referanslarında etiket yoktu.
Silinmiş veya erişilemeyen nesneler ve geçici workflow çıktıları bu taramaya dahil değildir.

## İçerik ilişkisi ve farklar

| Katman | ZIP | GitHub deposu |
|---|---|---|
| Morfoloji | mustafa0x/quran-morphology; 130.030 segment, 1.651 ayrı kök etiketi | Kanonik QAC v0.4; 128.219 segment, 1.642 ayrı kök etiketi |
| Lane | Özgün kaynak arşivi ve dönüştürülmüş `lane.sqlite` arama dizini | [Lane aracı](https://github.com/meditao/quran-offline-corpus/blob/a65d2d98baf1e5aab8146fa418349b460044319b/09_calisma_masasi/tezgah/ikincil/lane.py); veritabanı yerelde kurulur |
| İbranice/BDB | XML kaynak ve 1.836 satırlı kısa tanım dizini | [İbranice dizin](https://github.com/meditao/quran-offline-corpus/blob/a65d2d98baf1e5aab8146fa418349b460044319b/04_lexicons/generated/hebrew_lexical_index.tsv); farklı çıktı biçimi |
| Süryanice/SEDRA | Özgün arşiv ve değiştirilmemiş kaynak dosyaları | [Sâmî aracı](https://github.com/meditao/quran-offline-corpus/blob/a65d2d98baf1e5aab8146fa418349b460044319b/09_calisma_masasi/tezgah/ikincil/sami.py); veriler yerelde kurulur |
| Meal | Denetlenmiş yardımcı meal, kaynak kopyaları ve denetim kayıtları | Meal katmanları yerel kurulum üzerinden kullanılır |
| Kullanım | `python offline.py ...` | `python -m tezgah ...`; çalışma masası ve web arayüzü |

Morfoloji sayıları bu incelemede kaynak dosyalarından yeniden ölçüldü.
İki dosyada da 77.429 kelime konumu ve 6.236 ayet anahtarı vardır; bu ortaklık,
segmentlerin ve kök atamalarının eşdeğer olduğunu göstermez.
ZIP, depodaki kanonik korpusun üzerine yazılmamalıdır.

Lane kaynak commit'i ve özgün SQLite parmak izi, BDB kaynak commit'i ve SEDRA kaynak
commit'i depoda kayıtlı olanlarla aynıdır. SEDRA'nın dört kaynak dosyasının
parmak izleri de depodaki kurucunun beklediği değerlerle eşleşir. Dolayısıyla
kaynaklarda örtüşme vardır; bütün paket içerik veya çalışma biçimi bakımından
deponun aynısı değildir.

Paketin kendi meal denetim kaydında 7 açık sorun / 8 ayet belirtilir.
Bu inceleme dosya bütünlüğünü ve depo ilişkisini denetler; önceki anlam
denetimini yeniden yapmaz. Paket içindeki programlar çalıştırılmadı.

## Yerleşim

GitHub'da bu katalog kaydı ve `manifest.json` tutulur. `manifest.json`, ZIP'in
ve içindeki dosyaların SHA-256 değerlerini, karşılaştırılan commit'i ve kontrol
sonuçlarını içerir. Dosyanın kendisini veya kaynak metinleri içermez.

Tam arşiv ve açılmış veri için mevcut yerel alan uygundur:
`09_calisma_masasi/yerel/offline-paketler/denetlenmis-lane-sami/`.
Bu bir saklama konumudur; çalışma masasının veri yükleyicilerine otomatik
entegrasyon sağlamaz.

[CLAUDE.md §3 ve §9](https://github.com/meditao/quran-offline-corpus/blob/a65d2d98baf1e5aab8146fa418349b460044319b/CLAUDE.md) morfoloji karşılaştırma verisini,
meal/okunuş ve bazı sözlük kaynaklarını yerel alanda tutar.
[Yerel alanın kuralı](https://github.com/meditao/quran-offline-corpus/blob/a65d2d98baf1e5aab8146fa418349b460044319b/09_calisma_masasi/yerel/.gitignore):
“Lisansı doğrulanmamış veya dağıtılamaz veri burada kalır; depoya işlenmez”.
Bu nedenle bütün ZIP'i herkese açık depoya veya Release'e yüklemek,
bu katalog eklemesinden ayrı bir dağıtım kararıdır; kaynak koşulları
bileşen bazında değerlendirilmelidir. Release eki olmak bu ayrımı ortadan kaldırmaz.
