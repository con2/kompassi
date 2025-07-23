from __future__ import annotations

from collections.abc import Iterator
from functools import reduce
from typing import Any, Self

import pydantic

from kompassi.core.models.person import Person
from kompassi.forms.models.enums import Anonymity

from .enums import NameDisplayStyle


class ProfileFieldSelector(pydantic.BaseModel, populate_by_name=True, frozen=True):
    """
    Used to determine which profile fields are transferred from registry to another.
    NOTE: Must match ProfileFieldSelector in frontend/src/components/involvement/models.ts.

    For "no fields selected", use the default constructor.
    For "all fields selected", use `ProfileFieldSelector.all_fields()`.
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

    def __iter__(self) -> Iterator[str]:
        """
        Iterate over field names that are selected (True).
        """
        for field_name, is_included in super().__iter__():
            if is_included:
                yield field_name

    def __bool__(self) -> bool:
        """
        Returns True iff any field is selected.
        """
        return any(self)

    def __or__(self, other: ProfileFieldSelector) -> ProfileFieldSelector:
        """
        Combines two ProfileFieldSelectors using a logical OR.
        Returns a new ProfileFieldSelector with fields selected if either selector has them.
        """
        if not isinstance(other, ProfileFieldSelector):
            raise TypeError(f"Cannot __or__ ProfileFieldSelector with {type(other)}")

        return ProfileFieldSelector(
            first_name=self.first_name or other.first_name,
            last_name=self.last_name or other.last_name,
            nick=self.nick or other.nick,
            email=self.email or other.email,
            phone_number=self.phone_number or other.phone_number,
            discord_handle=self.discord_handle or other.discord_handle,
        )

    @classmethod
    def union(cls, *selectors: ProfileFieldSelector) -> ProfileFieldSelector:
        return reduce(
            lambda acc, inv: acc | inv,
            selectors,
            ProfileFieldSelector(),
        )

    def select(self, person: Person) -> dict[str, Any]:
        """
        Selects the fields from the given Person based on this selector.
        Returns a Profile with only the selected fields populated.
        """
        return dict(
            first_name=person.first_name if self.first_name else "",
            last_name=person.surname if self.last_name else "",
            nick=person.nick if self.nick else "",
            email=person.email if self.email else "",
            phone_number=person.normalized_phone_number if self.phone_number else "",
            discord_handle=person.discord_handle if self.discord_handle else "",
            name_display_style=NameDisplayStyle(person.preferred_name_display_style)
            if person.preferred_name_display_style
            else NameDisplayStyle.FIRSTNAME_NICK_LASTNAME,
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

    @classmethod
    def from_anonymity(cls, anonymity: Anonymity) -> Self:
        """
        Convert legacy Anonymity choices to ProfileFieldSelector.
        """
        match anonymity:
            case Anonymity.HARD:
                return cls()
            case Anonymity.SOFT:
                return cls()
            case Anonymity.NAME_AND_EMAIL:
                return cls(
                    first_name=True,
                    last_name=True,
                    nick=True,
                    email=True,
                )
            case Anonymity.FULL_PROFILE:
                return cls.all_fields()
