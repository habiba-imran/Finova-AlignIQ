"""Source-label comparisons only; independent synthetic demo rules, no clinical policy.

Every comparison is within one recognized lexical family and explicit unit.
Ranks use Decimal magnitudes, retain ties and never convert direction labels to
signs. FDI-style grouping is a disclosed token convention, not verified anatomy.
See docs/SYNTHETIC_ANALYSIS_RULES.md for the complete demonstration policy.
"""
from collections import Counter, defaultdict
import re

from app.interactive.models import AnalyticalFinding, ModuleSection
from app.interactive.narrative import LABELS

ANGULAR = ("rotation", "angulation", "inclination")
VERTICAL = ("vertical", "relative_vertical", "extrusion", "intrusion")
TRANSLATION = ("mesiodistal", "buccolingual")
SECTION_TITLES = {
    "macro": {"SAGITTAL": "Sagittal / Mesiodistal movement", "TRANSVERSE": "Transverse / Buccolingual movement",
              "VERTICAL": "Vertical movement", "ANGULAR": "Additional angular observations", "SUMMARY": "Overall movement summary"},
    "micro": {"ANGULAR_FOCUS": "Priority tooth profiles", "ATTACHMENT_DEMO": "Illustrative attachment considerations",
              "ANGULAR_COVERAGE": "Angular review coverage", "ATTACHMENT_SCOPE": "Attachment review scope"},
    "nano": {"DISTRIBUTION": "Arch and tooth-group distribution", "TRANSLATIONS": "Translation concentrations",
             "VERTICAL_PATTERNS": "Vertical concentrations", "MULTI_COMPONENT": "Multiple notable components",
             "SEQUENCE_REVIEW": "Sequencing review considerations"},
}


def magnitude_range(low, high, unit="mm"):
    """Display a single source magnitude once; comparison precision is unchanged."""
    return f"{low} {unit}" if low == high else f"{low}–{high} {unit}"


