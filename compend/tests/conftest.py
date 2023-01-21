from unittest.mock import AsyncMock
import pytest

import discord
from discord.ext import commands


@pytest.fixture(scope="function")
def fake_context() -> AsyncMock:
    ctx = AsyncMock(commands.Context)
    ctx.message = AsyncMock(discord.Message)

    return ctx
