import logging

from django.urls import reverse

from kompassi.core.models import Person
from kompassi.core.utils import url

logger = logging.getLogger(__name__)


def access_admin_menu_items(request, organization):
    aliases_url = url("access_admin_aliases_view", organization.slug)
    aliases_active = request.path == aliases_url
    aliases_text = "Sähköpostialiakset"

    return [(aliases_active, aliases_url, aliases_text)]


def access_profile_menu_items(request):
    privileges_url = reverse("access_profile_privileges_view")
    privileges_active = request.path.startswith(privileges_url)
    privileges_text = "Käyttöoikeudet"

    items: list[tuple[bool, str, str]] = [
        (privileges_active, privileges_url, privileges_text),
    ]

    try:
        aliases_visible = request.user.person.email_aliases.exists()
    except Person.DoesNotExist:
        aliases_visible = False

    if aliases_visible:
        aliases_url = reverse("access_profile_aliases_view")
        aliases_active = request.path == aliases_url
        aliases_text = "Sähköpostialiakset"

        items.append((aliases_active, aliases_url, aliases_text))

    return items
