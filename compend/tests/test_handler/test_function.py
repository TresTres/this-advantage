import pytest 
from unittest.mock import AsyncMock, patch
import discord

from handler import function

@pytest.mark.asyncio 
@patch('discord.Message', new_callable=AsyncMock)
async def test_handle_command_invalid(mock_message):
    await function.handle_command("!foo", mock_message)
    mock_message.add_reaction.assert_called_once_with("❌")
    mock_message.reply.assert_called_once_with("Command !foo is invalid.")
    
@pytest.mark.asyncio 
@patch('handler.function.handle_quote')
@patch('discord.Message', new_callable=AsyncMock)
async def test_handle_command_valid(mock_message, mock_handler):
    with patch.dict('handler.function.LIBRARY', {'foo': mock_handler}):
        await function.handle_command("!foo", mock_message)
    mock_handler.assert_called_once_with(mock_message)
