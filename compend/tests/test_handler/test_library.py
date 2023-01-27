from unittest.mock import patch
import pytest
from handler import library


@pytest.mark.asyncio
class TestEmojiReply:
    @pytest.mark.parametrize(
        "msg_type, emoji",
        [
            (library.MessageType.FAIL, "❌"),
            (library.MessageType.SUCCESS, "✅"),
            (library.MessageType.INFO, "ℹ️"),
        ],
    )
    async def test_reply(self, fake_discord_context, msg_type, emoji):
        await library.emoji_reply(fake_discord_context, "foo", msg_type)
        fake_discord_context.message.add_reaction.assert_called_with(emoji)
        fake_discord_context.message.reply.assert_called_with("foo")


@pytest.mark.asyncio
class TestGetHomeTitle:
    @patch("handler.library.emoji_reply")
    async def test_home_title_empty(self, mock_reply, fake_discord_context):
        with patch("handler.library.NOTE_HOME_PAGE", None):
            await library.get_home_title(fake_discord_context)
            mock_reply.assert_called_once_with(
                fake_discord_context,
                "Home page is not currently specified.",
                library.MessageType.INFO,
            )

    @patch("handler.library.emoji_reply")
    async def test_home_title_saved(
        self, mock_reply, fake_discord_context, fake_page_object
    ):
        with patch("handler.library.NOTE_HOME_PAGE", fake_page_object):
            fake_page_object.page_title = "foo"
            await library.get_home_title(fake_discord_context)
            mock_reply.assert_called_once_with(
                fake_discord_context,
                "Home page currently set to foo.",
                library.MessageType.INFO,
            )


@pytest.mark.asyncio
class TestTargetNoteHome:
    @patch("handler.library.get_home_title")
    async def test_no_args(self, mock_get_title, fake_discord_context):
        await library.target_note_home(fake_discord_context, "")
        mock_get_title.assert_called_once_with(fake_discord_context)
