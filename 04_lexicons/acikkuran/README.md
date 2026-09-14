# Açık Kuran yardımcı kök katmanı

Bu klasör Açık Kuran'ın kök metadata'sını **ikincil çapraz kontrol** olarak offline saklamak için ayrılmıştır.

Kaynak:
- https://acikkuran.com
- https://api.acikkuran.com
- https://github.com/acik-kuran/acikkuran-api

API projesi CC BY-NC-SA 4.0 lisans bildirimi taşır.

## Neyi saklıyoruz?

İlk aşamada yalnız kök metadata'sı:

- kök id
- Latin/Buckwalter-benzeri anahtar
- Arapça kök
- transkripsiyon
- `mean` / `mean_en`
- kök varyantları (`diffs`) ve onların sayımları

QAC zaten kök occurrence konumlarını verdiği için bütün Açık Kuran meal/ayet verisini çoğaltmıyoruz.

## Neden yardımcı katman?

Açık Kuran kök sayfaları araştırmada kullanışlıdır; ancak `mean` alanının lexikografik kaynak zinciri her kök için açıkça belirtilmiş olmayabilir. Bu yüzden burada yer alan anlamlar:

- hipotez üretmek,
- QAC kök ailesini ikinci kez kontrol etmek,
- varyant/sayım farklarını fark etmek

için kullanılacaktır. Tek başına nihai etimolojik/semantik kanıt sayılmaz.

## Snapshot

```bash
python 08_scripts/fetch_acikkuran_roots.py --i-accept-acikkuran-license
```

Çıktı:

`04_lexicons/acikkuran/roots.jsonl`

Script kaynak endpointlerini ve SHA-256 değerini ayrıca manifest dosyasına kaydeder.
