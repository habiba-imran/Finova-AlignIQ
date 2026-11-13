# **ORTHODONTIC TMT RULE ENGINE INDEPENDENT AUDIT** 

#### **Evidence audit  |  82 individual dispositions  |  Technical and clinical release gates** 

Audit date: 13 November 2026  |  Basis: supplied 19-page v1.0 specification and externally checked vendor, clinical and regulatory sources. 

**VERDICT  —  GO FOR CONTROLLED PARSER / DESCRIPTIVE PROTOTYPE; NO-GO FOR CLINICAL DECISION SUPPORT DEPLOYMENT.** 

This is a technical evidence appraisal, not an approval by a qualified orthodontist, a regulatory determination or clinical advice. Bibliographic availability does not validate the clinical applicability of a published effect size. 

## **1 | Bottom-line findings** 

**Overall assessment** Strong document architecture and cautious language; clinical rules remain drafts, not executable clinical policy. 

**82 rules ≠ 82 clinical algorithms** 18 gates, 16 descriptions, 16 candidate review rules, 8 staging, 6 attachments, 12 safety and 6 output controls. Clinical triggers have no approved numerical criteria. 

**Data sufficiency** A total TMT can support verified movement descriptions; it cannot establish patient anatomy, prognosis, sequence, attachments, IPR, occlusion or collisions. 

**Most significant semantics** ClinCheck: crown vs root basis, Align vs Doctor vs Comparison and notation. SureSmile: center vs cusp and incremental vs cumulative stages. These are not interchangeable. 

**Evidence strength** Vendor guides explain capabilities. Heterogeneous clinical studies and low/very-low certainty reviews do not calibrate patient-specific threshold alerts. 

**Current blocker** No independently inspected real clipboard exports or orthodontist-approved policy/case gold standard was included in the supplied research document. 

Interpretation of disposition: READY = implement technical/negative-safety/observational behavior after fixture verification; REVISE = technically possible but current wording or prerequisites are defective; VALIDATE = candidate clinical decision requiring orthodontist-approved criterion and independent case review; MORE DATA = impossible to execute from a total-movement TMT alone. READY does not equal clinically validated. 

TMT-only column: Yes = observable from verified complete TMT fields; Yes* = also requires verified source/notation/mode metadata; Metadata = convention must be supplied or independently confirmed; Extra = separate plan/patient/stage input; System = processing/provenance state; Request = user intent and absent-context guard; Partial = movement may be observed, but clinical interpretation needs more data; No = not evaluable from total TMT. 

## **2 | Priority 0 / Priority 1 correction backlog** 

#### **P0 - BLOCK · No genuine Clipboard schema yet** 

Acquire consented, de-identified verbatim ClinCheck and SureSmile clipboard exports from target versions, with independent screenshot/manual verification of mode, notation, arch and tooth basis. Illustrative JSON and screenshots are not serialization evidence. 

#### **P0 - BLOCK · Separate proven semantic mapping from hypothesis** 

Implement strict adapter versions and field-level UNKNOWN. Pay particular attention to crown-referenced B/L/M/D/I/E and angular sign/rotation meaning, dentition, stage scope and source mode. Unknown versions must not silently match. 

#### **P0 - BLOCK · Prevent total/stage and plan/difference confusion** 

Comparison values are deltas, not absolute prescriptions. Stage count does not reconstruct motion timing. Preserve plan identity, display mode and reference point as first-class dimensions. 

Independent critical audit  •  13 Nov 2026  •  Draft for clinical reviewer 

#### **P0 - BLOCK · No active clinical thresholds** 

All R clinical checks stay disabled by default. The 0.3mm/3deg and historical Invisalign colored bands are product configuration examples, not scientifically validated universal warnings. 

#### **P0 - BLOCK · Never infer unseen anatomy or techniques** 

TMT cannot establish roots, alveolar bounds, periodontal state, occlusal contacts, IPR, attachment presence or collision-free trajectories. Withhold those conclusions across every output path. 

#### **P0 - BLOCK · Define narrow intended use and regulation** 

Is product merely a descriptive TMT review aid for orthodontists or a prescriptive therapy optimizer? Regulatory assessment must be intended-use- and jurisdiction-specific; FDA clinician-review criterion is not sufficient by itself. 

#### **P1 - BEFORE BETA · Fix temporal wording and compound rules** 

D02/D10/D11 must say co-programmed in same total plan, not occurring concurrently. R13 belongs in staged module and overlaps T01; A06 is a safety wording gate. 

#### **P1 - BEFORE BETA · Correct comparison/stage arithmetic** 

D16 needs common starting geometry and coordinate semantics, not merely same basis. T02 must not naively add rotations or mixed coordinate transforms. 

#### **P1 - BEFORE BETA · Define status, precedence and abstention** 

Use PARSE_INVALID, SEMANTICS_UNKNOWN, OBSERVED, REVIEW_ELIGIBLE, CONTEXT_REQUIRED, DISABLED, SUPPRESSED and CLINICIAN_SIGNED. Missing data is not a negative clinical finding. 

#### **P1 - BEFORE BETA · Build clinically supervised policy governance** 

Orthodontists approve precise trigger, patient/device applicability, source quality, exceptions, wording, severity, test cases, versions and rollback. An engineer-entered cutoff is not approval. 

#### **P1 - BEFORE BETA · Establish an independent multi-reader evaluation** 

At minimum evaluate case-level discrepancies, critical misses, over-flagging, abstentions and inter-reviewer agreement, with adjudication and high-harm categories. Do not choose arbitrary universal safety percentage. 

#### **P1 - BEFORE BETA · Strong text safety and data governance** 

