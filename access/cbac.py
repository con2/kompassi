import logging

from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AbstractUser

from functools import wraps

from .models.cbac_entry import CBACEntry, Claims


logger = logging.getLogger("kompassi")


class CBACPermissionDenied(PermissionDenied):
    def __init__(self, attempted_claims):
        super()
        self.attempted_claims = attempted_claims


def get_default_claims(request):
    claims = {}

    # from core.middleware.EventOrganizationMiddleware
    if event := getattr(request, 'event'):
        claims['event'] = event.slug
    if organization := getattr(request, 'organization'):
        claims['organization'] = organization.slug

    # from Django router
    claims['method'] = request.method
    claims['path'] = request.path

    if url_name := request.resolver_match.url_name:
        claims['view'] = url_name
    if app_name := request.resolver_match.app_name:
        claims['app'] = app_name

    return claims


def check_claims(user: AbstractUser, claims: Claims):
    logger.debug("CBAC: Checking permissions: user=%r, claims=%s", user.username, claims)
    if not CBACEntry.is_allowed(user, claims):
        logger.warning("CBAC: Permission denied: user=%r, claims=%r", user.username, claims)
        raise CBACPermissionDenied(claims)


def default_cbac_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapped_view(request, *args, **kwargs):
        claims = get_default_claims(request)
        check_claims(request.user, claims)

        return view_func(request, *args, **kwargs)
    return wrapped_view
