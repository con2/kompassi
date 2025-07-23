from kompassi.access.models.cbac_entry import CBACEntry


def forms_event_box_context(request, event):
    claims = dict(
        organization=event.organization.slug,
        event=event.slug,
        app="forms",
    )

    return dict(
        is_forms_admin=CBACEntry.is_allowed(request.user, claims),
    )
