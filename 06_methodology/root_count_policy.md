# Kök Sayımı Politikası

## Sabit sonuç

Bu repoda kullanılan doğrulanmış QAC v0.4 morfoloji dosyası için **1.642 farklı `ROOT` etiketi** vardır.

Bu sayı, `02_morphology/qac/quranic-corpus-morphology-0.4.txt` dosyasının yapısal olarak parse edilmesi ve `ROOT:` özelliklerinin normalize edilerek benzersizleştirilmesiyle elde edilir.

Ham QAC SHA-256:

`a1d12923815341face765083805d2148ed2d9f5cc3f7d6665219d887675d8c46`

## 1.651 sayısı neden çıkıyor?

2019'da yayımlanan bir shell pipeline şu yöntemi kullanmıştır:

```text
sed 's/\t/,/g' | cut -d',' -f4 | grep -oE 'ROOT:[^|]*' | cut -d':' -f2 | sort | uniq
```

Aynı mantığı ham QAC dosyası üzerinde byte düzeyinde yeniden ürettiğimizde **1.651** benzersiz ham değer çıkar. Ancak bu gerçek kök sayısı değildir.

İki ayrı teknik artefakt birlikte sayıyı oluşturur:

1. QAC dosyası CRLF satır sonları taşır. `ROOT` satırın son özelliği olduğunda regex görünmeyen `\r` baytını da köke dahil eder. Böylece aşağıdaki 10 kök hem normal hem de `\r` ekli ikinci bir değer olarak sayılır:
   - `Any`
   - `End`
   - `Hyn`
   - `Hyv`
   - `bEd`
   - `byn`
   - `kll`
   - `kyf`
   - `mss`
   - `qbl`

2. Pipeline önce TSV ayırıcılarını virgüle çevirir. Fakat Buckwalter/QAC `FORM` alanının kendisinde virgül bulunabilir. 81:8'deki `mawo'u,dapu` bunun somut örneğidir. Bu satırın gerçek kökü `wAd` olduğu halde `cut -d',' -f4` sütunları kaydırır ve `wAd` hiç yakalanmaz.

Dolayısıyla:

```text
1.642 gerçek benzersiz ROOT
+ 10 CRLF kaynaklı sahte ikinci değer
- 1 virgül-ayırıcı hatasıyla kaçırılan wAd
= 1.651
```

## Bağımsız tarihsel kontrol

2019 tarihli `abdulbaqi/quranic_roots` deposundaki `quran-morphology-final.csv`, commit `86611929fd5a35220bc46e1944acc69c619aa57b` altında sabitlendi ve mevcut indeksimizle karşılaştırıldı.

Sonuç:

- eski türetilmiş CSV: 1.642 kök
- mevcut sağlam parser: 1.642 kök
- ortak kök: 1.642
- yalnız eskide: 0
- yalnız mevcutta: 0
- frekansı değişen ortak kök: 0

Yani 1.651, farklı bir kök annotation kümesi değil; kırılgan shell sayımının sonucudur.

Ayrıntılı yeniden üretilebilir rapor:

- `03_indices/audits/qac_1651_vs_1642.md`
- `03_indices/audits/qac_1651_vs_1642.json`
- `08_scripts/compare_qac_snapshots.py`

## Bundan sonraki zorunlu kural

Bir kök sayısı raporlanırken en az şu dört unsur belirtilmelidir:

1. korpus/snapshot ve hash,
2. sayım birimi (`ROOT` etiketi, kelime occurrence, ayet, sûre vb.),
3. parser/normalizasyon yöntemi,
4. Buckwalter veya başka transliterasyon normalizasyonu.

Bu repoda genel `ROOT` evreninin kanonik teknik referansı, yukarıdaki hash'e sahip QAC v0.4 dosyasından sağlam parser ile çıkarılan **1.642 köklük indeks** olacaktır.

Bu sayı "Arapçada/Kur'an dilinde ontolojik olarak yalnız 1.642 kök vardır" iddiası değildir. Yalnızca sabitlenmiş QAC annotation şemasındaki benzersiz `ROOT` etiketlerinin sayısıdır.
