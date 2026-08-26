from __future__ import annotations

from enum import Enum
from typing import Any, override

from django.db import models


class PostgresEnumField(models.Field):
    """
    Maps a Python Enum onto a native PostgreSQL enum type (as opposed to the
    varchar/integer columns django-enum produces). Values are stored and read
    back as the enum member's name, which is also the label declared on the
    PostgreSQL type.

    NOTE: the member *name* is the wire format throughout, in both directions.
    For the enums this is used with the name and the value happen to coincide,
    but relying on that would make a mismatch silently unrepresentable, so
    everything here goes through `Enum[name]` rather than `Enum(value)`.

    NOTE: pass `choices=[(m.name, m.name) for m in TheEnum]`. graphene-django
    needs them to build a GraphQL type for the field at all, and Django's admin
    and forms need them to render a select. Where the GraphQL type must expose
    the Python enum itself (a resolver returning a member), declare the field
    explicitly with `graphene.Enum.from_enum` — see
    kompassi/tickets_v2/graphql/meta.py.
    """

    def __init__(self, enum: type[Enum], db_type_name: str, *args: Any, **kwargs: Any):
        self.enum = enum
        self.db_type_name = db_type_name
        super().__init__(*args, **kwargs)

    @override
    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["enum"] = self.enum
        kwargs["db_type_name"] = self.db_type_name
        return name, path, args, kwargs

    @override
    def db_type(self, connection):
        return self.db_type_name

    @override
    def get_internal_type(self):
        # Django keys a few lookup/serialisation behaviours off this. There is no
        # built-in field whose semantics match a native enum, and TextField is the
        # closest: the value travels as a string and compares with the ordering
        # operators, which is exactly what Postgres does with enum labels.
        return "TextField"

    @override
    def get_prep_value(self, value):
        if value is None:
            return None
        if isinstance(value, self.enum):
            return value.name
        # A name, eg. from a GraphQL enum input or a dimension filter slug.
        return self.enum[str(value)].name

    @override
    def value_to_string(self, obj):
        # Used by dumpdata; loaddata comes back through to_python(). Goes via
        # get_prep_value rather than reading .name off the attribute, because an
        # instance may carry a plain label string that has not been round-tripped
        # through the database yet.
        return self.get_prep_value(self.value_from_object(obj)) or ""

    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        return self.enum[value]

    def to_python(self, value):
        if value is None or isinstance(value, self.enum):
            return value
        return self.enum[str(value)]
