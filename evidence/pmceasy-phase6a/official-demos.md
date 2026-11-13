# Official public documentation and demo-link investigation

Observed on 14 November 2026 (Asia/Karachi). Research notes only. No authentication, subscription purchase, form submission, extension installation, private-resource download, source-code copying or application modification was performed.

## Evidence method and boundary

Public pages were read through the web tool. Three public PMCEASY HTML responses were inspected in memory only to discover official video links; HTML, scripts, response headers, cookies and storage were not retained. The channel linked by those responses was inspected for public title metadata. Selected public watch-page metadata was read; no video was downloaded or watched in this subtask. No video frame or spoken demonstration is claimed below. Ephemeral caption URLs were neither printed nor retained. Public caption requests failed and were not circumvented.

The parent investigation owns original screenshot inspection and isolated browser observations. Its stronger visual evidence should be combined with these notes, not replaced by the page descriptions.

## Public source register

| ID | Public URL | Evidence actually acquired | Limits |
| --- | --- | --- | --- |
| DOC-HOME | https://www.pmceasy.com/ | Public module descriptions, step captions and linked image identities; scoped video-link discovery | Marketing text and static screenshots are not proof of clinical validity or algorithms |
| DOC-HOW | https://www.pmceasy.com/how-to | Public process explanation and numbered workflow | Does not demonstrate the actual paid selection controls or all their options |
| DOC-MORE | https://www.pmceasy.com/read-more | Public description of resources and membership | No private resource library was accessed |
| DOC-TERMS | https://www.pmceasy.com/terms-conditions | Public product/access/feature statements | Descriptive evidence, not legal advice, independent verification or permission to copy protected assets into a product |
| DOC-PRICE | https://www.pmceasy.com/pricing-plans/pricing | Public annual all-access offer and feature list | No purchase, entitlement or working account observed; price can change |
| DOC-ABOUT | https://www.pmceasy.com/about | Public company/product-history claims | Self-reported scale/history, not algorithm or clinical-validation evidence |
| DOC-PRIVACY | https://www.pmceasy.com/privacy-policy | Public policy, last-updated label May 5, 2024 | Policy promises are not implementation/security audit evidence; no inference of clinical-data processing approval |
| ACCESS-START | https://www.pmceasy.com/start-planning | Web fetch returned HTTP 403 Forbidden | Cause not established by this fetch; no access-control bypass attempted |
| VIDEO-CHANNEL | https://www.youtube.com/channel/UCibaxZc4yIFkitH9zHmy3eg/videos | Public channel title and video listing metadata; linked from PMCEASY page HTML | A bounded listing, not a full historic archive or proof of every available demonstration |

## Corroborated public workflow and feature statements

### Product form and access

The terms describe the product as a subscription website intended for dental professionals. They advertise a guided planning process, technician-comment library, attachment selection and sequencing comments. Users are assigned responsibility for comments supplied to technicians. The terms characterize the information as informational rather than professional advice. This establishes the operator's stated positioning, not safe clinical performance. [DOC-TERMS](https://www.pmceasy.com/terms-conditions)

