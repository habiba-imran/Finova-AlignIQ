# Finova — public TMT reference evaluation

14 November 2026, Asia/Karachi. **Offline, re-typeset reference evaluation. No vendor clipboard verification or clinical authorization.**

## Inputs and independent source check

Both requested files were located in [references/public_tmt](references/public_tmt/README.md), with the `(1)` filename suffix omitted:

| Supplied file | Identity and contents |
| --- | --- |
| [PDF pack](references/public_tmt/FINOVA_Public_TMT_Verification_Pack.pdf) | Five A4-landscape pages: inventory, Mamani re-typesetting, two Sabouni excerpts, source links and verification protocol. SHA-256 `8260592a37477351af30f1fd1e98e78dc03847968f2a32870a08bbff9c5a3bca`. |
| [CSV](references/public_tmt/FINOVA_Published_TMT_Values_Reference.csv) | 196 data rows plus header; source, figure, excerpt, tooth token, movement label, displayed value, URL and explicit not-clipboard flag. SHA-256 `4747683f3ee07fdf8c5bf0994269b378e4a8542c8323c96837ade9625789e980`. |

Both originals remain unchanged. The PDF is a later reference compilation, not a publisher original or native ClinCheck export. Its internal agreement with the CSV is not independent verification. Original publisher-hosted table images were retrieved and visually compared cell by cell; [fetch URLs/hashes](evidence/final/reference-review/fetch-manifest.json) and a separately entered [review grid](references/public_tmt/transcription_review.json) record the evidence. This is one coding agent's visual check, not independent dual-human/orthodontist adjudication. No OCR/model-generated transcription was accepted as evidence.

