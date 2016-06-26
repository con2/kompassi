# encoding: utf-8

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from core.utils import url
from core.admin_menus import AdminMenuItem

from ..models import Invitation


def programme_admin_menu_items(request, event):
    invitations_url = url('programme_admin_invitations_view', event.slug)
    invitations_active = request.path == invitations_url
    invitations_text = _('Open invitations')
    invitations_notifications = Invitation.objects.filter(programme__category__event=event, state='valid').count()

    timetable_url = url('programme_admin_timetable_view', event.slug)
    timetable_active = request.path == timetable_url
    timetable_text = 'Ohjelmakartan esikatselu'

    special_url = url('programme_admin_special_view', event.slug)
    special_active = request.path == special_url
    special_text = 'Ohjelmakartan ulkopuolisten esikatselu'

    publish_url = url('programme_admin_publish_view', event.slug)
    publish_active = request.path == publish_url
    publish_text = _('Publish schedule')

    index_url = url('programme_admin_view', event.slug)
    index_active = request.path.startswith(index_url) and not any((
        invitations_active,
        timetable_active,
        special_active,
    ))
    index_text = 'Ohjelmaluettelo'

    return [
        AdminMenuItem(is_active=index_active, href=index_url, text=index_text),
        AdminMenuItem(is_active=invitations_active, href=invitations_url, text=invitations_text, notifications=invitations_notifications),
        AdminMenuItem(is_active=timetable_active, href=timetable_url, text=timetable_text),
        AdminMenuItem(is_active=special_active, href=special_url, text=special_text),
        AdminMenuItem(is_active=publish_active, href=publish_url, text=publish_text),
    ]
