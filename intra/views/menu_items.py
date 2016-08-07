# encoding: utf-8

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from core.admin_menus import AdminMenuItem
from core.utils import url


def intra_admin_menu_items(request, event):
    return intra_organizer_menu_items(request, event) + [

    ]


def intra_organizer_menu_items(request, event):
    organizers_url = url('intra_organizer_view', event.slug)
    organizers_active = request.path.startswith(organizers_url)
    organizers_text = _('Teams and organizers')

    return [
        AdminMenuItem(
            is_active=organizers_active,
            href=organizers_url,
            text=organizers_text,
        ),
    ]
