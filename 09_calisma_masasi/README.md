# 09_calisma_masasi — Kur'an çalışma masası

Talimat ve ilkeler: depo kökündeki [`CLAUDE.md`](../CLAUDE.md). Kanonik korpus **QAC v0.4**.
Bu katman `01_raw`, `02_morphology`, `03_indices`, `04_lexicons` klasörlerinden yalnız okur.

Durum: **Aşama 1** (`veri.py`, `tara.py`, `kayit.py`, sağlama testleri), **Aşama 2a** (`harf.py`, `okunus.py`) **Aşama 2b** (`okuma.py`, `kavram.py`) ve **Aşama 3** (`tez.py`). Python 3.10+; dış bağımlılık yok.

## Çalıştırma

```bash
cd 09_calisma_masasi
python -m tezgah denetim          # sha256, telif bloğu, temel sayımlar
python -m tezgah test             # sağlama testleri (§6) — her değişiklikten sonra
```

Depo kökünden: `PYTHONPATH=09_calisma_masasi python -m tezgah ...`

## Komutlar

| komut | örnek | birim |
|---|---|---|
| `sayim` | `sayim` · `sayim --kok Slw` · `sayim --etiket "(IV)" POS:V` | kelime konumu / ayet / sûre; etikette segment |
| `kok` | `kok Slw` · `kok "ص ل و"` | kelime konumu |
| `lemma` | ``lemma 'Salaw`p'`` | kelime konumu |
| `kokler` | `kokler --limit 20` | kelime konumu / ayet / sûre |
| `dagilim` | `dagilim --kok Amn --gore tur\|lemma\|bab\|iyelik\|sure` | tür, lemma, sûre: kelime konumu · bab, iyelik: segment |
| `etiket` | `etiket PRON:3MP "(X)"` | segment |
| `birlikte` | `birlikte Amn Eml --pencere 3` | ayet (pencerede ayrıca kelime konumu çifti) |
| `kalip` | `kalip "ROOT:Amn&POS:V PRON:3MP bi+"` | segment dizisi |
| `okunus` | `okunus 2:3 30:30` · `okunus 1:1 --arapca` · `okunus --mukattaa` · `okunus 2:3 --durak` | — (Tanzil Uthmani v1.1; aktarım, delil değil); `--mukattaa`: ayet / sûre |
| `ayet` | `ayet 2:3` · `ayet 2:3 --meal` | kelime konumu (okunuş + QAC çözümlemesi + çalışma çevirisi; meal isteğe bağlı) |
| `ceviri` | `ceviri 2:3 "..."` · `ceviri 2:3` | — (kullanıcının yorumu) |
| `kur` | `kur meal` | — (yerel/, depoya işlenmez) |
| `kavram` | `kavram ac salat --soru "..." --kok Slw` · `kavram sorgu salat --bolum asama2 -- kalip "ROOT:Slw&POS:V"` · `kavram ayet salat 2:3` · `kavram oneri salat ...` · `kavram yenile salat` · `kavram denetle salat` | bkz. [`kavramlar/README.md`](kavramlar/README.md) |
| `tez` | `tez ac t --tez "..." --tanim "terim=tanım" --eksen kip=tanımlayıcı --eksen düzlem=oluşum --karsi "kalip ROOT:Slw&POS:V"` · `tez tara t` · `tez bulgu t --eksen ... --raf ... --aciklama ... -- kalip "..."` · `tez sonuc t ...` · `tez yeni-surum t --gerekce ...` · `tez goster t` · `tez denetle t` | bkz. [`kavramlar/README.md`](kavramlar/README.md) |

Kurallar:

- **Kök girişi** Arapça harf veya Buckwalter'dır. Latin okunuş (`s-l-v`, `salat`) reddedilir; araç olası
  Buckwalter karşılıklarını önerir ama sorguyu çalıştırmaz. Envanterde olmayan kök boş sonuç değil hata verir.
- Buckwalter büyük/küçük harf duyarlıdır: `Slw` = ص ل و, `slw` = س ل و. Böyle bir ikiz varsa çıktının başına uyarı basılır.
- Kökler çıktıda ayrık, kayıpsız Latin biçimde gösterilir: `Slw → ṣ-l-v`, `fTr → f-ṭ-r`, `rwH → r-v-ḥ`, `Amn → ʾ-m-n`.
  Noktalı harfler ص/س, ط/ت, ح/ه/خ ayrımını korur (`fTr` ile `ftr` ayrı köklerdir). Harf tablosu okunuşla
  ortaktır: [`okunus_kurallari.md`](okunus_kurallari.md) §1.
- **Etiket** tam eşleşmedir; QAC FEATURES belirteçleri olduğu gibi yazılır (`(IV)`, `PRON:3MP`, `ROOT:Amn`, `ACT`, `PCPL`),
  TAG sütunu için `TAG:V`. Alt-dize eşleşmesi yalnız `--alt-dize` ile yapılır ve uyarı basılır. QAC I. babı etiketlemez.
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
- `yerel/` — depoya işlenmeyen yerel veri (`.gitignore`): meal
- `okunus_kurallari.md` — okunuş ve kök gösteriminin ortak harf tablosu ve kuralları
