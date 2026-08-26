from __future__ import annotations

from enum import Enum
from typing import Any

from django.db import models


class PostgresEnumField(models.Field):
    """
    Maps a Python Enum onto a native PostgreSQL enum type (as opposed to the
    varchar/integer columns django-enum produces). Values are stored and read
    back as the enum member's name, which is also the label declared on the
    PostgreSQL type.
    """

    def __init__(self, enum: type[Enum], db_type_name: str, *args: Any, **kwargs: Any):
        self.enum = enum
        self.db_type_name = db_type_name
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["enum"] = self.enum
        kwargs["db_type_name"] = self.db_type_name
        return name, path, args, kwargs

    def db_type(self, connection):
        return self.db_type_name

    def get_prep_value(self, value):
        if value is None:
            return None
        if not isinstance(value, self.enum):
            value = self.enum(value)
        return value.name

    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        return self.enum[value]

    def to_python(self, value):
        if value is None or isinstance(value, self.enum):
            return value
        return self.enum[value]
