from __future__ import annotations

from typing import Any

from core.utils.locale_utils import get_message_in_language
from forms.models.field import Field, FieldType

TITLE = dict(en="Title", fi="Otsikko")
DESCRIPTION = dict(en="Description", fi="Kuvaus")


def get_program_offer_form_default_fields(language: str) -> list[dict[str, Any]]:
    fields = [
        Field(
            slug="title",
            type=FieldType.SINGLE_LINE_TEXT,
            required=True,
            title=get_message_in_language(TITLE, language),
        ),
        Field(
            slug="description",
            type=FieldType.MULTI_LINE_TEXT,
            title=get_message_in_language(DESCRIPTION, language),
        ),
    ]

    return [field.model_dump(mode="json", by_alias=True, exclude_defaults=True) for field in fields]
