from enum import Enum
from functools import cached_property
from typing import Any

from pydantic_core import CoreSchema, SchemaValidator
from pydantic_core.core_schema import bool_schema, float_schema, str_schema


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
