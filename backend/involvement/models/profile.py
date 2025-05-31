from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

import pydantic

if TYPE_CHECKING:
    from core.models.person import Person

    from .profile_field_selector import ProfileFieldSelector


class NameDisplayStyle(Enum):
    # NOTE: "surname" for compatibility with legacy
    FIRSTNAME_NICK_LASTNAME = "firstname_nick_surname", 'Firstname "Nickname" Lastname'
    FIRSTNAME_LASTNAME = "firstname_surname", "Firstname Lastname"
    FIRSTNAME = "firstname", "Firstname"
    NICK = "nick", "Nickname"

    _value_: str
    label: str

    def __new__(cls, value: str, label: str):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.label = label
        return obj

    def format(
        self,
        first_name: str,
        nick: str,
        last_name: str,
        always_include_real_name: bool = False,
    ) -> str:
        name_display_style = self
        if always_include_real_name:
            if "nick" in self.value:
                name_display_style = NameDisplayStyle.FIRSTNAME_NICK_LASTNAME
            else:
                name_display_style = NameDisplayStyle.FIRSTNAME_LASTNAME

        match name_display_style:
            case NameDisplayStyle.FIRSTNAME_NICK_LASTNAME:
                parts = [
                    first_name,
                    f"”{nick}”" if nick else "",
                    last_name,
                ]
            case NameDisplayStyle.FIRSTNAME_LASTNAME:
                parts = [
                    first_name,
                    last_name,
                ]
            case NameDisplayStyle.FIRSTNAME:
                parts = [first_name]
            case NameDisplayStyle.NICK:
                parts = [nick]

        return " ".join(part for part in parts) if parts else ""


class Profile(pydantic.BaseModel, populate_by_name=True, frozen=True):
    """
    Represents a user profile with fields that can be selected for transfer.
    NOTE: Must match Profile in frontend/src/components/involvement/models.ts.
    """

    first_name: str = pydantic.Field(
        default="",
        validation_alias="firstName",
        serialization_alias="firstName",
    )
    last_name: str = pydantic.Field(
        default="",
        validation_alias="lastName",
        serialization_alias="lastName",
    )
    nick: str = pydantic.Field(default="")
    email: str = pydantic.Field(default="")
    phone_number: str = pydantic.Field(
        default="",
        validation_alias="phoneNumber",
        serialization_alias="phoneNumber",
    )
    discord_handle: str = pydantic.Field(
        default="",
        validation_alias="discordHandle",
        serialization_alias="discordHandle",
    )

    name_display_style: NameDisplayStyle = pydantic.Field(
        default=NameDisplayStyle.FIRSTNAME_NICK_LASTNAME,
        validation_alias="nameDisplayStyle",
        serialization_alias="nameDisplayStyle",
    )

    @pydantic.computed_field
    @property
    def display_name(self) -> str:
        """
        The display name generally follows the format Firstname "Nickname" Lastname.
        If some parts are missing or the user has requested not to display them,
        we will adjust the format accordingly.
        """
        return self.name_display_style.format(
            first_name=self.first_name,
            nick=self.nick,
            last_name=self.last_name,
        )

    @pydantic.computed_field
    @property
    def full_name(self) -> str:
        """
        The full name is similar to display name, but includes the last name
        if it is available. The full name generally should not be displayed
        to the public (use display name instead), but is used internally for identification purposes.
        """
        return self.name_display_style.format(
            first_name=self.first_name,
            nick=self.nick,
            last_name=self.last_name,
            always_include_real_name=True,
        )

    @classmethod
    def from_person(cls, person: Person, profile_field_selector: ProfileFieldSelector) -> Profile:
        """
        Creates a Profile instance from a Person object and a ProfileFieldSelector.
        """
        return profile_field_selector.select(person)