Prefer deterministic templates; LLM only rephrases strictly structured findings if it is permitted, never introduces therapy recommendations. Explicit consent, PHI redaction, retention, access controls and provider terms. 

#### **P2 - ENHANCEMENT · Reduce duplication and policy complexity** 

Fold D10/D11 into co-programmed movement observations; consolidate H abstention checks by missing-context code while retaining externally traceable rule identifiers. 

#### **P2 - ENHANCEMENT · Model clinically relevant added inputs** 

Design optional schema for verified patient profile, stage transforms, initial/final meshes, IPR/attachments, occlusion, periodontal/root assessment and clinical goals; require separate validation for each module. 

## **3 | Independent evidence findings** 

**Manufacturer primary information** Align Technology ClinCheck Pro 6 (2020) explicitly states crown-center vs virtual-root-apex basis and Align final/Doctor final/Comparison. It also supports Universal, Palmer and FDI numbering; older vendor materials explicitly mention clipboard copying and crown-referenced directional labels. [S01; supplemental Align Pro 5 quick reference and 2015 fact sheet] 

**SureSmile primary information** Its public help confirms crown-center vs cusp-tip displacement; total at last cumulative stage; incremental per stage; editable constraints, staged overlap, root balancing and attachment timing. These are device behaviors, not validated biologic ceilings. [S03–S05] 

**ClearCorrect values** Official Straumann/ClearCorrect 2023 onboarding guide reports a default 0.3 mm 

translation/intrusion/extrusion and 3° rotation per step and a reduced 0.2 mm / 2° option. They are clinician-editable preferences for a different system, not cross-platform universal safety thresholds. [S06, corroborated] 

**Historic Invisalign bands** The historic Tooth Movement Assessment shows manufacturer color bands. It explicitly frames them as guidance on extent, not patient-level outcome probability. Numeric points read approximately from chart graphics should not be used as exact software bounds. [S02] 

Independent critical audit  •  13 Nov 2026  •  Draft for clinical reviewer 

**Clinical primary evidence** Haouili et al. 2020 is a prospective follow-up study of predicted vs achieved Invisalign movements; it helps establish that predicted and achieved movements diverge, not a safe cutoff for individual cases. Add primary clinical trials to future rule-specific evidence files. [Supplemental] 

**Rotation/intrusion/molar reviews** S10, S11, S12 cover specific movements, but their inclusion criteria and biases restrict generalization. S11 included 8 studies with 7 serious-risk-of-bias assessments; S12 grades evidence very low. No automated threshold approved. [S10–S12] 

**Attachments** S14's 7-study systematic review/meta-analysis found no statistically significant overall optimized-vs-conventional improvement for several movement outcomes, with substantial heterogeneity. Do not prescribe attachment shape. [S13, S14] 

**Complexity rubric is multi-input** S15 describes CAT-CAT case difficulty using model analysis, radiographs and clinical findings. Its molar movement categories cannot be extracted and substituted as a standalone TMT rule. [S15] 

**Regulatory status** FDA 2026 CDS guidance explains that the US non-device CDS exception depends on multiple statutory criteria; independent review of the basis is necessary but not sufficient. Intended use, geography and output authority need formal review. [S18, S19] 

**WHO source date clarification** WHO has a bibliographic catalog entry for a 2024 publication and a website item posted in March 2025 for the same ISBN; S20’s 2024 publication year is not inherently erroneous. [S20] 

## **4 | Source-by-source verification (all 21 cited entries)** 

