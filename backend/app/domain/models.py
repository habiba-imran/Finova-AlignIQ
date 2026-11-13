"""Lexical parsing is separate from source-semantic verification and clinical use."""

from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, StrictBool, field_validator

MAX_TEXT_CHARS = 100_000
MAX_REQUEST_BYTES = 1_048_576
MAX_LINES = 2_000
MAX_COLUMNS = 128
MAX_CELLS = 10_000
MAX_CELL_CHARS = 2_000

Platform = Literal["Unknown", "ClinCheck", "SureSmile"]
NumericStatus = Literal["PARSED", "EXPLICIT_ZERO", "MISSING", "NOT_PRESENT", "INVALID", "AMBIGUOUS"]
FieldStatus = Literal["SEMANTICS_UNKNOWN", "EXPLICIT_ZERO", "NOT_PRESENT", "PARSE_INVALID", "UNSUPPORTED", "AMBIGUOUS"]


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, allow_inf_nan=False)

class SourceContext(Contract):
    """All supplied metadata are unverified claims, including notation."""

    source_version: str | None = Field(default=None, max_length=64)
    notation: Literal["UNKNOWN", "FDI", "UNIVERSAL", "PALMER"] = "UNKNOWN"
    dentition: Literal["UNKNOWN", "PERMANENT", "PRIMARY", "MIXED"] = "UNKNOWN"
    arch: Literal["UNKNOWN", "UPPER", "LOWER", "BOTH"] = "UNKNOWN"
    plan_mode: Literal["UNKNOWN", "ALIGN_FINAL", "DOCTOR_FINAL", "COMPARISON"] = "UNKNOWN"
    reference_basis: Literal["UNKNOWN", "CROWN_CENTER", "VIRTUAL_ROOT_APEX", "CUSP_TIP"] = "UNKNOWN"
    scope: Literal["UNKNOWN", "TOTAL", "CUMULATIVE", "INCREMENTAL"] = "UNKNOWN"
    stage_index: int | None = Field(default=None, ge=0, le=2_147_483_647)
    coordinate_frame: str | None = Field(default=None, max_length=128)
    case_id: str | None = Field(default=None, max_length=64)
    plan_id: str | None = Field(default=None, max_length=64)
    decimal_separator: Literal["DOT", "COMMA"] = "DOT"

    @field_validator("source_version", "coordinate_frame", "case_id", "plan_id", mode="before")
    @classmethod
    def valid_unicode(cls, value):
        if isinstance(value, str) and any(0xD800 <= ord(character) <= 0xDFFF for character in value):
            raise ValueError("Unpaired Unicode surrogates are unsupported")
        return value


class LexicalInput(Contract):
    raw_text: str = Field(max_length=MAX_TEXT_CHARS)
    source_claim: Platform = "Unknown"
    context: SourceContext = Field(default_factory=SourceContext)

    @field_validator("raw_text")
    @classmethod
    def valid_unicode(cls, value: str) -> str:
        if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
            raise ValueError("Unpaired Unicode surrogates are unsupported")
        return value


class RawTMTSubmission(LexicalInput):
    synthetic_data_confirmed: StrictBool

    @field_validator("synthetic_data_confirmed")
    @classmethod
    def require_synthetic_confirmation(cls, value: bool) -> bool:
        if not value:
            raise ValueError("Synthetic-data confirmation is required")
        return value


class SourceSpan(Contract):
    """Offsets: zero-based Unicode code points, end exclusive. Line/columns: one-based."""

    line: int
    column_start: int
    column_end: int
    start: int
    end: int
    cell_index: int | None = None


class RawCell(Contract):
    raw: str
    span: SourceSpan


class ParseIssue(Contract):
    code: str
    severity: Literal["INFO", "WARNING", "ERROR"]
    message: str
    span: SourceSpan | None = None
    measurement_ids: list[str] = Field(default_factory=list)
    field: str | None = None


