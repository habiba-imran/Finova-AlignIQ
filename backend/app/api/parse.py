from fastapi import APIRouter

from app.domain.models import ParseResult, RawTMTSubmission
from app.parser.service import parse_table

router = APIRouter()


@router.post("/api/parse", response_model=ParseResult)
def parse_submission(submission: RawTMTSubmission) -> ParseResult:
    return parse_table(submission)
