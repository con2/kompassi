from functools import wraps

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _

from core.models import Organization
from core.utils import login_redirect


def directory_organization_required(view_func):
    @wraps(view_func)
    def wrapper(request, organization_slug, *args, **kwargs):
        organization = get_object_or_404(Organization, slug=organization_slug)
        meta = organization.directory_organization_meta

        if not meta:
            messages.error(request, _('This organization does not use the directory.'))
            return redirect('core_organization_view', organization.slug)

        return view_func(request, organization, *args, **kwargs)
    return wrapper


def directory_access_required(view_func):
    @wraps(view_func)
    def wrapper(request, organization_slug, *args, **kwargs):
        organization = get_object_or_404(Organization, slug=organization_slug)
        meta = organization.directory_organization_meta

        if not meta:
            messages.error(request, _('This organization does not use the directory.'))
            return redirect('core_organization_view', organization.slug)

        if not request.user.is_authenticated:
            return login_redirect(request)

        if not meta.is_user_allowed_to_access(request.user):
            messages.error(request, _('You do not have access to the directory.'))
            return redirect('core_organization_view', organization.slug)

        vars = dict(
            organization=organization,
            meta=meta,
            admin_title=_('Directory'),
        )

        return view_func(request, vars, organization, *args, **kwargs)
    return wrapper
