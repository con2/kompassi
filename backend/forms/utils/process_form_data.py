"""
Contains the `process_form_data` function which processes a form's data
in the form of `Object.fromEntries(formData.entries())` into a more
manageable format. Other things in this file are part of that function's
implementation.

NOTE: The exact semantics of `process_form_data` are defined by and documented in
`forms/tests.py:test_process_form_data`.
"""

import decimal
from collections.abc import Sequence
from enum import Enum
from typing import Any

from core.utils.model_utils import slugify

from ..models.field import Field, FieldType
from .s3_presign import is_valid_s3_url, presign_get


class FieldWarning(Enum):
    INVALID_CHOICE = "InvalidChoice"
    REQUIRED_MISSING = "RequiredMissing"
    INVALID_VALUE = "InvalidValue"
    UNKNOWN_FIELD_TYPE = "UnknownFieldType"


FALSY_VALUES = ("false", "0", "off", "no")

# sentinels
VALUE_MISSING = object()
INVALID_VALUE = object()


class FieldProcessor:
    def extract_value(self, field: Field, form_data: dict[str, Any]) -> Any:
        return form_data.get(field.slug, "")

    def validate_value(self, field: Field, value: Any) -> list[FieldWarning]:
        warnings = []

        if not isinstance(value, str):
            warnings.append(FieldWarning.INVALID_VALUE)

        if field.required and not value:
            warnings.append(FieldWarning.REQUIRED_MISSING)

        return warnings


class NullFieldProcessor(FieldProcessor):
    def extract_value(self, field: Field, form_data: dict[str, Any]) -> Any:
        return VALUE_MISSING

    def validate_value(self, field: Field, value: Any) -> list[FieldWarning]:
        return []


class NumberFieldProcessor(FieldProcessor):
    def extract_value(self, field: Field, form_data: dict[str, Any]) -> Any:
        value = form_data.get(field.slug, "")

        if not value:
            return VALUE_MISSING

        try:
            if field.decimal_places is not None and field.decimal_places > 0:
                return float(value)
            return int(value)
        except ValueError:
            return INVALID_VALUE

    def validate_value(self, field: Field, value: Any) -> list[FieldWarning]:
        warnings = []

        if field.required and value is VALUE_MISSING:
            warnings.append(FieldWarning.REQUIRED_MISSING)

        if value is INVALID_VALUE:
            warnings.append(FieldWarning.INVALID_VALUE)

        return warnings


class DecimalFieldProcessor(FieldProcessor):
    def extract_value(self, field: Field, form_data: dict[str, Any]) -> Any:
        value = form_data.get(field.slug, "")

        if not value:
            return VALUE_MISSING

        try:
            # It would be nice to keep this as decimal until it is serialized as JSON
            dec = decimal.Decimal(value)
            if field.decimal_places is not None and field.decimal_places > 0:
                dec = dec.quantize(decimal.Decimal(f"0.{'0' * field.decimal_places}"))
            return str(dec)
        except decimal.InvalidOperation:
            return INVALID_VALUE

    def validate_value(self, field: Field, value: Any) -> list[FieldWarning]:
        warnings = []

        if field.required and value is VALUE_MISSING:
            warnings.append(FieldWarning.REQUIRED_MISSING)
        elif value is INVALID_VALUE:
            warnings.append(FieldWarning.INVALID_VALUE)
        else:
            try:
                decimal.Decimal(value)
            except (decimal.InvalidOperation, TypeError):
                warnings.append(FieldWarning.INVALID_VALUE)

        return warnings


class SingleCheckboxFieldProcessor(FieldProcessor):
    def extract_value(self, field: Field, form_data: dict[str, Any]):
        value: str = form_data.get(field.slug, "")
        return bool(value and value.strip().lower() not in FALSY_VALUES)

    def validate_value(self, field: Field, value: Any) -> list[FieldWarning]:
        warnings = []

        if field.required and not value:
            warnings.append(FieldWarning.REQUIRED_MISSING)

        return warnings


class SingleSelectFieldProcessor(FieldProcessor):
    def validate_value(self, field: Field, value: Any) -> list[FieldWarning]:
        warnings = super().validate_value(field, value)

        if value and value not in [choice.slug for choice in field.choices or []]:
            warnings.append(FieldWarning.INVALID_CHOICE)

        return warnings


class DimensionSingleSelectFieldProcessor(SingleSelectFieldProcessor):
    def extract_value(self, field: Field, form_data: dict[str, Any]) -> Any:
        value = super().extract_value(field, form_data)

        if value and isinstance(value, str):
            return slugify(value)

        return value


class MultiSelectFieldProcessor(FieldProcessor):
    def extract_value(self, field: Field, form_data: dict[str, Any]):
        field_slug_dot = f"{field.slug}."
        return [
            key.removeprefix(field_slug_dot)
            for key, value in form_data.items()
            if key.startswith(field_slug_dot) and value and value.strip().lower() not in FALSY_VALUES
        ]

    def validate_value(self, field: Field, value: Any) -> list[FieldWarning]:
        values: list[str] = value
        warnings = []

        valid_choices = [choice.slug for choice in field.choices or []]

        if field.required and not values:
            warnings.append(FieldWarning.REQUIRED_MISSING)

        if not all(isinstance(value, str) for value in values):
            warnings.append(FieldWarning.INVALID_VALUE)

        if not all(value in valid_choices for value in values):
            warnings.append(FieldWarning.INVALID_CHOICE)

        return warnings


