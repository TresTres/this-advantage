from unittest.mock import AsyncMock, MagicMock
import pytest

import urllib3
import discord


import notion


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
