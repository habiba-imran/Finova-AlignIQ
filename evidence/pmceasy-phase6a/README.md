# Phase 6A evidence index

Observation date: **14 November 2026, Asia/Karachi**. Public functional research only. This folder is not a vendor-fixture corpus, a clinical-policy register or a copy of proprietary application code.

## Evidence classes

- **PUBLIC PAGE:** operator advertising/documentation, not independent performance validation.
- **PUBLIC DEMO FRAME:** a decoded frame of an operator-published recording. It demonstrates a recorded UI/output, not our execution of the paid product or knowledge of its algorithm.
- **INDEXED TRANSCRIPT:** text exposed by a public search result; weaker than watched narration or a decoded frame.
- **LOCAL SOURCE/PROBE:** owning Finova source or newly executed synthetic library behavior; not evidence about PMCEASY.
- **INFERENCE:** an explicitly qualified interpretation.
- **UNOBSERVED:** inaccessible, illegible, outside the sampled intervals or not independently exercised.

## Inventory

| Item | Contents / limits |
| --- | --- |
| `public-capture-manifest.json` | Eight public screenshot source URLs, unsuccessful retrieval diagnostics and three isolated-browser page captures. |
| `pages/P01-home.png`, `.json` | Public homepage rendering and sanitized headings/control/image/script-URL inventory. **Images did not load**; blue boxes are placeholders, not module screenshots. |
| `pages/P02-how-to.png`, `.json` | Public process documentation and structure. |
| `pages/P03-start-planning.png`, `.json` | Start Planning navigation redirected to `/paywall`; rendered capture was blank under the scoped request policy. It does not prove a specific login/purchase UI. |
| `videos/observation-manifest.json` | Verified decoded frame times for the first batch of privacy-cropped samples from the two official-linked videos. |
| `videos/observation-manifest-followup.json` | Additional bounded samples of intake/Planning Assistant/module intervals. Failed decoding is recorded without attributing a stale frame to the requested time. |
| `videos/observation-manifest-intake.json` | Final intake/preview/run observations with expected video-duration checks. Unrelated/mismatched media was excluded without retaining a frame. |
| `screenshot-observation-register.json` | Per-image public URL, module/step, visible content, inference/unknowns and privacy review for all retained frames and inaccessible homepage originals. |
| `videos/*-cropped.png` | Native browser captures excluding the browser URL/profile/account header and bottom strip. They retain relevant public demonstration UI; manual privacy/content review is recorded in the research report. |
| `official-demos.md` | Public pages, channel/video metadata, bounded searches and indexed-transcript limitations. This subtask did not watch video; the parent’s decoded-frame evidence is separate. |
| `rea-readiness.md`, `.json` | Bounded local readiness inspection and official supported setup prerequisites; no REA Evidence IDs or successful connection claimed. |
| `finova-audit.md` | Current owning-source inspection, file/line locators and historical-report reconciliation. |
| `finova-document-source-inventory.json` | Full document-read inventory, hashes and implementation-source identities. |
| `finova-local-probes.json` | Fresh synthetic in-process parser/review/report/model probes; zero provider calls. Not HTTP/browser/full-suite results. |
| `capture-public.mjs`, `observe-official-videos.mjs` | Research-only capture recipes using the existing Playwright installation. Not app implementation, REA output or an installation/configuration change. |

The official channel was discovered through links in PMCEASY’s public pages: [Plan My Case](https://www.youtube.com/channel/UCibaxZc4yIFkitH9zHmy3eg/videos). Videos: [How does it work?](https://www.youtube.com/watch?v=iEMJeuOXkq4), [Planning with PMCEASY AI](https://www.youtube.com/watch?v=1GHKNwNkL6Q).

## Privacy, access and capture boundary

Fresh owned temporary Chromium profiles were used; existing user profiles were never attached. Only PMCEASY and required public asset origins were permitted for site captures. The separate video context permitted only the two selected YouTube pages and required player/media origins. Other requests were blocked, which can affect rendering. Browser/profile cleanup runs on completion. No login, purchase, form submission, CAD access, patient upload or access-control bypass occurred.

No HAR, cookies, storage, tokens, request/response payloads, signed video/caption URLs or application JavaScript source were exported. The page inventories record public script **URLs only**, with queries removed. This is sufficient to identify the public Wix shell; it is not a server/application architecture reconstruction.

Initial naive seeks left stale video frames. Those preliminary uncropped PNGs were removed after checking resolved paths within this evidence folder. Retained samples require `requestVideoFrameCallback` media-time confirmation, not just `currentTime`. Crops exclude URL/account identifiers; selected images were manually reviewed. Public dental illustrations and tooth tokens remain demonstration content, never genuine clipboard exports, reviewed vendor semantics or verified recommendations.

The screenshot CDN reset connections across direct HTTP, browser and web-reader attempts. The eight original assets were **not retrieved**. No fabricated replacement, enhancement, OCR reconstruction or altered target image was created. The original-source manifest and failed status remain available for follow-up. Video crops are clearly labeled alternative public evidence, not the homepage’s original screenshot files.

No private/paid PMCEASY working session was exercised. No network observation of clinical analysis or server-side algorithm was performed. No local `.env.local` or other credentials were inspected.
