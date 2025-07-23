from kompassi.access.models.cbac_entry import CBACEntry


def tickets_v2_event_box_context(request, event):
    claims = dict(
        organization=event.organization.slug,
        event=event.slug,
        app="tickets_v2",
    )

    have_tickets_v2_products_available = (
        event.tickets_v2_event_meta is not None and event.tickets_v2_event_meta.have_available_products
    )

    return dict(
        have_tickets_v2_products_available=have_tickets_v2_products_available,
        is_tickets_v2_admin=CBACEntry.is_allowed(request.user, claims),
    )
