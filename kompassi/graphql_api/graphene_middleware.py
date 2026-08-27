import logging

from django.core.exceptions import ObjectDoesNotExist
from graphql import GraphQLError

from .errors import NOT_FOUND

logger = logging.getLogger(__name__)


class LoggingErrorsMiddleware:
    """
    Graphene-django will, by default, swallow errors. This middleware logs them.
    NOTE: Graphene middleware, not Django middleware
    """

    def resolve(self, next, root, info, **args):
        try:
            return next(root, info, **args)
        except Exception:
            logger.warning("Error occurred in GraphQL execution:", exc_info=True)
            raise


class NotFoundMiddleware:
    """
    Translates an unguarded `Model.objects.get(...)` raising ObjectDoesNotExist (as many
    mutations do, eg. Event.objects.get(slug=...) or Order.objects.get(...)) into a
    GraphQLError carrying a machine-readable extensions.code, so the frontend can branch
    on it (notFound()) instead of treating it as an unexpected crash.

    A resolver that already catches DoesNotExist itself (eg. to return None) is
    unaffected - the exception never reaches this middleware.
    """

    def resolve(self, next, root, info, **args):
        try:
            return next(root, info, **args)
        except ObjectDoesNotExist as e:
            raise GraphQLError("Not found", extensions={"code": NOT_FOUND}) from e
