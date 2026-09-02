import graphene
import graphene_django
from django.utils.duration import duration_iso_string

from kompassi.core.graphql.organization_limited import LimitedOrganizationType
from kompassi.core.models.organization import Organization
from kompassi.core.utils import normalize_whitespace
from kompassi.graphql_api.utils import resolve_localized_field_getattr

from ..models.registry import Registry


class LimitedRegistryType(graphene_django.DjangoObjectType):
    class Meta:
        model = Registry
        fields = (
            "slug",
            "created_at",
            "updated_at",
        )

    @staticmethod
    def resolve_organization(registry: Registry, info) -> Organization:
        # HACK To separate the root scope from the proper Tracon ry scope,
        # the root scope has organization=None.
        # We still want to show the root scope as belonging to Tracon ry.
        if registry.scope.organization is None:
            return Organization.objects.get(slug="tracon-ry")
        return registry.scope.organization

    organization = graphene.NonNull(LimitedOrganizationType)

    resolve_title = resolve_localized_field_getattr("title")
    title = graphene.NonNull(graphene.String, lang=graphene.String())

    resolve_policy_url = resolve_localized_field_getattr("policy_url")
    policy_url = graphene.NonNull(graphene.String, lang=graphene.String())

    @staticmethod
    def resolve_default_retention_period(registry: Registry, info) -> str | None:
        """
        The default retention period for personal data in this registry as an ISO 8601 duration.
        Null means personal data in this registry is retained indefinitely.
        """
        if registry.default_retention_period is None:
            return None
        return duration_iso_string(registry.default_retention_period)

    default_retention_period = graphene.Field(
        graphene.String,
        description=normalize_whitespace(resolve_default_retention_period.__doc__ or ""),
    )
