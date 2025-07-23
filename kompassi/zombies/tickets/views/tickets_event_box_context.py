def tickets_event_box_context(request, event):
    if event.tickets_event_meta:
        is_tickets_admin = event.tickets_event_meta.is_user_admin(request.user)
    else:
        is_tickets_admin = False

    return dict(is_tickets_admin=is_tickets_admin)
