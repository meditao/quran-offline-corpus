# kavramlar/ — ara çalışma dosyaları

Olgunlaşan çalışmalar `07_analyses/` altına taşınır.

| dosya | içerik | statü |
|---|---|---|
| `calisma_cevirisi.tsv` | ayet başına çalışma çevirisi (`python -m tezgah ceviri 2:3 "..."`); satırlar yalnız eklenir, son sürüm gösterilir | kullanıcının yorumu |
| `<ad>/kavram.md` | kavram dosyası (`python -m tezgah kavram ac <ad> --soru "..." --kok Slw`) | çalışma dosyası |
| `<ad>/oneriler.json` | anlam önerileri (`kavram oneri`); yalnız eklenir, eskisi silinmez | kullanıcının yorumu |
| `tezler/<ad>/` | tez kaydı (`python -m tezgah tez ...`): `surum-NNN.json` (dondurulmuş, salt okunur), `defter.json` (zincirli, yalnız eklenir), `tez.md` (üretilir) | kullanıcının tezi + sorgu bulguları |

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

Tez kaydı kuralları (`tez.py`):

- **Açılış (`tez ac`).** Tez tek cümleyle dondurulur ve olduğu gibi saklanır; araç tez ifadesini
  değiştirmez ya da güçlendirmez. Tanımlar (`terim=tanım`), eksenler (`kip=tanımlayıcı|normatif`,
  `düzlem=oluşum|sorumluluk`, başka boyutlar serbest) ve karşı örnek havuzu (sorgu tanımları) aynı anda,
  taramadan önce kaydedilir. Havuz açılışta çalıştırılmaz; `tez tara` ile taranır.
- **Değişiklik (`tez yeni-surum --gerekce`).** Değişiklik yalnız yeni sürümle olur; eski sürüm silinmez.
  Yeni sürüme önceki sürümdeki bulgu sayısı ve taramanın yapılıp yapılmadığı yazılır, böylece sonradan
  yapılan değişiklik görünür kalır. Bulgular sürüme bağlıdır ve yeni sürüme taşınmaz.
- **Bulgu (`tez bulgu ... -- <sorgu>`).** Her bulgu tezin bütün eksen boyutlarını etiketler ve bir sorguya
  dayanır. `--ayet` ile verilen ayetler o sorgunun çıktısında geçmek zorundadır.
- **Raf.** Raflar şunlardır: destekleyen · yalnız uyumlu · çelişen · belirsiz · farklı eksen. Eksenleri
  tezinkinden farklı olan bulgu yalnız "farklı eksen" rafına konur. CLAUDE.md §7 yalnız "çelişen" rafını
  yasaklar; araç simetri için destekleyen, yalnız uyumlu ve belirsiz raflarını da yasaklar. Farklı eksen
  rafı sonuç hesabına girmez.
- **Sonuç (`tez sonuc`).** Sonuç iki eksende yazılır: mantıksal durum ve delil derecesi. Tutarlılık kuralları:
  - Her sonuç için havuzun taranmış olması gerekir.
  - "Destekleniyor" için en az bir "destekleyen" bulgu gerekir ve hiç "çelişen" bulgu olmamalıdır.
    "Yalnız uyumlu" bulgular destek sayılmaz.
  - "Yalnız uyumlu" sonucu, çelişen bulgu varken yazılamaz.
  - "Çelişiyor" için en az bir çelişen bulgu gerekir.
- **Denetim (`tez denetle`).** Şunları bildirir:
  - bozulmuş defter zincirini;
  - değişmiş sürüm dosyasını;
  - yeniden çalıştırınca farklı çıkan sorgu çıktısını;
  - defterle uyuşmayan `tez.md` dosyasını;
  - sonuç yazıldıktan sonra eklenen bulguları.
