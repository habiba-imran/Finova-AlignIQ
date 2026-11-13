"""Candidates are extension points, not a promise of vendor compatibility."""

from dataclasses import dataclass

from app.domain.models import AdapterInfo, SourceContext


@dataclass(frozen=True)
class SourceAdapter:
    id: str
    platform: str
    incompatible_bases: frozenset[str]
    incompatible_modes: frozenset[str] = frozenset()
    version: str = "0.1.0"

    def info(self) -> AdapterInfo:
        # No public/request flag can override fixture verification.
        return AdapterInfo(id=self.id, version=self.version)

    def context_conflicts(self, context: SourceContext) -> list[str]:
        conflicts = []
        if context.reference_basis in self.incompatible_bases:
            conflicts.append("reference_basis")
        if context.plan_mode in self.incompatible_modes:
            conflicts.append("plan_mode")
        return conflicts
