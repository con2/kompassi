from __future__ import annotations

from collections.abc import Iterable
from typing import Any, Self

import pydantic


class Splat(pydantic.BaseModel, populate_by_name=True):
    """
    A splat is a way to make single response project into multiple items in the projected result.

    For example, given the following schema of two splats:

    [
        { targetField: "name", sourceFields: ["name1", "name2", "name3"], required: true },
        { targetField: "email", sourceFields: ["email1", "email2", "email3"], required: false}
    ]

    And the following response values:

    {
        name1: "Alice",
        email1: "alice@example.com",
        name2: "Bob",
        email2: "",
        name3: "",
        email3: "carol@example.com"
    }

    Projecting the response with this schema would yield:

    [
        { name: "Alice", email: "alice@example.com" },
        { name: "Bob", email: ""}
    ]

    Carol is omitted because name3 is empty and name has been designated as a required field.
    """

    target_field: str = pydantic.Field(
        validation_alias="targetField",
        serialization_alias="targetField",
    )
    source_fields: list[str] = pydantic.Field(
        validation_alias="sourceFields",
        serialization_alias="sourceFields",
    )
    required: bool = True

    # NOTE: None (null) is not currently supported as a default value.
    # If a need arises, use a sentinel object to denote "value missing" instead.
    # Typing for sentinels is hairy, so omitted for now.
    default: Any = ""

    def extract(self, values: dict[str, Any]) -> Iterable[Any | None]:
        """
        Extracts the values from the given response values based on the source fields.
        None at a given position means this schemoid thinks that position should not produce
        a result ie. a required field is empty.
        """
        for source_field in self.source_fields:
            value = values.get(source_field)

            if value in ("", None):
                yield None if self.required else self.default
                continue

            yield value

    @classmethod
    def project(cls, schema: list[Self], values: dict[str, Any]) -> Iterable[dict[str, Any]]:
        """
        Projects the given response values into a list of splat items based on the schema.
        """
        for item in zip(*[splat.extract(values) for splat in schema], strict=True):
            if any(splat.required and value is None for splat, value in zip(schema, item, strict=True)):
                continue

            yield {splat.target_field: value for splat, value in zip(schema, item, strict=True)}
