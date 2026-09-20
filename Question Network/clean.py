"""Shim so notebooks in this folder can `from clean import ...` unchanged.

The real module lives at the repository root; this file just loads it from there,
so there is only ever one copy of the cleaning logic.
"""

import importlib.util as _util
from pathlib import Path as _Path

_source = _Path(__file__).resolve().parent.parent / "clean.py"
_spec = _util.spec_from_file_location("_clean_impl", _source)
_impl = _util.module_from_spec(_spec)
_spec.loader.exec_module(_impl)

CSV_PATH = _impl.CSV_PATH
LIKERT = _impl.LIKERT
SECTIONS = _impl.SECTIONS
load_survey = _impl.load_survey
section_of = _impl.section_of
