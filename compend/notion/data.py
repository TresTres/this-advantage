from strenum import StrEnum
from typing import Dict, List, Optional, Union
from pydantic import BaseModel

RTOType = StrEnum("RTOType", ["text", "mention", "equation"])
PropertyType = StrEnum(
    "PropertyType",
    [
        "rich_text",
        "number",
        "select",
        "multi_select",
        "status",
        "date",
        "formula",
        "relation",
        "rollup",
        "title",
        "people",
        "files",
        "checkbox",
        "url",
        "email",
        "phone_number",
        "created_time",
        "created_by",
        "last_edited_time",
        "last_edited_by",
    ],
)


class TextObject(BaseModel):
    content: str
    link: Optional[dict]


class RichTextObject(BaseModel):
    type: RTOType
    text: TextObject
    plain_text: str
    href: Optional[str] 


class PropertyObject(BaseModel):
    id: str
    type: PropertyType

class TitleObject(PropertyObject):
    title: List[RichTextObject]
    
    def get_full_title(self) -> str: 
        return "".join([t.plain_text for t in self.title])

class PageObject(BaseModel):
    object: str = "page"
    id: str
    properties: Dict[str, Union[TitleObject, PropertyObject]]
    url: str
    
    @property
    def page_title(self) -> str:
        if 'title' not in self.properties:
            raise ValueError(f"Page {self.url} does not contain a title")
        return self.properties['title'].get_full_title()

