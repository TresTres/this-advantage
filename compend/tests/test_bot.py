import bot
import pytest

class FakeMessage():
    
    content: str
    
    def __init__(self, msg: str):
        self.content = msg


