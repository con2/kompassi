import graphene

from ...models.program import Program
from ...models.schedule_item import ScheduleItem


class FavoriteInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    program_slug = graphene.String(required=True)


class MarkProgramAsFavorite(graphene.Mutation):
    """
    Deprecated. Use MarkScheduleItemAsFavorite instead.
    """

    class Arguments:
        input = graphene.NonNull(FavoriteInput)

    success = graphene.NonNull(graphene.Boolean)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception("User not authenticated")

        program = Program.objects.get(event__slug=input.event_slug, slug=input.program_slug)
        for schedule_item in program.schedule_items.all():
            schedule_item.favorited_by.add(info.context.user)

        return MarkProgramAsFavorite(success=True)  # type: ignore


class UnmarkProgramAsFavorite(graphene.Mutation):
    """
    Deprecated. Use UnmarkScheduleItemAsFavorite instead.
    """

    class Arguments:
        input = graphene.NonNull(FavoriteInput)

    success = graphene.NonNull(graphene.Boolean)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception("User not authenticated")

        program = Program.objects.get(event__slug=input.event_slug, slug=input.program_slug)
        for schedule_item in program.schedule_items.all():
            schedule_item.favorited_by.remove(info.context.user)

        return MarkProgramAsFavorite(success=True)  # type: ignore


class FavoriteScheduleItemInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    schedule_item_slug = graphene.String(required=True)


class MarkScheduleItemAsFavorite(graphene.Mutation):
    class Arguments:
        input = graphene.NonNull(FavoriteScheduleItemInput)

    success = graphene.NonNull(graphene.Boolean)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception("User not authenticated")

        schedule_item = ScheduleItem.objects.get(cached_event__slug=input.event_slug, slug=input.schedule_item_slug)
        schedule_item.favorited_by.add(info.context.user)

        return MarkScheduleItemAsFavorite(success=True)  # type: ignore


class UnmarkScheduleItemAsFavorite(graphene.Mutation):
    class Arguments:
        input = graphene.NonNull(FavoriteScheduleItemInput)

    success = graphene.NonNull(graphene.Boolean)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception("User not authenticated")

        schedule_item = ScheduleItem.objects.get(cached_event__slug=input.event_slug, slug=input.schedule_item_slug)
        schedule_item.favorited_by.remove(info.context.user)

        return MarkScheduleItemAsFavorite(success=True)  # type: ignore
