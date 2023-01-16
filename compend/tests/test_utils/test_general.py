import pytest
from utils import general


@pytest.mark.parametrize(
    "test_str,expected_tuple",
    [
        ("", ("", "")),
        ("hello", ("hello", "")),
        ("foo bar   baz", ("foo", "bar   baz")),
    ]
)
def test_split_content(test_str, expected_tuple):
    
    assert general.split_first_token(test_str) == expected_tuple