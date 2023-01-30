# handler.library
import asyncio
from strenum import StrEnum
import logging
from typing import List
from discord import ApplicationContext, SelectOption, Interaction, Embed

from notion.data_types import BlockType
import notion.api as notion
from handler.state_management import StateManager
from views.menu import PaginatedDropdownMenu
import utils.logging as lg

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lg.attach_stdout_handler(logger)


MessageType = StrEnum("MessageType", ["FAIL", "SUCCESS", "INFO"])


async def emoji_reply(
    ctx: ApplicationContext,
    reply: str,
    msg_type: MessageType,
    additional_emojis: List[str] = None,
) -> None:
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


async def get_home_title(ctx: ApplicationContext, manager: StateManager) -> None:
    """
    Attempts to retrieve the title of the note home page
    """
    home_page = await manager.get_page(ctx.guild_id, "home")
    if not home_page:
        await emoji_reply(
            ctx, "Home page is not currently specified.", MessageType.INFO
        )
        return
    await emoji_reply(
        ctx,
        f"Home page currently set to {home_page.page_title}.",
        MessageType.INFO,
    )
    return


async def target_note_home(
    ctx: ApplicationContext, manager: StateManager, target_url: str
) -> None:
    """
    Defines the note home page using the sent url if not yet defined
    """
    if not target_url:

        await get_home_title(ctx, manager)
        return
    try:
        page_object = await notion.get_page_object_for_url(target_url)
        manager.save_page(ctx.guild_id, "home", page_object)
        page_title = page_object.page_title
        await emoji_reply(
            ctx, f"Home page set to {page_title}.", MessageType.SUCCESS, ["🏠"]
        )
    except ValueError as ve:
        await emoji_reply(ctx, str(ve), MessageType.FAIL)
    except notion.FailedRequestException as re:
        await emoji_reply(ctx, str(re), MessageType.FAIL, ["📡"])
    except notion.FailedURLParseException as ue:
        await emoji_reply(ctx, str(ue), MessageType.FAIL, ["🔤"])




async def get_session_info(ctx: ApplicationContext, manager: StateManager, full_info: bool) -> None:
    """
    Attempts to retrieve summary info of the note session page.
    """
    session_page = await manager.get_page(ctx.guild_id, "session")
    if not session_page:
        await emoji_reply(ctx, "No session set.  Need to specify a session page via /page session.", MessageType.FAIL)
        return
    
    if not full_info:
        await emoji_reply(
            ctx,
            f"Session currently set to {session_page.page_title}.",
            MessageType.INFO,
        )
        return
    children = await notion.get_children(session_page.id)
    elements = children.get_all_under_header("Summary")
    text_content = [e.paragraph.text_content for e in elements]
    embed = Embed(type='rich', title=session_page.page_title, description=text_content[0])
    await ctx.respond(embed=embed)


async def target_session_page(ctx: ApplicationContext, manager: StateManager) -> None:
    """
    Using the current note home page, creates a dropdown menu for the user to select a session page from.
    """
    home_page = await manager.get_page(ctx.guild_id, "home")
    try:
        if not home_page:
            raise ValueError(
                "Need to specify the note page via /page home <target_url> before selecting a session page."
            )
        children = await notion.get_children_by_type(home_page.id, BlockType.child_page)
        sorted_children = sorted(children, key=lambda c: c.child_page.title)
        options = [
            SelectOption(label=c.child_page.title, value=c.id) for c in sorted_children
        ]

        async def menu_callback(
            selections: List[SelectOption], _intxn: Interaction
        ) -> None:
            session_page = await notion.get_page_object_for_id(selections[0])
            manager.save_page(ctx.guild_id, "session", session_page)
            title = session_page.page_title
            await emoji_reply(
                ctx, f"Session page set to {title}", MessageType.SUCCESS, ["📓"]
            )

        view = PaginatedDropdownMenu(
            options=options, placeholder="Choose a session page", callback=menu_callback
        )
        await ctx.respond(view=view)
    except ValueError as ve:
        await emoji_reply(ctx, str(ve), MessageType.FAIL)
    except notion.FailedRequestException as re:
        await emoji_reply(ctx, str(re), MessageType.FAIL, ["📡"])
    except notion.FailedURLParseException as ue:
        await emoji_reply(ctx, str(ue), MessageType.FAIL, ["🔤"])
