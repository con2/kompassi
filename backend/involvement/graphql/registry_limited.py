import graphene
import graphene_django

from core.graphql.organization_limited import LimitedOrganizationType
from core.models.organization import Organization
from graphql_api.utils import resolve_localized_field_getattr

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
