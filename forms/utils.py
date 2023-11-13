"""
Contains the `process_form_data` function which processes a form's data
in the form of `Object.fromEntries(formData.entries())` into a more
manageable format. Other things in this file are part of that function's
implementation.

NOTE: The exact semantics of `process_form_data` are defined by and documented in
`forms/tests.py:test_process_form_data`.
"""

import sys
from enum import Enum
from typing import Any

from forms.models import Field

from .models import FieldType, Field


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


class MultiSelectFieldProcessor(FieldProcessor):
    def extract_value(self, field: Field, form_data: dict[str, Any]):
        return [
            key.split(".", 1)[1]
            for key, value in form_data.items()
            if key.startswith(f"{field.slug}.") and value and value.strip().lower() not in FALSY_VALUES
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


class RadioMatrixFieldProcessor(FieldProcessor):
    def extract_value(self, field: Field, form_data: dict[str, Any]):
        return {
            key.split(".", 1)[1]: value
            for key, value in form_data.items()
            if key.startswith(f"{field.slug}.")
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

        if not all(key in questions for key in values.keys()):
            warnings.append(FieldWarning.INVALID_CHOICE)

        return warnings


FIELD_PROCESSORS: dict[FieldType, FieldProcessor] = {
    FieldType.SINGLE_LINE_TEXT: FieldProcessor(),
    FieldType.MULTI_LINE_TEXT: FieldProcessor(),
    FieldType.SINGLE_CHECKBOX: SingleCheckboxFieldProcessor(),
    FieldType.STATIC_TEXT: NullFieldProcessor(),
    FieldType.DIVIDER: NullFieldProcessor(),
    FieldType.SPACER: NullFieldProcessor(),
    FieldType.SINGLE_SELECT: SingleSelectFieldProcessor(),
    FieldType.MULTI_SELECT: MultiSelectFieldProcessor(),
    FieldType.RADIO_MATRIX: RadioMatrixFieldProcessor(),
}

# TODO should NumberField instead of SingleLineText[htmlType="number"]?
# What about htmlType="email", "password" etc?
SINGLE_LINE_TEXT_PROCESSORS: dict[str, FieldProcessor] = {
    "number": NumberFieldProcessor(),
}


def process_form_data(fields: list[Field], form_data: dict[str, Any]):
    values: dict[str, Any] = {}
    warnings: dict[str, list[FieldWarning]] = {}

    for field in fields:
        if field.type == FieldType.SINGLE_LINE_TEXT:
            processor = SINGLE_LINE_TEXT_PROCESSORS.get(field.html_type or "", FieldProcessor())
        else:
            processor = FIELD_PROCESSORS.get(field.type)

        if processor is None:
            warnings[field.slug] = [FieldWarning.UNKNOWN_FIELD_TYPE]
            continue

        value = processor.extract_value(field, form_data)
        value_warnings = processor.validate_value(field, value)

        if value_warnings:
            warnings[field.slug] = value_warnings

        if value is VALUE_MISSING or value is INVALID_VALUE:
            continue

        if FieldWarning.INVALID_VALUE in value_warnings:
            continue

        # NOTE: Invalid choices are let through because the editor might remove a choice
        # after a user has already submitted a form with that choice selected.
        # It's better to let the editor see the invalid choice than silently ignore it.

        values[field.slug] = value

    return values, warnings
