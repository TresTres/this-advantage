from unittest.mock import call, patch
import pytest
from handler import library


@pytest.mark.asyncio
class TestEmojiReply:
    
    @pytest.fixture(scope="function", autouse=True)
    def setup_fixtures(self, fake_discord_context, fake_discord_interaction, fake_discord_intxn_message):
        self.context = fake_discord_context
        self.interaction = fake_discord_interaction
        self.message = fake_discord_intxn_message
        self.context.respond.return_value = self.interaction
        self.interaction.original_response.return_value = self.message

    
    @pytest.mark.parametrize(
        "msg_type, emoji",
        [
            (library.MessageType.FAIL, "❌"),
            (library.MessageType.SUCCESS, "✅"),
            (library.MessageType.INFO, "ℹ️"),
        ],
    )
    async def test_reply(self, msg_type, emoji):
        await library.emoji_reply(self.context, "foo", msg_type)
        self.context.respond.assert_called_once_with("foo")
        self.interaction.original_response.assert_called_once()
        self.message.add_reaction.assert_called_once_with(emoji)
        
        
    async def test_reply_with_other_emojis(self):
        await library.emoji_reply(self.context, "foo", library.MessageType.INFO, ["💰", "🗑"])
        self.message.add_reaction.assert_has_calls([call("ℹ️"), call("🗑"), call("💰")], any_order=True)   
        

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
        self, mock_reply, fake_discord_context, fake_notion_page_object
    ):
        with patch("handler.library.NOTE_HOME_PAGE", fake_notion_page_object):
            fake_notion_page_object.page_title = "foo"
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
