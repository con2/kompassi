import graphene
from django.http import HttpRequest
from django.urls import reverse
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType

from core.utils.text_utils import normalize_whitespace

from ..models import Program

# imported for side effects (register object type used by django object type fields)
from .schedule import ScheduleItemType  # noqa: F401


class ProgramType(DjangoObjectType):
    cached_dimensions = graphene.Field(GenericScalar)

    @staticmethod
    def resolve_cached_hosts(parent: Program, info):
        return parent.other_fields.get("formatted_hosts", "")

    cached_hosts = graphene.NonNull(graphene.String)

    @staticmethod
    def resolve_signup_link(parent: Program, info):
        return parent.other_fields.get("signup_link", "")

    signup_link = graphene.NonNull(graphene.String)

    @staticmethod
    def resolve_calendar_export_link(program: Program, info):
        """
        Returns a link to download this program as a calendar file.
        """
        request: HttpRequest = info.context
        return request.build_absolute_uri(
            reverse(
                "program_v2:single_program_calendar_export_view",
                kwargs=dict(
                    event_slug=program.event.slug,
                    program_slug=program.slug,
                ),
            )
        )

    calendar_export_link = graphene.NonNull(
        graphene.String,
        description=normalize_whitespace(resolve_calendar_export_link.__doc__ or ""),
    )

    class Meta:
        model = Program
        fields = ("title", "slug", "description", "dimensions", "cached_dimensions", "schedule_items")
