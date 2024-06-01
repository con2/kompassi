import graphene
from django.conf import settings
from django.http import HttpRequest
from django.urls import reverse
from graphene_django import DjangoObjectType

from access.cbac import graphql_check_instance
from core.graphql.common import DimensionFilterInput
from core.models import Event
from core.utils import get_objects_within_period
from core.utils.text_utils import normalize_whitespace

from ..filters import ProgramFilters
from ..models import (
    Dimension,
    OfferForm,
    Program,
    ProgramV2EventMeta,
)
from ..models.meta import ProgramV2ProfileMeta
from .dimension import DimensionType
from .offer_form import OfferFormType
from .program import ProgramType

DEFAULT_LANGUAGE: str = settings.LANGUAGE_CODE


class ProgramV2EventMetaType(DjangoObjectType):
    class Meta:
        model = ProgramV2EventMeta
        fields = ("skip_offer_form_selection", "location_dimension")

    @staticmethod
    def resolve_programs(
        meta: ProgramV2EventMeta,
        info,
        filters: list[DimensionFilterInput] | None = None,
        favorites_only: bool = False,
        hide_past: bool = False,
    ):
        request: HttpRequest = info.context
        programs = Program.objects.filter(event=meta.event)
        return ProgramFilters.from_graphql(
            filters,
            favorites_only=favorites_only,
            hide_past=hide_past,
        ).filter_program(programs, user=request.user)

    programs = graphene.NonNull(
        graphene.List(graphene.NonNull(ProgramType)),
        filters=graphene.List(DimensionFilterInput),
        favorites_only=graphene.Boolean(),
        hide_past=graphene.Boolean(),
    )

    @staticmethod
    def resolve_program(meta: ProgramV2EventMeta, info, slug: str):
        return Program.objects.get(event=meta.event, slug=slug)

    program = graphene.Field(ProgramType, slug=graphene.String(required=True))

    @staticmethod
    def resolve_dimensions(
        meta: ProgramV2EventMeta,
        info,
        is_list_filter: bool = False,
        is_shown_in_detail: bool = False,
    ):
        """
        `is_list_filter` - only return dimensions that are shown in the list filter.
        `is_shown_in_detail` - only return dimensions that are shown in the detail view.
        If you supply both, you only get their intersection.
        """
        dimensions = Dimension.objects.filter(event=meta.event)

        if is_list_filter:
            dimensions = dimensions.filter(is_list_filter=True)

        if is_shown_in_detail:
            dimensions = dimensions.filter(is_shown_in_detail=True)

        return dimensions

    dimensions = graphene.NonNull(
        graphene.List(graphene.NonNull(DimensionType)),
        is_list_filter=graphene.Boolean(),
        is_shown_in_detail=graphene.Boolean(),
        description=normalize_whitespace(resolve_dimensions.__doc__ or ""),
    )

    @staticmethod
    def resolve_offer_forms(meta: ProgramV2EventMeta, info, include_inactive: bool = False):
        if include_inactive:
            graphql_check_instance(meta, info, "offer_forms")
            qs = OfferForm.objects.filter(event=meta.event)
        else:
            qs = get_objects_within_period(OfferForm, event=meta.event)

        return qs

    offer_forms = graphene.List(graphene.NonNull(OfferFormType), include_inactive=graphene.Boolean())

    @staticmethod
    def resolve_offer_form(meta: ProgramV2EventMeta, info, slug: str):
        return OfferForm.objects.get(event=meta.event, slug=slug)

    offer_form = graphene.Field(OfferFormType, slug=graphene.String(required=True))

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
        include: list[ProfileProgramInclude] | None = None,
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
        graphene.NonNull(ProgramType),
        event_slug=graphene.String(),
        filters=graphene.List(DimensionFilterInput),
        include=graphene.List(ProfileProgramInclude),
        hide_past=graphene.Boolean(),
        description=normalize_whitespace(resolve_programs.__doc__ or ""),
    )