class AdapterInfo(Contract):
    id: str
    version: str
    verified: Literal[False] = False
    verified_source_versions: list[str] = Field(default_factory=list)


class SourceInfo(Contract):
    source_claim: Platform
    detected_claims: list[Platform] = Field(default_factory=list)
    claim_evidence: list[RawCell] = Field(default_factory=list)
    verification_status: Literal["UNVERIFIED"] = "UNVERIFIED"
    adapter: AdapterInfo
    candidate_adapter: AdapterInfo | None = None
    context: SourceContext
    metadata_status: Literal["USER_CLAIMS_UNVERIFIED"] = "USER_CLAIMS_UNVERIFIED"


class ToothIdentifier(Contract):
    id: str
    raw_identifier: str
    token: str
    notation_claim: str
    identifier_status: Literal["AMBIGUOUS", "UNVERIFIED", "INVALID", "UNSUPPORTED"]
    normalized_identifier: None = None
    span: SourceSpan
    clarification_fields: list[str] = Field(default_factory=list)


class ParsedMeasurement(Contract):
    id: str
    tooth_ref: str
    raw_label: str
    recognized_label: str | None = None
    raw_value: str | None
    raw_number: str | None = None
    signed_decimal: Decimal | None = None
    magnitude_decimal: Decimal | None = None
    raw_sign: str | None = None
    raw_unit: str | None = None
    header_unit: Literal["mm", "deg"] | None = None
    cell_unit: Literal["mm", "deg"] | None = None
    unit: Literal["mm", "deg"] | None = None
    raw_direction: str | None = None
    raw_suffix: str | None = None
    canonical_axis: None = None
    canonical_direction: None = None
    mapping_id: None = None
    numeric_status: NumericStatus
    field_status: FieldStatus
    missing_kind: Literal["BLANK", "DASH", "NOT_REPORTED", "NOT_APPLICABLE_TOKEN", "OMITTED_CELL"] | None = None
    semantics_verified: Literal[False] = False
    span: SourceSpan | None = None
    header_span: SourceSpan
    duplicate_group: str | None = None
    clarification_fields: list[str] = Field(default_factory=list)


class UnparsedLine(Contract):
    raw: str
    span: SourceSpan
    reason: str


class LayoutInfo(Contract):
    orientation: Literal["TEETH_IN_ROWS", "TEETH_IN_COLUMNS", "UNKNOWN"] = "UNKNOWN"
    delimiter: Literal["TAB", "PIPE", "SEMICOLON", "MULTISPACE"] | None = None
    header_line: int | None = None
    header_cells: list[RawCell] = Field(default_factory=list)
    declared_column_count: int = 0


class AxisCoverage(Contract):
    """Declared positions only; no expected clinical axes are invented."""

    expected_axes: None = None
    declared_measurements: int = 0
    numeric_present: int = 0
    explicit_zero: int = 0
    missing: int = 0
    invalid: int = 0
    ambiguous: int = 0
    unsupported: int = 0
    unverified: int = 0


class ParseResult(Contract):
    schema_version: Literal["1.0.0"] = "1.0.0"
    parser_version: Literal["0.1.0"] = "0.1.0"
    status: Literal["PARSED_UNVERIFIED", "PARTIAL", "UNSUPPORTED", "INVALID"]
    notice: Literal["Prototype — not for clinical use. Lexical parsing only; source semantics are unverified."] = (
        "Prototype — not for clinical use. Lexical parsing only; source semantics are unverified."
    )
    raw_text: str
    raw_sha256: str
    source: SourceInfo
    layout: LayoutInfo
    teeth: list[ToothIdentifier] = Field(default_factory=list)
    measurements: list[ParsedMeasurement] = Field(default_factory=list)
    coverage: AxisCoverage = Field(default_factory=AxisCoverage)
    issues: list[ParseIssue] = Field(default_factory=list)
    clarification_fields: list[str] = Field(default_factory=list)
    unparsed_lines: list[UnparsedLine] = Field(default_factory=list)
