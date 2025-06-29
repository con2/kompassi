from __future__ import annotations

from enum import Enum


class InvolvementApp(Enum):
    # NOTE: use dashes in app names (URL slugs)
    FORMS = "forms", "Surveys V2", "forms"
    PROGRAM = "program", "Program V2", "program_v2"

    value: str
    label: str
    app_name: str

    def __new__(cls, value: str, label: str, app_name: str):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.label = label
        obj.app_name = app_name
        return obj

    @classmethod
    def from_app_name(cls, app_name: str) -> InvolvementApp:
        """
        Converts a legacy app name to an InvolvementApp enum.
        """
        if app_name == "program_v2":
            return cls.PROGRAM
        return cls(app_name)


class InvolvementType(Enum):
    # NOTE: use dashes in app names (URL slugs)
    PROGRAM_OFFER = "program-offer", "Program offer", InvolvementApp.PROGRAM
    PROGRAM_HOST = "program-host", "Program host", InvolvementApp.PROGRAM
    SURVEY_RESPONSE = "survey-response", "Survey response", InvolvementApp.FORMS

    value: str
    label: str
    app: InvolvementApp

    def __new__(cls, value: str, label: str, app: InvolvementApp):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.label = label
        obj.app = app
        return obj


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
