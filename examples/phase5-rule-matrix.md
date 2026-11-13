| Rule v2.0.0 | Audited purpose | Disposition | Execution | Implementation kind |
| --- | --- | --- | --- | --- |
| A01 | Attachment presence audit | MORE DATA | DISABLED | REQUIRED_DATA_GUARD |
| A02 | Attachment-to-movement review | MORE DATA | DISABLED | REQUIRED_DATA_GUARD |
| A03 | Conflicting attachment preferences | MORE DATA | DISABLED | REQUIRED_DATA_GUARD |
| A04 | Attachment stage scheduling | MORE DATA | DISABLED | REQUIRED_DATA_GUARD |
| A05 | Attachment geometry placement guard | MORE DATA | ACTIVE | OUTPUT_GUARD |
| A06 | Conventional vs optimized comparison | READY | ACTIVE | OUTPUT_GUARD |
| D01 | Movement inventory per tooth | READY | ACTIVE | EXECUTABLE |
| D02 | Multiple concurrent movement types | REVISE | ACTIVE | EXECUTABLE |
| D03 | Rotation by tooth group | READY | ACTIVE | REQUIRED_DATA_GUARD |
| D04 | Extrusion by tooth group | READY | ACTIVE | REQUIRED_DATA_GUARD |
| D05 | Intrusion by tooth group | READY | ACTIVE | REQUIRED_DATA_GUARD |
| D06 | Crown inclination/angulation inventory | READY | ACTIVE | EXECUTABLE |
| D07 | Buccolingual translation inventory | READY | ACTIVE | EXECUTABLE |
| D08 | Mesiodistal translation inventory | READY | ACTIVE | EXECUTABLE |
| D09 | Molar distalization or mesialization indicator | READY | ACTIVE | REQUIRED_DATA_GUARD |
| D10 | Combined rotation and vertical movement | REVISE | ACTIVE | EXECUTABLE |
| D11 | Combined angular and translational movement | REVISE | ACTIVE | EXECUTABLE |
| D12 | Movement distribution summary | READY | ACTIVE | EXECUTABLE |
| D13 | Opposite-side comparison (descriptive only) | READY | ACTIVE | REQUIRED_DATA_GUARD |
| D14 | Missing key clinical context inventory | READY | ACTIVE | EXECUTABLE |
| D15 | Single tooth zero movement | READY | ACTIVE | EXECUTABLE |
| D16 | Historical plan difference | REVISE | DEFERRED | DEFERRED |
| G01 | Non-empty structured input | READY | ACTIVE | EXECUTABLE |
| G02 | Reliable source identity | READY | ACTIVE | EXECUTABLE |
| G03 | Tooth numbering convention | READY | ACTIVE | EXECUTABLE |
| G04 | Tooth ID validity | READY | ACTIVE | EXECUTABLE |
| G05 | Arch association | READY | ACTIVE | EXECUTABLE |
| G06 | Duplicate tooth records | READY | ACTIVE | EXECUTABLE |
| G07 | Canonical movement label mapping | READY | ACTIVE | EXECUTABLE |
| G08 | Numeric, unit and precision integrity | READY | ACTIVE | EXECUTABLE |
| G09 | Directional meaning verified | READY | ACTIVE | EXECUTABLE |
| G10 | Missing versus zero | READY | ACTIVE | EXECUTABLE |
| G11 | Reference basis: crown/root/cusp | READY | ACTIVE | EXECUTABLE |
| G12 | Total versus stage mode | READY | ACTIVE | EXECUTABLE |
| G13 | Plan/comparison mode | READY | ACTIVE | EXECUTABLE |
| G14 | Absent/unmovable teeth | REVISE | ACTIVE | REQUIRED_DATA_GUARD |
| G15 | Stage ordering and identifiers | READY | ACTIVE | REQUIRED_DATA_GUARD |
| G16 | Schema version and original evidence | READY | ACTIVE | EXECUTABLE |
| G17 | Conflict and unsupported input handling | READY | ACTIVE | EXECUTABLE |
| G18 | Recognized tooth types only | READY | ACTIVE | REQUIRED_DATA_GUARD |
| H01 | No clinical suitability diagnosis from TMT | READY | ACTIVE | EXECUTABLE |
| H02 | Periodontal condition unknown | READY | ACTIVE | EXECUTABLE |
| H03 | Root resorption/bone boundary unknown | READY | ACTIVE | EXECUTABLE |
| H04 | Occlusal contacts not inferable | READY | ACTIVE | EXECUTABLE |
| H05 | No unseen IPR planning | READY | ACTIVE | EXECUTABLE |
| H06 | No extraction/surgery recommendations | READY | ACTIVE | EXECUTABLE |
| H07 | No predicted success probability | READY | ACTIVE | EXECUTABLE |
| H08 | No absolute attachment prescriptions | READY | ACTIVE | EXECUTABLE |
| H09 | No claims of collision-free staging | READY | ACTIVE | EXECUTABLE |
| H10 | Monitoring and clinician sign-off | READY | ACTIVE | PARTIAL_SYSTEM_CONTROL |
| H11 | Context-dependent exclusions | READY | ACTIVE | EXECUTABLE |
| H12 | Privacy and data minimization | READY | ACTIVE | PARTIAL_SYSTEM_CONTROL |
| L01 | Only rule-approved facts in comments | READY | ACTIVE | OUTPUT_GUARD |
| L02 | Measurement exactness | READY | ACTIVE | OUTPUT_GUARD |
| L03 | Per-finding traceability | READY | ACTIVE | OUTPUT_GUARD |
| L04 | Deduplicate and resolve conflicts | READY | ACTIVE | OUTPUT_GUARD |
| L05 | Uncertainty disclosure | READY | ACTIVE | OUTPUT_GUARD |
| L06 | Final clinician review status | READY | ACTIVE | PARTIAL_SYSTEM_CONTROL |
| N01 | Table completeness / expected coverage | ADDITIONAL | ACTIVE | EXECUTABLE |
| N02 | Unknown format and layout drift | ADDITIONAL | ACTIVE | EXECUTABLE |
| N03 | Case / plan identity isolation | ADDITIONAL | ACTIVE | PARTIAL_SYSTEM_CONTROL |
| N04 | Unicode and raw evidence preservation | ADDITIONAL | ACTIVE | PARTIAL_SYSTEM_CONTROL |
| N05 | Mirrored tooth sign conventions | ADDITIONAL | ACTIVE | EXECUTABLE |
| N06 | External tooth-status metadata | ADDITIONAL | ACTIVE | EXECUTABLE |
| N07 | Stage and overcorrection states | ADDITIONAL | ACTIVE | EXECUTABLE |
| N08 | Coordinate frame and composition | ADDITIONAL | ACTIVE | EXECUTABLE |
| N09 | Field-scoped abstention | ADDITIONAL | ACTIVE | EXECUTABLE |
| N10 | Input/output claims filter | ADDITIONAL | ACTIVE | OUTPUT_GUARD |
| N11 | Immutable report amendments | ADDITIONAL | DEFERRED | DEFERRED |
| N12 | Clinical intended purpose | ADDITIONAL | ACTIVE | REQUIRED_DATA_GUARD |
| N13 | Rule-dependent eligibility | ADDITIONAL | ACTIVE | EXECUTABLE |
| N14 | Incident and rollback workflow | ADDITIONAL | DEFERRED | DEFERRED |
| R01 | Canine/premolar rotation review | VALIDATE | DISABLED | REQUIRED_DATA_GUARD |
| R02 | Rotation magnitude band by tooth type | VALIDATE | DISABLED | REQUIRED_DATA_GUARD |
| R03 | Anterior extrusion review | VALIDATE | DISABLED | REQUIRED_DATA_GUARD |
| R04 | Posterior extrusion review | VALIDATE | DISABLED | REQUIRED_DATA_GUARD |
| R05 | Lower incisor intrusion review | VALIDATE | DISABLED | REQUIRED_DATA_GUARD |
| R06 | Other intrusion review | VALIDATE | DISABLED | REQUIRED_DATA_GUARD |
| R07 | Incisor inclination / root control review | VALIDATE | DISABLED | REQUIRED_DATA_GUARD |
| R08 | Mesiodistal tipping/angulation review | VALIDATE | DISABLED | REQUIRED_DATA_GUARD |
| R09 | Posterior transverse movement review | VALIDATE | DISABLED | REQUIRED_DATA_GUARD |
| R10 | Maxillary molar distalization review | VALIDATE | DISABLED | REQUIRED_DATA_GUARD |
| R11 | Molar mesialization review | VALIDATE | DISABLED | REQUIRED_DATA_GUARD |
| R12 | Complex movement combination review | VALIDATE | DISABLED | REQUIRED_DATA_GUARD |
| R13 | Staged versus total movement concern | MORE DATA | DISABLED | REQUIRED_DATA_GUARD |
| R14 | Clinical-context-sensitive threshold withheld | READY | ACTIVE | EXECUTABLE |
| R15 | Attachment strategy merits review | VALIDATE | DISABLED | REQUIRED_DATA_GUARD |
| R16 | Potential complexity of whole case | MORE DATA | DISABLED | REQUIRED_DATA_GUARD |
| T01 | Per-stage movement ceilings | MORE DATA | DISABLED | REQUIRED_DATA_GUARD |
| T02 | Cumulative/incremental consistency | MORE DATA | DISABLED | REQUIRED_DATA_GUARD |
| T03 | Maximal stages override warning | MORE DATA | DISABLED | REQUIRED_DATA_GUARD |
| T04 | Sequential distalization pattern review | MORE DATA | DISABLED | REQUIRED_DATA_GUARD |
| T05 | Movement overlap interaction review | MORE DATA | DISABLED | REQUIRED_DATA_GUARD |
| T06 | Staging interferences from supplied geometry | MORE DATA | DISABLED | REQUIRED_DATA_GUARD |
| T07 | IPR timing and quantity review | MORE DATA | DISABLED | REQUIRED_DATA_GUARD |
| T08 | Anchorage and root balancing review | MORE DATA | DISABLED | REQUIRED_DATA_GUARD |
