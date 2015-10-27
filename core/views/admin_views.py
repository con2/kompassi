# encoding: utf-8

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_GET

from ..utils import get_next
from .login_views import do_login


@user_passes_test(lambda user: user.is_superuser)
@require_GET
def core_admin_impersonate_view(request, username):
    next = get_next(request)
    user = authenticate(username=username) # look, no password

    messages.warning(request,
        u'Käytät nyt Kompassia toisen käyttäjän oikeuksilla. Tämän toiminnon käyttö on sallittua '
        u'ainoastaan sellaisiin ylläpitotoimenpiteisiin, joiden hoitaminen ylläpitotunnuksilla on '
        u'muuten tarpeettoman työlästä tai hankalaa. Muista kirjautua ulos, kun olet saanut '
        u'ylläpitotoimenpiteet hoidettua.'
    )

    return do_login(request, user, password=None, next=next)


def organization_admin_menu_items(request, organization):
    items = []

    if 'membership' in settings.INSTALLED_APPS and organization.membership_organization_meta is not None:
        from membership.views.admin_views import membership_admin_menu_items
        items.extend(membership_admin_menu_items(request, organization))

    if 'access' in settings.INSTALLED_APPS and organization.access_organization_meta is not None:
        from access.views import access_admin_menu_items
        items.extend(access_admin_menu_items(request, organization))

    return items