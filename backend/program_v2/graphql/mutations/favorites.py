import graphene

from ...models.program import Program


class FavoriteInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    program_slug = graphene.String(required=True)


class MarkProgramAsFavorite(graphene.Mutation):
    class Arguments:
        input = graphene.NonNull(FavoriteInput)

    success = graphene.NonNull(graphene.Boolean)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception("User not authenticated")

        program = Program.objects.get(event__slug=input.event_slug, slug=input.program_slug)
        program.favorited_by.add(info.context.user)

        return MarkProgramAsFavorite(success=True)  # type: ignore


class UnmarkProgramAsFavorite(graphene.Mutation):
    class Arguments:
        input = graphene.NonNull(FavoriteInput)

    success = graphene.NonNull(graphene.Boolean)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception("User not authenticated")

        program = Program.objects.get(event__slug=input.event_slug, slug=input.program_slug)
        program.favorited_by.remove(info.context.user)

        return MarkProgramAsFavorite(success=True)  # type: ignore
