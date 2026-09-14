# QuranMorph (SinaLab / Birzeit University)

Bu klasör QuranMorph veri katmanı için ayrılmıştır.

Resmî proje sayfası: https://sina.birzeit.edu/quran/
Makale: Akra, Hammouda & Jarrar (2025), *QuranMorph: Morphologically Annotated Quranic Corpus*.

## Rolü

QuranMorph, QAC'ın yerine geçmez. QAC kök, clitic/segment ve ayrıntılı morfolojik özellikler sağlar; QuranMorph ise bağımsız bir ekip tarafından kelime düzeyinde manuel lemma + POS annotation sağlar. Bu yüzden burada **bağımsız çapraz doğrulama katmanı** olarak kullanılacaktır.

## Birleştirme anahtarı

QuranMorph kelimeleri `(sûre:ayet:kelime)` düzeyinde konumlandırır. QAC ise `(sûre:ayet:kelime:segment)` kullanır. Bu nedenle iki korpusun güvenli birleşim anahtarı ilk üç bileşendir.

Gözlenen dağıtım şemasında temel kolonlar şunlardır:

- `surah_number`
- `verse_number`
- `word_position`
- `word`
- `POS`
- `qabas_lemma`

## Beklenen boyut

- 77.429 kelime satırı
- 114 sûre
- QAC ile aynı 77.429 kelime konumu

### Ayet sayısı uyarısı

2025 makalesinin metninde 6.235 ayet ifadesi geçmektedir. Buna karşılık QAC/Tanzil 6.236 numaralı ayet kullanır ve kamuya açık olarak incelenebilen QuranMorph dağıtımının bağımsız bir doğrulamasında bütün 6.236 ayetin kelime konumlarının QAC ile eşleştiği raporlanmıştır. Bu nedenle 6.235 sayısı doğrudan doğru kabul edilmeyecek; veri dosyası geldiğinde `validate_quranmorph.py` ile gerçek anahtar kümesi hesaplanacaktır.

## Erişim ve lisans politikası

Resmî indirme sayfası erişimi kurumsal/şirket bağlantısına sahip kullanıcılarla sınırlandırdığını bildiriyor. Bu nedenle veri dosyası bu repoya otomatik olarak çekilmeyecek ve erişim koşulları aşılmayacaktır.

Veri yasal/izinli bir kanaldan edinilirse dosya değiştirilmeden şu adla saklanabilir:

`02_morphology/quranmorph/quran-dataset.csv`

Ardından:

```bash
python 08_scripts/validate_quranmorph.py
python 08_scripts/crosscheck_qac_quranmorph.py
```

## Yorum ilkesi

QAC ile QuranMorph uyuşmazlığı otomatik olarak birinin 'yanlış' olduğu anlamına gelmez. Özellikle lemma granülerliği farklı olabilir. Uyuşmazlıklar editoryal/lexikografik kararların etkisini ölçen bir belirsizlik katmanı olarak raporlanacaktır.
