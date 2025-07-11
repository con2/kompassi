import logging
from collections.abc import Callable
from datetime import timedelta

from django.db import models
from django.utils.timezone import now
from oauth2_provider.models import AccessToken, RefreshToken

from event_log_v2.utils.emit import emit

logger = logging.getLogger("kompassi")

FilterFunction = Callable[[models.QuerySet], models.QuerySet]
CleanupModel = tuple[type[models.Model], FilterFunction]

_cleanup_models: list[CleanupModel] = []


def register_cleanup(filter_func: FilterFunction):
    """
    Decorator to mark a model for cleanup.
    The filter_func should return a queryset that filters out the objects to be deleted.
    """

    def decorator[T: type[models.Model]](cls: T) -> T:
        _cleanup_models.append((cls, filter_func))
        return cls

    return decorator


def perform_cleanup():
    """
    Perform cleanup on all models marked with the @register_cleanup decorator.
    This will delete objects that match the filter functions defined in the decorators.
    """
    logger.info("Performing cleanup on models registered with @register_cleanup.")
    for Model, filter_func in _cleanup_models:
        queryset = Model.objects.all()
        queryset = filter_func(queryset)
        _, deleted = queryset.delete()
        if deleted:
            emit(
                "core.cleanup.performed",
                model_name=Model.__name__,
                deleted=deleted,
            )
    logger.info("Cleanup completed.")


def cleanup_oauth_provider_accesstoken(queryset: models.QuerySet[AccessToken]) -> models.QuerySet[AccessToken]:
    return queryset.filter(expires__lt=now())


def cleanup_oauth_provider_refreshtoken(queryset: models.QuerySet[RefreshToken]) -> models.QuerySet[RefreshToken]:
    return queryset.filter(created__lt=now() - timedelta(days=60))


# python manage.py cleartokens doesn't seem to do the needful
register_cleanup(cleanup_oauth_provider_accesstoken)(AccessToken)
register_cleanup(cleanup_oauth_provider_refreshtoken)(RefreshToken)
