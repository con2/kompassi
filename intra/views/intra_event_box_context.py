def intra_event_box_context(request, event):
    meta = event.intra_event_meta

    return dict(
        is_intra_organizer=meta.is_user_organizer(request.user),
        is_intra_admin=meta.is_user_admin(request.user),
    )
