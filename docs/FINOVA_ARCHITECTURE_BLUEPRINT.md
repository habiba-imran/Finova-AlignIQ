**FINOVA  /  ALIGNIQ     •     TECHNICAL SPECIFICATIONS** 

# **Finova AlignIQ  |  Final Architecture Blueprint** 

_React + FastAPI · Phase 0 through clinician-reviewed future features_ 

**Version 1.0 · 13 November 2026 · Product status: development blueprint, not a clinical-release approval** 

## **1. Executive decision and boundaries** 

**Build:** a clinician-facing web application that accepts copied Tooth Movement Table (TMT) text, checks source semantics, creates deterministic movement descriptions, and produces traceable review memos. Keep it explicitly distinguishable from autonomous dental treatment planning. 

**Do not build in the initial release:** Chrome extension, LLM-based parser, custom ML model, attachment shape prescriptions, clinical prognosis, treatment staging optimizer, IPR planning, collision detector, or risk scoring. 

**Audit decision:** GO for controlled parser/descriptive prototype; NO-GO for clinical decision support deployment. The corrected rule spec FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md is authoritative over the previous v1 research. See audit P0/P1 blockers. 

## **2. Confirmed technology stack** 

|**Area**|**Choice**|**Notes**|
|---|---|---|
|**Web UI**|React, TypeScript, Vite|SPA; no browser extension|
|**Styling**|Tailwind CSS|Responsive, accessible, restrained clinical-<br>style UI|
|**Client testing**|Vitest + React Testing Library|Component/unit tests|
|**E2E testing**|Playwright|Paste, whitespace and accessibility smoke<br>paths|
|**Backend**|Python 3.12+, FastAPI, Uvicorn|Typed JSON API; development-only initially|
|**Models/validation**|Pydantic v2|Strict API and domain contracts|
|**Parser (future phase)**|Python stdlib + Decimal + source adapters|Deterministic, no AI/LLM|
|**Clinical engine (future)**|Plain Python functions + versioned YAML<br>policy registry|No generic ungoverned rule language /<br>cutoffs|
|**Text (future)**|Typed deterministic templates|Optional bounded LLM only after separate<br>safety/PHI review<br>i|
|**Backend testing**|pytest + httpx|Contract, fixtures and rule tests<br>f|
|**DB**|None in first phase|PostgreSQL only if storage/sign-off becomes<br>necessary|
|**Deployment**|TBD following security/privacy/regulatory<br>review|No patient data in prototype by default|



## **3. End-to-end architecture (planned, not all implemented at once)** 

[Clinician / synthetic TMT] | v React input UI  -- raw pasted text, source claim, exact visible preview | v 

FastAPI intake -- size/security/consent gates -- no PHI logging |  (PHASE 1+, not in initial Codex task) v 

- Deterministic source + layout detection |-- known, version-verified ClinCheck adapter 

- |-- known, version-verified SureSmile adapter 

