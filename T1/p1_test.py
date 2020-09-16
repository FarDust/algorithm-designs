import pytest
from p1 import calc_substrings

valid_strings = [("909", 6), ("36", 3), ("21008", 7)]


@pytest.mark.parametrize("test_input,expected", valid_strings)
def test_correctness(test_input, expected):
    assert calc_substrings(test_input) == expected
