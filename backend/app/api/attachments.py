import os

from fastapi import APIRouter, HTTPException

from app.attachments.demo import input_demo, draft_demo
from app.attachments.models import AttachmentDemoInput, AttachmentDraft, AttachmentSubmission, EmptyDemoRequest
from app.attachments.service import attachment_review
from app.parser.receipts import resolve

router = APIRouter()


@router.post("/api/v1/attachments/draft", response_model=AttachmentDraft)
def create_attachment_draft(submission: AttachmentSubmission):
    if submission.recovery_receipt and any(i.code == "RECOVERY_RECEIPT_INVALID" for i in resolve(submission).issues):
        raise HTTPException(status_code=409, detail="Recovery expired or changed. Parse the original table again.")
    return attachment_review(submission)


def require_attachment_demo():
    if os.environ.get("FINOVA_ENVIRONMENT") != "development" or os.environ.get("FINOVA_ATTACHMENT_DEMO_ENABLED") != "true":
        raise HTTPException(status_code=404, detail="Development attachment demonstration is disabled.")


@router.post("/api/v1/development/attachment-demo/input", response_model=AttachmentDemoInput)
def attachment_demo_input(request: EmptyDemoRequest):
    require_attachment_demo()
    try:
        return input_demo()
    except (OSError, ValueError):
        raise HTTPException(status_code=503, detail="Fixed attachment demonstration evidence is unavailable.") from None


@router.post("/api/v1/development/attachment-demo/draft", response_model=AttachmentDraft)
def attachment_demo_draft(request: EmptyDemoRequest):
    require_attachment_demo()
    try:
        return draft_demo()
    except (OSError, ValueError):
        raise HTTPException(status_code=503, detail="Fixed attachment demonstration evidence is unavailable.") from None
