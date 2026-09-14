# QuranMorph (SinaLab / Birzeit University)

**Durum: INFRASTRUCTURE ONLY / DATASET NOT PRESENT.** Bu klasörde şu anda QuranMorph veri dosyası yoktur; yalnız parser/validator ve gelecekteki çapraz doğrulama için altyapı vardır.

Resmî proje sayfası: https://sina.birzeit.edu/quran/
Makale: Akra, Hammouda & Jarrar (2025), *QuranMorph: Morphologically Annotated Quranic Corpus*.

## Rolü

Veri izinli kanaldan edinilirse QuranMorph, QAC'ın yerine geçmeden bağımsız kelime-düzeyi lemma + POS annotation kontrolü olarak kullanılacaktır. Mevcut repo haliyle aktif QuranMorph çapraz doğrulaması sağladığı iddia edilmez.

## Birleştirme anahtarı

QuranMorph veri dosyası edinildiğinde önce gerçek anahtar kümesi doğrulanacaktır. QAC `(sûre:ayet:kelime:segment)` kullanır ve kelime düzeyine daraltılabilir; ancak veri dosyası görülmeden iki korpusun konum kümelerinin eşit olduğu varsayılmaz.

Beklenen aday kolonlar: `surah_number`, `verse_number`, `word_position`, `word`, `POS`, `qabas_lemma`.

## Erişim ve lisans politikası

Resmî indirme sayfası erişimi belirli kullanıcı/kurum koşullarına bağlamaktadır. Bu koşullar aşılmayacak; veri otomatik çekilmeyecektir. Veri yasal/izinli bir kanaldan edinilirse değiştirilmeden `02_morphology/quranmorph/quran-dataset.csv` yoluna konabilir ve ardından:

```bash
python 08_scripts/validate_quranmorph.py
python 08_scripts/crosscheck_qac_quranmorph.py
```

çalıştırılır.

QAC ile QuranMorph uyuşmazlığı otomatik olarak birinin yanlış olduğu anlamına gelmez; editoryal/lexikografik farklar ayrı belirsizlik katmanı olarak raporlanır.
