# Quranic Arabic Corpus (QAC) v0.4

Bu klasör Quranic Arabic Corpus morfoloji verisi için ayrılmıştır.

Resmî kaynak: https://corpus.quran.com/download/

## Neden burada?

QAC, Tanzil'in doğrulanmış Arapça metni üzerine kelime/parça düzeyinde morfolojik annotation sağlar. Başlıca alanlar:

- LOCATION: sûre:ayet:kelime:segment
- FORM: Buckwalter transliterasyonlu yüzey biçimi
- TAG: temel sözcük türü
- FEATURES: segment türü, POS, lemma, root ve diğer morfolojik özellikler

v0.4 için beklenen yapı yaklaşık olarak:

- 114 sûre
- 6.236 ayet
- 77.429 kelime konumu
- 128.219 morfolojik segment

## Lisans ve veri bütünlüğü

Resmî indirme sayfasındaki telif/lisans bloğu dosyanın içinde korunmalıdır. QAC v0.4 ham annotation dosyası **değiştirilmeden** saklanacaktır. Bizim düzeltmelerimiz veya alternatif annotationlarımız hiçbir zaman ham dosyanın üzerine yazılmayacak; ayrı türetilmiş katmanlarda tutulacaktır.

## Dosya adı

Ham dosya şu adla beklenir:

`02_morphology/qac/quranic-corpus-morphology-0.4.txt`

Resmî indirme sayfası e-posta ve şartları kabul etme adımı içerdiği için bu insan onayı gerektiren adım otomatikleştirilmeyecektir. Dosya resmî kaynaktan edinildikten sonra `08_scripts/validate_qac.py` ile doğrulanır.

## Analiz ilkesi

QAC annotationları yüksek değerli bir dilbilimsel kaynak olmakla birlikte 'yanılmaz veri' değildir. Kök veya lemma ataması kritik bir sonuca etki ediyorsa:

1. QAC kaydı kontrol edilir,
2. Açık Kuran ve bağımsız Arapça kaynaklarla karşılaştırılır,
3. Kur'an içi dağılım bizzat hesaplanır,
4. gerekiyorsa alternatif annotation karantina notuna alınır.
