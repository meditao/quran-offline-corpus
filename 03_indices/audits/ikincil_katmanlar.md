# İkincil katmanlar — Lane kapsamı ve Sâmî gürültü tabanı

Üretici: `08_scripts/measure_secondary_layers.py`. Her iki katman da **hipotez kaynağıdır, delil değildir**. Ölçümler QAC v0.4'ün 1.642 kökü üzerinden bu depoda yapıldı (birim: kök).

## Lane (LexiconDatabase v1.0.9)

Lane geneli: 5.160 kök, 47.919 madde.

| eşleşme | kök | oran |
|---|---:|---:|
| tam | 1.445 | %88,0 |
| kural | 168 | %10,2 |
| zayıf | 11 | %0,7 |
| yok | 18 | %1,1 |

- **tam**: hemze yazımı ve harekeler nötrlenince aynı kök.
- **kural**: Lane'in yazım geleneği — ikiz kök iki harfle (C1C2C2 → C1C2), yinelemeli dörtlü kısaltılmış (C1C2C1C2 → C1C2).
- **zayıf** (`<< DOĞRULA`, elle denetlenir): `hAt` (kök tablosunda yok, maddeleri h-y-t kökü altında), `mTw` (son harf و↔ي), `mlw` (son harf و↔ي), `mrA` (son hemze düşürüldü), `msw` (son harf و↔ي), `ndw` (son harf و↔ي), `nwm` (kök tablosunda yok, maddeleri n-ʾ-m kökü altında), `qSw` (son harf و↔ي), `qsw` (son harf و↔ي), `tyh` (orta harf و↔ي), `vyb` (orta harf و↔ي)
- **yok**: `dhq`, `dsw`, `hTE`, `hlE`, `hmn`, `hrE`, `kdy`, `khf`, `khn`, `lZy`, `ntq`, `nzg`, `wbq`, `wjf`, `wjl`, `wsn`, `ydy`, `ynE`. Bölge: {'ا-ق': 2, 'ك-ي (seyrek)': 16}.

Bölge yoğunluğu (madde / kök). ك-ي bölgesi Lane'in ölümünden sonra derlendi; bu bölgede "Lane'de yok" argümanı kurulamaz:

| bölge | kök | madde | madde/kök |
|---|---:|---:|---:|
| ا-ق | 3.703 | 39.408 | 10,64 |
| ك-ي (seyrek) | 1.457 | 8.511 | 5,84 |

Veri notu: LexiconDatabase kök tablosunda harekeli yazılmış kökler vardır (ör. `جَهِلَ`); eşleştirme harekeleri siler.

## Sâmî gürültü tabanı

İbranice: depodaki `04_lexicons/generated/hebrew_lexical_index.tsv` (1.797 kök, sonu-harfleri ve harekeler normalleştirilmiş). Süryanice: SEDRA 3 (1.827 kök yazımı; köke bağlanmamış kayıt atlandı: sözcük 36, anlam 229). Denklik tablosu: `python -m tezgah sami denklik`.

Yöntem: 1.642 gerçek QAC kökü ile aynı harf ve uzunluk dağılımından üretilmiş 10 × 1.642 sahte kök (tohum 20260924; gerçek köklerle çakışanlar atıldı) aynı işlemden geçirildi. Son-harf-zayıf kuralı (İbranice ה / Süryanice Alef) kapalı ve açık olarak aynı kümelerde ayrı ölçüldü.

| kural | dil | gerçek vuruş | rastgele vuruş (ort.; en az–en çok) | gerçek/rastgele | gürültü payı |
|---|---|---:|---:|---:|---:|
| kapalı (varsayılan) | İbranice | %58,5 | %20,7 (%19,0–%23,2) | 2,83 | %35,4 |
| kapalı (varsayılan) | Süryanice | %30,7 | %9,5 (%8,9–%10,0) | 3,23 | %30,9 |
| kapalı (varsayılan) | ikisi birden | %25,8 | %5,4 (%4,7–%5,9) | 4,79 | %20,9 |
| açık (--zayif-son) | İbranice | %67,8 | %25,8 (%24,2–%28,4) | 2,63 | %38,0 |
| açık (--zayif-son) | Süryanice | %38,1 | %13,4 (%13,1–%13,7) | 2,84 | %35,2 |
| açık (--zayif-son) | ikisi birden | %33,0 | %8,6 (%7,9–%9,4) | 3,84 | %26,1 |

Kural gerçek/rastgele oranını iyileştiriyor mu: İbranice: hayır, Süryanice: hayır, ikisi birden: hayır. Oranı iyileştirmediği için varsayılan kapalıdır; `sami kok --zayif-son` ile açılır.

Kurallar: kognat anlam değildir; tek dildeki vuruş tek başına raporlanmaz; "aday yok" bulgu değildir; İbranice ve Süryanice bağımsız iki tanık değildir. SEDRA verisi değiştirilmiş hâliyle dağıtılamaz ve depoya işlenmez; sonuç yayımlanırsa atıf zorunludur (`python -m tezgah sami atif`).
