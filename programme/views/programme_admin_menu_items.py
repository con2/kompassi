# encoding: utf-8

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from core.utils import url
from core.admin_menus import AdminMenuItem

from ..models import Invitation, ProgrammeFeedback, Programme


def programme_admin_menu_items(request, event):
    organizers_url = url('programme_admin_organizers_view', event.slug)
    organizers_active = request.path.startswith(organizers_url)
    organizers_text = _('Programme hosts')

    offers_url = url('programme_admin_view', event.slug) + '?state=offered&sort=created_at'
    offers_active = request.get_full_path() == offers_url
    offers_text = _('New offers')
    offers_notifications = Programme.objects.filter(category__event=event, state='offered').count()

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

    cold_offers_url = url('programme_admin_cold_offers_view', event.slug)
    cold_offers_active = request.path == cold_offers_url
    cold_offers_text = _('Cold offer period starting and ending times')

    publish_url = url('programme_admin_publish_view', event.slug)
    publish_active = request.path == publish_url
    publish_text = _('Publish schedule')

    feedback_url = url('programme_admin_feedback_view', event.slug)
    feedback_active = request.path == feedback_url
    feedback_text = _('Programme feedback')
    feedback_notifications = ProgrammeFeedback.objects.filter(
        programme__category__event=event,
        hidden_at__isnull=True
    ).count()

    index_url = url('programme_admin_view', event.slug)
    index_active = request.path.startswith(index_url) and not any((
        organizers_active,
        feedback_active,
        invitations_active,
        offers_active,
        cold_offers_active,
        publish_active,
        special_active,
        timetable_active,
    ))
    index_text = 'Ohjelmaluettelo'

    return [
        AdminMenuItem(is_active=index_active, href=index_url, text=index_text),
        AdminMenuItem(is_active=organizers_active, href=organizers_url, text=organizers_text),
        AdminMenuItem(is_active=offers_active, href=offers_url, text=offers_text, notifications=offers_notifications),
        AdminMenuItem(is_active=invitations_active, href=invitations_url, text=invitations_text, notifications=invitations_notifications),
        AdminMenuItem(is_active=timetable_active, href=timetable_url, text=timetable_text),
        AdminMenuItem(is_active=special_active, href=special_url, text=special_text),
        AdminMenuItem(is_active=cold_offers_active, href=cold_offers_url, text=cold_offers_text),
        AdminMenuItem(is_active=publish_active, href=publish_url, text=publish_text),
        AdminMenuItem(is_active=feedback_active, href=feedback_url, text=feedback_text, notifications=feedback_notifications),
    ]
