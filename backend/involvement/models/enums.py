from __future__ import annotations

from enum import Enum


class InvolvementApp(Enum):
    FORMS = "forms", "Surveys V2"
    PROGRAM = "program", "Program V2"

    value: str
    label: str

    def __new__(cls, value: str, label: str):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.label = label
        return obj

    @classmethod
    def from_app_name(cls, app_name: str) -> InvolvementApp:
        """
        Converts a legacy app name to an InvolvementApp enum.
        """
        if app_name == "program_v2":
            return cls.PROGRAM
        return cls(app_name)
