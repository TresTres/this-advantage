# handler.library
import asyncio
from strenum import StrEnum
import logging
from typing import List
from discord import ApplicationContext, SelectOption, Interaction

from notion.data_types import PageObject, BlockType
import notion.api as notion
from views.menu import PaginatedDropdownMenu
import utils.logging as lg

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lg.attach_stdout_handler(logger)


NOTE_HOME_PAGE: PageObject = None
NOTE_SESSION_PAGE: PageObject = None


MessageType = StrEnum("MessageType", ["FAIL", "SUCCESS", "INFO"])

async def emoji_reply(ctx: ApplicationContext, reply: str, msg_type: MessageType, additional_emojis: List[str] = None) -> None:
    """
    Reply to a message with an emoji and the attached reply content.
    If this is the first reply, it is treated as an interaction, otherwise it's treated as a webhook message.
    """
    if additional_emojis is None:
        additional_emojis = []
    emoji_lib = {
        MessageType.FAIL: "❌",
        MessageType.SUCCESS: "✅",
        MessageType.INFO: "ℹ️",
    }
    emoji = emoji_lib[msg_type]
    logger.info(f"{emoji} replying with: {reply}")
    response = await ctx.respond(reply)
    if isinstance(response, Interaction):
        response = await response.original_response()
    await response.add_reaction(emoji)
    if additional_emojis:
        asyncio.gather(*[response.add_reaction(eji) for eji in additional_emojis])
        


async def get_home_title(ctx: ApplicationContext) -> None:
    """
    Attempts to retrieve the title of the NOTE_HOME_PAGE
    TODO: This is something that should be stored in external memory
    """
    if not NOTE_HOME_PAGE:
        await emoji_reply(
            ctx, "Home page is not currently specified.", MessageType.INFO
        )
        return
    await emoji_reply(
        ctx,
        f"Home page currently set to {NOTE_HOME_PAGE.page_title}.",
        MessageType.INFO,
    )
    return


async def target_note_home(ctx: ApplicationContext, target_url: str) -> None:
    """
    Defines the NOTE_HOME_PAGE global using the sent url if not yet defined
    TODO: This is something that should be stored in external memory, not global vars
    """
    global NOTE_HOME_PAGE
    if not target_url:
        await get_home_title(ctx)
        return
    try:
        page_object = await notion.get_page_object_for_url(target_url)
        page_title = page_object.page_title
        NOTE_HOME_PAGE = page_object
        await emoji_reply(ctx, f"Home page set to {page_title}.", MessageType.SUCCESS, ["🏠"])
    except ValueError as ve:
        await emoji_reply(ctx, str(ve), MessageType.FAIL)
    except notion.FailedRequestException as re:
        await emoji_reply(ctx, str(re), MessageType.FAIL, ["📡"])
    except notion.FailedURLParseException as ue:
        await emoji_reply(ctx, str(ue), MessageType.FAIL, ["🔤"])


async def get_session_title(ctx: ApplicationContext) -> None:
    """
    Attempts to retrieve the title of the NOTE_SESSION_PAGE
    TODO: This is something that should be stored in external memory
    """
    if not NOTE_SESSION_PAGE:
        await emoji_reply(ctx, "Session is not currently specified.", MessageType.INFO)
        return
    await emoji_reply(
        ctx,
        f"Session currently set to {NOTE_SESSION_PAGE.page_title}.",
        MessageType.INFO,
    )
    return


async def target_session_page(ctx: ApplicationContext) -> None:
    """
    Using the current note home page, creates a dropdown menu for the user to select a session page from.
    TODO: This is something that should be stored in external memory
    """
    try:
        if not NOTE_HOME_PAGE:
            raise ValueError(
                "Need to specify the note page via /home <target_url> before selecting a session page."
            )
        children = await notion.get_children_by_type(
            NOTE_HOME_PAGE.id, BlockType.child_page
        )
        sorted_children = sorted(children, key=lambda c: c.child_page.title)
        options = [SelectOption(label = c.child_page.title, value=c.id) for c in sorted_children]
        async def menu_callback(selections: List[SelectOption], intxn: Interaction) -> None:
            global NOTE_SESSION_PAGE
            NOTE_SESSION_PAGE = await notion.get_page_object_for_id(selections[0])
            title = NOTE_SESSION_PAGE.page_title
            await emoji_reply(ctx, f"Session page set to {title}", MessageType.SUCCESS, ["📓"])
        view = PaginatedDropdownMenu(options=options, placeholder="Choose a session page", callback=menu_callback)
        await ctx.respond(view=view)
    except ValueError as ve:
        await emoji_reply(ctx, str(ve), MessageType.FAIL)
    except notion.FailedRequestException as re:
        await emoji_reply(ctx, str(re), MessageType.FAIL, ["📡"])
    except notion.FailedURLParseException as ue:
        await emoji_reply(ctx, str(ue), MessageType.FAIL, ["🔤"])
