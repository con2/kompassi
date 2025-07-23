import graphene
from django.http import HttpRequest

from kompassi.dimensions.models.dimension_value import DimensionValue


class DeleteDimensionValueInput(graphene.InputObjectType):
    scope_slug = graphene.String(required=True)
    universe_slug = graphene.String(required=True)
    dimension_slug = graphene.String(required=True)
    value_slug = graphene.String(required=True)


class DeleteDimensionValue(graphene.Mutation):
    class Arguments:
        input = DeleteDimensionValueInput(required=True)

    slug = graphene.Field(graphene.String)

    @staticmethod
    def mutate(
        root,
        info,
        input: DeleteDimensionValueInput,
    ):
        request: HttpRequest = info.context

        value = DimensionValue.objects.get(
            dimension__universe__scope__slug=input.scope_slug,
            dimension__universe__slug=input.universe_slug,
            dimension__slug=input.dimension_slug,
            slug=input.value_slug,
        )

        if not value.can_be_deleted_by(request):
            raise Exception("Cannot remove dimension value")

        value.delete()

        return DeleteDimensionValue(slug=input.value_slug)  # type: ignore
