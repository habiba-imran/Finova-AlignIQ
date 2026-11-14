"""Ephemeral lexical parsing and draft descriptive review. Clinical predicates disabled."""

from typing import Literal

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel

from app.api.parse import router
from app.api.review import router as review_router
from app.api.reports import router as reports_router
from app.api.automatic_parse import router as automatic_parse_router
from app.api.planning import router as planning_router
from app.api.attachments import router as attachments_router
from app.api.sequencing import router as sequencing_router
from app.api.privacy import PrivateIntakeMiddleware, private_validation_error

app = FastAPI(
    title="Finova AlignIQ",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)
app.add_middleware(PrivateIntakeMiddleware)
app.add_exception_handler(RequestValidationError, private_validation_error)
app.include_router(router)
app.include_router(review_router)
app.include_router(reports_router)
app.include_router(automatic_parse_router)
app.include_router(planning_router)
app.include_router(attachments_router)
app.include_router(sequencing_router)


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    service: Literal["finova-aligniq"] = "finova-aligniq"
    phase: Literal[1] = 1


@app.get("/api/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse()
