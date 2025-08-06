from __future__ import annotations

from enum import Enum, Flag
from functools import cached_property, reduce
from typing import Any

from django.db import models
from pydantic_core import CoreSchema, SchemaValidator
from pydantic_core.core_schema import bool_schema, float_schema, str_schema


class ValueOrdering(models.TextChoices):
    MANUAL = "MANUAL", "Manual"
    SLUG = "SLUG", "Alphabetical (slug)"
    TITLE = "TITLE", "Alphabetical (localized title)"


class DimensionApp(Enum):
    FORMS = "forms"
    PROGRAM_V2 = "program_v2"
    INVOLVEMENT = "involvement"


class AnnotationDataType(Enum):
    STRING = "string", str_schema()
    NUMBER = "number", float_schema()
    BOOLEAN = "boolean", bool_schema()

    core_schema: CoreSchema

    def __new__(cls, value: str, core_schema: CoreSchema):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.core_schema = core_schema
        return obj

    @cached_property
    def validator(self) -> SchemaValidator:
        return SchemaValidator(self.core_schema)

    def conform_value(self, value: Any) -> str | bool | int | float | None:
        try:
            return self.validator.validate_python(value)
        except Exception:
            return None


class AnnotationAppliesTo(Flag):
    NOTHING = 0

    PROGRAM_ITEM = 1 << 0
    SCHEDULE_ITEM = 1 << 1

    INVOLVEMENT = 1 << 2

    @classmethod
    def from_kwargs(
        cls,
        is_applicable_to_program_items: bool = False,
        is_applicable_to_schedule_items: bool = False,
        is_applicable_to_involvements: bool = False,
    ) -> AnnotationAppliesTo:
        return reduce(
            lambda acc, flag: acc | flag,
            [
                cls.PROGRAM_ITEM if is_applicable_to_program_items else cls.NOTHING,
                cls.SCHEDULE_ITEM if is_applicable_to_schedule_items else cls.NOTHING,
                cls.INVOLVEMENT if is_applicable_to_involvements else cls.NOTHING,
            ],
        )


class AnnotationFlags(Flag):
    NONE = 0

    PUBLIC = 1 << 0
    SHOWN_IN_DETAIL = 1 << 1
    COMPUTED = 1 << 2

    PERK = 1 << 3

    @classmethod
    def from_kwargs(
        cls,
        is_public: bool = False,
        is_shown_in_detail: bool = False,
        is_computed: bool = False,
        is_perk: bool = False,
    ) -> AnnotationFlags:
        return reduce(
            lambda acc, flag: acc | flag,
            [
                cls.PUBLIC if is_public else cls.NONE,
                cls.SHOWN_IN_DETAIL if is_shown_in_detail else cls.NONE,
                cls.COMPUTED if is_computed else cls.NONE,
                cls.PERK if is_perk else cls.NONE,
            ],
        )
