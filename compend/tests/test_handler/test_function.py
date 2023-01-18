import pytest
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, patch

from handler import function



class TestCommandParse(IsolatedAsyncioTestCase):
    
    @patch("discord.Message", new_callable=AsyncMock)
    async def test_parse_invalid(self, mock_message):
        await function.parse_command("%&%^&askdf", mock_message)
        mock_message.add_reaction.assert_called_once_with("❌")
        mock_message.reply.assert_called_once_with("Command format is invalid (must start with '?' or '!')")



class TestCommandExecute(IsolatedAsyncioTestCase):
    
    mock_function = AsyncMock(return_value="bar")
    FAKE_FUNCTIONS = {
        "foo": mock_function
    }

    @patch("discord.Message", new_callable=AsyncMock)
    async def test_handle_command_invalid(self, mock_message):
        await function.execute_command_from_table(self.FAKE_FUNCTIONS, "baz", mock_message)
        mock_message.add_reaction.assert_called_once_with("❌")
        mock_message.reply.assert_called_once_with("Command baz is not recognized.")


    @patch("discord.Message", new_callable=AsyncMock)
    async def test_handle_command_valid(self, mock_message):
        await function.execute_command_from_table(self.FAKE_FUNCTIONS, "foo", mock_message)
        self.mock_function.assert_called_once_with(mock_message)


