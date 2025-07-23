import graphene
from django.http import HttpRequest
from graphene_django import DjangoObjectType

from ..models.quota import Quota


class BareQuotaType(DjangoObjectType):
    class Meta:
        model = Quota
        fields = (
            "id",
            "name",
        )

    @staticmethod
    def resolve_count_total(quota: Quota, info):
        request: HttpRequest = info.context
        return quota.get_counters(request).count_total

    count_total = graphene.NonNull(graphene.Int)
