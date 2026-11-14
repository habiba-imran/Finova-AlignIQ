"""Additive Planning Assistant transport. Demonstration authority stays server-owned."""
import os

from fastapi import APIRouter, HTTPException

from app.api.reports import create_draft_report
from app.planning.demo import demo_input, demo_report
from app.planning.models import DemoInput, DemoRequest, PlanningDraft
from app.planning.service import organize
from app.reports.models import ReportSubmission
from app.semantics.fixtures import FixtureVerificationError

router = APIRouter()


@router.post("/api/v1/planning/draft", response_model=PlanningDraft)
def planning_draft(submission: ReportSubmission) -> PlanningDraft:
    return organize(create_draft_report(submission))


def require_demo():
    if os.environ.get("FINOVA_ENVIRONMENT") != "development" or os.environ.get("FINOVA_PLANNING_DEMO_ENABLED") != "true":
        raise HTTPException(status_code=404, detail="Development demonstration is disabled.")


@router.post("/api/v1/development/planning-demo/input", response_model=DemoInput)
def planning_demo_input(request: DemoRequest) -> DemoInput:
    require_demo()
    try:
        return demo_input()
    except (OSError, ValueError, FixtureVerificationError):
        raise HTTPException(status_code=503, detail="The fixed demonstration evidence is unavailable.") from None


@router.post("/api/v1/development/planning-demo/draft", response_model=PlanningDraft)
def planning_demo_draft(request: DemoRequest) -> PlanningDraft:
    require_demo()
    try:
        return demo_report(request.comment_mode)
    except (OSError, ValueError, FixtureVerificationError):
        raise HTTPException(status_code=503, detail="The fixed demonstration evidence is unavailable.") from None
