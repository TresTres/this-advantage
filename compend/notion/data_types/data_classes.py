from typing import Dict, List, Optional, Union
import unicodedata
from pydantic import BaseModel
from notion.data_types.type_enums import RTOType, PropertyType, BlockType


class TextObject(BaseModel):
    content: str
    link: Optional[dict]


class RichTextObject(BaseModel):
    type: RTOType
    text: TextObject
    plain_text: str
    href: Optional[str]


class TextContentMixin(BaseModel):

    rich_text: List[RichTextObject]
    color: str

    @property
    def text_content(self) -> str:
        content = "".join(t.plain_text for t in self.rich_text)
        return unicodedata.normalize("NFKD", content)


class PropertyObject(BaseModel):
    id: str
    type: PropertyType


class TitleObject(PropertyObject):
    title: List[RichTextObject]

    def get_full_title(self) -> str:
        return "".join([t.plain_text for t in self.title])


class HeadingObject(TextContentMixin):
    is_toggleable: bool


class ParagraphObject(TextContentMixin):
    children: Optional[List["BlockObject"]]


class ChildPageObject(BaseModel):
    title: str


class BlockObject(BaseModel):
    object: str = "block"
    id: str
    type: BlockType
    has_children: bool
    child_page: Optional[ChildPageObject]
    heading_1: Optional[HeadingObject]
    heading_2: Optional[HeadingObject]
    heading_3: Optional[HeadingObject]
    paragraph: Optional[ParagraphObject]

    @property
    def active_heading(self):
        return self.heading_1 or self.heading_2 or self.heading_3 or None


class PageObject(BaseModel):
    object: str = "page"
    id: str
    properties: Dict[str, Union[TitleObject, PropertyObject]]
    url: str

    @property
    def page_title(self) -> str:
        if "title" not in self.properties:
            raise ValueError(f"Page {self.url} does not contain a title")
        return self.properties["title"].get_full_title()


__all__ = ["PageObject", "BlockObject"]
