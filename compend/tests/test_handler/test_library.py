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
    async def test_reply(self, fake_context, msg_type, emoji):
        await library.emoji_reply(fake_context, "foo", msg_type)
        fake_context.message.add_reaction.assert_called_with(emoji)
        fake_context.message.reply.assert_called_with("foo")


@pytest.mark.asyncio
class TestGetHomeTitle:
    @patch("handler.library.emoji_reply")
    async def test_home_title_empty(self, mock_reply, fake_context):
        with patch("handler.library.NOTE_HOME_PAGE", {}):
            await library.get_home_title(fake_context)
            mock_reply.assert_called_once_with(
                fake_context,
                "Home page is not currently specified.",
                library.MessageType.INFO,
            )

    @patch("handler.library.emoji_reply")
    async def test_home_title_saved(self, mock_reply, fake_context):
        with patch("handler.library.NOTE_HOME_PAGE", {"foo": "bar"}):
            await library.get_home_title(fake_context)
            mock_reply.assert_called_once_with(
                fake_context,
                "Home page currently set to foo.",
                library.MessageType.INFO,
            )


@pytest.mark.asyncio
class TestTargetNoteHome:
    @patch("handler.library.get_home_title")
    async def test_no_args(self, mock_get_title, fake_context):
        await library.target_note_home(fake_context, "")
        mock_get_title.assert_called_once_with(fake_context)
