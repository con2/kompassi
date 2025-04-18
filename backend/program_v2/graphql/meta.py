from datetime import datetime

import graphene
from django.http import HttpRequest
from django.urls import reverse
from graphene_django import DjangoObjectType

from access.cbac import graphql_check_instance, graphql_check_model
from core.models import Event
from core.utils.text_utils import normalize_whitespace
from dimensions.graphql.dimension import FullDimensionType
from dimensions.graphql.dimension_filter_input import DimensionFilterInput
from forms.graphql.response_full import FullResponseType
from forms.models.response import Response
from graphql_api.language import DEFAULT_LANGUAGE

from ..filters import ProgramFilters
from ..models import (
    Program,
    ProgramV2EventMeta,
    ScheduleItem,
)
from ..models.annotations import ANNOTATIONS
from ..models.meta import ProgramV2ProfileMeta
from .annotations import AnnotationSchemoidType
from .program_full import FullProgramType
from .schedule_item_full import FullScheduleItemType


class ProgramV2EventMetaType(DjangoObjectType):
    """
    NOTE: There is no `programForms` because a program form is a Survey with `app: PROGRAM_V2`.
    Use `event.forms.surveys(app: PROGRAM_V2)` for that instead.
    """

    class Meta:
        model = ProgramV2EventMeta
        fields = ("location_dimension",)

    @staticmethod
    def resolve_programs(
        meta: ProgramV2EventMeta,
        info,
        filters: list[DimensionFilterInput] | None = None,
        favorites_only: bool = False,
        hide_past: bool = False,
        updated_after: datetime | None = None,
    ):
        request: HttpRequest = info.context
        programs = Program.objects.filter(event=meta.event)
        return ProgramFilters.from_graphql(
            filters,
            favorites_only=favorites_only,
            hide_past=hide_past,
            updated_after=updated_after,
        ).filter_program(programs, user=request.user)

    programs = graphene.NonNull(
        graphene.List(graphene.NonNull(FullProgramType)),
        filters=graphene.List(DimensionFilterInput),
        favorites_only=graphene.Boolean(),
        hide_past=graphene.Boolean(),
        updated_after=graphene.DateTime(),
        description=normalize_whitespace(resolve_programs.__doc__ or ""),
    )

    @staticmethod
    def resolve_program(meta: ProgramV2EventMeta, info, slug: str):
        return Program.objects.get(event=meta.event, slug=slug)

    program = graphene.Field(FullProgramType, slug=graphene.String(required=True))

    @staticmethod
    def resolve_schedule_items(
        meta: ProgramV2EventMeta,
        info,
        filters: list[DimensionFilterInput] | None = None,
        favorites_only: bool = False,
        hide_past: bool = False,
        updated_after: datetime | None = None,
    ):
        request: HttpRequest = info.context
        return ProgramFilters.from_graphql(
            filters,
            favorites_only=favorites_only,
            hide_past=hide_past,
            updated_after=updated_after,
        ).filter_schedule_items(meta.event.schedule_items.all(), user=request.user)

    schedule_items = graphene.NonNull(
        graphene.List(graphene.NonNull(FullScheduleItemType)),
        filters=graphene.List(DimensionFilterInput),
        favorites_only=graphene.Boolean(),
        hide_past=graphene.Boolean(),
        updated_after=graphene.DateTime(),
        description=normalize_whitespace(resolve_schedule_items.__doc__ or ""),
    )

    @staticmethod
    def resolve_annotations(meta: ProgramV2EventMeta, info, lang: str = DEFAULT_LANGUAGE):
        return ANNOTATIONS

    annotations = graphene.NonNull(
        graphene.List(graphene.NonNull(AnnotationSchemoidType)),
        lang=graphene.String(),
    )

    @staticmethod
    def resolve_dimensions(
        meta: ProgramV2EventMeta,
        info,
        # TODO unify naming
        is_list_filter: bool = False,
        is_shown_in_detail: bool = False,
        public_only: bool = True,
        key_dimensions_only: bool = False,
    ):
        """
        `is_list_filter` - only return dimensions that are shown in the list filter.
        `is_shown_in_detail` - only return dimensions that are shown in the detail view.
        If you supply both, you only get their intersection.
        """
        if public_only:
            dimensions = meta.universe.dimensions.filter(is_public=True)
        else:
            graphql_check_instance(
                meta.universe,  # type: ignore
                info,
                field="dimensions",
                app="program_v2",
            )
            dimensions = meta.universe.dimensions.all()

        if is_list_filter:
            dimensions = dimensions.filter(is_list_filter=True)

        if is_shown_in_detail:
            dimensions = dimensions.filter(is_shown_in_detail=True)

        if key_dimensions_only:
            dimensions = dimensions.filter(is_key_dimension=True)

        return dimensions.order_by("order")

    dimensions = graphene.NonNull(
        graphene.List(graphene.NonNull(FullDimensionType)),
        is_list_filter=graphene.Boolean(),
        is_shown_in_detail=graphene.Boolean(),
        public_only=graphene.Boolean(),
        key_dimensions_only=graphene.Boolean(),
        description=normalize_whitespace(resolve_dimensions.__doc__ or ""),
    )

    @staticmethod
    def resolve_calendar_export_link(meta: ProgramV2EventMeta, info):
        """
        Returns a link to the calendar export view for the event.
        The calendar export view accepts the following GET parameters, all optional:
        `favorited` - set to a truthy value to receive only favorites,
        `slug` - include only these programmes (can be multi-valued or separated by commas),
        `language` - the language to use when resolving dimensions.
        """
        request: HttpRequest = info.context
        return request.build_absolute_uri(
            reverse("program_v2:calendar_export_view", kwargs={"event_slug": meta.event.slug})
        )

    calendar_export_link = graphene.NonNull(
        graphene.String,
        description=normalize_whitespace(resolve_calendar_export_link.__doc__ or ""),
    )

    @staticmethod
    def resolve_program_offers(
        meta: ProgramV2EventMeta,
        info,
        filters: list[DimensionFilterInput] | None = None,
    ):
        """
        Returns all responses to all program offer forms of this event.
        """
        graphql_check_model(Response, meta.event.scope, info, app="program_v2")
        program_offers = meta.program_offers.all()

        if filters:
            program_offers = ProgramFilters.from_graphql(filters).filter_program_offers(program_offers)

        return program_offers.order_by("-created_at")

    program_offers = graphene.NonNull(
        graphene.List(graphene.NonNull(FullResponseType)),
        filters=graphene.List(DimensionFilterInput),
        description=normalize_whitespace(resolve_program_offers.__doc__ or ""),
    )

    @staticmethod
    def resolve_count_program_offers(meta: ProgramV2EventMeta, info):
        """
        Returns the total number of program offers (not taking into account filters).
        """
        return meta.program_offers.count()

    count_program_offers = graphene.NonNull(
        graphene.Int,
        description=normalize_whitespace(resolve_count_program_offers.__doc__ or ""),
    )

    @staticmethod
    def resolve_program_offer(meta: ProgramV2EventMeta, info, id: str):
        """
        Returns a single response program offer.
        """
        response = meta.program_offers.filter(id=id).first()

        if response:
            graphql_check_instance(response, info, app="program_v2")

        return response

    program_offer = graphene.Field(
        FullResponseType,
        id=graphene.String(required=True),
        description=normalize_whitespace(resolve_program_offer.__doc__ or ""),
    )

    @staticmethod
    def resolve_state_dimension(meta: ProgramV2EventMeta, info):
        """
        Returns the state dimension of the event, if there is one.
        """
        # TODO does it make sense to hard-code the name "state"?
        return meta.universe.dimensions.filter(slug="state").first()

    state_dimension = graphene.Field(
        FullDimensionType,
        description=normalize_whitespace(resolve_state_dimension.__doc__ or ""),
    )


