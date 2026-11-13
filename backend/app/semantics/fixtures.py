"""Read-only local fixture verification. No downloads, capture storage, or raw diagnostics."""

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path, PureWindowsPath

from pydantic import ValidationError

from app.domain.models import LexicalInput, MAX_REQUEST_BYTES
from app.parser.service import parse_table
from app.semantics.models import Artifact, FixtureExpectedOutput, FixtureManifest, FixtureRecord


class FixtureVerificationError(ValueError):
    """Only a static code is exposed, never an input token or artifact path."""


def digest_json(value: dict) -> str:
    return sha256(json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":")).encode()).hexdigest()


@dataclass(frozen=True, repr=False)
class CheckedFixture:
    # Immutable serialized snapshots prevent mutation of reviewed Pydantic nested lists after checking.
    record_json: str
    expected_json: str
    lexical_json: str
    release_digest: str


def _read_artifact(root: Path, artifact: Artifact, limit: int) -> bytes:
    try:
        relative = Path(artifact.path)
        windows = PureWindowsPath(artifact.path)
        if relative.is_absolute() or windows.drive or windows.root or ":" in artifact.path or ".." in relative.parts:
            raise FixtureVerificationError("UNSAFE_ARTIFACT_PATH")
        target = (root.resolve() / relative).resolve(strict=True)
        if not target.is_relative_to(root.resolve()) or not target.is_file():
            raise FixtureVerificationError("UNSAFE_ARTIFACT_PATH")
        with target.open("rb") as handle:
            data = handle.read(limit + 1)
        if len(data) > limit:
            raise FixtureVerificationError("ARTIFACT_LIMIT")
        if sha256(data).hexdigest() != artifact.sha256:
            raise FixtureVerificationError("ARTIFACT_HASH_MISMATCH")
        return data
    except FixtureVerificationError:
        raise
    except (OSError, ValueError):
        raise FixtureVerificationError("ARTIFACT_UNAVAILABLE") from None


def load_manifest(path: Path) -> FixtureManifest:
    try:
        with path.open("rb") as handle:
            data = handle.read(MAX_REQUEST_BYTES + 1)
        if len(data) > MAX_REQUEST_BYTES:
            raise FixtureVerificationError("MANIFEST_LIMIT")
        return FixtureManifest.model_validate_json(data)
    except FixtureVerificationError:
        raise
    except (OSError, ValueError, ValidationError):
        raise FixtureVerificationError("MANIFEST_INVALID") from None


def verify_fixture(record: FixtureRecord, root: Path) -> CheckedFixture:
    """Verify integrity and exact independent oracle equality, NOT reviewer identity or clinical truth."""
    try:
        record = FixtureRecord.model_validate_json(record.model_dump_json())
        if record.status not in {"REVIEWED", "TEST_ONLY"}:
            raise FixtureVerificationError("FIXTURE_NOT_REVIEWED")
        if not record.raw or not record.expected or not record.submission_context:
            raise FixtureVerificationError("FIXTURE_INCOMPLETE")
        raw_bytes = _read_artifact(root, record.raw, MAX_REQUEST_BYTES)
        expected_bytes = _read_artifact(root, record.expected, 32 * MAX_REQUEST_BYTES)
        if record.source_evidence:
            _read_artifact(root, record.source_evidence, 16 * MAX_REQUEST_BYTES)
        expected = FixtureExpectedOutput.model_validate_json(expected_bytes)
        if expected.kind != record.kind:
            raise FixtureVerificationError("EVIDENCE_KIND_MISMATCH")
        # Decode verbatim UTF-8 bytes; read_text() would normalize CRLF/CR on some platforms.
        submission = LexicalInput.model_validate({**record.submission_context.model_dump(), "raw_text": raw_bytes.decode("utf-8")})
        actual = parse_table(submission)
        if actual.model_dump(mode="json") != expected.lexical.model_dump(mode="json"):
            raise FixtureVerificationError("LEXICAL_ORACLE_MISMATCH")
        if record.kind == "AUTHENTIC":
            if any(claim != record.application for claim in actual.source.detected_claims):
                raise FixtureVerificationError("CAPTURE_SOURCE_CONFLICT")
            for measurement in expected.measurements:
                for component in measurement.components:
                    if component.name == "source_application" and component.value not in {None, record.application}:
                        raise FixtureVerificationError("CAPTURE_SOURCE_CONFLICT")
                    if component.name == "source_version" and component.value not in {None, record.source_version}:
                        raise FixtureVerificationError("CAPTURE_VERSION_CONFLICT")
        expected_json = expected.model_dump_json()
        record_json = record.model_dump_json()
        release_digest = digest_json({"record": json.loads(record_json), "expected": json.loads(expected_json)})
        return CheckedFixture(record_json, expected_json, actual.model_dump_json(), release_digest)
    except FixtureVerificationError:
        raise
    except (ValueError, UnicodeError, ValidationError):
        raise FixtureVerificationError("FIXTURE_INVALID") from None


def assert_fixture_matches(record: FixtureRecord, root: Path) -> None:
    """Pytest helper whose failure message contains no raw/expected patient text."""
    verify_fixture(record, root)