class Analysis:
    def __init__(self, parsed):
        self.parsed = parsed
        self.teeth = {t.id: t for t in parsed.teeth}
        self.cells = parsed.measurements
        self.findings = []
        self.by_family = defaultdict(list)
        for m in self.cells:
            self.by_family[m.recognized_label].append(m)

    def name(self, m):
        return self.teeth[m.tooth_ref].raw_identifier.strip()

    def tokens(self, cells):
        names = sorted({self.name(m) for m in cells})
        return ("Tooth " if len(names) == 1 else "Teeth ") + ", ".join(names)

    @staticmethod
    def usable(m, unit):
        return m.numeric_status in {"PARSED", "EXPLICIT_ZERO"} and m.field_status != "AMBIGUOUS" and m.unit == unit

    def numeric(self, family):
        return [m for m in self.by_family[family] if self.usable(m, "deg" if family in ANGULAR else "mm")]

    def add(self, section, kind, text, evidence=(), selected=(), demo_rule=None):
        self.findings.append(AnalyticalFinding(finding_id=f"F{len(self.findings)+1:04d}", section_id=section,
            kind=kind, text=text, source_refs=list(dict.fromkeys(m.id for m in evidence)),
            selected_refs=list(dict.fromkeys(m.id for m in selected)), demo_rule=demo_rule,
            origin="SIMULATED_DEMO" if demo_rule else "DESCRIPTIVE_COMPARISON"))

    def value(self, m):
        return f"{m.signed_decimal}{'°' if m.unit == 'deg' else ' mm'}" + (f" ({m.raw_direction}-labelled)" if m.raw_direction else " (no direction label)")

    def coverage(self, section, families):
        # Extrusion/intrusion/vertical are lexical alternatives, not compulsory
        # independent columns. Do not imply a missing column when another form is present.
        has_vertical = any(self.by_family[f] for f in VERTICAL)
        for family in families:
            cells = self.by_family[family]
            unavailable = [m for m in cells if m not in self.numeric(family)]
            label = LABELS[family]
            if not cells:
                if family in VERTICAL and has_vertical:
                    continue
                self.add(section, "ABSENT_FIELD", f"No {label} field was supplied; comparisons for this field are unavailable.")
            elif unavailable:
                reasons = sorted({"ambiguous" if m.field_status == "AMBIGUOUS" else "unit unknown" if m.numeric_status in {"PARSED", "EXPLICIT_ZERO"} else m.numeric_status.lower().replace("not_present", "omitted") for m in unavailable})
                self.add(section, "INCOMPLETE_COMPARISON", f"{self.tokens(unavailable)}: {label} unavailable in {len(unavailable)} position{'s' if len(unavailable) != 1 else ''} ({', '.join(reasons)}). Unknown values are excluded from comparisons.", cells, unavailable)

    def compare(self, section, families, distributions=True):
        for family in families:
            cells = self.numeric(family)
            if not cells:
                continue
            label = LABELS[family]
            high = max(m.magnitude_decimal for m in cells)
            winners = [m for m in cells if m.magnitude_decimal == high]
            # Keep different recorded precision/directions in separate tied facts.
            groups = defaultdict(list)
            for m in winners:
                groups[(str(m.signed_decimal), m.raw_direction)].append(m)
            for group in groups.values():
                self.add(section, "MAXIMUM", f"{self.tokens(group)}: largest recorded {label} magnitude, {self.value(group[0])}{' each' if len(group)>1 else ''}, among {len(cells)} comparable entries.", cells, group)
            if distributions:
                labels = Counter(m.raw_direction or "unlabelled" for m in cells)
                counts = "; ".join(f"{key}: {count}" for key, count in sorted(labels.items()))
                self.add(section, "DIRECTION_DISTRIBUTION", f"{label.capitalize()} source-label distribution: {counts}.", cells, cells)
            low = min(m.magnitude_decimal for m in cells)
            if low != high:
                lows = [m for m in cells if m.magnitude_decimal == low]
                # A range compares magnitudes; never subtract signed movements.
                self.add(section, "RANGE", f"{label.capitalize()} magnitude range: {magnitude_range(low, high, '°' if family in ANGULAR else 'mm')}; smallest at {self.tokens(lows).lower()}.", cells, lows + winners)
        self.coverage(section, families)

    def repeated(self, section, families):
        for family in families:
            groups = defaultdict(list)
            for m in self.numeric(family):
                if m.magnitude_decimal:
                    groups[(str(m.signed_decimal), m.raw_direction)].append(m)
            # At most two largest repeated profiles per family, no full inventory.
            repeated = sorted((g for g in groups.values() if len(g) >= 3), key=lambda g: (-g[0].magnitude_decimal, -len(g)))[:2]
            for group in repeated:
                self.add(section, "SHARED_PROFILE", f"{self.tokens(group)} share recorded {LABELS[family]} entries of {self.value(group[0])} each.", self.numeric(family), group)

    def token_group(self, tooth):
        # An explicit conflicting numbering claim precludes even token grouping.
        if tooth.notation_claim not in {"Unknown", "UNKNOWN", "FDI", "unknown"}:
            return "Unassigned tokens"
        token = tooth.token.strip()
        if not re.fullmatch(r"[1-4][1-8]", token):
            return "Unassigned tokens"
        return ("Upper" if token[0] in "12" else "Lower") + "-arch " + ("anterior" if token[1] in "123" else "posterior")

    def distribution(self, section):
        groups = defaultdict(list)
        for tooth in self.teeth.values():
            groups[self.token_group(tooth)].append(tooth)
        for name, teeth in sorted(groups.items()):
            refs = {t.id for t in teeth}
            cells = [m for m in self.cells if m.tooth_ref in refs]
            numeric = sum(self.usable(m, m.unit) for m in cells if m.unit is not None)
            self.add(section, "TOKEN_GROUP", f"{name}: {len(teeth)} tooth tokens, {numeric} available numerical entries across {len(cells)} positions.", cells, cells)
        self.add(section, "TOKEN_GROUP_SCOPE", "Grouping assumes FDI-style token syntax only; anatomical identity remains unverified. Other or conflicting numbering conventions remain unassigned.", self.cells)

    def concentration(self, section, families):
        for family in families:
            cells = [m for m in self.numeric(family) if m.magnitude_decimal > 0]
            if not cells:
                continue
            ordered = sorted((m.magnitude_decimal for m in cells), reverse=True)
            # Upper half of nonzero positions by magnitude; ties are kept.
            boundary = ordered[(len(ordered)-1)//2]
            selected = [m for m in cells if m.magnitude_decimal >= boundary]
            groups = defaultdict(list)
            for m in selected:
                groups[(self.token_group(self.teeth[m.tooth_ref]), m.raw_direction or "unlabelled")].append(m)
            # Groups partition the entire selected set. A display limit here used
            # to drop qualifying ties belonging to a fourth arch/label group.
            for (name, direction), group in sorted(groups.items(), key=lambda pair: (-len(pair[1]), pair[0])):
                low, high = min(m.magnitude_decimal for m in group), max(m.magnitude_decimal for m in group)
                self.add(section, "CONCENTRATION", f"{LABELS[family].capitalize()}: {self.tokens(group)} in {name.lower()}, {direction} source label, {magnitude_range(low, high)}; {len(group)} of {len(cells)} nonzero entries in this field's upper half (ties retained).", cells, group)
            runs = defaultdict(list)
            for m in selected:
                tooth = self.teeth[m.tooth_ref]
                if self.token_group(tooth) != "Unassigned tokens":
                    runs[(tooth.token[0], m.raw_direction)].append(m)
            for (_, direction), group in sorted(runs.items(), key=lambda p: str(p[0])):
                ordered_group = sorted(group, key=lambda m: self.teeth[m.tooth_ref].token)
                contiguous = []
                for m in ordered_group:
                    if contiguous and int(self.teeth[m.tooth_ref].token) != int(self.teeth[contiguous[-1].tooth_ref].token) + 1:
                        if len(contiguous) >= 3:
                            self.add_run(section, family, cells, contiguous, direction)
                        contiguous = []
                    contiguous.append(m)
                if len(contiguous) >= 3:
                    self.add_run(section, family, cells, contiguous, direction)
        self.repeated(section, families)
        self.coverage(section, families)

    def add_run(self, section, family, cells, group, direction):
        low, high = min(m.magnitude_decimal for m in group), max(m.magnitude_decimal for m in group)
        self.add(section, "CONTIGUOUS_TOKEN_PATTERN", f"{self.tokens(group)} form a consecutive FDI-style token run among the upper-half {LABELS[family]} entries: {direction or 'unlabelled'} source label, {magnitude_range(low, high)}.", cells, group)

    def micro(self):
        ranks, maxima = defaultdict(list), defaultdict(list)
        for family in ANGULAR:
            cells = [m for m in self.numeric(family) if m.magnitude_decimal]
            levels = sorted({m.magnitude_decimal for m in cells}, reverse=True)
            for m in cells:
                if m.magnitude_decimal in levels[:2]:
                    ranks[m.tooth_ref].append(m)
                if levels and m.magnitude_decimal == levels[0]:
                    maxima[m.tooth_ref].append(m)
        priority = sorted(ranks, key=lambda ref: (-len(maxima[ref]), -len(ranks[ref]), self.teeth[ref].token))[:5]
        all_angular = [m for m in self.cells if m.recognized_label in ANGULAR]
        for ref in priority:
            selected = ranks[ref]
            maximum = maxima[ref]
            details = "; ".join(f"{LABELS[m.recognized_label]} {self.value(m)} ({'dataset maximum' if m in maximum else 'second distinct magnitude'})" for m in selected)
            self.add("ANGULAR_FOCUS", "ANGULAR_PRIORITY", f"Tooth {self.teeth[ref].raw_identifier.strip()}: {details}.", all_angular, selected)
            kind = "CANDIDATE" if maximum else "ALTERNATIVE"
            focus = "combined angular" if len(maximum) >= 2 else LABELS[(maximum or selected)[0].recognized_label]
            alternative = " An alternative is to review the angular components separately." if len(maximum) >= 2 else ""
            self.add("ATTACHMENT_DEMO", kind, f"Tooth {self.teeth[ref].raw_identifier.strip()} — illustrative {kind.lower()}: {focus}-control attachment review, triggered by the angular ranks above.{alternative}", all_angular, selected, "DEMO-ANGULAR-RANK-v1")
        for tooth in self.teeth.values():
            own = [m for m in all_angular if m.tooth_ref == tooth.id]
            if len(own) == 3 and {m.recognized_label for m in own} == set(ANGULAR) and all(self.usable(m, "deg") and m.magnitude_decimal == 0 for m in own):
                self.add("ATTACHMENT_DEMO", "NO_CANDIDATE", f"Tooth {tooth.raw_identifier.strip()} — no candidate in this illustrative angular-only screen: rotation, angulation and inclination are explicitly zero. This does not establish that no attachment is clinically needed.", own, own, "DEMO-ZERO-ANGULAR-v1")
                break
        if not priority:
            self.add("ANGULAR_FOCUS", "NO_ANGULAR_PRIORITY", "No nonzero comparable angular profile can be prioritized from the available fields.", all_angular)
        if not any(f.section_id == "ATTACHMENT_DEMO" for f in self.findings):
            self.add("ATTACHMENT_DEMO", "UNKNOWN_CANDIDATE", "Illustrative attachment candidate unknown: the angular-only demonstration has insufficient comparable evidence.", all_angular, demo_rule="DEMO-ANGULAR-RANK-v1")
        self.coverage("ANGULAR_COVERAGE", ANGULAR)
        self.add("ANGULAR_COVERAGE", "REVIEW_COVERAGE", f"{len(priority)} priority profiles shown from {len(self.teeth)} teeth. The shortlist uses the two largest distinct nonzero magnitudes per angular field, ordered by number of maxima, highlighted components, then tooth identifier. Up to five profiles are shown; these ranks are not clinical severity classifications.", all_angular)
        self.add("ATTACHMENT_SCOPE", "SCOPE", "Illustrative attachment review only. Clinical need, shape, dimensions, orientation and placement are not established.")

    def nano(self):
        self.distribution("DISTRIBUTION")
        if self.parsed.source.context.stage_index is not None:
            self.add("DISTRIBUTION", "SOURCE_STAGE_CONTEXT", f"Unverified source-context stage index: {self.parsed.source.context.stage_index}; this is not a stage-by-stage schedule.")
        self.concentration("TRANSLATIONS", TRANSLATION)
        self.concentration("VERTICAL_PATTERNS", VERTICAL)
        notable = defaultdict(list)
        for family in (*TRANSLATION, *VERTICAL, *ANGULAR):
            cells = [m for m in self.numeric(family) if m.magnitude_decimal]
            if not cells:
                continue
            levels = sorted((m.magnitude_decimal for m in cells), reverse=True)
            boundary = levels[(len(levels)-1)//4]
            for m in cells:
                if m.magnitude_decimal >= boundary:
                    notable[m.tooth_ref].append(m)
        for ref, group in sorted(notable.items(), key=lambda p: (-len(p[1]), self.teeth[p[0]].token))[:4]:
            if len(group) < 2:
                continue
            self.add("MULTI_COMPONENT", "MULTI_COMPONENT", f"Tooth {self.teeth[ref].raw_identifier.strip()}: " + "; ".join(f"{LABELS[m.recognized_label]} {self.value(m)}" for m in group) + ".", self.cells, group)
        if not any(f.section_id == "MULTI_COMPONENT" for f in self.findings):
            self.add("MULTI_COMPONENT", "NO_MULTI_COMPONENT", "No tooth has multiple components in the dataset's upper-quarter comparison, or comparable data are insufficient.", self.cells)
        else:
            self.add("MULTI_COMPONENT", "MULTI_COMPONENT_SCOPE", "Each listed tooth has multiple components in their family's upper quarter of nonzero magnitudes (ties retained). Review their coexistence without inferring simultaneous delivery.", self.cells)
        self.add("SEQUENCE_REVIEW", "REVIEW_CONSIDERATION", "Review translation and vertical clusters alongside teeth with multiple highlighted components. These ranks describe this table, not clinical thresholds. Total movements do not establish a stage schedule, timing, force or anchorage prescription.", self.cells)
        self.add("SEQUENCE_REVIEW", "SIMULATED_REVIEW_ORDER", "Illustrative review order only: inspect translation clusters, then vertical clusters, then cross-check teeth shared by those profiles. This is a simulated order for reviewing information, not a calculated movement sequence or treatment schedule.", self.cells, demo_rule="DEMO-REVIEW-ORDER-v1")

    def run(self, module):
        if module == "macro":
            self.compare("SAGITTAL", ("mesiodistal",))
            self.repeated("SAGITTAL", ("mesiodistal",))
            self.compare("TRANSVERSE", ("buccolingual",))
            self.compare("VERTICAL", VERTICAL)
            self.repeated("VERTICAL", VERTICAL)
            self.compare("ANGULAR", ANGULAR, distributions=False)
            highlights = []
            highlighted = []
            for family in (*TRANSLATION, "vertical"):
                cells = self.numeric(family)
                if cells:
                    high = max(m.magnitude_decimal for m in cells)
                    selected = [m for m in cells if m.magnitude_decimal == high]
                    highlights.append(f"{LABELS[family]} peaks at {self.tokens(selected).lower()}")
                    highlighted.extend(cells)
            if highlights:
                self.add("SUMMARY", "OVERALL_PATTERN", "Overall recorded profile: " + "; ".join(highlights) + ". Compare these cross-tooth concentrations alongside the separate angular findings.", highlighted)
            self.distribution("SUMMARY")
            self.add("SUMMARY", "SCOPE", "Compare recorded translations across teeth and vertical entries within each field separately. Relative vertical values are not added to absolute vertical values; angular observations remain separate. These descriptive patterns establish no clinical risk classification.", self.cells)
        elif module == "micro":
            self.micro()
        else:
            self.nano()
        sections = []
        for key, title in SECTION_TITLES[module].items():
            findings = [f for f in self.findings if f.section_id == key]
            refs = list(dict.fromkeys(ref for f in findings for ref in f.source_refs))
            status = "SIMULATED_DEMO" if key == "ATTACHMENT_DEMO" else "SOURCE_REPORTED" if refs else "UNAVAILABLE"
            sections.append(ModuleSection(section_id=key, title=title, status=status,
                text="\n\n".join(f.text for f in findings), source_refs=refs))
        return sections, self.findings


def analyze(parsed, module):
    return Analysis(parsed).run(module)
