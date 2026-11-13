"""Synthetic-only, versioned final DRAFT report transport. No supplied findings/trust flags."""

from fastapi import APIRouter, HTTPException

from app.reports.models import FinalDraftReport, ReportSubmission
from app.reports.service import generate_report
from app.parser.receipts import resolve

router = APIRouter()


@router.post("/api/v1/reports/draft", response_model=FinalDraftReport)
def create_draft_report(submission: ReportSubmission) -> FinalDraftReport:
    if submission.recovery_receipt and any(i.code=='RECOVERY_RECEIPT_INVALID' for i in resolve(submission).issues):
        raise HTTPException(status_code=409,detail='Recovery expired or changed. Parse the original table again.')
    return generate_report(submission, mode=submission.comment_mode, requested_assessments=tuple(submission.requested_assessments))
