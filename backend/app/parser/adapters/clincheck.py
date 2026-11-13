from app.parser.adapters.base import SourceAdapter

# Only negative context checks supported by the supplied audit. No direction/axis/tooth maps.
CLINCHECK = SourceAdapter("clincheck-candidate", "ClinCheck", frozenset({"CUSP_TIP"}))
