from fastapi import APIRouter, HTTPException

from app.interactive.models import InteractiveReport, InteractiveSubmission
from app.interactive.service import generate_interactive

router = APIRouter()


@router.get('/api/v1/interactive/scenarios/{scenario_id}')
def functional_scenario(scenario_id: str):
    from app.functional.scenarios import scenario
    try:
        return scenario(scenario_id)
    except KeyError:
        raise HTTPException(status_code=404, detail='Synthetic scenario not found.') from None


@router.get("/api/v1/interactive/capabilities")
def interactive_capabilities():
    # Public contract identification only: no keys, environment, raw input,
    # development-route switches or clinical authority are exposed.
    return {"report_format": "MODULE_SPECIFIC_V1", "analytical_report_format": "ANALYTICAL_V1", "revision": "analytical-reviews-2026-11-15-v1",
        "functional_report_format": "FUNCTIONAL_DEMO_V1", "functional_scenarios": ['macro-distribution','micro-catalog','nano-phases'],
        "generalized_review_supported": True, "planning_options_version": "1.0.0",
        "modules": ["macro", "micro", "nano"], "supplied_review_details": True, "clinical_analysis_enabled": False}


@router.post("/api/v1/interactive/review", response_model=InteractiveReport)
def interactive_review(submission: InteractiveSubmission):
    try:
        return generate_interactive(submission)
    except ValueError as exc:
        if str(exc) == "REPARSE_REQUIRED":
            raise HTTPException(status_code=409, detail="Input changed or recovery expired. Parse the original table again.") from None
        if str(exc) == "PARSE_REQUIRED":
            raise HTTPException(status_code=422, detail="A supported parsed table is required.") from None
        if str(exc) in {"FUNCTIONAL_CONTEXT_SOURCE_MISMATCH", "FUNCTIONAL_CONTEXT_MODULE_MISMATCH", "FUNCTIONAL_CONTEXT_INVALID", "DETAILS_MODULE_MISMATCH", "ATTACHMENT_REFERENCE_INVALID", "ATTACHMENT_CHOICE_CONFLICT", "STAGE_REFERENCE_INVALID", "ALLOCATION_REFERENCE_INVALID", "ALLOCATION_UNIT_INVALID", "ANCHORAGE_REFERENCE_INVALID"}:
            raise HTTPException(status_code=422, detail=str(exc)) from None
        raise