|**ID**|**Audit status**|**Document/source**|**Evidence relevance / limitation**|
|---|---|---|---|
|S01|VERIFIED|Align Technology, ClinCheck Pro 6<br>manual, 2020|Primary vendor semantics: crown vs virtual root; comparison views;<br>numbering options. User-guide excerpt does not validate clipboard<br>serialization.<br>i|
|S02|VERIFIED /<br>HISTORICAL|Invisalign Quick Start: Tooth<br>Movement Assessment, older<br>undatedguide|Old threshold bands are visual/manufacturer-specific. Avoid numeric<br>extraction from approximate figure or clinical transfer.|
|S03|VERIFIED|SureSmile DIY Step 4 staging<br>constraints|Strong primary vendor description of editable rates, sequence, IPR and root-<br>balancingsetting,not validatedpatient-safe maxima.|
|S04|VERIFIED|SureSmile Aligner Step 4 stages|Primary vendor description: crown-center/cusp, cumulative/incremental<br>and interference display. Scope only.|
|S05|VERIFIED|SureSmile Using Attachments|Primary vendor account of placement and start/end stages, not proof of best<br>shape.|
|S06|PARTIALLY VERIFIED|ClearCorrect Clinical Preferences<br>(provided link inaccessible to<br>crawler)|Values cross-checked in official Straumann/ClearCorrect 2023 Onboarding<br>Guide: 0.3mm/3 deg and 0.2mm/2 deg as preferences, not safety maxima.|
|S07|PARTIALLY VERIFIED|ClearCorrect Engagers article<br>(direct link not fullyverified)|General workflow independently consistent with manufacturer guidance and<br>S05;noquantified indication established from cited item.|
|S08|VERIFIED ABSTRACT|Borzabadi-Farahani, scoping<br>review,Front Dent Med,July2026|Evidence maps heterogeneity, not threshold quality or case-level calibration.|
|S09|METADATA<br>VERIFIED / FULL<br>TEXT LIMITED|Naoum & Lee, Semin Orthod, 2026|Publisher ScienceDirect full text blocked in this review; bibliographic DOI<br>independently corroborated; do not claim fully inspected evidence.|
|S10|VERIFIED|Benedetti et al., Dentistry, 2025<br>rotation systematic review|Variable rotation outcomes; does not directly validate universal patient<br>thresholds.|
|S11|VERIFIED|Fracchia et al., J Clin Med, 2025<br>lower-incisor intrusion review|8 studies; 7 serious risk of bias; nonpooled heterogeneity; study ranges are<br>not clinical decision cutoffs.|
|S12|VERIFIED|Garcia-Marin et al., Angle Orthod,<br>2025 molar MD review|6 studies, very-low-certainty overall evidence; not basis for a universal rule<br>threshold.|
|S13|VERIFIED|Yangin et al., Turkish J Orthod, 2025<br>attachment review|Review supports biomechanical context and individualization, not specific<br>shape dominance.|
|S14|VERIFIED|Pandian et al., J Oral Biol Craniofac<br>Res,2025 systematic review|7 studies; 4 meta-analyzed; no overall significant optimized-vs-conventional<br>differences,substantial heterogeneity.|
|S15|VERIFIED|Wang et al., Int J Oral Sci, 2025<br>expert consensus|Full case-complexity rubric requires models, X-ray and clinical exam; tables<br>cannot be repurposed as TMT-onlyrisk thresholds.|
|S16|VERIFIED ABSTRACT|Modified Delphi international expert<br>study,ProgOrthod,2025|Expert consensus on scope/limits, not a mathematical gold standard or<br>proof of individualplan outcome.|
|S17|VERIFIED|Periodontal orthodontic expert<br>consensus,Int J Oral Sci,2025|Supports need for clinical periodontal assessment; TMT cannot replace it.|
|S18|VERIFIED|FDA Clear Dental Aligners, regulator|Supports clinician oversight and realistic disclosure; jurisdiction is US; not a<br>universal license to operate.|
|S19|VERIFIED|FDA Clinical Decision Support<br>Software finalguidance,Jan 2026|Non-device exclusion requires multiple conditions, not transparency alone;<br>seekjurisdiction-specific legal advice.|
|S20|VERIFIED; DATE<br>NUANCE|i<br>WHO AI/health large multimodal<br>modelsguidance,original 2024|i<br>WHO bibliographic catalog and 2024 release confirm 2024; one WHO item<br>webpage displays 2025posting. Document 2024 label is defensible.|
|S21|VERIFIED|Alsulaiman,Saudi Dental Journal,7|Useful biological explanation,weaker thanprimary quantitative validation;|



Independent critical audit  •  13 Nov 2026  •  Draft for clinical reviewer 

**ID Audit status Document/source Evidence relevance / limitation** <mark>Oct 2026 narrative review no patient-specif</mark> i <mark>c probabilities.</mark> 

A status of VERIFIED means the source/page or supporting official record was checked for the stated high-level claim; it does not imply that every statement, numerical figure, appendix or original study in that source was replicated. S06/S07/S09 should be obtained in full before treating them as fully audited rule-specific authorities. 

## **5 | Individual audit of all 82 rules** 

### **G01–G18 | Data and semantics gates** 

|**Rule**|**Decision**|**TMT only?**|**Independent assessment and required change**|
|---|---|---|---|
|G01|READY|Yes|Sound structural gate. Define recognizable headers, minimum row/column cardinality, encoding<br>and payload limits; an empty but valid zero-movement table must not be rejected merely for lacking<br>nonzero values.|
|G02|READY|Metadata|Necessary but a pasted table may not identify its source; user-selected source is a claim, not<br>verification. Confirm against signatures and make unmatched versions UNVERIFIED, not ClinCheck<br>bydefault.|
|G03|READY|Metadata|Critical. ClinCheck permits Universal, Palmer and FDI numbering; numeric 13 is ambiguous across<br>systems. Require verified notation, plus arch context and a normalization lookup with exhaustive<br>examples.|
|G04|READY|Yes*|Sound technical validation only after notation and dentition are known. Support optional third<br>molars, deciduous teeth, pontics and explicit unsupported identifiers; do not treat an absent row as<br>an invalid tooth.|
|G05|READY|Metadata|Useful if the source actually provides an independent arch marker. A mismatch should quarantine<br>an affected record rather than reinterpret itsquadrant automatically.|
|G06|READY|Yes*|f<br>Detect duplicate (case, plan, basis, scope, stage, tooth, axis) keys, not just repeated tooth numbers.<br>Repeated columns maybe legitimateplan comparisons and must not be combined.|
|G07|READY|Metadata|Essential. Make an explicit adapter-specific dictionary for extrusion/intrusion, B/L, M/D, rotation,<br>angulation and inclination. Preserve source name and axis; no generic cross-vendor conversion by<br>label similarityalone.|
|G08|READY|Yes|Correct engineering principle; specify decimal comma, unicode minus, empty cell, whitespace,<br>thousands separators, exponent notation, NaN/Infinity and unexpected degree signs. Units may be<br>implicit in a verified row header;lack ofper-cell unit is not always an error.|
|G09|READY|Metadata|i<br>Top priority: validate letters and sign convention for each MOVEMENT axis, arch, tooth, platform and<br>version. Direction labels for ClinCheck refer to the crown even in root basis; do not translate B<br>inclination to lingual root torque without validated semantics.|
|G10|READY|Yes*|Essential: distinguish explicit 0, blank, dash, excluded/absent tooth, and an unsupported movement<br>field. Introduce an observed/expected axis coverage mask;nonlisted axes cannot be assumed zero.|
|G11|READY|Metadata|i<br>Verified ClinCheck crown-center vs virtual-root-apex affects linear, not angular values. SureSmile<br>crown center vs cusp tip is also distinct. Require basis metadata and disallow cross-basis<br>arithmetic/comparisons.|
|G12|READY|Metadata|Verified SureSmile incremental/cumulative/total distinction. Total ClinCheck and last cumulative<br>SureSmile stage are not automatically equivalent without same start/end, coordinate frame and<br>content. No stage limits on a total-only paste.|
|G13|READY|Metadata|Verified Align final, Doctor final and Comparison/difference distinction; a difference row is never the<br>absolute programmed plan. Store plan ID and comparison operands; hold clinical rules if mode<br>unconfirmed.|
|G14|REVISE|Extra|i<br>The TMT alone cannot confirm that a tooth is absent, excluded, fixed or truly unmovable. A dash,<br>pontic or absent column is insufficient. Only check contradictions against independently supplied<br>verifiedpresence/exclusion metadata.|
|G15|READY|Extra|i<br>Sound only for actual stage datasets. Define indexed stages, stage zero, optional<br>accommodation/overcorrection/passive stages, skipped stages, arch alignment, and duplicate<br>handling;don't impose staged checks on total-onlydata.|
|G16|READY|System|Strong provenance gate, but raw value retention and rule-version checks are system-owned<br>metadata rather than TMT measurements. Block clinical comments for unverifiable findings; a<br>parse-error message should still be deliverable.|
|G17|READY|System|Correct fail-closed principle, yet use partial abstention: an unverified rotation must not suppress<br>independently verified extrusion for the same case. Implement field-scoped blocking and report<br>coverage.|
|G18|READY|Metadata|Appropriate: tooth-group logic requires verified adult/primary mapping. Distinguish permanent vs<br>primary, mixed dentition, supernumeraries and nonteeth; avoid treating unexpected IDs as normal<br>molars.|



