"""
Security-critical rendering pipeline for Messages V2. Unlike V1 mailings, there is no
template engine: placeholder values are user-controlled data (eg. a program offerer's
own program title) and must never be allowed to introduce Markdown or HTML structure.

To guarantee that, placeholders are substituted *after* Markdown rendering and
sanitization, using opaque sentinels that pass through both steps verbatim, and the
substituted values are always HTML-escaped in the HTML output. See PLACEHOLDERS for the
whitelist of recognized tokens - there is no `{{ ... }}`, no control structures, and no
object traversal; only a fixed set of scalars pulled from (event, person, involvement,
program).
"""

from __future__ import annotations

import html
import re
import uuid
from dataclasses import dataclass
from typing import TYPE_CHECKING

from django.template.loader import render_to_string

from kompassi.core.utils.markdown_utils import render_markdown

if TYPE_CHECKING:
    from kompassi.core.models.event import Event
    from kompassi.core.models.person import Person
    from kompassi.involvement.models.involvement import Involvement
    from kompassi.program_v2.models.program import Program


@dataclass(frozen=True)
class Placeholder:
    token: str
    description_en: str
    per_involvement_only: bool = False

    def resolve(
        self,
        *,
        event: Event,
        person: Person,
        involvement: Involvement | None,
        program: Program | None,
    ) -> str:
        match self.token:
            case "EVENT_NAME":
                return event.name
            case "FIRST_NAME":
                return person.first_name
            case "PROGRAM_TITLE":
                return program.title if program else ""
            case _:
                raise ValueError(f"Unknown placeholder token: {self.token}")


# Recognized tokens are a whitelist only. PROGRAM_TITLE varies per involvement, so it is
# only offered for MessageDispatch.PER_INVOLVEMENT in the compose UI.
PLACEHOLDERS = [
    Placeholder("EVENT_NAME", "The name of the event"),
    Placeholder("FIRST_NAME", "The recipient's first name"),
    Placeholder("PROGRAM_TITLE", "The title of the program item", per_involvement_only=True),
]
PLACEHOLDERS_BY_TOKEN = {placeholder.token: placeholder for placeholder in PLACEHOLDERS}

_PLACEHOLDER_RE = re.compile(r"\{(" + "|".join(re.escape(token) for token in PLACEHOLDERS_BY_TOKEN) + r")\}")


def _tokenize(source: str) -> tuple[str, dict[str, str]]:
    """
    Replace each recognized placeholder token with an opaque sentinel that survives
    Markdown rendering and HTML sanitization verbatim. Returns the tokenized source and
    a sentinel -> placeholder token map.
    """
    sentinel_by_token: dict[str, str] = {}

    def replace(match: re.Match[str]) -> str:
        token = match.group(1)
        return sentinel_by_token.setdefault(token, f"MSGV2{uuid.uuid4().hex}SENTINEL")

    tokenized = _PLACEHOLDER_RE.sub(replace, source)
    return tokenized, {sentinel: token for token, sentinel in sentinel_by_token.items()}


def _resolve_sentinel_values(
    sentinel_to_token: dict[str, str],
    *,
    event: Event,
    person: Person,
    involvement: Involvement | None,
    program: Program | None,
) -> dict[str, str]:
    return {
        sentinel: PLACEHOLDERS_BY_TOKEN[token].resolve(
            event=event, person=person, involvement=involvement, program=program
        )
        for sentinel, token in sentinel_to_token.items()
    }


def render_subject(
    source: str,
    *,
    event: Event,
    person: Person,
    involvement: Involvement | None = None,
    program: Program | None = None,
) -> str:
    """
    Subject lines carry no Markdown formatting, only placeholder substitution.
    The result is later consumed as plain text (email subject, GraphQL string field).
    """
    tokenized, sentinel_to_token = _tokenize(source)
    values = _resolve_sentinel_values(
        sentinel_to_token, event=event, person=person, involvement=involvement, program=program
    )

    rendered = tokenized
    for sentinel, value in values.items():
        rendered = rendered.replace(sentinel, value)

    return rendered


def render_body(
    source: str,
    *,
    event: Event,
    person: Person,
    involvement: Involvement | None = None,
    program: Program | None = None,
) -> tuple[str, str]:
    """
    Renders the Markdown body into a (sanitized_html, plaintext) pair, with placeholder
    values substituted as inert literal text in both - never interpreted as Markdown or
    HTML, even if the value itself looks like a link, an image tag, or a heading.
    """
    tokenized, sentinel_to_token = _tokenize(source)
    values = _resolve_sentinel_values(
        sentinel_to_token, event=event, person=person, involvement=involvement, program=program
    )

    sanitized_html = render_markdown(tokenized)
    for sentinel, value in values.items():
        sanitized_html = sanitized_html.replace(sentinel, html.escape(value))

    plaintext = tokenized
    for sentinel, value in values.items():
        plaintext = plaintext.replace(sentinel, value)

    return sanitized_html, plaintext


def render_email_html(body_html: str, *, event: Event, subject: str) -> str:
    return render_to_string(
        "messages_v2/email.html",
        {"body_html": body_html, "event": event, "subject": subject},
    )