| Reference | Figure/excerpt and order checked | Review result |
| --- | --- | --- |
| [Mamani et al. 2024](https://www.mdpi.com/2077-0383/13/14/4216), DOI 10.3390/jcm13144216 | Figure 2, original PDF page 4: seven rows × 16 columns. Order **18,17,16,15,14,13,12,11,21,22,23,24,25,26,27,28**. The article documents ClinCheck Pro 5.3; screenshot mode/basis is not established by this cropped table. | 112 reviewed; **111 agree, 1 conflict**. Both terminal columns display dashes in all seven rows. |
| [Sabouni & Al-Ibrahim 2026](https://apospublications.com/roll-pitch-and-yaw-control-using-targeted-mechanics-in-clear-aligner-therapy-a-case-report/), DOI 10.25259/APOS_256_2024 | Figure 4a and 4b are separate first/second treatment-phase panels. Each supplied excerpt is seven rows × six columns, order **1.8,1.7,1.6,1.5,1.4,1.3**. The full figure contains additional columns outside the CSV; the excerpts are not complete arch datasets. | **42/42 + 42/42 agree**. Original tokens retain their dots; they are not converted to numbers/anatomy. Panel/phase identity stays separate from aligner stage semantics. |
| [Paquet et al. 2026](https://doi.org/10.1007/s44525-026-00011-7) | Figure 7/linked publisher image was inspected for layout only: four movement rows and Upper/Lower, Crown/Root controls. | **0 CSV cells; excluded from numerical denominators.** No extra values were invented/transcribed. |
| [ClinCheck Pro 6 guide](https://assets.ctfassets.net/vh25xg5i1h5l/qwpf6aq8qtSj0keD5bJzB/71bf896a5584a0a6311f52d03bce4581/MKT-0003721_Rev_J_User_Guide_ClinCheck_Pro_6-87-.pdf), section 3.15, printed p9 / PDF page 14; [SureSmile help](https://docs.suresmile.com/sure_clear_webhelp/treatment_planning/displacements_tab.htm) | Reviewed basis/mode and source-specific context. Manufacturer definitions are not a clipboard serialization oracle or universal cross-vendor map. | No manufacturer numerical sample added to the corpus or registry. |

The APOS article's earlier online date is 2024; its current volume publication is 2026, 16(3):236–244. The CSV's older `/2024/0/1/` image URL and the current publisher `/2026/16/3/` image were both accessible. Source/excerpt identity is retained rather than relabeling one phase as another.

## Confirmed transcription conflict

**Mamani Figure 2 → Angulation → tooth 25 → CSV line 94**:

- Supplied CSV and re-typeset PDF: **`24D`**.
- Publisher's original figure: **`2.4 D`**, compacted as **`2.4D`** in the independent review grid.
- Source grid location: movement row 6, tooth column 13. The decimal point is visible; it is not guessed from a clinical expectation.

The provided values were not silently corrected. The primary evaluation keeps `24D` and reports the source conflict. Separately named `*-corrected.tsv` fixtures apply the explicit reviewed overlay. Those generated files retain attribution, a re-typeset notice and the statement that a correction was applied. The parser correctly reading `24D` cannot establish that the transcription is faithful to the research figure.

All 196 positions were visually reviewable. **195 CSV cells were confirmed to agree; 1 was confirmed to conflict; 0 remained unreadable/unconfirmed.** Agreement is 195/196 = **99.49%** for this CSV, not parser accuracy, clinical accuracy or a general OCR/transcription benchmark. Cross-review by qualified independent humans remains absent.

## Evaluation method and separation of authority

[evaluate_public_tmt.py](backend/scripts/evaluate_public_tmt.py) reconstructs generic tab-separated tables using the **actual unchanged parser**, original CSV tooth tokens, label strings and cell values. These are deliberately authored **re-typeset evaluation fixtures**, not clipboard captures. The script uses existing `LexicalInput` and `parse_table`, then checks the unchanged semantic assessor. It never asserts `synthetic_data_confirmed` for published case-derived data and never sends them through the synthetic-only website/API, Groq, clinical review or fixed-demo admission.

The primary representation uses teeth in columns. A transposed control tests the same 196 cells with teeth in rows; it is a second representation, not additional independent source data. An explicit correction-overlay control repeats the same cells with the one source correction. Do not add these repeats into the 196-cell headline denominator.

For each original CSV row, checks compare tooth/movement identity, original compact value, exact numeric token/Decimal spelling, suffix, explicit header unit, missing/zero status and exact value/header/tooth spans against independently calculated authored-TSV coordinates. This catches swapped equal-valued cells as well as changed values. Each result links its CSV line, figure/panel, row/column and parser span; parser spans locate the **generated TSV**, not original PDF pixels or clipboard bytes.

Row labels are preserved **as supplied in the CSV**. They already standardize original figure punctuation and `°` to `(deg)`, and values compact number/suffix spaces. A crosswalk retains original visible labels. The evaluation does not claim byte-original screenshot typography or clipboard formatting fidelity.

## Exact results

| Primary as-supplied table | Source cells | Reviewed / agreeing CSV | Exact lexical positions | Numeric / zero / dash | Missing/unrecognized positions | Incorrect associations/values | Unsupported-label positions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Mamani Figure 2 | 112 | 112 / 111 | **112/112** | 98 numeric, including 2 zeros; 14 dashes | 0 | 0 | 64 |
| Sabouni Figure 4a | 42 | 42 / 42 | **42/42** | 42 numeric, including 3 zeros; 0 dashes | 0 | 0 | 24 |
| Sabouni Figure 4b | 42 | 42 / 42 | **42/42** | 42 numeric, including 3 zeros; 0 dashes | 0 | 0 | 24 |
| **Total** | **196** | **196 / 195** | **196/196 (100%)** | **182 numeric, including 8 zeros; 14 dashes** | **0** | **0** | **112** |

Denominators and limits:

- **Structural association coverage:** 196 assigned / 196 declared source positions, 100%; zero extra positions.
- **Exact lexical fidelity to supplied CSV:** 196/196, 100%, including 14 correctly retained dashes. Numeric extraction alone is **182/182**, not 196 numeric measurements. Decimal precision and literal suffixes are retained, including `2.0`, `1.0` and the supplied erroneous integer `24`.
- **Fidelity to independently reviewed figure values, as supplied:** **195/196** overall; **181/182** numeric. The one discrepancy originates in transcription, not parser substitution.
- **Explicit correction-overlay control:** 196/196 exact to source-reviewed compact values, including `2.4D`; source CSV/PDF remain unchanged.
- **Transpose control:** 196/196 exact to the same supplied values, with original tooth order preserved. Phase 1 and Phase 2 are never concatenated as one case/plan; a regression test confirms combined tables are rejected as ambiguous.
- **Lexical label support:** 84/196 positions use recognized Rotation/Angulation/Inclination aliases. Four CSV row families remain unsupported: `Extrusion / Intrusion`, `Relative Ext / Int`, `Translation B / L`, `Translation M / D`. Their 112 cell positions are retained; 104 numeric fields have UNSUPPORTED field status, while eight are missing dashes. Explicit unit labels remain available. Unsupported label recognition is not silently upgraded into a canonical axis.
- **Ambiguous numeric values in the original corpus:** 0; correctly withheld ambiguous source values = **0/0, not applicable**, not a 100% ambiguity score. Two separately mutated non-corpus tokens (`1.2Q`, `1e3`) are withheld **2/2** with null accepted numbers in regression testing.
- **Semantic/clinical eligibility:** **0/196**; semantic service status remains **DISABLED** under the empty release registry. This is the expected guard, not a parser failure. Zero provider calls; no clinical policies or vendor releases added.

Machine-readable results: [public-reference-evaluation.json](evidence/final/public-reference-evaluation.json). Ten new regression cases cover both orientations, independently located source spans, the correction conflict, input immutability, phase separation, ambiguity withholding, network prohibition and lack of semantic promotion. **No parser defect requiring a code change was identified.** Unsupported labels remain explicit limitations; no published-table-specific aliases or hardcoded parser cases were introduced.

## Reproduction and attribution

From the repository root:

```powershell
.\backend\.venv\Scripts\python.exe backend/scripts/evaluate_public_tmt.py --write-fixtures --output evidence/final/public-reference-evaluation.json
```

Exit 0 means the as-supplied lexical evaluation matches, **not** that every supplied transcription is correct. Read `confirmed_csv_cells=195`, `conflicting_csv_cells=1` and the per-cell records separately. Fixture writing is an explicit developer action; the application never imports them. The evaluator runs offline without credentials or downloaded figures. A later independent re-review can use the cited publisher URLs/hashes; online availability is not guaranteed.

Mamani-derived material is attributed under CC BY 4.0; Sabouni-derived adaptations retain CC BY-NC-SA 4.0 attribution and noncommercial/share-alike conditions within the reference assets. Paquet is CC BY-NC-ND 4.0 and supplies only a linked/layout observation, with no adapted numerical dataset. The ClinCheck manual is all rights reserved and is not redistributed. See the [reference README](references/public_tmt/README.md) for exact citations/license links. Local source/rendered images are ignored QA artifacts, not app content.

These references improve value-level regression coverage on independently checked published examples. They do **not** close the authentic clipboard/semantic adapter, clinical policy, patient privacy or production release gates. Original authorized clipboard bytes, source/version/mode/basis/scope context, independently reviewed semantic mappings and separately approved clinical validation remain required.