Independent critical audit  •  13 Nov 2026  •  Draft for clinical reviewer 

### **D01–D16 | Descriptive observations** 

|**Rule**|**Decision**|**TMT only?**|**Independent assessment and required change**|
|---|---|---|---|
|D01|READY|Yes*|Accurate if strictly a report of programmed, not achieved, movements with original basis, scope,<br>plan mode and direction. Report omitted/missingdimensions separately.|
|D02|REVISE|Yes*|Rename to co-programmed movement axes, not concurrent movement. Total TMT does not show<br>temporal overlap;simultaneityis a staging question.<br>i|
|D03|READY|Yes*|Safe tooth-group description, subject to verified numbering and rotation sign mapping. No inference<br>that canine/premolar rotation will fail.|
|D04|READY|Yes*|Safe description of programmed extrusion; anterior/posterior grouping must rely on tooth map, and<br>no clinical interpretation should follow automatically.|
|D05|READY|Yes*|Safe description of programmed intrusion. Highlighting mandibular incisors is a navigation<br>preference,not evidence of danger.<br>i|
|D06|READY|Yes*|Keep source-specific terms inclination and angulation. ClinCheck angular values are not changed by<br>crown/root basis selection;neither alone specifies achieved root movement or torque control.|
|D07|READY|Yes*|Descriptive buccolingual displacement only. Neither skeletal/dental expansion nor bodily<br>translation can be established from one-axis crown movement.|
|D08|READY|Yes*|Descriptive mesiodistal displacement only. Do not infer space closure, anchorage loss, root<br>movement or treatment speed.<br>i|
|D09|READY|Yes*|Valid molar movement label if mesial/distal convention is confirmed for that arch. Not a proof of<br>sequential distalization or Class II correction.|
|D10|REVISE|Yes*|Same-tooth rotation and vertical movement can co-exist in a total plan, but cannot be called<br>temporallycombined without stage values. Pure fact only;arguablyredundant with D02.|
|D11|REVISE|Yes*|The same total-vs-staged problem. Avoid implying bodily motion, root control or force-system<br>interaction. Merge into ageneric co-programmingobservation.<br>i|
|D12|READY|Yes*|Count verified nonzero axes/tooth groups/arches with separate data-coverage denominators. Never<br>sum degrees with millimeters orpresent case difficultyfrom counts.|
|D13|READY|Yes*|Numerically compare paired anatomic teeth only within equivalent plan, basis and axis. Mirrored<br>left/right signs require explicit convention;difference does not imply pathologic asymmetry.|
|D14|READY|System|Useful data-availability report, but missing-context entries should be derived from requested<br>decisions,not ageneric exhaustive list on every paste.|
|D15|READY|Yes*|Use wording 'all supported, observed axes are zero'; missing/unsupported axes and absent teeth<br>prevent a categorical 'no movement' conclusion.|
|D16|REVISE|Extra|Two plans need same patient, tooth, starting geometry/reference, compatible coordinates, stage<br>and movement semantics. Equal basis alone does not make two rotations/paths subtractable;<br>compute scalar deltas onlywherejustified.|



### **R01–R16 | Clinical candidate rules** 

