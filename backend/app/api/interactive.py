from fastapi import APIRouter, HTTPException

from app.interactive.models import InteractiveReport, InteractiveSubmission
from app.interactive.service import generate_interactive

router = APIRouter()


@router.post("/api/v1/interactive/review", response_model=InteractiveReport)
def interactive_review(submission: InteractiveSubmission):
    try:
        return generate_interactive(submission)
    except ValueError as exc:
        if str(exc) == "REPARSE_REQUIRED":
            raise HTTPException(status_code=409, detail="Input changed or recovery expired. Parse the original table again.") from None
        if str(exc) == "PARSE_REQUIRED":
            raise HTTPException(status_code=422, detail="A supported parsed table is required.") from None
        raise
