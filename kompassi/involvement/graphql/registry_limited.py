import graphene
import graphene_django

from kompassi.core.graphql.organization_limited import LimitedOrganizationType
from kompassi.core.models.organization import Organization
from kompassi.core.utils import normalize_whitespace
from kompassi.core.utils.retention_period import timedelta_to_days
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
    def resolve_default_retention_period_days(registry: Registry, info) -> int | None:
        """
        The default retention period for personal data in this registry, in days.
        Null means personal data in this registry is retained indefinitely.
        """
        return timedelta_to_days(registry.default_retention_period)

    default_retention_period_days = graphene.Field(
        graphene.Int,
        description=normalize_whitespace(resolve_default_retention_period_days.__doc__ or ""),
    )