class DimensionMultiSelectFieldProcessor(MultiSelectFieldProcessor):
    def extract_value(self, field: Field, form_data: dict[str, Any]):
        value = super().extract_value(field, form_data)

        if isinstance(value, list):
            return [slugify(val) for val in value]

        return value


class RadioMatrixFieldProcessor(FieldProcessor):
    def extract_value(self, field: Field, form_data: dict[str, Any]):
        field_slug_dot = f"{field.slug}."
        return {
            key.removeprefix(field_slug_dot): value
            for key, value in form_data.items()
            if key.startswith(field_slug_dot)
        }

    def validate_value(self, field: Field, value: Any) -> list[FieldWarning]:
        values: dict[str, str] = value
        warnings: list[FieldWarning] = []

        questions = [question.slug for question in field.questions or []]
        valid_choices = [choice.slug for choice in field.choices or []]

        if field.required and not all(question in values for question in questions):
            warnings.append(FieldWarning.REQUIRED_MISSING)

        if not all(value in valid_choices for value in values.values()):
            warnings.append(FieldWarning.INVALID_CHOICE)

        if not all(key in questions for key in values):
            warnings.append(FieldWarning.INVALID_CHOICE)

        return warnings


class FileUploadFieldProcessor(FieldProcessor):
    # TODO rethink. here extract_value de facto both extracts and validates
    # should "extract" always be values.get, then validate and then possibly process?
    def extract_value(self, field: Field, form_data: dict[str, Any]):
        s3_urls = form_data.get(field.slug, VALUE_MISSING)
        if s3_urls is VALUE_MISSING:
            return VALUE_MISSING

        # presign s3 urls in value
        if not (
            isinstance(s3_urls, list)
            and all(isinstance(item, str) for item in s3_urls)
            and all(is_valid_s3_url(url) for url in s3_urls)
        ):
            return INVALID_VALUE

        return [presign_get(url) for url in s3_urls]

    def validate_value(self, field: Field, value: Any) -> list[FieldWarning]:
        warnings = []

        # TODO should not have to both return INVALID_VALUE and make it an explicit warning
        if value is INVALID_VALUE:
            warnings.append(FieldWarning.INVALID_VALUE)

        if field.required and (value is VALUE_MISSING or not value):
            warnings.append(FieldWarning.REQUIRED_MISSING)

        return warnings


FIELD_PROCESSORS: dict[FieldType, FieldProcessor] = {
    FieldType.SINGLE_LINE_TEXT: FieldProcessor(),
    FieldType.MULTI_LINE_TEXT: FieldProcessor(),
    FieldType.SINGLE_CHECKBOX: SingleCheckboxFieldProcessor(),
    FieldType.DIMENSION_SINGLE_CHECKBOX: SingleCheckboxFieldProcessor(),
    FieldType.STATIC_TEXT: NullFieldProcessor(),
    FieldType.DIVIDER: NullFieldProcessor(),
    FieldType.SPACER: NullFieldProcessor(),
    FieldType.SINGLE_SELECT: SingleSelectFieldProcessor(),
    FieldType.DIMENSION_SINGLE_SELECT: DimensionSingleSelectFieldProcessor(),
    FieldType.MULTI_SELECT: MultiSelectFieldProcessor(),
    FieldType.DIMENSION_MULTI_SELECT: DimensionMultiSelectFieldProcessor(),
    FieldType.RADIO_MATRIX: RadioMatrixFieldProcessor(),
    FieldType.FILE_UPLOAD: FileUploadFieldProcessor(),
    FieldType.NUMBER_FIELD: NumberFieldProcessor(),
    FieldType.DECIMAL_FIELD: DecimalFieldProcessor(),
    # TODO(#436) Time zone handling
    FieldType.DATE_FIELD: FieldProcessor(),
    FieldType.TIME_FIELD: FieldProcessor(),
    FieldType.DATE_TIME_FIELD: FieldProcessor(),
}

# This is deprecated in favour of NumberField but kept for backwards compatibility
# What about htmlType="email", "password" etc?
SINGLE_LINE_TEXT_PROCESSORS: dict[str, FieldProcessor] = {
    "number": NumberFieldProcessor(),
}


def process_form_data(
    fields: Sequence[Field],
    form_data: dict[str, Any],
    *,
    slug_prefix: str = "",
):
    """
    :param slug_prefix: If set, this prefix plus a dot will be removed from the field slugs.
    """
    values: dict[str, Any] = {}
    warnings: dict[str, list[FieldWarning]] = {}

    slug_prefix_dot = f"{slug_prefix}." if slug_prefix else ""

    for field in fields:
        field_slug = field.slug.removeprefix(slug_prefix_dot)
        processor = FIELD_PROCESSORS.get(field.type)

        if processor is None:
            warnings[field_slug] = [FieldWarning.UNKNOWN_FIELD_TYPE]
            continue

        # NOTE: uses possibly prefixed slug
        value = processor.extract_value(field, form_data)
        value_warnings = processor.validate_value(field, value)

        if value_warnings:
            warnings[field_slug] = value_warnings

        if value is VALUE_MISSING or value is INVALID_VALUE:
            continue

        if FieldWarning.INVALID_VALUE in value_warnings:
            continue

        # NOTE: Invalid choices are let through because the editor might remove a choice
        # after a user has already submitted a form with that choice selected.
        # It's better to let the editor see the invalid choice than silently ignore it.

        values[field_slug] = value

    return values, warnings
