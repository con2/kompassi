import graphene
import graphene_pydantic
from django.db import transaction
from django.http import HttpRequest

from kompassi.access.cbac import graphql_check_instance

from ...models import Program
from ...models.schedule_item_dto import ScheduleItemDTO
from ..schedule_item_full import FullScheduleItemType


class ScheduleItemInput(graphene_pydantic.PydanticInputObjectType):
    class Meta:
        model = ScheduleItemDTO


class PutScheduleItemInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    program_slug = graphene.String(required=True)
    schedule_item = graphene.Argument(ScheduleItemInput, required=True)


class PutScheduleItem(graphene.Mutation):
    class Arguments:
        input = PutScheduleItemInput(required=True)

    schedule_item = graphene.Field(FullScheduleItemType)

    @transaction.atomic
    @staticmethod
    def mutate(root, info, input: PutScheduleItemInput):
        request: HttpRequest = info.context

        program = Program.objects.select_for_update(of=("self",), no_key=True).get(
            event__slug=input.event_slug,
            slug=input.program_slug,
        )

        graphql_check_instance(
            program,
            request,
            field="schedule_items",
            operation="update",
        )

        schedule_item_dto: ScheduleItemDTO = ScheduleItemDTO.model_validate(
            input.schedule_item,
            from_attributes=True,
        )
        schedule_item = schedule_item_dto.save(program)

        return PutScheduleItem(schedule_item=schedule_item)  # type: ignore
