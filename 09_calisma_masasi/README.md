# 09_calisma_masasi — Kur'an çalışma masası

Talimat ve ilkeler: depo kökündeki [`CLAUDE.md`](../CLAUDE.md). Kanonik korpus **QAC v0.4**.
Bu katman `01_raw`, `02_morphology`, `03_indices`, `04_lexicons` klasörlerinden yalnız okur.

Durum: **Aşama 1** (`veri.py`, `tara.py`, `kayit.py`, sağlama testleri), **Aşama 2a** (`harf.py`, `okunus.py`) **Aşama 2b** (`okuma.py`, `kavram.py`) **Aşama 3** (`tez.py`), **Aşama 4** (`qm.py`, `--capraz`), **Aşama 5** (`ikincil/lane.py`, `ikincil/sami.py`) ve **Aşama 6** (`arayuz.py`). Python 3.10+; dış bağımlılık yok.

## Çalıştırma

```bash
cd 09_calisma_masasi
python -m tezgah denetim          # sha256, telif bloğu, temel sayımlar
python -m tezgah test             # sağlama testleri (§6) — her değişiklikten sonra
```

Depo kökünden: `PYTHONPATH=09_calisma_masasi python -m tezgah ...`

**Windows.** `-X utf8` ya da `PYTHONUTF8` gerekmez: giriş noktaları stdout/stderr'i UTF-8'e ayarlar (çıktı dosyaya
yönlendirildiğinde de), bütün dosyalar `encoding="utf-8"` ile açılır, metin dosyaları `newline="\n"` ile, hash'lenen
dosyalar ikili kipte yazılır ve sha diskteki baytlardan alınır. Depodaki `.gitattributes` satır sonu çevirisini
kapatır (git'in Windows varsayılanı `core.autocrlf=true` Tanzil dosyasının sha256'sını değiştirirdi). CI bunları
Linux ve Windows'ta Python 3.10 / 3.12 / 3.14 ile sınar (`.github/workflows/calisma-masasi-testleri.yml`).

## Web arayüzü

```bash
cd 09_calisma_masasi
python -m tezgah arayuz                     # http://127.0.0.1:8765/ tarayıcıda açılır
python -m tezgah arayuz --port 8766 --tarayici-acma
```

- Yalnız Python standart kütüphanesi (`http.server`); ek paket gerekmez.
- Yalnız bu bilgisayardan erişilir (127.0.0.1). Host başlığı denetlenir, her form oturum belirteci taşır.
- Ekranlar: tarama · ayet okuma · kavram dosyası · tez sınama · ikincil katmanlar (hipotez).
- Arayüzün kendi sorgu mantığı yoktur. Her form bir `python -m tezgah ...` komutuna çevrilir ve paketin `main()`
  işleviyle çalıştırılır. Çıktı komut satırındakiyle aynıdır ve süzülmez. Uyarılar (ikiz kök, iki korpus farkı)
  sarı, `[hipotez]` satırları mor vurgulanır; kayıt satırı sonuç panelinin altında sabit durur, hata olsa da yazılır.
- Meal kutusu varsayılan olarak kapalıdır. Açılınca meal "kurumsal okuma — sınanan, delil değil" etiketiyle,
  çalışma çevirisinin altında gösterilir.
- Sonuç sınırı olan her formda **Tümünü göster** kutusu vardır (`--limit 0`); varsayılan kapalıdır.
- **Hemze ve ayn** eş aralıklı yazı tipinde düz kesmeden ve birbirinden ayırt edilemeyecek kadar küçüktür. Arayüz
  harfin hücresini boyar: `ʾ` hemze (U+02BE) mavi zemin + düz alt çizgi, `ʿ` ayn (U+02BF) turuncu zemin + noktalı
  alt çizgi; düz kesme `'` (U+0027, yalnız Türkçe yazımda) işaretsizdir. Üstte lejant, harfin üzerinde kod noktası
  ipucu vardır. Metin değişmez (kopyalanınca yine U+02BE / U+02BF).
- `test` ve `kur` arayüzden çalışmaz; komut satırından çalıştırılır.

## Komutlar

