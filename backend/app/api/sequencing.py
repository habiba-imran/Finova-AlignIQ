import os

from fastapi import APIRouter, HTTPException

from app.parser.receipts import resolve
from app.sequencing.demo import input_demo, draft_demo
from app.sequencing.models import EmptyDemoRequest, SequencingDemoInput, SequencingDraft, SequencingSubmission
from app.sequencing.service import sequencing_review

router = APIRouter()


@router.post("/api/v1/sequencing/draft", response_model=SequencingDraft)
def create_sequencing_draft(submission: SequencingSubmission):
    if submission.recovery_receipt and any(i.code == "RECOVERY_RECEIPT_INVALID" for i in resolve(submission).issues):
        raise HTTPException(status_code=409, detail="Recovery expired or changed. Parse the original table again.")
    return sequencing_review(submission)


def require_demo():
    if os.environ.get("FINOVA_ENVIRONMENT") != "development" or os.environ.get("FINOVA_SEQUENCER_DEMO_ENABLED") != "true":
        raise HTTPException(status_code=404, detail="Development sequencing demonstration is disabled.")


@router.post("/api/v1/development/sequencer-demo/input", response_model=SequencingDemoInput)
def sequencing_demo_input(request: EmptyDemoRequest):
    require_demo()
    try:
        return input_demo()
    except (OSError, ValueError):
        raise HTTPException(status_code=503, detail="Fixed sequencing demonstration evidence is unavailable.") from None


@router.post("/api/v1/development/sequencer-demo/draft", response_model=SequencingDraft)
def sequencing_demo_draft(request: EmptyDemoRequest):
    require_demo()
    try:
        return draft_demo()
    except (OSError, ValueError):
        raise HTTPException(status_code=503, detail="Fixed sequencing demonstration evidence is unavailable.") from None
