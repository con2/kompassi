from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from core.admin_menus import AdminMenuItem
from core.utils import url

from ..models import Invitation, Programme, ProgrammeFeedback


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

    mail_url = url("programme:admin_mail_view", event.slug)
    mail_active = request.path.startswith(mail_url)
    mail_text = _("Mass messages")

    feedback_url = url("programme:admin_feedback_view", event.slug)
    feedback_active = request.path == feedback_url
    feedback_text = _("Programme feedback")
    feedback_notifications = ProgrammeFeedback.objects.filter(
        programme__category__event=event, hidden_at__isnull=True
    ).count()

    schedule_url = event.programme_event_meta.schedule_link
    schedule_active = False
    schedule_text = _("Schedule") + "…"

    menu_items = [
        AdminMenuItem(is_active=organizers_active, href=organizers_url, text=organizers_text),
        AdminMenuItem(is_active=offers_active, href=offers_url, text=offers_text, notifications=offers_notifications),
        AdminMenuItem(
            is_active=invitations_active,
            href=invitations_url,
            text=invitations_text,
            notifications=invitations_notifications,
        ),
        AdminMenuItem(is_active=mail_active, href=mail_url, text=mail_text),
        AdminMenuItem(
            is_active=feedback_active, href=feedback_url, text=feedback_text, notifications=feedback_notifications
        ),
    ]

    if schedule_url:
        menu_items.append(AdminMenuItem(is_active=schedule_active, href=schedule_url, text=schedule_text))

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
            reservations_active,
            mail_active,
        )
    )
    index_text = "Ohjelmaluettelo"

    menu_items.insert(0, AdminMenuItem(is_active=index_active, href=index_url, text=index_text))

    return menu_items
