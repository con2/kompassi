from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_safe

from event_log_v2.utils.emit import emit

from ..models import Person
from ..utils import get_next
from .login_views import do_login


@user_passes_test(lambda user: user.is_superuser)  # type: ignore
@require_safe
def core_admin_impersonate_view(request, username):
    user = get_object_or_404(get_user_model(), username=username)

    try:
        person = user.person  # type: ignore
    except Person.DoesNotExist:
        person = None

    emit("core.person.impersonated", request=request, person=person.pk if person else None)

    next = get_next(request)

    messages.warning(
        request,
        "Käytät nyt Kompassia toisen käyttäjän oikeuksilla. Tämän toiminnon käyttö on sallittua "
        "ainoastaan sellaisiin ylläpitotoimenpiteisiin, joiden hoitaminen ylläpitotunnuksilla on "
        "muuten tarpeettoman työlästä tai hankalaa. Muista kirjautua ulos, kun olet saanut "
        "ylläpitotoimenpiteet hoidettua.",
    )

    return do_login(request, user, next=next, backend="django.contrib.auth.backends.ModelBackend")


def organization_admin_menu_items(request, organization):
    items = []

    if "membership" in settings.INSTALLED_APPS and organization.membership_organization_meta is not None:
        from membership.views.membership_admin_menu_items import membership_admin_menu_items

        items.extend(membership_admin_menu_items(request, organization))

    if "access" in settings.INSTALLED_APPS and organization.access_organization_meta is not None:
        from access.views import access_admin_menu_items

        items.extend(access_admin_menu_items(request, organization))

    return items
