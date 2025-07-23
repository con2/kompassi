from __future__ import annotations

from typing import Any

from django.http import HttpRequest

from kompassi.access.models.cbac_entry import CBACEntry
from kompassi.core.models.event import Event


def program_v2_event_box_context(
    request: HttpRequest,
    event: Event,
) -> dict[str, Any]:
    if meta := event.program_v2_event_meta:
        is_program_v2_admin = CBACEntry.is_allowed(
            request.user,
            dict(
                organization=event.organization.slug,
                event=event.slug,
                app="program_v2",
            ),
        )
        is_program_v2_published = meta.is_program_published
        is_program_v2_event_box_shown = is_program_v2_admin or is_program_v2_published
    else:
        is_program_v2_admin = False
        is_program_v2_published = False
        is_program_v2_event_box_shown = False

    return dict(
        is_program_v2_admin=is_program_v2_admin,
        is_program_v2_published=is_program_v2_published,
        is_program_v2_event_box_shown=is_program_v2_event_box_shown,
    )
