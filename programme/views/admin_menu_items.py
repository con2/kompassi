from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

from core.utils import url
from core.admin_menus import AdminMenuItem

from ..models import Invitation, ProgrammeFeedback, Programme


def programme_admin_menu_items(request, event):
    t = now()

    organizers_url = url("programme:admin_organizers_view", event.slug)
    organizers_active = request.path.startswith(organizers_url)
    organizers_text = _("Programme hosts")

    offers_url = url("programme:admin_view", event.slug) + "?state=offered&sort=created_at"
    offers_active = request.get_full_path() == offers_url
    offers_text = _("New offers")
    offers_notifications = Programme.objects.filter(category__event=event, state="offered").count()

    invitations_url = url("programme:admin_invitations_view", event.slug)
    invitations_active = request.path == invitations_url
    invitations_text = _("Open invitations")
    invitations_notifications = Invitation.objects.filter(programme__category__event=event, state="valid").count()

    rooms_url = url("programme:admin_rooms_view", event.slug)
    rooms_active = request.path.startswith(rooms_url)
    rooms_text = _("Edit rooms")

    schedule_url = url("programme:admin_schedule_view", event.slug)
    schedule_active = request.path.startswith(schedule_url)
    schedule_text = _("Edit schedule")

    special_url = url("programme:admin_special_view", event.slug)
    special_active = request.path == special_url
    special_text = "Ohjelmakartan ulkopuolisten esikatselu"

    cold_offers_url = url("programme:admin_cold_offers_view", event.slug)
    cold_offers_active = request.path == cold_offers_url
    cold_offers_text = _("Cold offer period starting and ending times")

    publish_url = url("programme:admin_publish_view", event.slug)
    publish_active = request.path == publish_url
    publish_text = _("Publish schedule")

    mail_url = url("programme:admin_mail_view", event.slug)
    mail_active = request.path.startswith(mail_url)
    mail_text = _("Mass messages")

    feedback_url = url("programme:admin_feedback_view", event.slug)
    feedback_active = request.path == feedback_url
    feedback_text = _("Programme feedback")
    feedback_notifications = ProgrammeFeedback.objects.filter(
        programme__category__event=event, hidden_at__isnull=True
    ).count()

    menu_items = [
        AdminMenuItem(is_active=organizers_active, href=organizers_url, text=organizers_text),
        AdminMenuItem(is_active=offers_active, href=offers_url, text=offers_text, notifications=offers_notifications),
        AdminMenuItem(
            is_active=invitations_active,
            href=invitations_url,
            text=invitations_text,
            notifications=invitations_notifications,
        ),
        AdminMenuItem(is_active=rooms_active, href=rooms_url, text=rooms_text),
        AdminMenuItem(is_active=schedule_active, href=schedule_url, text=schedule_text),
        AdminMenuItem(is_active=special_active, href=special_url, text=special_text),
        AdminMenuItem(is_active=cold_offers_active, href=cold_offers_url, text=cold_offers_text),
        AdminMenuItem(is_active=publish_active, href=publish_url, text=publish_text),
        AdminMenuItem(is_active=mail_active, href=mail_url, text=mail_text),
        AdminMenuItem(
            is_active=feedback_active, href=feedback_url, text=feedback_text, notifications=feedback_notifications
        ),
    ]

    programmes_with_reservations = Programme.objects.filter(category__event=event, is_using_paikkala=True)
    if programmes_with_reservations.exists():
        reservations_url = url("programme:admin_reservation_status_view", event.slug)
        reservations_active = request.path == reservations_url
        reservations_text = _("Seat reservations")
        reservations_notifications = programmes_with_reservations.filter(
            paikkala_program__reservation_start__lte=t,
            paikkala_program__reservation_end__gt=t,
        ).count()

        menu_items.append(
            AdminMenuItem(
                is_active=reservations_active,
                href=reservations_url,
                text=reservations_text,
                notifications=reservations_notifications,
            )
        )
    else:
        reservations_active = False

    index_url = url("programme:admin_view", event.slug)
    index_active = request.path.startswith(index_url) and not any(
        (
            organizers_active,
            feedback_active,
            invitations_active,
            offers_active,
            cold_offers_active,
            publish_active,
            rooms_active,
            schedule_active,
            special_active,
            reservations_active,
            mail_active,
        )
    )
    index_text = "Ohjelmaluettelo"

    menu_items.insert(0, AdminMenuItem(is_active=index_active, href=index_url, text=index_text))

    return menu_items