The pricing page advertises annual access to the companion and tools, account favourites and online availability across devices. It supports a browser-delivered subscription interpretation. It does not establish the existence or absence of a browser extension, a CAD plug-in, a desktop client or automatic application integration. No entitlement was acquired or exercised. [DOC-PRICE](https://www.pmceasy.com/pricing-plans/pricing)

Public about-page descriptions frame PMCEASY as a planning companion and describe a 2024 launch. Those are operator claims; company experience, case counts and marketing history are not evidence for its rules, thresholds, dataset or effectiveness. [DOC-ABOUT](https://www.pmceasy.com/about)

### Broader user journey

The how-to page introduces a modification-stage workflow before table intake. Its four numbered steps are stage selection, AI-tool selection, pasting the movement table, then running and observing suggestions. It describes three review passes: larger sagittal/transverse/vertical modifications; individual-tooth strategies with attachment orientation and anchorage; then sequencing and a final checklist. The number of passes may vary. This is documentation of the intended process, not an observed execution or a fixed requirement that every case has three modifications. Actual selectors, allowed transitions, their effect on output and state persistence remain unobserved in this subtask. [DOC-HOW](https://www.pmceasy.com/how-to)

### The three modules

Homepage step illustrations describe the Planning Assistant as copy table → paste/run → send comments to a CAD designer. Attachment Interface describes the same intake followed by visually presented suggestions/alternatives and placement in the external plan. Sequencer describes intake followed by reviewing/modifying a plan and noting anchorage suggestions. The common intake does not prove that these modules use the same hidden input schema or algorithm. Advertised collision and treatment-time benefits are claims, not demonstrated performance. The static site alone does not establish automatic copy, send, CAD modification, attachment placement or sequencing-file generation. [DOC-HOME](https://www.pmceasy.com/)

### Resources, favourites and language

The read-more page advertises resources concerning complex cases, monitoring and troubleshooting. No paid resource entries or usable resource controls were inspected. [DOC-MORE](https://www.pmceasy.com/read-more)

Account favourites are a pricing-page claim, not a tested save/retrieve capability. Turkish public marketing pages also exist; this does not establish multilingual generated output, supported table locales or localization of paid modules. [DOC-PRICE](https://www.pmceasy.com/pricing-plans/pricing), [Turkish public homepage](https://www.pmceasy.com/tr)

## Official-linked public videos

The public PMCEASY homepage, how-to and read-more HTML each linked the same YouTube channel. Its public title was **Plan My Case**. Current listing markup used `lockupViewModel`; looking only for legacy `videoRenderer` structures would incorrectly suggest no videos. No content or source script was copied into Finova.

| Video | Public URL | Retrieved public metadata | Evidence classification |
| --- | --- | --- | --- |
| PMCEASY - How does it work? | https://www.youtube.com/watch?v=iEMJeuOXkq4 | Author Plan My Case; duration 400 seconds (6:40); watch metadata reported playability OK; English automatic-caption track advertised | Metadata only; frames and narration UNOBSERVED here |
| PLANNING WITH PMCEASY AI | https://www.youtube.com/watch?v=1GHKNwNkL6Q | Author Plan My Case; duration 372 seconds (6:12); playability OK; English automatic-caption track advertised | Metadata only; frames and narration UNOBSERVED here |
| How to Place Attachments | https://www.youtube.com/watch?v=BOk-Otzgj2M | Author Plan My Case; duration 132 seconds (2:12); playability OK; no caption track listed | Description is about physical attachment placement; no basis to classify it as the AI interface demonstration |
| Q&A with Arda Dingiloğlu on the PMCEASY journey | https://www.youtube.com/watch?v=Jc9CJPt3Veo | Author Plan My Case; duration 984 seconds (16:24); playability OK; English automatic-caption track advertised | Founder/product-background metadata; no software behavior observed |

The channel also lists a Turkish counterpart, https://www.youtube.com/watch?v=xe-WieKNu5A. It was not watched or independently translated here.

The web tool could not fetch the four watch URLs. Direct public watch HTML yielded the above metadata without sign-in. For the two English demonstrations, direct public automatic-caption requests failed with HTTPError. Neither captions nor timestamps of actions were acquired. Playability metadata is not proof that playback succeeded in a browser. No spoken claims, technician comments, attachment geometry or sequencing rules can be attributed to these videos from this subtask.

## Consequences for the functional comparison

1. A modification-stage/tool choice is a documented interaction class worth investigating separately from the simple paste/run flow. It does not authorize a three-stage clinical policy in Finova.
2. Technician-comment library, account favourites and resource/checklist features are publicly advertised product-surface categories. Mark behaviour not independently exercised as advertised/unobserved; do not conflate them with dynamic TMT analysis.
3. Visual attachment alternatives and sequencing/anchorage advice are advertised, but precise output contracts must come from legible screenshots or an authorized live session, not names alone.
4. Copying/applying output to another planning application is described as a user activity. Automatic synchronization or browser-extension injection has not been established.
5. The public website and subscription positioning are supported by primary sources. A categorical “extension” claim is unsupported; the absence of an extension is also not proven by these bounded observations.
6. No verified input-format matrix, authentic clipboard fixtures, source-version mappings, explicit threshold policy, accuracy study, collision model or clinical approval was established by these sources. Screenshot example values are not authentic clipboard exports.

## Useful next authorized observation

If the parent can play the two official demonstrations in its dedicated profile, capture only relevant module frames and action timestamps; keep player/network tokens out of evidence. Otherwise mark their behavioral contents unobserved and retain these links for a later authorized observation. No paid access is implied, requested, obtained or bypassed by this note.

## Follow-up: bounded founder-post / indexed-transcript research

Additional investigation was requested after the parent reported image-CDN connection resets and broken homepage image placeholders. The parent independently attempted bounded frames from the official videos. This section adds public primary-post evidence; it does not claim those frames were watched in this subtask.

### Evidence added

| ID | Public source | Acquisition | Supported conclusion | Boundary |
| --- | --- | --- | --- | --- |
| POST-ATTACH | https://www.linkedin.com/posts/arda-dingiloglu-21880b67_aligners-orthodontics-artificialintelligence-activity-7206744629927415808-Ar98 | Public search index exposed a founder-post transcript excerpt; direct page fetch denied by robots.txt | The narrated attachment workflow includes a table-display action followed by an attachment action, with placement/modification/removal and optimized/conventional alternatives described | Search-extracted transcript only; no clip watched, source UI controls exercised or exact geometry established; transcript may contain automatic naming errors |
| POST-LAUNCH | https://tr.linkedin.com/posts/arda-dingiloglu-21880b67_inplasticwetrust-pmceasy-aligners-activity-7194389057609576449-iKSA | Public indexed page opened successfully; text and transcript section extracted | Launch announcement promotes technician-comment and attachment libraries, anchorage solutions and sequencing scenarios; transcript also promotes malocclusion-specific content | Public promotional text, not a live case output, complete library inventory or clinical validation |
| POST-FEEDBACK | https://www.linkedin.com/posts/arda-dingiloglu-21880b67_pmceasyai-inplasticwetrust-activity-7300794706144215041-k0lR | Public indexed page opened successfully | Operator claims AI-feature adoption and positive user feedback | Does not demonstrate any algorithm, actual UI output, measured accuracy or clinical outcome; not used as performance evidence |

### Attachment transcript, paraphrased

The publicly indexed founder-post narration says to copy the TMT, paste it into the attachment module, show its table using **Display table**, then invoke **AI Attachments**. It describes a resulting list of changes: attachments to add/place, modify or remove, with optimized or conventional alternatives and positional presentation. Its speed and predictability claims were not measured. The post supports a **two-action intake/analysis pattern** and an **action-oriented suggestion list** at the level of narrated workflow. It does not establish which source platform/version the table uses, field semantics, geometry, exact labels in a current paid build, clinically justified attachment indications or whether suggestions automatically modify CAD. [POST-ATTACH](https://www.linkedin.com/posts/arda-dingiloglu-21880b67_aligners-orthodontics-artificialintelligence-activity-7206744629927415808-Ar98)

To evaluate an attachment change rather than merely suggest a new item, Finova would need an independently verified existing attachment plan as well as approved indications and an intended surface/stage/geometry contract. These are reconstruction requirements, not facts inferred about PMCEASY's hidden input or computation.

### Planning Assistant / Sequencer evidence limit

The launch transcript corroborates broad product categories—technician communication, tooth-movement attachment selection and sequencing/scenario information—but supplies **no legible patient/case-specific Planning Assistant comment**, no tooth-numbered clinical directive, no numerical trigger, no stage schedule, no anchorage-decision logic and no source-format contract. Its generic promotional assertions do not demonstrate table-conditioned analysis. [POST-LAUNCH](https://tr.linkedin.com/posts/arda-dingiloglu-21880b67_inplasticwetrust-pmceasy-aligners-activity-7194389057609576449-iKSA)

No analogous detailed Planning Assistant or Sequencer transcript was established by this bounded follow-up. The 12 targeted searches combined the founder's public post path with PMCEASY, planning, sequencing, comments, TMT, planning-assistant or sequencer terms, plus broader quoted product/module/transcript queries. Returned unrelated jobs/profiles and third-party commentary were excluded, and their personal details were not retained. This negative result is limited to these accessible/indexed searches on this date; it does not establish that no such demonstration exists.

### Reconstruction implications, not target-algorithm claims

- Keep table display separate from attachment-generation actions in the **observed/narrated target workflow**; Finova already has separate parse/review/report actions but does not have attachment generation.
- Add/modify/remove are useful future output-contract categories, conditional on a verified current attachment map; TMT totals alone cannot justify them.
- Library browsing, malocclusion/scenario content and automated TMT comments must remain separate capability rows in the gap matrix. The same promotional paragraph does not prove a common engine.
- Planning Assistant clinical comment classes beyond the published broad categories remain UNKNOWN until a legible screenshot, watched public demo or authorized target session establishes them. Map hypothetical Finova R/T/A categories as candidate requirements rather than asserting PMCEASY emits each one.
