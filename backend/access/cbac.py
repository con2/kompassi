import logging
from functools import wraps
from typing import TYPE_CHECKING, Callable, Literal, Protocol

from django.contrib.auth.decorators import login_required
from django.db import models

from event_log.utils import emit

from .exceptions import CBACPermissionDenied
from .models.cbac_entry import CBACEntry, Claims

if TYPE_CHECKING:
    from core.models.event import Event


logger = logging.getLogger("kompassi")


def get_default_claims(request, **overrides: str):
    claims = {}

    # from core.middleware.EventOrganizationMiddleware
    if event := request.event:
        claims["event"] = event.slug
    if organization := request.organization:
        claims["organization"] = organization.slug

    # from Django router
    claims["method"] = request.method
    claims["path"] = request.path

    if url_name := request.resolver_match.url_name:
        claims["view"] = url_name
    if app_name := request.resolver_match.app_name:
        claims["app"] = app_name

    claims.update(overrides)

    return claims


def default_cbac_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapped_view(request, *args, **kwargs):
        claims = get_default_claims(request)
        user = request.user

        logger.debug("CBAC: Checking permissions: user=%r, claims=%s", user.username, claims)
        if not CBACEntry.is_allowed(user, claims):
            logger.warning("CBAC: Permission denied: user=%r, claims=%r", user.username, claims)
            emit("access.cbac.denied", request=request, other_fields={"claims": claims})
            raise CBACPermissionDenied(claims)

        return view_func(request, *args, **kwargs)

    return wrapped_view


def make_graphql_claims(
    *,
    event: "Event",
    operation: Literal["query"] | Literal["mutation"],
    app: str,
    object_type: str,
    field: str,
    **extra: str,
) -> Claims:
    return dict(
        event=event.slug,
        organization=event.organization.slug,
        operation=operation,
        app=app,
        object_type=object_type,
        field=field,
        view="graphql",
        **extra,
    )


def is_graphql_allowed(
    user,
    *,
    event: "Event",
    operation: Literal["query"] | Literal["mutation"],
    app: str,
    object_type: str,
    field: str,
    **extra: str,
):
    claims = make_graphql_claims(
        event=event,
        operation=operation,
        app=app,
        object_type=object_type,
        field=field,
        **extra,
    )

    return CBACEntry.is_allowed(user, claims), claims


class HasEventProperty(Protocol):
    event: "Event"


class HasEventForeignKey(Protocol):
    event: models.ForeignKey["Event"]


def is_graphql_allowed_for_model(
    user,
    *,
    instance: HasEventProperty | HasEventForeignKey,
    operation: Literal["query"] | Literal["mutation"],
    field: str,
    **extra: str,
):
    event = instance.event
    object_type = instance.__class__.__name__
    app = instance.__class__._meta.app_label  # type: ignore

    return is_graphql_allowed(
        user,
        event=event,  # type: ignore
        operation=operation,
        app=app,
        object_type=object_type,
        field=field,
        **extra,
    )


def graphql_check_access(instance, info, field: str):
    user = info.context.user
    operation = "query"
    extra = dict(slug=instance.slug) if hasattr(instance, "slug") else {}

    allowed, claims = is_graphql_allowed_for_model(
        user,
        instance=instance,
        operation=operation,
        field=field,
        **extra,
    )
    if not allowed:
        emit(
            "access.cbac.denied",
            request=info.context,
            other_fields={"claims": claims},
        )

        raise Exception("Unauthorized")


def graphql_query_cbac_required(func: Callable):
    """
    Wrap a field resolver with this function to make it
    require CBAC permissions.

    The object type must be a Django object type.
    """

    @wraps(func)
    def wrapper(instance, info, *args, **kwargs):
        # used instead of info.field_name because info.field_name is camel case
        field = func.__name__.removeprefix("resolve_")

        graphql_check_access(instance, info, field=field)
        return func(instance, info, *args, **kwargs)

    return wrapper
