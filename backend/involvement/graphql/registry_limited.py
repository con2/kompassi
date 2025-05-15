import graphene
import graphene_django

from graphql_api.utils import resolve_localized_field_getattr

from ..models.registry import Registry


class LimitedRegistryType(graphene_django.DjangoObjectType):
    """
    Represent Registry (and the Event involved) without a way to traverse back to Event.
    """

    class Meta:
        model = Registry
        fields = ("slug", "created_at", "updated_at", "profile_field_selector")

    resolve_title = resolve_localized_field_getattr("title")
    title = graphene.NonNull(graphene.String)

    resolve_policy_url = resolve_localized_field_getattr("policy_url")
    policy_url = graphene.NonNull(graphene.String)
