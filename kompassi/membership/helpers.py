from functools import wraps

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

from kompassi.core.helpers import person_required

from .models import Membership


def membership_admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, organization_slug, *args, **kwargs):
        from kompassi.core.models import Organization
        from kompassi.core.utils import login_redirect
        from kompassi.core.views.admin_views import organization_admin_menu_items

        organization = get_object_or_404(Organization, slug=organization_slug)
        meta = organization.membership_organization_meta

        if not meta:
            messages.error(request, "Tämä organisaatio ei käytä Kompassia jäsenrekisterin hallintaan.")
            return redirect("core_organization_view", organization.slug)

        if not organization.membership_organization_meta.is_user_admin(request.user):
            return login_redirect(request)

        vars = dict(
            organization=organization,
            admin_menu_items=organization_admin_menu_items(request, organization),
            admin_title="Jäsenrekisterin ylläpito",
        )

        return view_func(request, vars, organization, *args, **kwargs)

    return wrapper


def membership_organization_required(view_func):
    @wraps(view_func)
    def wrapper(request, organization_slug, *args, **kwargs):
        from kompassi.core.models import Organization

        organization = get_object_or_404(Organization, slug=organization_slug)
        meta = organization.membership_organization_meta

        if not meta:
            messages.error(request, "Tämä organisaatio ei käytä Kompassia jäsenrekisterin hallintaan.")
            return redirect("core_organization_view", organization.slug)

        return view_func(request, organization, *args, **kwargs)

    return wrapper


def membership_required(view_func):
    @wraps(view_func)
    @person_required
    def wrapper(request, organization_slug, *args, **kwargs):
        from kompassi.core.models import Organization

        organization = get_object_or_404(Organization, slug=organization_slug)
        meta = organization.membership_organization_meta

        if not meta:
            messages.error(request, "Tämä organisaatio ei käytä Kompassia jäsenrekisterin hallintaan.")
            return redirect("core_organization_view", organization.slug)

        try:
            membership = Membership.objects.get(organization=organization, person=request.user.person)
        except Membership.DoesNotExist:
            messages.error(request, "Et ole tämän organisaation jäsen.")
            return redirect("core_organization_view", organization.slug)

        return view_func(request, membership, *args, **kwargs)

    return wrapper
