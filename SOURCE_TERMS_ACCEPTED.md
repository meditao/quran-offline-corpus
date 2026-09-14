# Source Terms Accepted

The repository owner has explicitly confirmed acceptance of the source terms required for the automated bootstrap of the offline Quran corpus.

Accepted sources:

- Tanzil Quran Text terms/license
- Quranic Arabic Corpus (QAC) v0.4 terms/license
- Açık Kuran API/data license terms applicable to the snapshot workflow

Acceptance statement received in ChatGPT on 2026-09-14:

> “Tanzil, QAC ve Açık Kuran şartlarını kabul ediyorum.”

This marker exists solely to authorize the repository's bootstrap workflow to retrieve, validate, and store the permitted source data according to the source-specific terms recorded in `SOURCES.md` and `LICENSES.md`.

Bootstrap notes:
- QAC v0.4 validator accepts legitimate zero-form suffix segments and pins the verified source SHA-256.
- Tanzil v1.1 source hashes are pinned by the validator.
- The retired `api.acikkuran.com` REST endpoint is decoupled from the core bootstrap; Açık Kuran remains an optional auxiliary cross-check source.
- Core refresh rebuilds the QAC indices and the Tanzil Uthmani v1.1 ↔ QAC v0.4 alignment audit.
