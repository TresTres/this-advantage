from typing import Any, Callable, List
from discord.ui.view import View
from discord.ui import Button, Select, button
from discord import ButtonStyle, SelectOption, Interaction, Embed, Colour
from discord.utils import get


class PaginatedDropdownMenu(View):
    """
    Menu class that builds for a list of options that may exceed discord's limit of 25.
    Aside from the dropdown menu, two buttons will be shown allowing users to
    page between options menus.
    """

    options: List[SelectOption] = []
    page_index: int = 0
    page_max: int = 0
    placeholder: str = "Make a selection"
    select_menu_callback: Callable[[List[SelectOption], Interaction], None] = None

    def __init__(
        self,
        options: List[SelectOption],
        placeholder: str,
        callback: Callable[[List[SelectOption], Interaction], None] = None,
    ):
        super().__init__()
        if not options:
            raise ValueError("Dropdown menus need at least one option to render.")
        self.options = options
        self.placeholder = placeholder
        self.page_max = int((len(options) - 1) / 10)
        self.select_menu_callback = callback
        self.load_menu()

    def load_menu(self) -> None:
        """
        Loads the menu choices depending on the current page index
        """
        select_placeholder = (
            f"{self.placeholder} (page {self.page_index + 1}/{self.page_max + 1})"
        )

        menu = self.get_item("select-menu")
        if menu is None:
            menu = Select(
                options=self.options[:10],
                custom_id="select-menu",
                row=2,
                placeholder=select_placeholder,
            )

            async def callback(intxn: Interaction) -> None:
                await intxn.response.defer()
                menu.view.stop()
                menu.view.clear_items()
                if self.select_menu_callback:
                    await self.select_menu_callback(menu.values, intxn)
                else:
                    await intxn.message.reply(f"You selected {menu.values}")
                embed = Embed(
                    colour=Colour.dark_gray(),
                    type="rich",
                    description="Menu closed upon selection.",
                )
                await intxn.edit_original_response(view=menu.view, embed=embed)

            menu.callback = callback
            self.add_item(menu)

        else:
            start_range = self.page_index * 10
            end_range = start_range + 10
            menu.options = self.options[start_range:end_range]
            menu.placeholder = select_placeholder

        back_button = get(self.children, custom_id="back-page")
        forward_button = get(self.children, custom_id="forward-page")

        back_button.disabled = self.page_index == 0
        forward_button.disabled = self.page_index == self.page_max

    @button(
        custom_id="back-page",
        style=ButtonStyle.primary,
        disabled=True,
        label="Previous page",
        row=1,
    )
    async def back_callback(self, _button: Button, intxn: Interaction) -> None:
        """
        Callback for the page back button
        """
        await intxn.response.defer()
        assert self.page_index != 0
        self.page_index -= 1
        self.load_menu()
        await intxn.edit_original_response(view=self)

    @button(
        custom_id="forward-page",
        style=ButtonStyle.primary,
        disabled=True,
        label="Next page",
        row=1,
    )
    async def forward_callback(
        self,
        _button: Button,
        intxn: Interaction,
    ) -> None:
        """
        Callback for the page forward button
        """
        await intxn.response.defer()
        assert self.page_index != self.page_max
        self.page_index += 1
        self.load_menu()
        await intxn.edit_original_response(view=self)
