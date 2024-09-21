from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from .models import Organization, Person
from .utils import event_meta_property, login_redirect  # noqa: F401


def person_required(view_func):
    @login_required
    @wraps(view_func)
    def inner(request, *args, **kwargs):
        try:
            person = request.user.person  # noqa: F841
        except Person.DoesNotExist:
            return login_redirect(request, view="core_personify_view")

        return view_func(request, *args, **kwargs)

    return inner


def public_organization_required(view_func):
    @wraps(view_func)
    def wrapper(request, organization_slug, *args, **kwargs):
        if request.user.is_staff:
            organization = get_object_or_404(Organization, slug=organization_slug)
            if not organization.public:
                messages.warning(request, "Tämä yhdistys ei ole julkinen. Tämä sivu ei näy tavallisille käyttäjille.")
        else:
            organization = get_object_or_404(Organization, slug=organization_slug, public=True)

        return view_func(request, organization, *args, **kwargs)

    return wrapper
