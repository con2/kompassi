import logging

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
