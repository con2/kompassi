from django.utils.translation import gettext_lazy as _

from core.utils import url


def programme_profile_menu_items(request):
    programme_url = url("programme:profile_view")
    programme_active = request.path.startswith(programme_url)
    programme_text = _("Programmes")

    reservations_url = url("programme:profile_reservations_view")
    reservations_active = request.path.startswith(reservations_url)
    reservations_text = _("Seat reservations")

    return [
        (programme_active, programme_url, programme_text),
        (reservations_active, reservations_url, reservations_text),
    ]
