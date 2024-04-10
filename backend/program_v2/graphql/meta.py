import graphene
from django.conf import settings
from django.http import HttpRequest
from django.urls import reverse
from graphene_django import DjangoObjectType

from access.cbac import graphql_check_instance
from core.graphql.common import DimensionFilterInput
from core.utils import get_objects_within_period
from core.utils.text_utils import normalize_whitespace

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
        fields = ("skip_offer_form_selection",)

    programs = graphene.List(
        graphene.NonNull(ProgramType),
        filters=graphene.List(DimensionFilterInput),
        favorites_only=graphene.Boolean(),
    )

    @staticmethod
    def resolve_programs(
        meta: ProgramV2EventMeta,
        info,
        filters: list[DimensionFilterInput] | None = None,
        favorites_only: bool = False,
    ):
        if filters is None:
            filters = []

        queryset = Program.objects.filter(event=meta.event)

        if filters:
            for filter in filters:
                queryset = queryset.filter(
                    dimensions__dimension__slug=filter.dimension,
                    dimensions__value__slug__in=filter.values,
                )

        if (user := info.context.user) and user.is_authenticated and favorites_only:
            queryset = queryset.filter(favorited_by=user)

        return queryset.order_by("schedule_items__start_time")

    dimensions = graphene.List(graphene.NonNull(DimensionType))

    @staticmethod
    def resolve_program(meta: ProgramV2EventMeta, info, slug: str):
        return Program.objects.get(event=meta.event, slug=slug)

    program = graphene.Field(ProgramType, slug=graphene.String(required=True))

    @staticmethod
    def resolve_dimensions(meta: ProgramV2EventMeta, info):
        return Dimension.objects.filter(event=meta.event)

    offer_forms = graphene.List(graphene.NonNull(OfferFormType), include_inactive=graphene.Boolean())

    @staticmethod
    def resolve_offer_forms(meta: ProgramV2EventMeta, info, include_inactive: bool = False):
        if include_inactive:
            graphql_check_instance(meta, info, "offer_forms")
            qs = OfferForm.objects.filter(event=meta.event)
        else:
            qs = get_objects_within_period(OfferForm, event=meta.event)

        return qs

    offer_form = graphene.Field(OfferFormType, slug=graphene.String(required=True))

    @staticmethod
    def resolve_offer_form(meta: ProgramV2EventMeta, info, slug: str):
        return OfferForm.objects.get(event=meta.event, slug=slug)

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
    ):
        """
        Get programs that relate to this user in some way.
        Currently only favorites are implemented, but in the future also signed up and hosting.
        Dimension filter may only be specified when event_slug is given.
        """
        if include is None:
            include = list(ProfileProgramInclude)

        # TODO implement SIGNED_UP, HOSTING
        if ProfileProgramInclude.FAVORITED in include:
            programs = Program.objects.filter(favorited_by=meta.person.user)
        else:
            return Program.objects.none()

        if event_slug:
            programs = programs.filter(event__slug=event_slug)

        if filters:
            if not event_slug:
                raise ValueError("Event slug is required when filtering by dimensions")

            for filter in filters:
                programs = programs.filter(
                    dimensions__dimension__slug=filter.dimension,
                    dimensions__value__slug__in=filter.values,
                )

        return programs.order_by("schedule_items__start_time").distinct()

    programs = graphene.List(
        graphene.NonNull(ProgramType),
        event_slug=graphene.String(),
        filters=graphene.List(DimensionFilterInput),
        include=graphene.List(ProfileProgramInclude),
        description=normalize_whitespace(resolve_programs.__doc__ or ""),
    )
