import graphene
from django.http import HttpRequest

from ..models.registry import Registry
from .registry_limited import LimitedRegistryType


class FullRegistryType(LimitedRegistryType):
    class Meta:
        model = Registry
        fields = (
            "slug",
            "created_at",
            "updated_at",
            # NOTE SUPPORTED_LANGUAGES
            "title_en",
            "title_fi",
            "title_sv",
            "policy_url_en",
            "policy_url_fi",
            "policy_url_sv",
        )

    @staticmethod
    def resolve_can_remove(registry: Registry, info):
        """
        Whether the current user can delete this registry. A registry that is still
        referenced by any involvement, survey, badge, or event meta cannot be deleted.
        """
        request: HttpRequest = info.context
        return registry.can_be_deleted_by(request)

    can_remove = graphene.NonNull(graphene.Boolean)
