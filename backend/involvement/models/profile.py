from __future__ import annotations

from collections.abc import Collection
from typing import TYPE_CHECKING, Self

import pydantic

from .enums import NameDisplayStyle
from .involvement import Involvement
from .profile_field_selector import ProfileFieldSelector

if TYPE_CHECKING:
    from core.models.person import Person


class Profile(pydantic.BaseModel, populate_by_name=True, frozen=True, arbitrary_types_allowed=True):
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

    # NOTE: ProfileType does not expose this to GraphQL (ProfileWithInvolvementType does)
    involvements: list[Involvement] = pydantic.Field(
        default_factory=list,
        description="List of involvements associated with this profile.",
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
    def from_person(cls, person: Person, profile_field_selector: ProfileFieldSelector) -> Self:
        """
        Creates a Profile instance from a Person object and a ProfileFieldSelector.
        """
        return cls(**profile_field_selector.select(person))

    @classmethod
    def from_person_involvements(cls, person: Person, involvements: Collection[Involvement]) -> Self:
        field_selector = ProfileFieldSelector.union(*[inv.profile_field_selector for inv in involvements])
        profile_fields = field_selector.select(person)

        return cls(**profile_fields, involvements=list(involvements))
