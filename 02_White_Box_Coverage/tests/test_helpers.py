"""Final specification and robustness cases; known defects remain real failures."""
import pytest
from cases import CASES


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["id"])
def test_helper_case(case, check_case):
    check_case(case)
