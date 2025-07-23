def programme_event_box_context(request, event):
    return dict(
        is_programme_admin=event.programme_event_meta.is_user_admin(request.user),
    )
