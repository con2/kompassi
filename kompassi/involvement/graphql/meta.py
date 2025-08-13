from __future__ import annotations

import graphene
from django.http import HttpRequest
from graphene_django import DjangoObjectType

from kompassi.access.cbac import graphql_check_instance, graphql_check_model
from kompassi.core.models.person import Person
from kompassi.core.utils.text_utils import normalize_whitespace
from kompassi.dimensions.graphql.annotation import AnnotationType
from kompassi.dimensions.graphql.dimension_filter_input import DimensionFilterInput
from kompassi.dimensions.graphql.dimension_full import FullDimensionType
from kompassi.dimensions.models.enums import AnnotationFlags
from kompassi.graphql_api.language import DEFAULT_LANGUAGE
from kompassi.involvement.filters import InvolvementFilters
from kompassi.involvement.reports.combined_perks_reports import get_combined_perks_reports
from kompassi.reports.graphql.report import ReportType

from ..models.involvement import Involvement
from ..models.meta import InvolvementEventMeta
from .invitation_full import FullInvitationType
from .profile_with_involvement import ProfileWithInvolvementType


class InvolvementEventMetaType(DjangoObjectType):
    class Meta:
        model = InvolvementEventMeta

    @staticmethod
    def resolve_invitation(
        meta: InvolvementEventMeta,
        info,
        invitation_id: str,
    ):
        request: HttpRequest = info.context

        if not request.user.is_authenticated:
            raise Exception("User is not authenticated")

        return meta.invitations.get(id=invitation_id)

    invitation = graphene.Field(
        FullInvitationType,
        invitation_id=graphene.String(required=True),
    )

    @staticmethod
    def resolve_people(
        meta: InvolvementEventMeta,
        info,
        filters: list[DimensionFilterInput] | None = None,
        search: str = "",
        return_none: bool = False,
    ):
        """
        List of people involved in the event, filtered by dimensions.
        """
        request: HttpRequest = info.context

        graphql_check_model(
            Involvement,
            meta.event.scope,
            request,
        )

        if return_none:
            return []

        involvement_filters = InvolvementFilters.from_graphql(filters=filters, search=search)
        return meta.get_people(involvement_filters)

    people = graphene.NonNull(
        graphene.List(
            graphene.NonNull(ProfileWithInvolvementType),
        ),
        filters=graphene.List(DimensionFilterInput, required=False),
        search=graphene.String(default_value=""),
        return_none=graphene.Boolean(default_value=False),
        description=normalize_whitespace(resolve_people.__doc__ or ""),
    )

    @staticmethod
    def resolve_person(
        meta: InvolvementEventMeta,
        info,
        id: int,
    ):
        request: HttpRequest = info.context

        graphql_check_model(
            Involvement,
            meta.event.scope,
            request,
        )

        try:
            return meta.get_person(id)
        except Person.DoesNotExist:
            return None

    person = graphene.Field(
        ProfileWithInvolvementType,
        id=graphene.Int(required=True),
        description=normalize_whitespace(resolve_person.__doc__ or ""),
    )

    @staticmethod
    def resolve_dimensions(
        meta: InvolvementEventMeta,
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
                app=meta.universe.app_name,
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
    def resolve_annotations(
        meta: InvolvementEventMeta,
        info,
        public_only: bool = True,
        perks_only: bool = False,
    ):
        request: HttpRequest = info.context

        graphql_check_model(
            Involvement,
            meta.event.scope,
            request,
        )

        return meta.universe.annotations.filter(
            flags__has_all=AnnotationFlags.from_kwargs(
                is_public=public_only,
                is_perk=perks_only,
            ),
        )

    annotations = graphene.NonNull(
        graphene.List(graphene.NonNull(AnnotationType)),
        public_only=graphene.Boolean(default_value=True),
        perks_only=graphene.Boolean(default_value=False),
        description=normalize_whitespace(resolve_annotations.__doc__ or ""),
    )

    @staticmethod
    def resolve_reports(
        meta: InvolvementEventMeta,
        info,
        lang: str = DEFAULT_LANGUAGE,
    ):
        request: HttpRequest = info.context

        graphql_check_model(
            Involvement,
            meta.event.scope,
            request,
        )

        reports = get_combined_perks_reports(meta.universe, lang)

        Emperkelator = meta.emperkelator_class
        if Emperkelator is not None:
            reports.extend(Emperkelator.get_reports(meta.event, lang))

        return reports

    reports = graphene.NonNull(
        graphene.List(graphene.NonNull(ReportType)),
        lang=graphene.String(default_value=DEFAULT_LANGUAGE),
        description=normalize_whitespace(resolve_reports.__doc__ or ""),
    )
