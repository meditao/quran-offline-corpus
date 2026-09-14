# Tanzil Uthmani v1.1 ↔ QAC v0.4 alignment audit

Bu rapor otomatik üretilir. `(sûre,ayet)` anahtarı ortaktır; `(sûre,ayet,kelime)` doğrudan ortak anahtar kabul edilmez.

- Tanzil Uthmani whitespace-token total: **77,881**
- QAC orthographic word-position total: **77,429**
- Difference: **+452**
- Exact count-match ayat: **6,120**
- Basmala-offset ayat: **112**
- Other tokenization-difference ayat: **4**

## Non-basmala tokenization differences

| ayah | Tanzil words | QAC words | delta |
|---|---:|---:|---:|
| 2:181 | 14 | 13 | +1 |
| 8:6 | 12 | 11 | +1 |
| 13:37 | 20 | 19 | +1 |
| 37:130 | 4 | 3 | +1 |

## Join rule

- QAC içi morfoloji/kök/lemma sorgularında QAC `(sûre,ayet,kelime)` anahtarı kullanılabilir.
- Tanzil ile kelime düzeyinde birleştirme yapılırken bu alignment tablosu kullanılmalıdır.
- `basmala_offset` satırlarında QAC word `n`, Tanzil whitespace word `n+4` konumuna karşılık gelir.
- `tokenization_difference` satırlarında otomatik pozisyon eşitlemesi yapılmaz; ayrı split/merge eşlemesi gerekir.

Total non-count-match ayat: **116**
