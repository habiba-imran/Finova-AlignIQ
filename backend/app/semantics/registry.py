"""Release trust is code-controlled and separate from self-described fixture reviews."""

from dataclasses import dataclass

from app.semantics.fixtures import CheckedFixture, digest_json
from app.semantics.models import FixtureExpectedOutput, FixtureRecord

# Empty intentionally. Adding a manifest entry, metadata claim, or env flag cannot enable a vendor.
APPROVED_RELEASE_DIGESTS: frozenset[str] = frozenset()
REVOKED_RELEASE_DIGESTS: frozenset[str] = frozenset()


@dataclass(frozen=True)
class EvidenceRegistry:
    approved: frozenset[str] = APPROVED_RELEASE_DIGESTS
    revoked: frozenset[str] = REVOKED_RELEASE_DIGESTS

    def authority(self, checked: CheckedFixture, *, allow_test_only: bool = False) -> str | None:
        record = FixtureRecord.model_validate_json(checked.record_json)
        expected = FixtureExpectedOutput.model_validate_json(checked.expected_json)
        digest = digest_json({"record": record.model_dump(mode="json"), "expected": expected.model_dump(mode="json")})
        if digest != checked.release_digest or digest in self.revoked:
            return None
        if record.kind == "SYNTHETIC":
            return "TEST_ONLY" if allow_test_only and record.application == "TEST_ONLY" else None
        if record.status == "REVIEWED" and digest in self.approved:
            return "VERIFIED"
        return None


DEFAULT_REGISTRY = EvidenceRegistry()
