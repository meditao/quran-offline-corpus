# kavramlar/ — ara çalışma dosyaları

Olgunlaşan çalışmalar `07_analyses/` altına taşınır.

| dosya | içerik | statü |
|---|---|---|
| `calisma_cevirisi.tsv` | ayet başına çalışma çevirisi (`python -m tezgah ceviri 2:3 "..."`); satırlar yalnız eklenir, son sürüm gösterilir | kullanıcının yorumu |
| `<ad>/kavram.md` | kavram dosyası (`python -m tezgah kavram ac <ad> --soru "..." --kok Slw`) | çalışma dosyası |
| `<ad>/oneriler.json` | anlam önerileri (`kavram oneri`); yalnız eklenir, eskisi silinmez | kullanıcının yorumu |

Kavram dosyası kuralları:

- **Sorgu blokları.** Sayımlar elle yazılmaz. Sorgu blokları (`<!-- tezgah:sorgu ... -->`) komutu çalıştırıp
  çıktıyı kayıt satırıyla birlikte gömer. `kavram yenile` blokları yeniden üretir ve elle yazılan metne dokunmaz.
- **Denetim.** `kavram denetle` şunları bildirir:
  - elle değiştirilmiş ya da eskimiş blokları (hata);
  - sorgu dışında yazılmış sayıları (uyarı);
  - "Yalnız uyumlu" bir öneri varken metinde "destekleniyor" geçmesini (uyarı).
- **Bölüm kaydı.** Her bölüm otomatik bir bölüm kaydıyla biter (CLAUDE.md §8).
- **Zorunlu öneri alanları.** Anlam önerisinde şu alanlar boş bırakılamaz:
  - iç-tanım;
  - falsifikasyon ve fiilen bulunan ayetler (bulunamadıysa `yok` ve hangi taramayla bulunamadığı);
  - muhalif okumanın en güçlü hâli;
  - kurulduğu ve sonradan uygulandığı örneklem;
  - mantıksal durum ve delil derecesi.
- **Meal.** Meal kavram dosyasına gömülmez: delil değildir, lisansı doğrulanmamıştır ve depo herkese açıktır.
