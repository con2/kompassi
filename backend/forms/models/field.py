from __future__ import annotations

from enum import Enum
from typing import Literal

import pydantic

from dimensions.models.dimension import Dimension


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
    FILE_UPLOAD = "FileUpload"
    NUMBER_FIELD = "NumberField"
    DECIMAL_FIELD = "DecimalField"
    DATE_FIELD = "DateField"
    TIME_FIELD = "TimeField"
    DATE_TIME_FIELD = "DateField"


class Choice(pydantic.BaseModel):
    slug: str
    title: str = ""


class Field(pydantic.BaseModel, populate_by_name=True):
    """
    This Pydantic model should roughly correspond to BaseField in
    src/components/SchemaForm/models.ts of the v2 frontend. Note that
    the authoritative source is the frontend and this model is only
    provided for convenience.
    """

    type: FieldType = pydantic.Field(repr=False)
    slug: str = pydantic.Field()
    title: str | None = pydantic.Field(default=None, repr=False)
    summary_title: str | None = pydantic.Field(
        default=None,
        validation_alias="summaryTitle",
        serialization_alias="summaryTitle",
        repr=False,
    )
    help_text: str | None = pydantic.Field(
        default=None,
        validation_alias="helpText",
        serialization_alias="helpText",
        repr=False,
    )
    required: bool | None = pydantic.Field(
        default=None,
        validation_alias="required",
        serialization_alias="required",
        repr=False,
    )
    read_only: bool | None = pydantic.Field(
        default=None,
        validation_alias="readOnly",
        serialization_alias="readOnly",
        repr=False,
    )

    # TODO silly union of all field types. refactor this into proper (GraphQL?) types
    # htmlType only makes sense for SingleLineText
    # choices only makes sense for SingleSelect, Multiselect, RadioMatrix
    # multiple only makes sense for FileUpload
    # decimal_places only makes sense for NumberField, DecimalField
    html_type: str | None = pydantic.Field(
        default=None,
        validation_alias="htmlType",
        serialization_alias="htmlType",
        repr=False,
    )

    choices: list[Choice] | None = pydantic.Field(default=None, repr=False)
    questions: list[Choice] | None = pydantic.Field(default=None, repr=False)
    multiple: bool | None = pydantic.Field(default=None, repr=False)
    decimal_places: int | None = pydantic.Field(
        default=None,
        validation_alias="decimalPlaces",
        serialization_alias="decimalPlaces",
        repr=False,
    )
    encrypt_to: list[str] | None = pydantic.Field(
        default=None,
        validation_alias="encryptTo",
        serialization_alias="encryptTo",
        repr=False,
    )

    @classmethod
    def from_dimension(
        cls,
        dimension: Dimension,
        type: Literal[FieldType.SINGLE_SELECT] | Literal[FieldType.MULTI_SELECT],
        language: str | None = None,
    ) -> Field:
        return cls(
            slug=dimension.slug,
            type=type,
            choices=dimension.as_choices(language=language),
        )
