"""Deliberately limited starting suite, preserved for the coverage comparison."""
import pytest
from cases import CASES, BASELINE_IDS


@pytest.mark.parametrize("case", [c for c in CASES if c["id"] in BASELINE_IDS],
                         ids=lambda case: case["id"])
def test_baseline_helper_case(case, check_case):
    check_case(case)
