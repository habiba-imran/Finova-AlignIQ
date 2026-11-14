# Public TMT references — offline evaluation only

The supplied PDF and CSV are preserved unchanged. Their filenames omit the attachment's `(1)` suffix. These are published screenshot-derived references, **not original vendor clipboard exports, synthetic clinical cases, released semantic evidence or clinically approved recommendations**.

`transcription_review.json` is a separate visual transcription from the publisher-hosted figures, performed by the coding agent on 14 November 2026. It is not a dual-human or clinical verification. Every cell has a figure/row/column/CSV-line mapping in `evidence/final/public-reference-evaluation.json` after evaluation. Number/suffix spacing is compacted in the CSV; row punctuation and `°` → `(deg)` notation are re-typesetting choices, not byte-original figure labels.

One supplied error is retained: **Mamani Figure 2, row Angulation, tooth 25, CSV line 94: `24D` versus source `2.4 D`**. The supplied PDF also has `24D`. The `*-corrected.tsv` fixtures apply the explicitly documented source-review overlay; the `*-as-supplied.tsv` fixtures keep the original error. Neither changes the supplied CSV/PDF or enrolls a vendor mapping.

Reproduce from the repository root:

```powershell
.\backend\.venv\Scripts\python.exe backend/scripts/evaluate_public_tmt.py --write-fixtures --output evidence/final/public-reference-evaluation.json
```

This invokes the existing lexical parser through `LexicalInput`, offline, without a synthetic-data declaration, provider call, HTTP request or clinical rule execution. Do not paste these research case-derived values into the synthetic-only website or use its confirmation checkbox for them. Demonstrate this reference test at the terminal; use the fixed fictional examples in the website.

## Attribution and scope

- **Mamani J. et al. (2024).** *Effectiveness of Clear Aligners on Sequential Maxillary Molar Distalization: Discrepancy between Treatment Goal and Outcome.* J. Clin. Med. 13(14):4216, Figure 2. [Article](https://www.mdpi.com/2077-0383/13/14/4216), [DOI](https://doi.org/10.3390/jcm13144216), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Mamani-derived re-typesettings retain this attribution/license and identify the correction.
- **Sabouni W., Al-Ibrahim H.M. (2026).** *Roll, pitch, and yaw control using targeted mechanics in clear aligner therapy – A case report.* APOS Trends Orthod. 16:236–244, Figure 4(a)/(b), first six columns only. [Article](https://apospublications.com/roll-pitch-and-yaw-control-using-targeted-mechanics-in-clear-aligner-therapy-a-case-report/), [DOI](https://doi.org/10.25259/APOS_256_2024), [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Sabouni-derived re-typesettings/reviewed numerical data in this directory are attributed adaptations under CC BY-NC-SA 4.0; noncommercial/share-alike conditions apply to those assets. This does not license unrelated application code.
- **Paquet G. et al. (2026).** [Article / Figure 7](https://doi.org/10.1007/s44525-026-00011-7). Linked/layout-only reference; **zero numerical entries** in this corpus. The article states CC BY-NC-ND 4.0; no adapted Paquet numerical fixture is supplied.
- The linked ClinCheck guide is all rights reserved; no manufacturer screenshot/manual is redistributed here. SureSmile help supplies contextual definitions only; it does not authorize ClinCheck interpretation.

Downloaded source images/PDFs and rendered review pages are ignored local QA material, with provenance in `evidence/final/reference-review/fetch-manifest.json`. They are not bundled app assets. The offline evaluator has no network dependency. Rechecking original source images requires access to the cited publisher URLs. Do not present this single-agent transcription check as manufacturer certification, clinical validation or human-reviewed vendor gold.