`-- UNKNOWN -> structured clarification/abstention v Field-by-field canonical representation + original provenance v G/N semantic/coverage rules -> verified-only D descriptions v Sufficiency gate -> (later) clinician-approved R policies ONLY v Dedup/conflict/safety guards H/A05/A06/L -> vetted text templates v 

Draft review memo + evidence trail -> clinician review/sign-off 

Finova AlignIQ  |  Working specification  |  13 Nov 2026 

**FINOVA  /  ALIGNIQ     •     TECHNICAL SPECIFICATIONS** 

## **4. Intended use and explicit nonclaims** 

- Audience: authorized orthodontists or their supervised staff evaluating movement summaries; prototype uses only synthetic/deidentified data. 

- Does not diagnose, prescribe, guarantee movement or determine appliance suitability. 

- Total movements are programmed, not achieved; co-programmed is not necessarily simultaneous. 

- No claims about anchorage, roots, bone, periodontium, occlusion, 3D collisions, stage suitability, attachment omission, IPR, treatment duration or success percentages from total TMT. 

- Clinical deployment requires local legal/regulatory classification, independent expert rule approval, technical validation, privacy controls and real-world monitoring. US FDA transparency alone does not determine status in Pakistan or elsewhere. 

## **5. Flexible formatting without an LLM: two different concerns** 

### **5.1 Phase 0 = accept imperfect raw paste; DO NOT parse** 

The input UI must accept pasted multiline text exactly as browser text input provides it, including ragged whitespace, tabs, spaces, multiple blank lines, uneven columns, unicode punctuation and line breaks. **Do not trim, clean, split into columns, normalize numbering, validate movements or infer platform semantics in this first task.** The first UI shows a faithful monospaced raw preview using CSS white-space: pre-wrap/tab-size, plus character/line counts (descriptive UI metadata only). 

Known browser limitation: textareas typically normalize platform newline sequences; do not promise byte-for-byte original clipboard reconstruction. Preserve the logical user-pasted characters and spacing without app-level mutation. Keep raw data local in memory in phase 0; no persistence or network upload. 

### **5.2 Later parser = tolerate formatting but do NOT infer unknown semantics** 

Layer 1 tokenization/delimiters; layer 2 orientation/header detection; layer 3 verified source/version mapping; layer 4 exact numeric + direction parsing; layer 5 provenance and coverage; layer 6 semantic eligibility and abstention. Configurable adapters handle ClinCheck/SureSmile variants **only after real clipboard fixtures** confirm serialization. Unknown vendors/versions can be accepted as raw input but cannot silently become clinically interpretable data. 

### **5.3 Source metadata that cannot be guessed** 

Tooth notation (FDI, Universal, Palmer), arch, dentition, plan mode (Align/Doctor/Comparison), total/cumulative/incremental scope, stage index, and reference basis (crown center / virtual root apex / cusp tip), plus validated direction sign convention and coordinate meaning. 

## **6. Domain data contracts for future implementation** 

Create schemas/ with versioned JSON examples **as design artifacts only** in phase 0; do not build parsing around illustrative exports. Proposed future types: RawTMTSubmission, SourceContext, ParsedMeasurement, AxisCoverage, ParseIssue, RuleEligibility, StructuredFinding, DraftMemo, ReviewEvent. 

### **Submission (planned contract, NOT phase-0 endpoint)** 

{ 

"case_id": "demo-case-001", "raw_text": "<pasted raw text>", "source_claim": "UNKNOWN", "source_version": null, "notation": "UNKNOWN", "plan_mode": "UNKNOWN", "reference_basis": "UNKNOWN", "scope": "UNKNOWN" } 

### **Three independent status dimensions** 

1. **Field parse status:** CONFIRMED, SEMANTICS_UNKNOWN, PARSE_INVALID, UNSUPPORTED, NOT_PRESENT, EXPLICIT_ZERO (not every value is a parsed measurement). 

2. **Rule evaluation status:** OBSERVED, REVIEW_ELIGIBLE, CONTEXT_REQUIRED, DISABLED, SUPPRESSED, NOT_APPLICABLE. 3. **Report review status:** DRAFT, REVIEWED, APPROVED, REJECTED, SUPERSEDED with authorized reviewer, version and timestamps. 

Use stable, source-referenced typed findings; every sentence must map to a finding ID and original displayed value. No untraceable free-text-only output. 

Finova AlignIQ  |  Working specification  |  13 Nov 2026 

**FINOVA  /  ALIGNIQ     •     TECHNICAL SPECIFICATIONS** 

## **7. Future API boundaries (design, not build-now)** 

|**Endpoint**|**Intent**|**Earliest phase**|
|---|---|---|
|**GET /api/health**|Health check; no patient information|Phase 0|
|**POST /api/v1/tmt/parse**|Deterministic parsing/metadata<br>clarification; NO clinical advice|Phase 1|
|**POST /api/v1/tmt/observations**|Run vetted G/N/D/H safety & descriptive<br>outputs|Phase 2|
|**POST /api/v1/reports/draft**|Render structured template memo (same<br>validated input)<br>f|Phase 2|
|**POST /api/v1/reports/{id}/review**|Authorized sign-off and amendment<br>handling|After auth/audit storage|
|**POST /api/v1/rules/evaluate**|Approved clinical rule evaluation only|After clinical policy sign-off|



Avoid broad POST /analyze with uncontrolled AI decisions; separate parsing, descriptive observation, clinical policy and report rendering in code and API permissions. 

## **8. Repository layout (create only phase-0 portions initially)** 

finova-aligniq/ docs/ FINOVA_ARCHITECTURE_BLUEPRINT.md FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md Orthodontic_TMT_Independent_Critical_Audit(2).docx  # user-supplied frontend/ src/ app/                         # app root / routes if needed components/ TmtInputPanel.tsx RawPastePreview.tsx StatusNote.tsx styles/ main.tsx tests/ backend/ app/ main.py                     # /api/health only in Phase 0 api/ domain/                    # empty scaffold / README only tests/ schemas/                       # design docs only initially .env.example .gitignore README.md 

No database, auth, LLM provider, clinical policy execution or parser implementation in phase 0. Empty future directories are optional; avoid elaborate speculative services. 

## **9. Phase 0 — exact first Codex implementation scope** 

**Build a polished, small responsive single-page UI** under Finova AlignIQ branding: navigation/header, short description and explicit “prototype / not for clinical use” label; optional source selector (Unknown / ClinCheck / SureSmile, default Unknown and described as **user claim only** ); large multiline paste area; character and line counts; original-text preview; clear-input button; synthetic example button clearly labeled as demo; “Parsing not enabled yet” status; optional disabled Analyze button. Keep keyboard/screen reader friendly and loading/error states if any. 

**No parser even in disguise:** no header recognition, tokenization, split on tabs, automatic column alignment, numerical extraction, platform detection, semantic inference, dental rules, JSON normalization, LLM, backend processing of pasted clinical text or recommendations. 

**Frontend state:** locally retain raw text; accept pasted input with tabs, arbitrary spacing, irregular line breaks and Unicode. Do not call trim() or replace() on the raw state. Preview with <pre> and white-space: pre-wrap/overflow-wrap:anywhere, horizontal overflow management and tab-size for display only. No real patient data or browser storage in phase 0. 

**Backend:** FastAPI app with only GET /api/health and basic CORS limited to dev origin. Frontend health indicator optional. No endpoint accepting TMT text yet. 

Finova AlignIQ  |  Working specification  |  13 Nov 2026 

**FINOVA  /  ALIGNIQ     •     TECHNICAL SPECIFICATIONS** 

## **10. Phase 0 acceptance tests** 

- npm run dev, npm run build, frontend tests and backend startup work locally with README instructions (Windows PowerShell friendly). 

- Pasting ragged, tab-separated, mixed-spacing, blank-line, Unicode-minus or degree-symbol text retains the same logical text in state and preview; character/line counts update; no content silently removed. 

- Unknown format is accepted as raw text, with no falsely “parsed successfully” label. 

- Clear and demo controls work. Demo is synthetic and visibly nonclinical. 

- Mobile and desktop layouts do not clip long lines; keyboard, labels, focus indicators and screen reader support work. 

- No network request containing pasted content, no localStorage persistence, no browser console logging of sensitive content. 

- Health endpoint returns JSON with app status; no backend clinical implementation. 

- Tests cover irregular whitespace, empty input, very long line handling, clear/reset and safe rendering of <script> as inert text. 

## **11. Later implementation phases and gates** 

|**Phase**|**Deliverable**|**Exit gate**|
|---|---|---|
|**0**|Scaffold + raw input UI|Paste fidelity + build/tests|
|**1**|Format-verifiable deterministic parser +<br>source semantics|Consented real clipboard oracles; known<br>adapters exact; unknown fails closed|
|**2**|G/N gates + D descriptions + H/L safeguards<br>and templates|Automated deterministic oracle tests, no<br>unsupported clinical claims|
|**3**|Clinician-approved review policies (small R<br>subset)|Individual signed thresholds, cases,<br>applicability, overrides and independent<br>shadow study|
|**4**|Secure clinician beta and review workflow|Privacy/security/regulatory assessment,<br>audit/review identity and rollback|
|**Later**|Advanced staging/attachment/geometry<br>and/or ML|Additional data source and independent<br>module-specific validation|



## **12. Governance, risk register and decision log** 

**P0 blockers for parser release:** authentic anonymized ClinCheck + SureSmile clipboard captures; source version and notation; mode and reference basis; verified cross-vendor mappings; supported/unsupported fixtures. Screenshots alone are not serialization proof. 

**P0 blockers for clinical rule release:** explicit exact intended use, qualified orthodontist approval, no manufacturer bands as universal cutoffs, missing-context guards and independent multi-reader evaluations. 

**Security:** untrusted text may contain PII, HTML/script, formula payloads, or prompt injection. In early prototype avoid real patient data entirely; no persistence, external LLM calls, telemetry of raw input or secrets in frontend. 

**Model/LLM:** absent in phase 0–2; later text-only optional feature with separately reviewed privacy agreement, structured-finding entailment validator and deterministic fallback. 

**ML:** not necessary for parser or deterministic descriptive MVP. An eventual outcome predictor requires independently labeled actual clinical outcomes, proper patient-level evaluation, calibration and prospective validation; do not call it a “validator” of rule outputs. 

**Dependencies/assumptions:** all clinical source policies stay disabled by default; signed versions required; no patient-specific promises; clinical and regulatory reviews are distinct. 

## **13. Source of truth and handoff procedure** 

4. Developer shall read this architecture document **and** the full corrected rules v2 **and** the user-supplied independent audit (all pages, tables and addenda) before changing code. 

5. In conflicts, follow the independent audit and corrected v2 guardrails; note uncertainty and do not silently choose a more permissive policy. 

6. First build only Phase 0. Keep parser and engine interfaces as documented plans—not working functions. 

7. After finishing, report exact files changed, install/run/test commands, test results, unresolved decisions and specific next phase proposals. 

## **14. Primary publicly checked references and remaining limits** 

- SureSmile Step 4 staged model review: https://docs.suresmile.com/suresmile_webhelp/Aligners/Aligner_Step_4.htm 

- SureSmile using attachments: https://docs.suresmile.com/suresmile_webhelp/treatment_planning/Using_Attachments.htm 

- FDA Clinical Decision Support final guidance (January 2026): https://www.fda.gov/regulatory-information/search-fda-guidancedocuments/clinical-decision-support-software 

Finova AlignIQ  |  Working specification  |  13 Nov 2026 

**FINOVA  /  ALIGNIQ     •     TECHNICAL SPECIFICATIONS** 

- Primary Align/ClinCheck documents and 21-source audit-status list appear in the corrected rule spec. Vendor documentation establishes feature semantics, not clinical threshold validity. 

### **Final implementation verdict** 

**Start Phase 0 immediately.** Start parsing once real source clipboard samples and conventions are verified. Keep the future clinical decision engine inactive until specific rules have expert-approved policies and independent testing. Neither the 82-rule count nor inclusion of citations constitutes clinical readiness. 

Finova AlignIQ  |  Working specification  |  13 Nov 2026 

