# TODO: not sure if the current version of Pydantic would allow new-style annotations
# ruff: noqa: UP007
from enum import Enum
from typing import TYPE_CHECKING, Literal, Optional

import pydantic

if TYPE_CHECKING:
    from .dimension import Dimension


class FieldType(str, Enum):
    SINGLE_LINE_TEXT = "SingleLineText"
    MULTI_LINE_TEXT = "MultiLineText"
    SINGLE_CHECKBOX = "SingleCheckbox"
    STATIC_TEXT = "StaticText"
    DIVIDER = "Divider"
    SPACER = "Spacer"
    SINGLE_SELECT = "SingleSelect"
    MULTI_SELECT = "MultiSelect"
    RADIO_MATRIX = "RadioMatrix"


class Choice(pydantic.BaseModel):
    slug: str
    title: str


class Field(pydantic.BaseModel):
    """
    This Pydantic model should roughly correspond to BaseField in
    src/components/SchemaForm/models.ts of the v2 frontend. Note that
    the authoritative source is the frontend and this model is only
    provided for convenience.
    """

    type: FieldType = pydantic.Field(alias="type", repr=False)
    slug: str = pydantic.Field(alias="slug")
    title: Optional[str] = pydantic.Field(default=None, alias="title", repr=False)
    summary_title: Optional[str] = pydantic.Field(default=None, alias="summaryTitle", repr=False)
    help_text: Optional[str] = pydantic.Field(default=None, alias="helpText", repr=False)
    required: Optional[bool] = pydantic.Field(default=None, alias="required", repr=False)
    read_only: Optional[bool] = pydantic.Field(default=None, alias="readOnly", repr=False)
    html_type: Optional[str] = pydantic.Field(default=None, alias="htmlType", repr=False)
    choices: Optional[list[Choice]] = pydantic.Field(default=None, alias="choices", repr=False)
    questions: Optional[list[Choice]] = pydantic.Field(default=None, alias="questions", repr=False)

    @classmethod
    def from_dimension(
        cls,
        dimension: "Dimension",
        type: Literal[FieldType.SINGLE_SELECT] | Literal[FieldType.MULTI_SELECT],
    ) -> "Field":
        return cls(
            slug=dimension.slug,
            type=type,
            choices=dimension.get_choices(),
        )

    class Config:
        populate_by_field_name = True
