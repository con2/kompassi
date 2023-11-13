from enum import Enum
from typing import Optional

import pydantic


class FieldType(Enum):
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

    type: FieldType = pydantic.Field(alias="type")
    slug: str = pydantic.Field(alias="slug")
    title: Optional[str] = pydantic.Field(None, alias="title")
    help_text: Optional[str] = pydantic.Field(None, alias="helpText")
    required: Optional[bool] = pydantic.Field(None, alias="required")
    read_only: Optional[bool] = pydantic.Field(None, alias="readOnly")
    html_type: Optional[str] = pydantic.Field(None, alias="htmlType")
    choices: Optional[list[Choice]] = pydantic.Field(None, alias="choices")
    questions: Optional[list[Choice]] = pydantic.Field(None, alias="questions")

    class Config:
        allow_population_by_field_name = True