|**Rule**|**Decision**|**TMT only?**|**Independent assessment and required change**|
|---|---|---|---|
|R01|VALIDATE|Yes*|Review prompt is plausible because rotational predictability varies; cited studies do not establish<br>universal canine/premolar cutoffs. Needs tooth-, platform-, basis- and intent-specific trigger,<br>exception list and blinded case validation.|
|R02|VALIDATE|Yes*|Only acceptable as a clearly labeled clinician-selected movement-size category, never a validated<br>risk tier. Historical Invisalign categories are not contemporarycross-platform clinical thresholds.|
|R03|VALIDATE|Yes*|Potential movement review only. Anterior extrusion studies are heterogeneous; absence of<br>attachments/staging/occlusion means no specific auxiliaryrecommendation orprediction.|
|R04|VALIDATE|Yes*|i<br>Posterior extrusion review is a candidate; historic manufacturer colors are a poor universal basis.<br>Require device-specific rationale and limit language to 'reviewplanned extrusion'.|
|R05|VALIDATE|Yes*|Lower-incisor intrusion deserves focused review, but S11 includes only eight studies, seven with<br>serious bias, and measurement heterogeneity; do not derive a 1.5/2.0 mm default cutoff or a safety<br>flagfrom its summary.|
|R06|VALIDATE|Yes*|Other intrusion by group is a plausible policy only; root support, occlusal objectives, staging,<br>baseline bite and appliance details are absent. Nogeneralized success rating.|
|R07|VALIDATE|Partial|Risk of misinterpreting crown inclination as root torque or periodontal root risk. Without actual root-<br>position/geometry, allow only a conditional 'review inclination/root-control strategy' prompt<br>approved byan orthodontist.|
|R08|VALIDATE|Yes*|Angular movement is observable, but space closure and control of roots are unobserved. Require a<br>movement-specific criterion and do not infer need for mechanics.|
|R09|VALIDATE|Yes*|Posterior buccolingual displacement may invite review; TMT is insufficient to distinguish<br>tipping/bodily expansion, assess bone envelope or compute arch expansion. Avoid threshold<br>masqueradingasperiodontal safety.|
|R10|VALIDATE|Yes*|Upper molar distal movement can be identified. S12 finds very-low-certainty evidence and cannot<br>justify cross-system anchorage or overcorrection instructions; stage/anchorage adequacy requires<br>more data.|
|R11|VALIDATE|Yes*|Molar mesial movement can be identified, but extraction status, space closure, anchorage and root<br>trajectoryare absent. Do notprescribe control mechanics.|
|R12|VALIDATE|Partial|Proposed interaction matrix is unbuilt and unsupported by transferable clinical validation. Vendor<br>antagonistic/synergistic staging settings demonstrate configurability, not a scientifically validated<br>universal matrix.|



Independent critical audit  •  13 Nov 2026  •  Draft for clinical reviewer 

|**Rule**|**Decision**|**TMT only?**|**Independent assessment and required change**|
|---|---|---|---|
|R13|MORE DATA|No|Misclassified under TMT-only clinician rules: per-stage scrutiny requires stage-level input, a device-<br>specific profile and clinician approval. Merge with T01; never divide a total by stage count as a<br>substitute.<br>f|
|R14|READY|System|Sound abstention control, not a clinical numeric threshold. Move into global data-sufficiency/safety<br>policy;absentpatient context mustyield 'cannot assess',not normal/low risk.|
|R15|VALIDATE|Partial|Review question from movement alone is permissible only as open-ended, not as implied<br>attachment deficiency. To check whether a required attachment is absent, acquire an actual<br>attachmentplan as in A02.|
|R16|MORE DATA|No|Whole-case clinical complexity requires occlusion, malocclusion, skeletal/periodontal assessment<br>and treatment objectives. Keep disabled as case score; S15's CAT-CAT classification itself uses<br>models,radiographs and examinations.|



### **T01–T08 | Staging, geometry and IPR** 

|**Rule**|**Decision**|**TMT only?**|**Independent assessment and required change**|
|---|---|---|---|
|T01|MORE DATA|No|Valid technical comparison only with actual per-stage values, manufacturer/version profile and<br>clinician-approved limit. ClearCorrect 0.3 mm/3 deg is a setting, not a safety limit; source profile<br>must match.<br>i|
|T02|MORE DATA|No|Do not blindly sum angular increments or mixed-reference translations. Define coordinate frames<br>and valid source operations; compare only values whose composition semantics are demonstrated,<br>with ajustified numeric tolerance.|
|T03|MORE DATA|No|An observed threshold exceedance can be reported if actual stage values exist, but the claim that<br>'maximal stages override caused it' needs staging config/history or counterfactual evidence.<br>Rephrase as observed constraint exceedance.<br>i|
|T04|MORE DATA|No|Sequence comparison needs stage-by-stage positions plus a verified intended<br>distalization/anchorage protocol; total TMT has no order. No universal sequence shall be<br>hardcoded.<br>i|
|T05|MORE DATA|No|Requires staged overlap and an expert-approved, device-specific interaction policy. A clinician-<br>designed rule is notproven beneficial absent case evaluations.|
|T06|MORE DATA|No|TMT lacks shape/surface data. Require independently validated geometry/contact engine, accurate<br>alignment and numeric output;vendor colored UI cells alone are notportable collision evidence.|
|T07|MORE DATA|No|IPR sites and quantities require approved IPR/contact plan, crown/enamel considerations, stage<br>timingand clinician review. Never infer site or amount bysummingmesiodistal displacement.|
|T08|MORE DATA|No|Anchorage/root balancing requires staged force strategy and root/crown coordinates; virtual apex<br>movement is not aperiodontal exam. Policymismatch only,not automatic biomechanical diagnosis.|



### **A01–A06 | Attachments** 

