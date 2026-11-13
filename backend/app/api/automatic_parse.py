"""Versioned automatic/assisted routes; legacy lexical and report contracts are intact."""

from fastapi import APIRouter

from app.domain.models import RawTMTSubmission
from app.parser.contracts import AssistedSubmission, AutomaticParseResult, PipelineSubmission, SyntheticFixture
from app.parser.pipeline import automatic_parse
from app.parser.phase4 import parse_pipeline
from app.parser.generated import generate

router = APIRouter()


@router.post("/api/v1/tmt/parse", response_model=AutomaticParseResult)
def parse_automatic(submission: PipelineSubmission) -> AutomaticParseResult:
    return parse_pipeline(submission)


@router.post("/api/v1/development/synthetic")
def development_synthetic(identity: SyntheticFixture):
    """No free-text enrollment; returns original generated synthetic content only."""
    sample=generate(identity)
    return {"raw_text":sample.raw_text,"synthetic_fixture":identity.model_dump(),"category":sample.category,
            "notice":"Original synthetic test content; not authentic vendor evidence."}


@router.post("/api/v1/tmt/parse/assisted", response_model=AutomaticParseResult)
def parse_assisted(submission: AssistedSubmission) -> AutomaticParseResult:
    return automatic_parse(submission, assisted=True)
