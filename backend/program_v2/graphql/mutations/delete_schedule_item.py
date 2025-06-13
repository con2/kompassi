import graphene
import graphene_pydantic
from django.db import transaction
from django.http import HttpRequest

from access.cbac import graphql_check_instance

from ...models.schedule_item import ScheduleItem
from ...models.schedule_item_dto import ScheduleItemDTO


class ScheduleItemInput(graphene_pydantic.PydanticInputObjectType):
    class Meta:
        model = ScheduleItemDTO


class DeleteScheduleItemInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    program_slug = graphene.String(required=True)
    schedule_item_slug = graphene.String(required=True)


class DeleteScheduleItem(graphene.Mutation):
    class Arguments:
        input = DeleteScheduleItemInput(required=True)

    slug = graphene.String()

    @transaction.atomic
    @staticmethod
    def mutate(root, info, input: DeleteScheduleItemInput):
        request: HttpRequest = info.context

        schedule_item = ScheduleItem.objects.select_for_update().get(
            program__event__slug=input.event_slug,
            program__slug=input.program_slug,
            slug=input.schedule_item_slug,
        )

        graphql_check_instance(
            schedule_item,
            request,
            field="schedule_items",
            operation="delete",
        )

        schedule_item.delete()

        return DeleteScheduleItem(slug=schedule_item.slug)  # type: ignore
