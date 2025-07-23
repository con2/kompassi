from django.utils.translation import gettext_lazy as _

from kompassi.core.admin_menus import AdminMenuItem
from kompassi.core.utils import url


def labour_admin_menu_items(request, event):
    dashboard_url = url("labour:admin_dashboard_view", event.slug)
    dashboard_active = request.path == dashboard_url
    dashboard_text = _("Dashboard")

    signups_url = url("labour:admin_signups_view", event.slug)
    signups_active = request.path.startswith(signups_url)
    signups_text = _("Applications")

    mail_url = url("labour:admin_mail_view", event.slug)
    mail_active = request.path.startswith(mail_url)
    mail_text = _("Mass messages")

    roster_url = url("labour:admin_roster_view", event.slug)
    roster_active = request.path.startswith(roster_url)
    roster_text = _("Shift planning")

    shifts_url = url("labour:admin_shifts_view", event.slug)
    shifts_active = request.path.startswith(shifts_url)
    shifts_text = _("Shift lists")

    jobcategories_url = url("labour:admin_jobcategories_view", event.slug)
    jobcategories_active = request.path.startswith(jobcategories_url)
    jobcategories_text = _("Edit job categories")

    startstop_url = url("labour:admin_startstop_view", event.slug)
    startstop_active = request.path == startstop_url
    startstop_text = _("Application period")

    menu_items = [
        (dashboard_active, dashboard_url, dashboard_text),
        (signups_active, signups_url, signups_text),
        (mail_active, mail_url, mail_text),
        AdminMenuItem(
            is_active=roster_active,
            href=roster_url,
            text=roster_text,
            is_mobile_incompatible=True,
        ),
        AdminMenuItem(
            is_active=shifts_active,
            href=shifts_url,
            text=shifts_text,
        ),
        (jobcategories_active, jobcategories_url, jobcategories_text),
        (startstop_active, startstop_url, startstop_text),
    ]

    SignupExtra = event.labour_event_meta.signup_extra_model

    if SignupExtra and SignupExtra.get_shirt_size_field():
        shirts_url = url("labour:admin_shirts_view", event.slug)
        shirts_active = request.path == shirts_url
        shirts_text = _("Shirt sizes")

        menu_items.append((shirts_active, shirts_url, shirts_text))

    if SignupExtra and (SignupExtra.get_special_diet_field() or SignupExtra.get_special_diet_other_field()):
        special_diets_url = url("labour:admin_special_diets_view", event.slug)
        special_diets_active = request.path == special_diets_url
        special_diets_text = _("Special diets")

        menu_items.append((special_diets_active, special_diets_url, special_diets_text))

    return menu_items