| komut | örnek | birim |
|---|---|---|
| `sayim` | `sayim` · `sayim --kok Slw` · `sayim --etiket "(IV)" POS:V` | kelime konumu / ayet / sûre; etikette segment |
| `kok` | `kok Slw` · `kok "ص ل و"` · `kok Slw --bw` | kelime konumu |
| `lemma` | ``lemma 'Salaw`p'`` | kelime konumu |
| `kokler` | `kokler --limit 20` | kelime konumu / ayet / sûre |
| `dagilim` | `dagilim --kok Amn --gore tur\|lemma\|bab\|iyelik\|sure` | tür, lemma, sûre: kelime konumu · bab, iyelik: segment |
| `etiket` | `etiket PRON:3MP "(X)"` | segment |
| `birlikte` | `birlikte Amn Eml --pencere 3` | ayet (pencerede ayrıca kelime konumu çifti) |
| `kalip` | `kalip "ROOT:Amn&POS:V PRON:3MP bi+"` | segment dizisi |
| `okunus` | `okunus 2:3 30:30` · `okunus 1:1 --arapca` · `okunus --mukattaa` · `okunus 2:3 --durak` | — (Tanzil Uthmani v1.1; aktarım, delil değil); `--mukattaa`: ayet / sûre |
| `ayet` | `ayet 2:3` · `ayet 2:3 --meal` | kelime konumu (okunuş + QAC çözümlemesi + çalışma çevirisi; meal isteğe bağlı) |
| `ceviri` | `ceviri 2:3 "..."` · `ceviri 2:3` | — (kullanıcının yorumu) |
| `arayuz` | `arayuz` · `arayuz --port 8766 --tarayici-acma` | — (yerel web arayüzü; aynı komutlar) |
| `kur` | `kur meal` · `kur quran-morphology` · `kur lane` · `kur sedra` | — (yerel/, depoya işlenmez) |
| `lane` | `lane kok Slw` · `lane kok Slw --madde 2 --tam` · `lane kapsam` · `lane sigla` | hipotez; `kapsam`: kök; `sigla`: atıf geçişi (tablo: [`lane_kisaltmalari.tsv`](lane_kisaltmalari.tsv)) |
| `sami` | `sami kok Slw` · `sami kok Slw --zayif-son` · `sami kok Elm --tek-dil` · `sami gurultu` · `sami denklik` · `sami atif` | hipotez; `gurultu`: kök |
| `--capraz` | `kok Slw --capraz` · `sayim --kok nws --capraz` | kelime konumu / ayet / sûre; QAC ve quran-morphology ayrı tablolar + kök ataması farklı konumlar |
| `kavram` | `kavram liste` · `kavram goster salat` · `kavram ac salat --soru "..." --kok Slw` · `kavram sorgu salat --bolum asama2 -- kalip "ROOT:Slw&POS:V"` · `kavram ayet salat 2:3` · `kavram oneri salat ...` · `kavram yenile salat` · `kavram denetle salat` | bkz. [`kavramlar/README.md`](kavramlar/README.md) |
| `tez` | `tez liste` · `tez ac t --tez "..." --tanim "terim=tanım" --eksen kip=tanımlayıcı --eksen düzlem=oluşum --karsi "kalip ROOT:Slw&POS:V"` · `tez tara t` · `tez bulgu t --eksen ... --raf ... --aciklama ... -- kalip "..."` · `tez sonuc t ...` · `tez yeni-surum t --gerekce ...` · `tez goster t` · `tez denetle t` | bkz. [`kavramlar/README.md`](kavramlar/README.md) |

Kurallar:

- **Kök girişi** Arapça harf veya Buckwalter'dır. Latin okunuş (`s-l-v`, `salat`) reddedilir; araç olası
  Buckwalter karşılıklarını önerir ama sorguyu çalıştırmaz. Envanterde olmayan kök boş sonuç değil hata verir.
- Buckwalter büyük/küçük harf duyarlıdır: `Slw` = ص ل و, `slw` = س ل و. Böyle bir ikiz varsa çıktının başına uyarı basılır.
- Kökler çıktıda ayrık, kayıpsız Latin biçimde gösterilir: `Slw → ṣ-l-v`, `fTr → f-ṭ-r`, `rwH → r-v-ḥ`, `Amn → ʾ-m-n`.
  Noktalı harfler ص/س, ط/ت, ح/ه/خ ayrımını korur (`fTr` ile `ftr` ayrı köklerdir). Harf tablosu okunuşla
  ortaktır: [`okunus_kurallari.md`](okunus_kurallari.md) §1.
- **Etiket** tam eşleşmedir; QAC FEATURES belirteçleri olduğu gibi yazılır (`(IV)`, `PRON:3MP`, `ROOT:Amn`, `ACT`, `PCPL`),
  TAG sütunu için `TAG:V`. Alt-dize eşleşmesi yalnız `--alt-dize` ile yapılır ve uyarı basılır. QAC I. babı etiketlemez.
- **Liste sütunları** (`kok`, `lemma`, `etiket`, `kalip`, `dagilim --gore lemma`): *biçim* kelimenin ayet içindeki
  okunuşudur (okunuş motoru + `tanzil_qac_alignment.csv`; ayet görünümüyle aynı: 2:3:5 `ṣṣalâta`), *lemma* lemmanın
  tek başına okunuşudur (`ṣalât`, `ʾinsân`; kurallar: [`okunus_kurallari.md`](okunus_kurallari.md) §6). Hizalaması
  farklı kelimede okunuşun yanında `[not: ...]` yazar. Buckwalter yalnız `--bw` ile, ek sütun olarak gösterilir.
  Okunuş Tanzil'den üretildiği için bu listelerin kayıt satırında kaynak `QAC v0.4 | + Tanzil Uthmani v1.1` olur.
- **Kalıp**: boşlukla ayrılmış ardışık segmentler; `&` aynı segmentte birlikte, `!X` X olmasın, `*` herhangi bir segment.
  Varsayılan kapsam ayettir (kelime sınırı geçilebilir); `--kelime-ici` ile tek kelime konumuyla sınırlanır.
- **Bab**: QAC I. babı işaretlemez. Fiilde işaretsiz gövde `I` olarak, isimde `işaretsiz` olarak raporlanır.
- **İyelik**: isim gövdesinin etiketlerinde zamir aranmaz, sonraki son ek segmentine bakılır. Fiildeki ek zamirin
  özne mi nesne mi olduğu QAC morfoloji dosyasında etiketli değildir; ayrı tabloda gösterilir.

Her çıktı §8 kayıt bloğuyla biter (kaynak, sayım birimi, tam komut, veri izi, durum). Çalışmayan sorgu
`Durum: çalıştırılmadı` yazar ve 2 çıkış koduyla döner.

## Klasörler

- `tezgah/` — Python paketi
- `testler/` — sağlama testleri (`unittest`; CI'da `core-integrity.yml` içinde de çalışır)
- `kavramlar/` — çalışma çevirisi ve kavram dosyaları
- `yerel/` — depoya işlenmeyen yerel veri (`.gitignore`): meal, quran-morphology, lane, sedra
- `okunus_kurallari.md` — okunuş ve kök gösteriminin ortak harf tablosu ve kuralları
- `lane_kisaltmalari.tsv` — Lane kaynak kısaltmaları: kategori, eser, kimlik ve kategori dayanağı (hipotez katmanı)
