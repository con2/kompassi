import graphene

from kompassi.core.middleware import RequestWithCache

from ...models.dimension import Dimension


class DeleteDimensionInput(graphene.InputObjectType):
    scope_slug = graphene.String(required=True)
    universe_slug = graphene.String(required=True)
    dimension_slug = graphene.String(required=True)


class DeleteDimension(graphene.Mutation):
    class Arguments:
        input = DeleteDimensionInput(required=True)

    slug = graphene.Field(graphene.String)

    @staticmethod
    def mutate(
        root,
        info,
        input: DeleteDimensionInput,
    ):
        request: RequestWithCache = info.context

        dimension = Dimension.objects.get(
            universe__scope__slug=input.scope_slug,
            universe__slug=input.universe_slug,
            slug=input.dimension_slug,
        )

        if not dimension.can_be_deleted_by(request):
            raise Exception("Cannot remove dimension")

        dimension.delete()

        return DeleteDimension(slug=input.dimension_slug)  # type: ignore
