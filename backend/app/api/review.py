"""Versioned, synthetic-only review transport; accepts no verification/release flags."""

from fastapi import APIRouter, HTTPException

from app.review.models import DraftReview, ReviewSubmission
from app.review.service import review_table
from app.parser.receipts import resolve

router = APIRouter()


@router.post("/api/v1/tmt/observations", response_model=DraftReview)
def review_submission(submission: ReviewSubmission) -> DraftReview:
    if submission.recovery_receipt and any(i.code=='RECOVERY_RECEIPT_INVALID' for i in resolve(submission).issues):
        raise HTTPException(status_code=409,detail='Recovery expired or changed. Parse the original table again.')
    return review_table(submission, requested_assessments=tuple(submission.requested_assessments))
