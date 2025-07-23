import graphene
from django.http import HttpRequest
from graphene_django import DjangoObjectType

from kompassi.core.utils.text_utils import normalize_whitespace

from ..models.quota import Quota


class LimitedQuotaType(DjangoObjectType):
    class Meta:
        model = Quota
        fields = (
            "id",
            "name",
        )

    @staticmethod
    def resolve_count_paid(quota: Quota, info):
        request: HttpRequest = info.context
        return quota.get_counters(request).count_paid

    count_paid = graphene.NonNull(graphene.Int)

    @staticmethod
    def resolve_count_reserved(quota: Quota, info):
        request: HttpRequest = info.context
        return quota.get_counters(request).count_reserved

    count_reserved = graphene.NonNull(graphene.Int)

    @staticmethod
    def resolve_count_available(quota: Quota, info):
        request: HttpRequest = info.context
        return quota.get_counters(request).count_available

    count_available = graphene.NonNull(graphene.Int)

    @staticmethod
    def resolve_count_total(quota: Quota, info):
        request: HttpRequest = info.context
        return quota.get_counters(request).count_total

    count_total = graphene.NonNull(graphene.Int)

    @staticmethod
    def resolve_can_delete(quota: Quota, info):
        """
        Returns true if the product can be deleted.
        A product can be deleted if it has not been sold at all.
        """
        request: HttpRequest = info.context
        return quota.can_be_deleted_by(request)

    can_delete = graphene.NonNull(
        graphene.Boolean,
        description=normalize_whitespace(resolve_can_delete.__doc__ or ""),
    )
