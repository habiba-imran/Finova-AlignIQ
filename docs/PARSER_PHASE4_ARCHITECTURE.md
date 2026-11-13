# Phase 4 parser architecture

This implementation note supplements the governing audit, corrected v2 specification and final blueprint. It does not supersede their clinical restrictions or activate any clinical rule. See `../PARSER_PHASE4_REPORT.md` for supported grammars, quantitative validation and limitations.

## Data flow

```text
Explicit Parse Table
  Raw text + unverified context + optional generated-fixture identity
    -> existing lexical parser; deterministic Markdown wrapper support
    -> structural quality / relevance assessment
    -> no cloud for success, irrelevant text, semantic gaps or unprovable alignment
    -> optional automatic development recovery for server-reproduced synthetic text
       -> Groq proposes original-span associations using role-constrained IDs
       -> independent association proofs accept/quarantine each original position
    -> standardized ParseResult + detection/quality + optional signed receipt

Explicit review / report
  Same raw text + context + optional receipt
    -> signature, expiry and exact input/context binding check
    -> recompute source-span association proofs; reconstruct lexical result locally
    -> existing semantic assessor and empty vendor release registry
    -> existing descriptive safeguards / DRAFT report
```

## Module boundaries

- `backend/app/parser/service.py`, `values.py`, `teeth.py`, `labels.py`: original lexical routines and provenance. No source convention is verified here.
- `phase4.py`: deterministic-first orchestration, relevance/structural quality, gated automatic recovery. A recognized vendor indicator cannot trigger a provider call.
- `recovery.py`: explicit-record and delimited-ordinal witnesses, original-span lattice, role-constrained provider schema, validation, quarantine and lexical assembly. It does not interpret clinical axes/directions.
- `generated.py`: deterministic original synthetic recipes and independently constructed gold positions/values. Only recipe enums and bounded integer seeds are accepted. No arbitrary text enrollment exists.
- `receipts.py`: stateless HMAC-SHA256 receipt, 15-minute expiry, raw/source/context hash binding, independent proof recomputation on use. No raw source or values are stored in receipts.
- `semantics/`: existing exact evidence and release authorization. No vendor approvals/mappings were added.
- `review/service.py`: resolves the lexical evidence before the existing semantic checks. Structural unknowns additionally withhold zero-inventory statements. Clinical R predicates remain disabled.
- `reports/`: existing approved-wording/templates and local facts; the separate comment key is unchanged.

## Authority boundaries

The browser cannot submit trusted parsed JSON or semantic evidence. A receipt attests only that the server previously accepted some original-text associations; it is not a vendor release, semantic mapping, clinical finding or user approval. Even a valid signature is insufficient unless the associations can be re-proven from the exact supplied source.

Cloud access requires development environment, server feature permission, parser key and text that the server can regenerate from a controlled recipe/seed. Only an original generated rendering or its predefined browser-newline rendering is accepted; the input itself is never rewritten. A synthetic checkbox/prefix, claimed vendor or caller-provided confidence grants no authority. Arbitrary/real patient data remain ineligible for external parsing. Default configuration keeps cloud access disabled.

The legacy `/api/parse` and explicit `/api/v1/tmt/parse/assisted` remain compatibility routes. The UI uses the Phase 4 `/api/v1/tmt/parse` orchestration; it has no second AI action/consent checkbox. The existing intake synthetic-data confirmation remains a claim, not the authorization mechanism.

## Runtime constraints

Recovery: at most 8,000 source characters, 200 physical lines, 512 proposed association positions and 1,600 referenced cells. Exceeding proof bounds abstains as a whole, without sending a prefix. Existing lexical/body/number limits remain. Provider prompts/responses retain existing byte bounds, single-attempt parsing, timeout and strict-output validation. No tools, retries, account rotation or model-voting authority is introduced.

Receipt signing keys exist only in process memory and change on restart. Use one backend process for this development workflow; multiple independent workers cannot interchange receipts. Expired/restarted/context-changed evidence returns HTTP 409 with static reparse guidance. Supporting distributed receipts would require a separately managed signing-key/deployment design; no database, persistence or deployment change was introduced here.

No input/result cache, browser storage or patient-data persistence was added. All live checks are optional, fixed synthetic tests. Production cloud processing of actual clinical input remains a separate privacy/provider-authorization and clinical-governance task.
