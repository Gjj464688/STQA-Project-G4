"""Load the preserved source and freeze only its clock dependencies in memory."""
import importlib.util
from datetime import date, datetime
from pathlib import Path

import pytest
from cases import TODAY, NOW


@pytest.fixture(scope="session")
def helper_module():
    source = Path(__file__).resolve().parents[1] / "target" / "helpers.py"
    spec = importlib.util.spec_from_file_location("pytodo_week2_helpers", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def check_case(helper_module, monkeypatch, request):
    def check(case):
        if case["clock"] == "date":
            class FixedDate(date):
                @classmethod
                def today(cls):
                    return TODAY
            monkeypatch.setattr(helper_module, "date", FixedDate)
        elif case["clock"] == "datetime":
            class FixedDateTime(datetime):
                @classmethod
                def now(cls, tz=None):
                    return NOW
            monkeypatch.setattr(helper_module, "datetime", FixedDateTime)

        try:
            actual = getattr(helper_module, case["function"])(**case["args"])
            exception = None
        except Exception as error:
            actual = None
            exception = type(error).__name__
        request.node.week2_result = dict(
            case_id=case["id"], actual=actual, exception=exception,
            expected=case["expected"], expected_exception=case["exception"],
            defect=case["defect"], basis=case["basis"],
        )
        assert exception == case["exception"], f"Unexpected exception outcome: {exception}"
        if case["exception"] is None:
            assert actual == case["expected"], (
                f"{case['id']} {case['function']}: expected {case['expected']!r}, "
                f"observed {actual!r}; specification basis: {case['basis']}"
            )
    return check