|**Rule**|**Decision**|**TMT only?**|**Independent assessment and required change**|
|---|---|---|---|
|A01|MORE DATA|No|Attachment presence cannot be audited from ordinary total TMT. Need independently imported<br>attachment-tooth-and-stage map and handle intentional removal, lingual surfaces and multiple<br>attachments.|
|A02|MORE DATA|No|Clinician-approved indications plus actual attachment presence and stage are required to assert<br>omission. Literature on attachment performance is heterogeneous; do not promote a movement<br>amount into a mandatoryattachment rule.<br>l|
|A03|MORE DATA|No|Conflict-resolution is an engine policy and only meaningful when two approved attachment<br>proposals exist. Do not select an attachment automaticallybased on arbitrary priority.|
|A04|MORE DATA|No|Attachment timing demands start/end stage data, plan mode and stage conventions. Not part of a<br>total TMT.|
|A05|MORE DATA|No|Correct prohibition on numerical geometry placement from a TMT. Even with meshes,<br>clinical/geometry validation is necessary; make the withholding guard globally active rather than<br>waitingforgeometryinput.|
|A06|READY|System|A universal-superiority claim should be blocked immediately as an output safeguard, not treated as<br>an automatic attachment selection candidate. S14 finds no significant overall superiority; note<br>subgroupuncertainty.|



### **H01–H12 | Safety and scope** 

|**Rule**|**Decision**|**TMT only?**|**Independent assessment and required change**|
|---|---|---|---|
|H01|READY|Request|Clinically appropriate scope guard. No plan suitability, diagnosis or guarantee from a movement<br>table;visible on exported reports and API responses.|
|H02|READY|Request|Sound withholding guard for periodontal claims; periodontium cannot be assessed from TMT or|
||||virtual root coordinates. Do not interpret missingdata as healthy periodontium.|
|H03|READY|Request|Sound withholding guard for root resorption,rootproximityand bone housing. A virtual root apex|



Independent critical audit  •  13 Nov 2026  •  Draft for clinical reviewer 

|**Rule**|**Decision**|**TMT only?**|**Independent assessment and required change**|
|---|---|---|---|
||||position is not a radiographic/biological risk assessment.<br>i|
|H04|READY|Request|Sound; total movement does not show occlusal contact distribution or final bite. Neither transverse<br>nor vertical TMT arithmetic is an occlusion simulator.|
|H05|READY|Request|Sound; even when movement suggests crowding or space creation, no IPR amount/site may be<br>derived from total TMT alone.|
|H06|READY|Request|Sound; do not recommend extractions, surgery, adjunctive device substitution or contraindications<br>from TMT without full assessment.|
|H07|READY|Request|Sound. No patient-level success rate, treatment duration or risk percentage from clinical population<br>averages or rules;anyfuturepredictor needs separate validated data and evaluation.|
|H08|READY|Request|Sound; no mandatory size, orientation or tooth-surface location from movement table. Avoid<br>'missingattachment' claims when attachmentplan unobserved.|
|H09|READY|Request|Sound; cannot promise collision-free motion or safe stage transitions without 3D models and path<br>validation.|
|H10|READY|System|Required draft/review label and sign-off workflow. Human-review flag alone is insufficient if<br>clinicians cannot inspect the numeric evidence and rationale.|
|H11|READY|Request|Appropriate abstention but overlaps H01-H03/H06; consolidate implementation as a context-<br>requirement matrix whilepreservingdistinct audit codes.|
|H12|READY|System|Privacy guard essential but source S18 is not a jurisdiction-specific data-protection law. Require<br>explicit PHI policy, redaction, retention, encryption, access control and no unsanctioned LLM<br>transmission.|



### **L01–L06 | Wording and sign-off** 

|**Rule**|**Decision**|**TMT only?**|**Independent assessment and required change**|
|---|---|---|---|
|L01|READY|System|Important invariant. Prefer templates backed by typed structured findings; unconstrained LLM prose<br>cannot be guaranteed clinically correct by prompt instructions alone. Validate/reject generated<br>claims if anyLLM is used.|
|L02|READY|System|Essential deterministic token/measurement preservation: compare normalized tooth, numeric<br>value, sign/direction, scope and basis, not approximate prose similarity. Never silently alter<br>precision.|
|L03|READY|System|Require finding-to-source map for each clinical sentence; labels from literature are provenance, not<br>evidence of apatient-specific conclusion. Keepraw displaylinks.|
|L04|READY|System|Deduplicate only identical clinical propositions; retain all triggering rule IDs and source fields.<br>Report real contradictions instead of droppinglower-priorityfindings silently.|
|L05|READY|System|Make unsupported/missing-context states explicit and localized to each finding; distinguish 'not<br>evaluated' from 'evaluated and no concern flagged'.|
|L06|READY|System|l<br>Maintain Draft -> Reviewed -> Approved or Rejected with authorized reviewer identity, timestamps,<br>immutable version and reapproval on content changes. Approval is not delegated to the LLM.|



## **6 | Missing essential safeguards / rules** 

**N01 — Table completeness / expected coverage:** Verify required header set, tooth columns, arch coverage and number of axes; mark partial input explicitly. 

**N02 — Unknown format and layout drift:** Detect future revisions and transposed table variants; do not silently select best-effort adapter based on similarity. 

**N03 — Patient/case/plan identity isolation:** Require safe pseudonymous case identity for multi-plan comparison and prevent cross-patient merges. 

**N04 — Raw byte + Unicode normalization:** Preserve byte-original and parse unicode minus, nonbreaking spaces, typographic symbols, decimals and clipboard artifacts deterministically. 

**N05 — Mirrored side sign conventions:** Normalize left/right tooth-specific rotation, angulation, mesial/distal labels without assuming opposite raw signs represent unequal movement. 

**N06 — Tooth status from independent input:** Represent pontic, extracted, unerupted, impacted, excluded, fixed and mixed dentition as distinct externally verified states. 

**N07 — Stage and overcorrection semantics:** Define baseline/0, active, accommodation, correction, overcorrection and passive aligner identifiers before any staged rule. 

**N08 — Coordinate frame and movement composition:** Track coordinate systems, initialization and angular composition methods; prohibit unsupported subtraction/summation. 

Independent critical audit  •  13 Nov 2026  •  Draft for clinical reviewer 

