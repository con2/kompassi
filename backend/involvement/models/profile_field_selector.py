from __future__ import annotations

from typing import Self

import pydantic


class ProfileFieldSelector(pydantic.BaseModel, populate_by_name=True, frozen=True):
    """
    Used to determine which profile fields are transferred from registry to another.
    NOTE: Must match ProfileFieldSelector in frontend/src/components/involvement/models.ts.
    """

    first_name: bool = pydantic.Field(
        default=False,
        validation_alias="firstName",
        serialization_alias="firstName",
    )
    last_name: bool = pydantic.Field(
        default=False,
        validation_alias="lastName",
        serialization_alias="lastName",
    )
    nick: bool = pydantic.Field(default=False)
    email: bool = pydantic.Field(default=False)
    phone_number: bool = pydantic.Field(
        default=False,
        validation_alias="phoneNumber",
        serialization_alias="phoneNumber",
    )
    discord_handle: bool = pydantic.Field(
        default=False,
        validation_alias="discordHandle",
        serialization_alias="discordHandle",
    )

    @classmethod
    def all_fields(cls) -> Self:
        return cls(
            first_name=True,
            last_name=True,
            nick=True,
            email=True,
            phone_number=True,
            discord_handle=True,
        )
