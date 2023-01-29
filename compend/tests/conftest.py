from unittest.mock import AsyncMock, MagicMock
import pytest

import redis
import urllib3
import discord
import notion
from handler.state_management import StateManager


@pytest.fixture(scope="function")
def fake_discord_context() -> AsyncMock:
    return AsyncMock(discord.ApplicationContext)


@pytest.fixture(scope="function")
def fake_discord_interaction() -> AsyncMock:
    return AsyncMock(discord.Interaction)


@pytest.fixture(scope="function")
def fake_discord_intxn_message() -> AsyncMock:
    return AsyncMock(discord.InteractionMessage)


@pytest.fixture(scope="function")
def fake_http_response() -> MagicMock:
    return MagicMock(urllib3.HTTPResponse)


@pytest.fixture(scope="function")
def fake_notion_page_object() -> MagicMock:
    return MagicMock(notion.data_types.PageObject)


@pytest.fixture(scope="function")
def fake_redis_client() -> MagicMock:
    return MagicMock(redis.Redis)


@pytest.fixture(scope="function")
def fake_state_manager() -> MagicMock:
    return MagicMock(StateManager)