**N09 — Finding coverage and partial abstention:** A failed field should withhold only dependent findings while preserving verified unrelated observations. 

**N10 — Safety prompt/claim filter:** Reject attempt to elicit unsupported patient-specific advice regardless of whether request is direct, LLM-generated or embedded in copied table. 

**N11 — Repeated reports and amendment history:** Make input, policy and signed outputs immutable; any material change invalidates prior sign-off. 

**N12 — Clinical intended purpose and endpoints:** Record why a movement was programmed and which patient goal it serves before labeling plan relevance; a movement magnitude is not a diagnosis. 

**N13 — Source-dependent parameter availability:** Every rule must declare required data, exact semantics, valid sources/versions, scope, allowed bases and fallback status. 

**N14 — Adverse-event/incident reporting workflow:** For future real clinical use, define escalation of material software errors, incident log, remediation and field rollback. 

## **7 | Recommended processing architecture** 

**1. Ingest** Size-limit and isolate raw clipboard text. Redact/omit identifiers. Keep immutable hash and source capture metadata. 

**2. Detect & ask** Deterministic adapter candidate detection. Require source, mode, arch, tooth numbering, crown/root/cusp basis, total/stage; operator confirms when not encoded. 

**3. Parse** Parse each cell into raw token, Decimal magnitude, source code, canonical axis/direction, units, field status, adapter mapping and provenance. 

**4. Semantic checks** Run all applicable G rules with field-level status. Do not turn missing data into 0. Build completeness/coverage matrix. 

**5. Descriptive facts** Execute D movement observations on verified fields. Distinguish planned movement from actual achieved movement and total co-programming from stage simultaneity. 

**6. Sufficiency gate** Evaluate required-field predicates for candidate clinical rules; return 

CONTEXT_REQUIRED/NOT_APPLICABLE before any configured threshold. 

**7. Approved clinical checks** Only allow clinically signed device/patient/intent-specific policies, fixed comparator semantics and documented exceptions; no implicit defaults. 

**8. Resolve/word** Combine duplicates with all underlying IDs; keep conflicts. Produce typed finding objects and vetted templates. Optional LLM must not add clinical claims. 

**9. Sign and monitor** DRAFT only until authorized sign-off. Audit versions, review disagreements, logging, monitoring, error reports and rollback. 

## **8 | Rule policy and typed output contract** 

Every executable rule requires: id; semver; description; purpose; intended user; allowed source + version; supported dentition/tooth groups; required input fields; valid basis/mode/scope; direction semantics; predicate; comparison precision/tolerance; exclusion/override conditions; policy status; clinical approver ID/date; evidence reference(s) with evidence level; output template; severity label (if validated); dependencies; test-fixture IDs; and change-control approval. 

Suggested evaluation result: {rule_id, rule_version, case_id, tooth_id, input_refs[], observed_values[], source_metadata, status, predicate_result, policy_id, evidence_ids[], provenance[], missing_required_fields[], abstain_reason, finding_type, template_id, reviewer_status, timestamps}. Store evaluated=false explicitly for unsupported fields. 

Predicate priority: (1) structural validation -> (2) source identity/semantics -> (3) per-field eligibility -> (4) non-prescriptive observations -> (5) missing-context guard -> (6) orthodontist-approved review predicates -> (7) output suppression/conflict resolution -> (8) manual sign-off. Safety controls outrank every clinical review rule. Deny by default if policy version/approval missing. Only order-independent, reproducible finding results may be exported. 

Example safe comment: “Tooth 13: programmed rotation 18° in the clinician-confirmed ClinCheck Doctor-final total TMT (crown basis). Direction as reported by source: M. This is a description of programmed movement; it does not estimate achieved 

Independent critical audit  •  13 Nov 2026  •  Draft for clinical reviewer 

movement or indicate an attachment requirement.” Publish such a sentence only if the real source mapping confirms tooth notation and M rotation semantics. Example unsafe comment: “18° canine rotation is high risk and requires a vertical optimized attachment.” 

## **9 | Minimum evaluation strategy and release criteria** 

**Parser fidelity** Actual pastes from both source products; all tooth axes; both arches and source modes; numbering systems; roots/crowns; delimiter, missing, unicode, locale, duplicate, transposed and unknown revisions; double-read gold records. Require zero silent reinterpretations. 

**Math & semantics** Exact boundary, negative and direction codes, mirror teeth, missing vs zero, basis changes, mode deltas, staged vs total, valid/invalid composition, noncommuting transforms and within-source stage tolerances. 

**Metamorphic** Reordering columns/rows must not change findings; known representations of same clinical meaning must normalize identically; changes in missing fields must not masquerade as zero; changing plan scope must change eligibility. 

**Engine & conflicts** All enabled/disabled branches, missing required fields, expert-policy version, overlapping duplicates, simultaneous triggers, warnings against override, reviewer changes, replay reproducibility. 

**Clinical shadow study** De-identified representative cases across appliance types, movement groups, dentitions and anomalous contexts. At least two independent reviewers, dispute adjudication, critical miss severity and subgroup reporting; no automated good score from TMT alone. 

**Text and privacy** Sentence-to-finding entailment checks, numeric exactness, output length, prompt injection, HTML/CSV formula payload, PII leakage, vendor API telemetry, protected report approval, invalid sign-off on revisions. 

Technical gate: 100% match against independently verified parser oracle fixtures for supported source formats and 100% passing deterministic rule logic tests, including expected rejection of unsupported samples. Clinical gate: orthodontist-approved policies and a preregistered clinical shadow-evaluation plan, no unresolved high-severity output errors, independent adjudication and documented residual risk. Neither a universal 95% accuracy requirement nor zero errors on a small nonrepresentative sample is sufficient. 

