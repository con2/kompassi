from __future__ import annotations

from enum import Enum

from graphql_api.language import SUPPORTED_LANGUAGE_CODES


class InvolvementApp(Enum):
    # NOTE: use dashes in app names (URL slugs)
    FORMS = "forms", "forms", "Surveys V2", "Kyselyt V2", "Enkät V2"
    PROGRAM = "program", "program_v2", "Program V2", "Ohjelma V2", "Program V2"

    value: str
    app_name: str

    # NOTE SUPPORTED_LANGUAGES
    title_en: str
    title_fi: str
    title_sv: str

    def __new__(cls, value: str, app_name: str, title_en: str, title_fi: str, title_sv: str):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.title_en = title_en
        obj.title_fi = title_fi
        obj.title_sv = title_sv
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

    def get_title_dict(self) -> dict[str, str]:
        return {
            language_code: title
            for language_code in SUPPORTED_LANGUAGE_CODES
            if (title := getattr(self, f"title_{language_code}"))
        }


class InvolvementType(Enum):
    # NOTE: use dashes in app names (URL slugs)
    PROGRAM_OFFER = "program-offer", InvolvementApp.PROGRAM, "Program offer", "Ohjelmatarjous", "Programerbjudande"
    PROGRAM_HOST = "program-host", InvolvementApp.PROGRAM, "Program host", "Ohjelmanumero", "Programvärd"
    SURVEY_RESPONSE = "survey-response", InvolvementApp.FORMS, "Survey response", "Kyselyvastaus", "Enkätsvar"

    value: str
    app: InvolvementApp

    # NOTE SUPPORTED_LANGUAGES
    title_en: str
    title_fi: str
    title_sv: str

    def __new__(cls, value: str, app: InvolvementApp, title_en: str, title_fi: str, title_sv: str):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.app = app
        obj.title_en = title_en
        obj.title_fi = title_fi
        obj.title_sv = title_sv
        return obj

    def get_title_dict(self) -> dict[str, str]:
        return {
            language_code: title
            for language_code in SUPPORTED_LANGUAGE_CODES
            if (title := getattr(self, f"title_{language_code}"))
        }


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
