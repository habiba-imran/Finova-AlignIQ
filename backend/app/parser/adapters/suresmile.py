from app.parser.adapters.base import SourceAdapter

SURESMILE = SourceAdapter(
    "suresmile-candidate", "SureSmile", frozenset({"VIRTUAL_ROOT_APEX"}),
    frozenset({"ALIGN_FINAL", "DOCTOR_FINAL"}),
)