## **10 | Final implementation-readiness verdict** 

**GO now** React/TypeScript + FastAPI/Pydantic, deterministic source adapters, raw provenance, machine-checkable schema, QA gates, narrow D descriptions, H/L guards, clinician review UI, rigorous test harness. No patient-facing diagnosis or treatment directive. 

**GO after evidence and approval** Small number of tooth-group review flags with fully specified criteria, device scope, clinical rationale, exceptions, shadow study, clinician sign-off and policy governance. 

**NO-GO with total TMT alone** Per-stage biomechanics, attachment omission/prescription/geometry, IPR calculations, collision/occlusion judgments, root and periodontal safety, full case complexity, prognosis, successful-treatment likelihood or time estimates. 

A defensible MVP is a “Verified TMT Interpretation and Clinician Review Memo,” not an autonomous orthodontic planning engine. Adding more rules cannot substitute for missing physical and clinical evidence. 

## **11 | Evidence register and links** 

**[S01] Align Technology, ClinCheck Pro 6 manual, 2020.** https://storagy-advent-core-ppr.s3.amazonaws.com/storage/7eb29931-ffda-4e28-a15fcb100d8db964.pdf 

#### **[S02] Invisalign Quick Start: Tooth Movement Assessment, older undated guide.** 

https://s3.amazonaws.com/storagy-gati-production-us/docs/10%20Key%20Points%20for%20Effective%20ClinCheck%20Software%20Communication_emea-enen.pdf 

**[S03] SureSmile DIY Step 4 staging constraints.** https://docs.suresmile.com/suresmile_webhelp/DIY_Aligners/DIY_Step_4.htm 

**[S04] SureSmile Aligner Step 4 stages.** https://docs.suresmile.com/suresmile_webhelp/Aligners/Aligner_Step_4.htm 

**[S05] SureSmile Using Attachments.** https://docs.suresmile.com/suresmile_webhelp/treatment_planning/Using_Attachments.htm 

#### **[S06] ClearCorrect Clinical Preferences (provided link inaccessible to crawler).** 

https://www.straumann.com/content/dam/sites/clearcorrect/xy/resources/education/ClearCorrect%20Onboarding%20Guide%20480.274_en_02.pdf 

Independent critical audit  •  13 Nov 2026  •  Draft for clinical reviewer 

**[S07] ClearCorrect Engagers article (direct link not fully verified).** https://support.clearcorrect.com/s/article/engagers-also-known-asattachments?language=en_US 

**[S08] Borzabadi-Farahani, scoping review, Front Dent Med, July 2026.** https://pubmed.ncbi.nlm.nih.gov/42516363/ 

**[S09] Naoum & Lee, Semin Orthod, 2026.** https://doi.org/10.1053/j.sodo.2025.06.003 

**[S10] Benedetti et al., Dentistry, 2025 rotation systematic review.** https://pmc.ncbi.nlm.nih.gov/articles/PMC12564582/ 

**[S11] Fracchia et al., J Clin Med, 2025 lower-incisor intrusion review.** https://pubmed.ncbi.nlm.nih.gov/40944102/ 

**[S12] Garcia-Marin et al., Angle Orthod, 2025 molar MD review.** https://pubmed.ncbi.nlm.nih.gov/40936630/ 

**[S13] Yangin et al., Turkish J Orthod, 2025 attachment review.** https://pmc.ncbi.nlm.nih.gov/articles/PMC12485647/ 

**[S14] Pandian et al., J Oral Biol Craniofac Res, 2025 systematic review.** https://pubmed.ncbi.nlm.nih.gov/40778386/ 

**[S15] Wang et al., Int J Oral Sci, 2025 expert consensus.** https://doi.org/10.1038/s41368-025-00350-2 

**[S16] Modified Delphi international expert study, Prog Orthod, 2025.** https://pmc.ncbi.nlm.nih.gov/articles/PMC12321729/ 

**[S17] Periodontal orthodontic expert consensus, Int J Oral Sci, 2025.** https://pmc.ncbi.nlm.nih.gov/articles/PMC11965299/ 

**[S18] FDA Clear Dental Aligners, regulator.** https://www.fda.gov/medical-devices/dental-devices/clear-dental-aligners 

**[S19] FDA Clinical Decision Support Software final guidance, Jan 2026.** https://www.fda.gov/regulatory-information/search-fda-guidancedocuments/clinical-decision-support-software 

**[S20] WHO AI/health large multimodal models guidance, original 2024.** https://www.who.int/publications/b/70584 

**[S21] Alsulaiman, Saudi Dental Journal, 7 Oct 2026 narrative review.** https://pubmed.ncbi.nlm.nih.gov/42842148/ 

Supplemental independent crosschecks: Align 2015 ClinCheck fact sheet (clipboard copy): https://s3.amazonaws.com/storagygati-production-us/documents/2015/12/04/B10163%E2%80%9342_Rev_A.pdf ; Align 2016 Pro 5 quick reference (direction referenced to crown): https://s3.amazonaws.com/storagy-gati-production-us/documents/2016/10/15/ 

M20482_Rev_A__ClinCheck_Pro_5.0_Quick_Reference_Guide.pdf ; Haouili et al. 2020 prospective study: 

https://pubmed.ncbi.nlm.nih.gov/32620479/ ; FDA non-device CDS criteria: https://www.fda.gov/medical-devices/digital-healthcenter-excellence/step-6-software-function-intended-provide-clinical-decision-support 

Independent critical audit  •  13 Nov 2026  •  Draft for clinical reviewer 

