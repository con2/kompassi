from __future__ import annotations

from enum import StrEnum
from typing import Literal

import pydantic

from kompassi.dimensions.models.dimension import Dimension


class FieldType(StrEnum):
    SINGLE_LINE_TEXT = "SingleLineText"
    MULTI_LINE_TEXT = "MultiLineText"
    MARKDOWN_TEXT = "MarkdownText"
    SINGLE_CHECKBOX = "SingleCheckbox"
    TRISTATE = "Tristate"
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
    DATE_TIME_FIELD = "DateTimeField"
    DIMENSION_SINGLE_SELECT = "DimensionSingleSelect"
    DIMENSION_MULTI_SELECT = "DimensionMultiSelect"
    DIMENSION_SINGLE_CHECKBOX = "DimensionSingleCheckbox"

    @property
    def is_convertible_to_dimension(self) -> bool:
        """
        Returns True iff this field type can be converted to a dimension.
        """
        return self in (
            FieldType.SINGLE_SELECT,
            FieldType.MULTI_SELECT,
            FieldType.SINGLE_CHECKBOX,
            FieldType.TRISTATE,
        )

    @property
    def are_attachments_allowed(self) -> bool:
        """
        Returns True iff this field has the possibility of having attached files.
        """
        return self == FieldType.FILE_UPLOAD

    @property
    def can_propagate_to_annotation(self) -> bool:
        """
        Returns True iff the value of this field is a scalar string, number, date or boolean
        and can thus be passed forward to an annotation.
        """
        return self in (
            FieldType.SINGLE_LINE_TEXT,
            FieldType.MULTI_LINE_TEXT,
            FieldType.MARKDOWN_TEXT,
            FieldType.SINGLE_CHECKBOX,
            FieldType.NUMBER_FIELD,
            FieldType.DECIMAL_FIELD,
            FieldType.DATE_FIELD,
            FieldType.TIME_FIELD,
            FieldType.DATE_TIME_FIELD,
        )

    @property
    def is_dimension_field(self) -> bool:
        """
        Returns True iff this field is a dimension field.
        """
        return self in (
            FieldType.DIMENSION_SINGLE_SELECT,
            FieldType.DIMENSION_MULTI_SELECT,
            FieldType.DIMENSION_SINGLE_CHECKBOX,
        )


class Choice(pydantic.BaseModel):
    slug: str
    title: str = ""


class SingleSelectPresentation(StrEnum):
    DROPDOWN = "dropdown"
    RADIO = "radio"


BOOLEAN_CHOICES = [
    Choice(slug="true"),
    Choice(slug="false"),
]
BOOLEAN_TRANSLATIONS = {
    "true": {
        "en": "Yes",
        "fi": "Kyllä",
        "sv": "Ja",
    },
    "false": {
        "en": "No",
        "fi": "Ei",
        "sv": "Nej",
    },
}


class Field(pydantic.BaseModel, populate_by_name=True):
    """
    This Pydantic model should roughly correspond to BaseField in
    src/components/SchemaForm/models.ts of the v2 frontend. Note that
    the authoritative source is the frontend and this model is only
    provided for convenience.
    """

    type: FieldType = pydantic.Field()
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
    is_key_field: bool | None = pydantic.Field(
        default=None,
        validation_alias="isKeyField",
        serialization_alias="isKeyField",
        repr=False,
    )

    # TODO silly union of all field types. refactor this into proper (GraphQL?) types
    # dimension and subsetValues only make sense for DimensionSingleSelect, DimensionMultiSelect
    # choices only makes sense for SingleSelect, Multiselect, RadioMatrix
    # multiple only makes sense for FileUpload
    # decimal_places only makes sense for NumberField, DecimalField
    dimension: str | None = pydantic.Field(default=None, repr=False)
    subset_values: list[str] | None = pydantic.Field(
        default=None,
        validation_alias="subsetValues",
        serialization_alias="subsetValues",
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
    # max_length only makes sense for SingleLineText, MultiLineText, MarkdownText
    max_length: int | None = pydantic.Field(
        default=None,
        validation_alias="maxLength",
        serialization_alias="maxLength",
        repr=False,
    )
    # presentation only makes sense for SingleSelect
    presentation: SingleSelectPresentation | None = pydantic.Field(default=None, repr=False)

    encrypt_to: list[str] | None = pydantic.Field(
        default=None,
        validation_alias="encryptTo",
        serialization_alias="encryptTo",
        repr=False,
    )

    propagate_dimension_on_create: bool | None = pydantic.Field(
        default=None,
        validation_alias="propagateDimensionOnCreate",
        serialization_alias="propagateDimensionOnCreate",
        repr=False,
    )
    propagate_dimension_on_edit: bool | None = pydantic.Field(
        default=None,
        validation_alias="propagateDimensionOnEdit",
        serialization_alias="propagateDimensionOnEdit",
        repr=False,
    )
    propagate_to_annotation: str | None = pydantic.Field(
        default=None,
        validation_alias="propagateToAnnotation",
        serialization_alias="propagateToAnnotation",
        repr=False,
    )
    propagate_to_annotation_on_edit: bool | None = pydantic.Field(
        default=None,
        validation_alias="propagateToAnnotationOnEdit",
        serialization_alias="propagateToAnnotationOnEdit",
        repr=False,
    )

    @pydantic.model_validator(mode="after")
    def validate_propagation(self) -> Field:
        wants_dimension = self.propagate_dimension_on_create or self.propagate_dimension_on_edit
        if wants_dimension and not self.type.is_dimension_field:
            raise ValueError(f"Field {self.slug}: only Dimension* fields can propagate dimension values")

        wants_annotation = self.propagate_to_annotation or self.propagate_to_annotation_on_edit
        if wants_annotation and not self.type.can_propagate_to_annotation:
            raise ValueError(f"Field {self.slug}: {self.type} fields cannot propagate to an annotation")

        if self.propagate_to_annotation_on_edit and not self.propagate_to_annotation:
            raise ValueError(f"Field {self.slug}: propagateToAnnotationOnEdit requires propagateToAnnotation")

        return self

    @classmethod
    def from_dimension(
        cls,
        dimension: Dimension,
        type: Literal[FieldType.DIMENSION_SINGLE_SELECT, FieldType.DIMENSION_MULTI_SELECT],
        *,
        language: str | None = None,
        slug_prefix: str | None = None,
    ) -> Field:
        slug = f"{slug_prefix}.{dimension.slug}" if slug_prefix else dimension.slug

        return cls(
            slug=slug,
            type=type,
            dimension=dimension.slug,
            choices=dimension.as_choices(language=language),
        )
