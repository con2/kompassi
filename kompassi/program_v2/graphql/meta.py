from datetime import datetime

import graphene
from django.http import HttpRequest
from django.urls import reverse
from graphene_django import DjangoObjectType

from kompassi.access.cbac import graphql_check_instance, graphql_check_model, graphql_query_cbac_required
from kompassi.core.models import Event
from kompassi.core.utils.text_utils import normalize_whitespace
from kompassi.dimensions.filters import DimensionFilters
from kompassi.dimensions.graphql.annotation import AnnotationType
from kompassi.dimensions.graphql.dimension_filter_input import DimensionFilterInput
from kompassi.dimensions.graphql.dimension_full import FullDimensionType
from kompassi.dimensions.graphql.universe_annotation_limited import LimitedUniverseAnnotationType
from kompassi.dimensions.models.enums import AnnotationFlags
from kompassi.forms.graphql.response_full import FullResponseType
from kompassi.forms.graphql.response_profile import ProfileResponseType
from kompassi.forms.models.response import Response
from kompassi.graphql_api.language import DEFAULT_LANGUAGE
from kompassi.reports.graphql.report import ReportType
from kompassi.reports.models.report import Report

from ..filters import ProgramFilters, ProgramUserRelation
from ..models import (
    Program,
    ProgramV2EventMeta,
    ScheduleItem,
)
from ..models.meta import ProgramV2ProfileMeta
from ..reports.paikkala_reports import ReservationsByZone, ReservationStatus
from .program_full import FullProgramType
from .program_host_full import FullProgramHostType, ProgramHost
from .schedule_item_full import FullScheduleItemType


