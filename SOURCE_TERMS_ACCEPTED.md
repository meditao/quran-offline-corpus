# Source Terms Accepted

The repository owner has explicitly confirmed acceptance of the source terms required for the automated bootstrap of the offline Quran corpus.

Accepted sources:

- Tanzil Quran Text terms/license
- Quranic Arabic Corpus (QAC) v0.4 terms/license
- Açık Kuran API/data license terms applicable to the snapshot workflow

Acceptance statement received in ChatGPT on 2026-09-14:

> “Tanzil, QAC ve Açık Kuran şartlarını kabul ediyorum.”

This marker exists solely to authorize the repository's bootstrap workflow to retrieve, validate, and store the permitted source data according to the source-specific terms recorded in `SOURCES.md`.

Bootstrap notes:
- QAC v0.4 validator was corrected to accept the official lowercase version header and legitimate zero-form suffix segments.
- The retired `api.acikkuran.com` REST endpoint was decoupled from the core bootstrap; Açık Kuran remains an auxiliary root-by-root cross-check source via the live website.
