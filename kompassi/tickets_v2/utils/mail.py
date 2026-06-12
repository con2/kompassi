from __future__ import annotations

from typing import TYPE_CHECKING

from django.conf import settings

from kompassi.graphql_api.language import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGE_CODES

if TYPE_CHECKING:
    from kompassi.core.models.event import Event

MAIL_DOMAIN = settings.DEFAULT_FROM_EMAIL.split("@", 1)[1].rstrip(">")


def tickets_from_email(event: Event) -> str:
    """
    The sender address for emails sent to ticket shop customers of an event.
    """
    return f"{event.name} ({settings.KOMPASSI_INSTALLATION_NAME}) <{event.slug}-tickets@{MAIL_DOMAIN}>"


def email_template_language(language: str) -> str:
    """
    The language of the .eml templates to use for a customer who speaks `language`.

    TODO Missing Swedish message templates. When they are added, update all
    users of this function at once.
    """
    language = language.lower()

    if language == "sv" or language not in SUPPORTED_LANGUAGE_CODES:
        return DEFAULT_LANGUAGE

    return language