class ProgramV2EventMetaType(DjangoObjectType):
    """
    NOTE: There is no `programForms` because a program form is a Survey with `app: PROGRAM_V2`.
    Use `event.forms.surveys(app: PROGRAM_V2)` for that instead.
    """

    class Meta:
        model = ProgramV2EventMeta
        fields = ()

    @staticmethod
    def resolve_programs(
        meta: ProgramV2EventMeta,
        info,
        filters: list[DimensionFilterInput] | None = None,
        favorites_only: bool = False,  # TODO use user_relation instead
        hide_past: bool = False,
        updated_after: datetime | None = None,
    ):
        request: HttpRequest = info.context
        programs = Program.objects.filter(event=meta.event).select_related("event")
        return ProgramFilters.from_graphql(
            filters,
            user_relation=ProgramUserRelation.FAVORITED if favorites_only else None,
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
        public_only: bool = True,
        hide_past: bool = False,
        updated_after: datetime | None = None,
    ):
        request: HttpRequest = info.context

        if not public_only:
            graphql_check_model(
                ScheduleItem,
                meta.event.scope,
                request,
                app="program_v2",
            )

        schedule_items = ScheduleItem.objects.filter(cached_event=meta.event).select_related(
            "program",
            "program__event",
        )
        return ProgramFilters.from_graphql(
            filters,
            user_relation=ProgramUserRelation.FAVORITED if favorites_only else None,
            hide_past=hide_past,
            updated_after=updated_after,
            public_only=public_only,
        ).filter_schedule_items(schedule_items, user=request.user)

    schedule_items = graphene.NonNull(
        graphene.List(graphene.NonNull(FullScheduleItemType)),
        filters=graphene.List(DimensionFilterInput),
        favorites_only=graphene.Boolean(),
        hide_past=graphene.Boolean(),
        updated_after=graphene.DateTime(),
        description=normalize_whitespace(resolve_schedule_items.__doc__ or ""),
    )

    @staticmethod
    def resolve_schedule_item(meta: ProgramV2EventMeta, info, slug: str):
        return ScheduleItem.objects.get(program__event=meta.event, slug=slug)

    schedule_item = graphene.Field(FullScheduleItemType, slug=graphene.String(required=True))

    @staticmethod
    def resolve_annotations(
        meta: ProgramV2EventMeta,
        info,
        slug: list[str] | None = None,
        public_only: bool = True,
    ):
        queryset = meta.annotations_with_fallback.all()

        if public_only:
            queryset = queryset.filter(flags__has_all=AnnotationFlags.PUBLIC)

        if slug is not None:
            queryset = queryset.filter(slug__in=slug)

        return queryset

    annotations = graphene.NonNull(
        graphene.List(graphene.NonNull(AnnotationType)),
        slug=graphene.List(graphene.NonNull(graphene.String)),
        public_only=graphene.Boolean(default_value=True),
    )

    @graphql_query_cbac_required
    @staticmethod
    def resolve_event_annotations(
        meta: ProgramV2EventMeta,
        info,
    ):
        """
        Used for admin purposes changing settings of annotations in events.
        Usually you should use `event.program.annotations` instead.
        """
        return meta.universe.all_universe_annotations.all().select_related("annotation").order_by("annotation__slug")

    event_annotations = graphene.NonNull(
        graphene.List(graphene.NonNull(LimitedUniverseAnnotationType)),
        description=normalize_whitespace(resolve_event_annotations.__doc__ or ""),
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

        return dimensions.select_related("universe").order_by("order")

    dimensions = graphene.NonNull(
        graphene.List(graphene.NonNull(FullDimensionType)),
        is_list_filter=graphene.Boolean(),
        is_shown_in_detail=graphene.Boolean(),
        public_only=graphene.Boolean(),
        key_dimensions_only=graphene.Boolean(),
        description=normalize_whitespace(resolve_dimensions.__doc__ or ""),
    )

    @staticmethod
    def resolve_involvement_dimensions(
        meta: ProgramV2EventMeta,
        info,
        # TODO unify naming
        is_list_filter: bool = False,
        is_shown_in_detail: bool = False,
        public_only: bool = True,
        key_dimensions_only: bool = False,
    ):
        """
        Like `dimensions` but returns dimensions from the Involvement universe.
        Differs from `event.involvement.dimensions` in that permissions are checked
        based on the Program V2 application privileges, not Involvement.

        `is_list_filter` - only return dimensions that are shown in the list filter.
        `is_shown_in_detail` - only return dimensions that are shown in the detail view.
        If you supply both, you only get their intersection.
        """
        if public_only:
            dimensions = meta.event.involvement_universe.dimensions.filter(is_public=True)
        else:
            graphql_check_instance(
                meta.universe,  # type: ignore
                info,
                field="dimensions",
                app="program_v2",
            )
            dimensions = meta.event.involvement_universe.dimensions.all()

        if is_list_filter:
            dimensions = dimensions.filter(is_list_filter=True)

        if is_shown_in_detail:
            dimensions = dimensions.filter(is_shown_in_detail=True)

        if key_dimensions_only:
            dimensions = dimensions.filter(is_key_dimension=True)

        return dimensions.select_related("universe").order_by("order")

    involvement_dimensions = graphene.NonNull(
        graphene.List(graphene.NonNull(FullDimensionType)),
        is_list_filter=graphene.Boolean(),
        is_shown_in_detail=graphene.Boolean(),
        public_only=graphene.Boolean(),
        key_dimensions_only=graphene.Boolean(),
        description=normalize_whitespace(resolve_involvement_dimensions.__doc__ or ""),
    )

    @staticmethod
    def resolve_calendar_export_link(meta: ProgramV2EventMeta, info):
        """
        Returns a link to the calendar export view for the event.
        The calendar export view accepts the following GET parameters, all optional:

        `favorited` - set to a truthy value to receive only favorites,
        `slug` - include only these programmes (can be multi-valued or separated by commas),
        `language` - the language to use when resolving dimensions.

        Further GET parameters are used to filter by dimensions.
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
    def resolve_program_offers_excel_export_link(meta: ProgramV2EventMeta, info):
        """
        Returns a link to the the program offers Excel export view for the event.
        The program offers Excel export view returns all or filtered program offers
        in an Excel file, grouped into worksheets by the program form.

        `favorited` - set to a truthy value to receive only favorites,
        `slug` - include only these programmes (can be multi-valued or separated by commas),
        `language` - the language to use when resolving dimensions.

        Further GET parameters are used to filter by dimensions.
        """
        request: HttpRequest = info.context
        return request.build_absolute_uri(
            reverse("program_v2:program_offers_excel_export_view", kwargs={"event_slug": meta.event.slug})
        )

    program_offers_excel_export_link = graphene.NonNull(
        graphene.String,
        description=normalize_whitespace(resolve_program_offers_excel_export_link.__doc__ or ""),
    )

    @staticmethod
    def resolve_program_hosts_excel_export_link(meta: ProgramV2EventMeta, info):
        request: HttpRequest = info.context
        return request.build_absolute_uri(
            reverse("program_v2:program_hosts_excel_export_view", kwargs={"event_slug": meta.event.slug})
        )

    program_hosts_excel_export_link = graphene.NonNull(
        graphene.String,
        description=normalize_whitespace(resolve_program_hosts_excel_export_link.__doc__ or ""),
    )

    @staticmethod
    def resolve_schedule_items_excel_export_link(meta: ProgramV2EventMeta, info):
        request: HttpRequest = info.context
        return request.build_absolute_uri(
            reverse("program_v2:schedule_items_excel_export_view", kwargs={"event_slug": meta.event.slug})
        )

    schedule_items_excel_export_link = graphene.NonNull(
        graphene.String,
        description=normalize_whitespace(resolve_schedule_items_excel_export_link.__doc__ or ""),
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
        program_offers = meta.current_program_offers.all()

        if filters:
            program_offers = ProgramFilters.from_graphql(filters).filter_program_offers(program_offers)

        return program_offers

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
        return meta.current_program_offers.count()

    count_program_offers = graphene.NonNull(
        graphene.Int,
        description=normalize_whitespace(resolve_count_program_offers.__doc__ or ""),
    )

    @staticmethod
    def resolve_program_offer(meta: ProgramV2EventMeta, info, id: str):
        """
        Returns a single program offer.
        Also old versions of program offers can be retrieved by their ID.
        """
        # check done on this level so that we do not give off information
        # about the existence of a program offer to unauthorized users
        graphql_check_instance(
            meta.event,  # type: ignore
            info,
            app="program_v2",
            field="program_offers",
        )

        return meta.all_program_offers.filter(id=id).first()

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

    @staticmethod
    def resolve_program_hosts(
        meta: ProgramV2EventMeta,
        info,
        program_filters: list[DimensionFilterInput] | None = None,
        # involvement_filters: list[DimensionFilterInput] | None = None,
    ):
        graphql_check_model(Event, meta.event.scope, info, app="program_v2", field="program_hosts")

        return ProgramHost.from_event(
            meta,
            program_filters=DimensionFilters.from_graphql(program_filters),
            # involvement_filters=DimensionFilters.from_graphql(involvement_filters),
        )

    program_hosts = graphene.NonNull(
        graphene.List(graphene.NonNull(FullProgramHostType)),
        program_filters=graphene.List(DimensionFilterInput),
    )

    @staticmethod
    def resolve_reports(
        meta: ProgramV2EventMeta,
        info,
        lang: str = DEFAULT_LANGUAGE,
    ):
        request: HttpRequest = info.context

        graphql_check_model(
            ScheduleItem,
            meta.event.scope,
            request,
        )

        reports: list[Report] = []
        reports.extend(ReservationStatus.report(meta.event))
        reports.extend(
            ReservationsByZone.report(schedule_item, lang=lang)
            for schedule_item in meta.schedule_items.filter(
                cached_combined_dimensions__contains=dict(paikkala=[]),
            )
        )
        return reports

    reports = graphene.NonNull(
        graphene.List(graphene.NonNull(ReportType)),
        lang=graphene.String(required=False),
        description=normalize_whitespace(resolve_reports.__doc__ or ""),
    )


ProgramUserRelationType = graphene.Enum.from_enum(ProgramUserRelation)


class ProgramV2ProfileMetaType(graphene.ObjectType):
    @staticmethod
    def resolve_programs(
        meta: ProgramV2ProfileMeta,
        info,
        event_slug: str | None = None,
        filters: list[DimensionFilterInput] | None = None,
        user_relation: ProgramUserRelation = ProgramUserRelation.FAVORITED,
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
            user_relation=user_relation,
            hide_past=hide_past,
        ).filter_program(
            programs,
            user=request.user,
        )

    programs = graphene.List(
        graphene.NonNull(FullProgramType),
        event_slug=graphene.String(),
        filters=graphene.List(DimensionFilterInput),
        user_relation=graphene.Argument(ProgramUserRelationType),
        hide_past=graphene.Boolean(),
        description=normalize_whitespace(resolve_programs.__doc__ or ""),
    )

    @staticmethod
    def resolve_schedule_items(
        meta: ProgramV2ProfileMeta,
        info,
        event_slug: str | None = None,
        filters: list[DimensionFilterInput] | None = None,
        user_relation: ProgramUserRelation = ProgramUserRelation.FAVORITED,
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
            user_relation=user_relation,
            hide_past=hide_past,
        ).filter_schedule_items(
            schedule_items,
            user=request.user,
        )

    schedule_items = graphene.List(
        graphene.NonNull(FullScheduleItemType),
        event_slug=graphene.String(),
        filters=graphene.List(DimensionFilterInput),
        user_relation=graphene.Argument(ProgramUserRelationType),
        hide_past=graphene.Boolean(),
        description=normalize_whitespace(resolve_programs.__doc__ or ""),
    )

    @staticmethod
    def resolve_program_offers(
        meta: ProgramV2EventMeta,
        info,
        filters: list[DimensionFilterInput] | None = None,
    ):
        """
        Returns all current responses to all program offer forms of this event.
        """
        program_offers = meta.current_program_offers.all()

        if filters:
            program_offers = ProgramFilters.from_graphql(
                filters,
                user_relation=ProgramUserRelation.HOSTING,
            ).filter_program_offers(
                program_offers,
                user=info.context.user,
            )

        return program_offers

    program_offers = graphene.NonNull(
        graphene.List(graphene.NonNull(ProfileResponseType)),
        filters=graphene.List(DimensionFilterInput),
        description=normalize_whitespace(resolve_program_offers.__doc__ or ""),
    )
