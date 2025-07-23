from django.utils.translation import gettext_lazy as _

from kompassi.core.admin_menus import AdminMenuItem
from kompassi.core.utils import url


def get_organizers_menu_item(request, event, may_be_active=True, notifications=0):
    organizers_url = url("intra:organizer_view", event.slug)
    organizers_active = may_be_active and request.path.startswith(organizers_url)
    organizers_text = _("Teams and organizers")

    return AdminMenuItem(
        is_active=organizers_active,
        href=organizers_url,
        text=organizers_text,
        notifications=notifications,
    )


def intra_admin_menu_items(request, event):
    meta = event.intra_event_meta

    privileges_url = url("intra:admin_privileges_view", event.slug)
    privileges_active = request.path.startswith(privileges_url)
    privileges_text = _("Privileges")

    other_menu_items = [
        AdminMenuItem(
            is_active=privileges_active,
            href=privileges_url,
            text=privileges_text,
        ),
    ]

    return [
        get_organizers_menu_item(
            request,
            event,
            may_be_active=not any(item.is_active for item in other_menu_items),
            notifications=len(meta.unassigned_organizers),
        ),
        *other_menu_items,
    ]


def intra_organizer_menu_items(request, event, is_intra_admin=False):
    return [
        get_organizers_menu_item(request, event),
    ]
