from unittest.mock import AsyncMock, MagicMock
import pytest

import urllib3
import discord
from discord.ext import commands


@pytest.fixture(scope="function")
def fake_discord_context() -> AsyncMock:
    ctx = AsyncMock(commands.Context)
    ctx.message = AsyncMock(discord.Message)
    return ctx

@pytest.fixture(scope="function")
def fake_http_response() -> MagicMock:
    return MagicMock(urllib3.HTTPResponse)
