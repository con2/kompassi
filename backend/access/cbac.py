import logging
from collections.abc import Callable
from enum import Enum
from functools import wraps
from typing import Literal, Protocol

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from graphene import ResolveInfo

from core.utils.view_utils import get_event_and_organization
from dimensions.models.scope import Scope
from event_log_v2.utils.emit import emit

from .exceptions import CBACPermissionDenied
from .models.cbac_entry import CBACEntry, Claims

logger = logging.getLogger("kompassi")
Operation = Literal["query", "create", "update", "delete", "put"]


def get_default_claims(request, **overrides: str):
    claims = {}

    event, organization = get_event_and_organization(request)
    if event:
        claims["event"] = event.slug
    if organization:
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
    scope: Scope,
    operation: Operation,
    app: str | Enum,
    model: str,
    field: str,
    **extra: str,
) -> Claims:
    # event and organization
    extra.update(scope.cbac_claims)

    if hasattr(app, "app_name"):
        # InvolvementApp etc. that skip the _v2 madness
        app_name = app.app_name  # type: ignore
    elif isinstance(app, Enum):
        app_name = app.value
    else:
        app_name = app

    return dict(
        operation=operation,
        app=app_name,
        model=model,
        field=field,
        view="graphql",
        **extra,
    )


def is_graphql_allowed(
    user,
    *,
    scope: Scope,
    operation: Operation,
    app: str | Enum,
    model: str,
    field: str = "self",
    **extra: str,
) -> bool:
    claims = make_graphql_claims(
        scope=scope,
        operation=operation,
        app=app,
        model=model,
        field=field,
        **extra,
    )

    return CBACEntry.is_allowed(user, claims)


class HasScope(Protocol):
    scope: Scope


class HasImmutableScope(Protocol):
    @property
    def scope(self) -> Scope: ...


def is_graphql_allowed_for_model(
    user,
    *,
    instance: HasScope | HasImmutableScope,
    operation: Operation,
    field: str = "self",
    app: str | Enum = "",
    **extra: str,
) -> bool:
    model_name = instance.__class__.__name__
    if not app:
        app = instance.__class__._meta.app_label  # type: ignore
    slug = getattr(instance, "slug", None)
    extra = dict(slug=slug) if slug is not None else {}

    claims = make_graphql_claims(
        scope=instance.scope,
        operation=operation,
        app=app,
        model=model_name,
        field=field,
        **extra,
    )

    return CBACEntry.is_allowed(user, claims)


def graphql_check_model(
    model,
    scope: Scope,
    info: ResolveInfo | HttpRequest,
    *,
    field: str = "self",
    operation: Operation = "query",
    app: str | Enum = "",
):
    request: HttpRequest = info.context if isinstance(info, ResolveInfo) else info
    if not app:
        app = model._meta.app_label

    claims = make_graphql_claims(
        scope=scope,
        operation=operation,
        app=app,
        model=model.__name__,
        field=field,
    )

    if not CBACEntry.is_allowed(request.user, claims):
        emit(
            "access.cbac.denied",
            request=request,
            other_fields={"claims": claims},
        )

        raise CBACPermissionDenied(claims)


def graphql_check_instance(
    instance: HasScope | HasImmutableScope,
    info: ResolveInfo | HttpRequest,
    *,
    field: str = "self",
    operation: Operation = "query",
    app: str | Enum = "",
):
    """
    Check that the user has access to a single object. Pass "self" as the field
    for operations targeting the entire model instance.
    """
    request: HttpRequest = info.context if isinstance(info, ResolveInfo) else info
    model_name = instance.__class__.__name__
    if not app:
        app = instance.__class__._meta.app_label  # type: ignore
    slug = getattr(instance, "slug", None)
    extra = dict(slug=slug) if slug is not None else {}

    claims = make_graphql_claims(
        scope=instance.scope,
        operation=operation,
        app=app,
        model=model_name,
        field=field,
        **extra,
    )

    if not CBACEntry.is_allowed(request.user, claims):
        emit(
            "access.cbac.denied",
            request=request,
            other_fields={"claims": claims},
        )

        raise CBACPermissionDenied(claims)


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

        graphql_check_instance(instance, info, field=field)
        return func(instance, info, *args, **kwargs)

    return wrapper
