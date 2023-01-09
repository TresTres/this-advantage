import bot
import pytest

class FakeMessage():
    
    content: str
    
    def __init__(self, msg: str):
        self.content = msg



@pytest.mark.parametrize(
    "test_msg,expected_tuple",
    [
        ("", ("", "")),
        ("hello", ("hello", "")),
        ("foo bar   baz", ("foo", "bar baz"))
    ]
)
def test_split_content(test_msg, expected_tuple):
    msg = FakeMessage(test_msg)
    assert bot.split_content(msg) == expected_tuple