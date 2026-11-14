# Finova AlignIQ — final local demonstration guide

Use only the bundled fictional examples and independently invented synthetic input in the website. Published case-derived references have a separate **offline lexical-only** command below. No credentials, patient input, live Groq request or public deployment is needed.

## 1. Install and start

Prerequisites: Node 22.12+ (verified locally with Node 24), Python 3.12 and PowerShell. From separate terminals:

```powershell
Set-Location 'C:\Finova AlignIQ\frontend'
npm ci
npx playwright install chromium

Set-Location 'C:\Finova AlignIQ\backend'
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Reuse an existing correct virtual environment; recreating it is not necessary for ordinary startup. Browser installation is required only for automated acceptance tests. Neither install command is needed every time you demonstrate.

Backend terminal:

```powershell
Set-Location 'C:\Finova AlignIQ\backend'
$env:FINOVA_ENVIRONMENT = 'development'
$env:FINOVA_PLANNING_DEMO_ENABLED = 'true'
$env:FINOVA_ATTACHMENT_DEMO_ENABLED = 'true'
$env:FINOVA_SEQUENCER_DEMO_ENABLED = 'true'
$env:FINOVA_GROQ_SYNTHETIC_ENABLED = 'false'
$env:FINOVA_PARSER_GROQ_ENABLED = 'false'
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --no-access-log
```

Frontend terminal:

```powershell
Set-Location 'C:\Finova AlignIQ\frontend'
npm run dev
```

Open [http://127.0.0.1:5173](http://127.0.0.1:5173). One backend process keeps optional recovery receipts consistent. No key loading or `.env.local` is required. Keep these development-demo flags off in production. Stop only your own servers with Ctrl+C when finished.

## 2. Suggested presentation sequence

Introduce it as **“an independently implemented PMCEASY-inspired engineering review prototype, using synthetic demonstrations and controlled evidence.”** Show the clinical warning, workflow steps and Macro/Micro/Nano navigation. Review purposes are not aligner stage numbers. Labels and counts indicate software/evidence state, not clinical risk.

### Macro — calculated descriptive findings

1. Choose Macro / Planning, then **Load Finova planning demo**.
2. Inspect the raw/lexical values and conventions. The fixed demo is already parsed. Choose **Deterministic templates**, then **Run Planning Assistant**.
3. Show **4 of 20 positions eligible**, **16 unavailable**, and five eligible descriptive comment units. These units are calculated from the admitted synthetic evidence; the phrasing is an authored template.
4. Show Sagittal / Transverse / Vertical, Other and withheld assessments. Exact examples retain `1.2300 D`, `0.4500 B`, `0.200 E`, `2.500 M`. The fifth numeric value has deliberately unverified semantics.
5. Expand a source/evidence disclosure. Select one eligible comment; **Copy selected comments** retains DRAFT context and unavailable assessments/limits. Copy the full DRAFT and download TXT. Neither action approves a plan or contacts CAD.

Say: “This is a description of programmed synthetic values. It does not prescribe changes, assess clinical dimensions, or predict achieved movement.” Groq is optional phrase selection only; the offline demonstration does not call it.

### Micro — supplied fictional attachment choices

1. Choose Micro / Attachments; the previous result clears. Load **Finova attachment demo**, then **Run Attachment Review**.
2. Show six rows: **two supplied candidates, one linked alternative, one supplied no-attachment decision, one unknown, one withheld**.
3. Expand row 1. Its invented dimensions remain **2.000 × 1.250 × 0.500 mm**; design/orientation/surface/window data are supplied examples with provenance, not calculated clinical geometry.
4. Contrast supplied no attachment with unknown/withheld. Inspect the alternative link, source refs and missing prerequisites. Copy/download the attachment DRAFT.

Say: “The application validates and presents these authored fictional decisions. It did not choose attachments from movement magnitudes, evaluate fit or determine that an attachment is unnecessary.”

### Nano — supplied fictional sequence/context plus real metadata checks

1. Choose Nano / Sequencing, load **Finova sequencing demo**, then **Run Sequencing Review**.
2. Show upper/lower arch, segments and separate right/left anchorage sections. Six strategy/context statements are supplied fictional inputs.
3. Expand the five stage records and evidence details. G15 checks actual supplied identifiers/order/kinds; those records contain **no stage-bound movement values**. Show **NO_STAGE_MOVEMENT_BINDING** and the unavailable assessment.
4. Explain that N07 remains not applicable to the source TOTAL values, and R13/T01–T08 remain disabled. No optimal order, force, auxiliary, anchorage-absence or duration decision was calculated.
5. Copy/download the sequencing DRAFT, which includes supplied origins, source values, missing prerequisites and the ledger.

### Published-reference parser check — terminal only

Keep the website's synthetic confirmation out of this step. In a terminal at the repository root:

```powershell
Set-Location 'C:\Finova AlignIQ'
.\backend\.venv\Scripts\python.exe backend/scripts/evaluate_public_tmt.py --write-fixtures --output evidence/final/public-reference-evaluation.json
```

Expected headline output: **196 source cells, 196 parsed exactly, 182 numeric positions, 195 CSV cells agreeing with original figures, 1 transcription conflict, 0 provider calls and 0 approved vendor releases**. Explain the difference between source fidelity and parser fidelity: the original Mamani figure shows `2.4 D` for tooth 25 angulation, but the supplied CSV/PDF says `24D`. Original files stay unchanged; separately labeled corrected fixtures document the overlay.

Open [the evaluation report](FINOVA_PUBLIC_TMT_REFERENCE_EVALUATION.md) and one generated TSV if useful. These are re-typeset fixtures, not original clipboard bytes. Four row-label families remain unsupported, all semantics remain disabled, and phase excerpts stay separate. The test does not turn research values into treatment instructions or establish vendor compatibility. No published case-derived values are sent to the website, Groq or clinical rules.

### Ordinary synthetic input — demonstrate safe abstention

Return to Macro and paste this independently invented table, then confirm synthetic input and Parse Table:

```text
# INDEPENDENT SYNTHETIC DEMO — not a published patient/case
Tooth|Rotation (deg)|Extrusion (mm)
A|1.2300 M|0.000 E
B|-|0.200 E
```

Run the Planning Assistant with deterministic templates. Expect four lexical positions, one explicit zero, one missing value and **zero eligible semantic observations**. The opaque tokens are retained without anatomy. An unavailable DRAFT is correct behavior. Micro and Nano on ordinary input also withhold attachment/sequence advice. Edit a value or change purpose and show that old results/exports clear.

## 3. Important handling of fixed demos

Fixed module demos use their own server-owned load/review route. **Load → inspect → run the module action.** Do not click Parse Table again unless demonstrating declassification. Editing, changing context/purpose/consent or ordinary re-parsing clears that demo path. Even an exact copy of the demo table through normal intake remains UNVERIFIED. Load the selected module's dedicated demo again to restore its fixed example. Neither a checkbox, raw-text prefix nor availability flag grants clinical authority.

## 4. Common troubleshooting

| Symptom | Check/action |
| --- | --- |
| Backend connection failure | Run the backend terminal; verify [health](http://127.0.0.1:8000/api/health). The compatibility field `phase:1` is historical, not the project phase. |
| Address/port already in use | Do not start a second server on that port. Stop the server you own, or use the existing correctly configured session. Avoid stopping unrelated processes. |
| Demo disabled / 404 | Restart the backend with exact development environment plus that module's flag. Those flags control fixed-route availability only. |
| Copied demo produces only unavailable results | Expected normal-input behavior. Use that module's dedicated load button again. |
| Recovery receipt expired/changed / 409 | Reparse unchanged synthetic input. Receipts last 15 minutes and are lost after backend restart; one process is required. They never verify semantics. |
| Generated recovery example has no values with Groq off | Expected bounded-parser behavior for that layout. It is not needed for the offline presentation; use clean/fixed examples. |
| Clipboard blocked | Keep the exact TXT download/export preview. Clipboard behavior can depend on browser/OS permissions. |
| Blank development page or intermittent browser startup | Check the frontend terminal, reload the local page and retain any reproducible failure. For acceptance use the isolated **production-bundle** command below. The historical shared-dev startup flakiness remains documented. |

## 5. Reproduce automated acceptance

Backend:

```powershell
Set-Location 'C:\Finova AlignIQ\backend'
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m pip check
```

Frontend:

```powershell
Set-Location 'C:\Finova AlignIQ\frontend'
npm test
npm run build
npm run test:e2e -- --config=playwright.final.config.ts --output=../evidence/final/browser-results
```

The final harness runs every existing scenario at **1440, 1024, 768, 672 and 375 px**, using fresh loopback backend 8019 and built preview 5179. Leave those ports free; it starts/stops its own servers, keeps Groq disabled and does not disturb ordinary 8000/5173 sessions. No timeout increase/retries hide failures. See [final integration results](FINOVA_FINAL_INTEGRATION_REPORT.md) for actual totals and warnings.

## Responsible closing statement

The deliverable demonstrates structure/value parsing, bounded evidence/rules, three module workflows, exact DRAFT reporting and explicit refusal. It does not recover PMCEASY's proprietary algorithms, validate native ClinCheck/SureSmile clipboard support, prescribe treatment, calculate attachments/forces/sequences, assess root/bone/collision safety or provide clinical approval. No clinical release or public deployment is part of this handoff.
