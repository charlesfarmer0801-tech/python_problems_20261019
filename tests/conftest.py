"""Friendly result checker shared by every assignment's test cases."""
import math
import pytest


def _describe(value):
    try:
        representation = repr(value)
    except Exception:
        representation = "<value could not be displayed>"
    if len(representation) > 150:
        representation = representation[:147] + "..."
    return f"{representation} ({type(value).__name__})"


def _hint(actual, expected):
    if actual is None:
        return "Your function returned None. Check that all paths return an answer."
    if type(actual) is not type(expected) and not (
        isinstance(actual, (int, float)) and not isinstance(actual, bool)
        and isinstance(expected, (int, float)) and not isinstance(expected, bool)
    ):
        return "Check the required return type. A correct value in the wrong type does not match."
    if isinstance(expected, str):
        return "Check the exact text, capitalization, spaces, and number formatting."
    if isinstance(expected, list):
        return "Check the list's values, length, and order."
    if isinstance(expected, bool):
        return "Check the comparison and whether the boundary should count as equal."
    if isinstance(expected, (int, float)):
        return "Review the calculation, order of operations, and any rounding requirements."
    return "Compare your return value with the problem's required output format."


@pytest.fixture
def verify_output():
    def verify(actual, expected):
        if (isinstance(actual, (int, float)) and not isinstance(actual, bool)
            and isinstance(expected, (int, float)) and not isinstance(expected, bool)):
            matches = math.isclose(actual, expected, rel_tol=1e-9, abs_tol=1e-9)
        else:
            matches = (type(actual) is type(expected) and actual == expected)
        if not matches:
            raise AssertionError(
                f"Expected: {_describe(expected)}\n"
                f"Received: {_describe(actual)}\n"
                f"Hint: {_hint(actual, expected)}"
            )
    return verify
