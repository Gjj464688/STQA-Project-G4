"""Unit regression layer: re-runs all 41 Week 2 white-box cases.

The case definitions in week2_cases.py are an unchanged copy of
02_White_Box_Coverage/tests/cases.py (SHA-256 e042b91c...). Here they run
against the helpers.py inside the supplied app folder, so a future change to
the app is checked directly. Cases linked to an open defect run as strict
expected failures.
"""
from datetime import date, datetime

import pytest

from week2_cases import CASES, NOW, TODAY

pytestmark = pytest.mark.unit

SMOKE_IDS = {"TC-WB-005", "TC-WB-006", "TC-WB-010", "TC-WB-021", "TC-WB-024", "TC-WB-031", "TC-WB-034"}

# Week 1 manual cases that exercise the same rule through the browser.
MANUAL_LINKS = {
    "TC-WB-004": ["TC-BB-006"], "TC-WB-005": ["TC-BB-007"], "TC-WB-006": ["TC-BB-007"],
    "TC-WB-009": ["TC-BB-002"], "TC-WB-010": ["TC-BB-001"], "TC-WB-011": ["TC-BB-003"],
    "TC-WB-012": ["TC-BB-004"], "TC-WB-014": ["TC-BB-005"],
    "TC-WB-020": ["TC-BB-019"], "TC-WB-021": ["TC-BB-020"], "TC-WB-022": ["TC-BB-021"],
    "TC-WB-023": ["TC-BB-022"], "TC-WB-024": ["TC-BB-023"],
}
REQUIREMENT = {
    "is_valid_password": "R-01", "is_valid_username": "R-01",
    "compute_urgency": "R-07", "completed_in_last_n_days": "R-09",
}


def _params():
    params = []
    for case in CASES:
        marks = [pytest.mark.trace(
            case["id"].replace("TC-WB", "AUTO-UNIT"),
            manual=[case["id"], *MANUAL_LINKS.get(case["id"], [])],
            req=[REQUIREMENT[case["function"]]],
        )]
        if case["id"] in SMOKE_IDS:
            marks.append(pytest.mark.smoke)
        if case["defect"]:
            marks.append(pytest.mark.known_defect(case["defect"]))
        params.append(pytest.param(case, id=case["id"], marks=marks))
    return params


@pytest.mark.parametrize("case", _params())
def test_week2_case(case, helpers_module, monkeypatch):
    if case["clock"] == "date":
        class FixedDate(date):
            @classmethod
            def today(cls):
                return TODAY
        monkeypatch.setattr(helpers_module, "date", FixedDate)
    elif case["clock"] == "datetime":
        class FixedDateTime(datetime):
            @classmethod
            def now(cls, tz=None):
                return NOW
        monkeypatch.setattr(helpers_module, "datetime", FixedDateTime)

    function = getattr(helpers_module, case["function"])
    if case["exception"]:
        with pytest.raises(Exception) as error:
            function(**case["args"])
        assert type(error.value).__name__ == case["exception"]
    else:
        actual = function(**case["args"])
        assert actual == case["expected"], (
            f"{case['id']} {case['function']}{case['args']}: "
            f"expected {case['expected']!r}, observed {actual!r}"
        )