class ProfileProgramInclude(graphene.Enum):
    FAVORITED = "FAVORITED"
    SIGNED_UP = "SIGNED_UP"
    HOSTING = "HOSTING"


class ProgramV2ProfileMetaType(graphene.ObjectType):
    @staticmethod
    def resolve_programs(
        meta: ProgramV2ProfileMeta,
        info,
        event_slug: str | None = None,
        filters: list[DimensionFilterInput] | None = None,
        include: list[ProfileProgramInclude] | None = None,  # TODO
        hide_past: bool = False,
    ):
        """
        Get programs that relate to this user in some way.
        Currently only favorites are implemented, but in the future also signed up and hosting.
        Dimension filter may only be specified when event_slug is given.
        """
        request: HttpRequest = info.context

        if event_slug is not None:
            # validate event_slug
            event = Event.objects.get(slug=event_slug)
            programs = Program.objects.filter(event=event)
        else:
            programs = Program.objects.all()

        return ProgramFilters.from_graphql(
            filters,
            favorites_only=True,
            hide_past=hide_past,
        ).filter_program(programs, user=request.user)

    programs = graphene.List(
        graphene.NonNull(FullProgramType),
        event_slug=graphene.String(),
        filters=graphene.List(DimensionFilterInput),
        include=graphene.List(ProfileProgramInclude),
        hide_past=graphene.Boolean(),
        description=normalize_whitespace(resolve_programs.__doc__ or ""),
    )

    @staticmethod
    def resolve_schedule_items(
        meta: ProgramV2ProfileMeta,
        info,
        event_slug: str | None = None,
        filters: list[DimensionFilterInput] | None = None,
        include: list[ProfileProgramInclude] | None = None,  # TODO
        hide_past: bool = False,
    ):
        """
        Get programs that relate to this user in some way.
        Currently only favorites are implemented, but in the future also signed up and hosting.
        Dimension filter may only be specified when event_slug is given.
        """
        request: HttpRequest = info.context

        if event_slug is not None:
            # validate event_slug
            event = Event.objects.get(slug=event_slug)
            schedule_items = ScheduleItem.objects.filter(cached_event=event)
        else:
            schedule_items = ScheduleItem.objects.all()

        return ProgramFilters.from_graphql(
            filters,
            favorites_only=True,
            hide_past=hide_past,
        ).filter_schedule_items(schedule_items, user=request.user)

    schedule_items = graphene.List(
        graphene.NonNull(FullScheduleItemType),
        event_slug=graphene.String(),
        filters=graphene.List(DimensionFilterInput),
        include=graphene.List(ProfileProgramInclude),
        hide_past=graphene.Boolean(),
        description=normalize_whitespace(resolve_programs.__doc__ or ""),
    )
