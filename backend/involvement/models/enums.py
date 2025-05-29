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
