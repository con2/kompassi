import graphene
from django.http import HttpRequest
from django.utils.timezone import now
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType

from core.utils.locale_utils import get_message_in_language
from core.utils.text_utils import normalize_whitespace
from graphql_api.language import DEFAULT_LANGUAGE
from graphql_api.utils import resolve_localized_field

from ..consts import ANNOTATION_SCHEMA
from ..models import Program
from .annotations import ProgramAnnotationType
from .dimension import ProgramDimensionValueType

# imported for side effects (register object type used by django object type fields)
from .schedule import ScheduleItemType  # noqa: F401


class ProgramLinkType(graphene.Enum):
    SIGNUP = "SIGNUP"
    RESERVATION = "RESERVATION"
    TICKETS = "TICKETS"
    RECORDING = "RECORDING"
    REMOTE = "REMOTE"
    FEEDBACK = "FEEDBACK"
    CALENDAR = "CALENDAR"
    OTHER = "OTHER"


# This is an interim solution until Program V2 has an editing UI.
DEFAULT_LINK_TITLES = dict(
    en={
        ProgramLinkType.SIGNUP: "Sign up",
        ProgramLinkType.RESERVATION: "Reserve seats",
        ProgramLinkType.TICKETS: "Buy tickets",
        ProgramLinkType.RECORDING: "Watch recording",
        ProgramLinkType.REMOTE: "Participate remotely",
        ProgramLinkType.FEEDBACK: "Give feedback",
        ProgramLinkType.OTHER: "Link",
        ProgramLinkType.CALENDAR: "Add to calendar",
    },
    fi={
        ProgramLinkType.SIGNUP: "Ilmoittaudu",
        ProgramLinkType.RESERVATION: "Varaa paikkoja",
        ProgramLinkType.TICKETS: "Osta liput",
        ProgramLinkType.RECORDING: "Katso tallenne",
        ProgramLinkType.REMOTE: "Osallistu etänä",
        ProgramLinkType.FEEDBACK: "Anna palautetta",
        ProgramLinkType.OTHER: "Linkki",
        ProgramLinkType.CALENDAR: "Lisää kalenteriin",
    },
    sv={
        ProgramLinkType.SIGNUP: "Anmäl dig",
        ProgramLinkType.RESERVATION: "Reservera platser",
        ProgramLinkType.TICKETS: "Köp biljetter",
        ProgramLinkType.RECORDING: "Se inspelningen",
        ProgramLinkType.REMOTE: "Delta på distans",
        ProgramLinkType.FEEDBACK: "Ge feedback",
        ProgramLinkType.OTHER: "Länk",
        ProgramLinkType.CALENDAR: "Lägg till i kalendern",
    },
)


class ProgramLink(graphene.ObjectType):
    type = graphene.NonNull(ProgramLinkType)
    href = graphene.NonNull(graphene.String)
    title = graphene.NonNull(graphene.String)

    @classmethod
    def from_program(
        cls,
        request: HttpRequest,
        program: Program,
        link_type: ProgramLinkType,
        language: str = DEFAULT_LANGUAGE,
        include_expired: bool = False,
    ):
        """
        TODO should this be pushed into the Program model?
        TODO should this be cached? (probably not, as some links are time-sensitive)
        """
        link_type_str = link_type.value  # type: ignore[attr-defined]
        title_specifier = ""
        link_annotation = f"internal:links:{link_type_str.lower()}"

        match link_type:
            case ProgramLinkType.CALENDAR:
                # Do not show these links if the program has ended
                if not include_expired and program.cached_latest_end_time and now() > program.cached_latest_end_time:
                    href = ""
                else:
                    href = program.get_calendar_export_link(request)
            case (
                ProgramLinkType.SIGNUP
                | ProgramLinkType.RESERVATION
                | ProgramLinkType.TICKETS
                | ProgramLinkType.REMOTE
            ):
                # Do not show these links if the program has ended
                if not include_expired and program.cached_latest_end_time and now() > program.cached_latest_end_time:
                    href = ""
                else:
                    href = program.annotations.get(link_annotation, "")
            case ProgramLinkType.FEEDBACK:
                # Do not show feedback link if the program has not started yet
                if program.cached_earliest_start_time and now() < program.cached_earliest_start_time:
                    href = ""
                else:
                    href = program.annotations.get(link_annotation, "")
            case _:
                href = program.annotations.get(link_annotation, "")

        if not href:
            return None

        titles = get_message_in_language(DEFAULT_LINK_TITLES, language) or {}
        title = program.annotations.get(
            f"{link_type_str.lower()}",
            titles.get(link_type_str, ""),
        )

        if title_specifier:
            title = f"{title} ({title_specifier})"

        return cls(
            type=link_type,
            href=href,
            title=title,
        )  # type: ignore[call-arg]


class ProgramType(DjangoObjectType):
    cached_dimensions = graphene.Field(GenericScalar)

    @staticmethod
    def resolve_cached_hosts(parent: Program, info):
        return parent.annotations.get("internal:formattedHosts", "")

    cached_hosts = graphene.NonNull(graphene.String)

    resolve_location = resolve_localized_field("cached_location")

    location = graphene.String(
        description=normalize_whitespace(
            """
            Supplied for convenience. Prefer scheduleItem.location if possible.
            Caveat: When a program item has multiple schedule items, they may be in different locations.
            In such cases, a comma separated list of locations is returned.
        """
        ),
        lang=graphene.String(),
    )

    @staticmethod
    def resolve_links(
        parent: Program,
        info,
        types: list[ProgramLinkType] | None = None,
        lang=DEFAULT_LANGUAGE,
        include_expired: bool = False,
    ):
        """
        Get the links associated with the program. If types are not specified, all links are returned.
        """
        if types is None:
            types = list(ProgramLinkType)

        return [
            program_link
            for link_type in types
            if (
                program_link := ProgramLink.from_program(
                    info.context,
                    parent,
                    link_type,
                    lang,
                    include_expired=include_expired,
                )
            )
        ]

    links = graphene.NonNull(
        graphene.List(graphene.NonNull(ProgramLink)),
        description=normalize_whitespace(resolve_links.__doc__ or ""),
        types=graphene.List(ProgramLinkType),
        lang=graphene.String(),
        include_expired=graphene.Boolean(),
    )

    @staticmethod
    def resolve_signup_link(program: Program, info):
        """
        Deprecated. Use `links(types: SIGNUP)` instead.
        """
        if links := ProgramType.resolve_links(
            program,
            info,
            types=[ProgramLinkType.SIGNUP],  # type: ignore[arg-type]
        ):
            return links[0].href
        return ""

    signup_link = graphene.NonNull(
        graphene.String,
        description=normalize_whitespace(resolve_signup_link.__doc__ or ""),
    )

    @staticmethod
    def resolve_calendar_export_link(program: Program, info):
        """
        Deprecated. Use `links(types: CALENDAR)` instead.
        """
        if links := ProgramType.resolve_links(
            program,
            info,
            types=[ProgramLinkType.CALENDAR],  # type: ignore[arg-type]
        ):
            return links[0].href
        return ""

    calendar_export_link = graphene.NonNull(
        graphene.String,
        description=normalize_whitespace(resolve_calendar_export_link.__doc__ or ""),
    )

    @staticmethod
    def resolve_cached_annotations(program: Program, info, is_shown_in_detail: bool = False):
        """
        A mapping of program annotation slug to annotation value. Only public annotations are returned.

        TODO: Provide a way to supply is_public=False annotations to the GraphQL importer.
        Perhaps make the importer authenticate?
        """
        annotations = [annotation for annotation in ANNOTATION_SCHEMA if annotation.is_public]

        if is_shown_in_detail:
            annotations = [annotation for annotation in annotations if annotation.is_shown_in_detail]

        annotations_dict = {annotation.slug: annotation for annotation in annotations}

        return {
            k: v
            for (k, v) in program.annotations.items()
            if v not in (None, "") and (annotation := annotations_dict.get(k)) and annotation.is_public
        }

    cached_annotations = graphene.NonNull(
        GenericScalar,
        description=normalize_whitespace(resolve_cached_annotations.__doc__ or ""),
        is_shown_in_detail=graphene.Boolean(description="Only return annotations that are shown in the detail view."),
    )

    @staticmethod
    def resolve_annotations(program: Program, info, is_shown_in_detail: bool = False):
        """
        Program annotation values with schema attached to them. Only public annotations are returned.

        NOTE: If querying a lot of program items, consider using cachedAnnotations instead for SPEED.
        """
        annotations = [annotation for annotation in ANNOTATION_SCHEMA if annotation.is_public]

        if is_shown_in_detail:
            annotations = [annotation for annotation in annotations if annotation.is_shown_in_detail]

        return [
            ProgramAnnotationType(
                annotation=annotation,
                value=value,
            )  # type: ignore
            for annotation in annotations
            if (value := program.annotations.get(annotation.slug, None))
        ]

    annotations = graphene.NonNull(
        graphene.List(graphene.NonNull(ProgramAnnotationType)),
        description=normalize_whitespace(resolve_annotations.__doc__ or ""),
        is_shown_in_detail=graphene.Boolean(description="Only return annotations that are shown in the detail view."),
    )

    @staticmethod
    def resolve_other_fields(parent: Program, info):
        """
        Deprecated. Use `annotations` instead.
        """
        return ProgramType.resolve_cached_annotations(parent, info)

    other_fields = graphene.NonNull(
        GenericScalar,
        description=normalize_whitespace(resolve_other_fields.__doc__ or ""),
    )

    @staticmethod
    def resolve_dimensions(
        program: Program,
        info,
        is_list_filter: bool = False,
        is_shown_in_detail: bool = False,
    ):
        """
        `is_list_filter` - only return dimensions that are shown in the list filter.
        `is_shown_in_detail` - only return dimensions that are shown in the detail view.
        If you supply both, you only get their intersection.
        """
        pdvs = program.dimensions.all()

        if is_list_filter:
            pdvs = pdvs.filter(dimension__is_list_filter=True)

        if is_shown_in_detail:
            pdvs = pdvs.filter(dimension__is_shown_in_detail=True)

        return pdvs

    dimensions = graphene.NonNull(
        graphene.List(graphene.NonNull(ProgramDimensionValueType)),
        is_list_filter=graphene.Boolean(),
        is_shown_in_detail=graphene.Boolean(),
        description=normalize_whitespace(resolve_dimensions.__doc__ or ""),
    )

    @staticmethod
    def resolve_color(program: Program, info):
        return program.cached_color

    color = graphene.NonNull(graphene.String)

    class Meta:
        model = Program
        fields = (
            "title",
            "slug",
            "description",
            "cached_dimensions",
            "schedule_items",
            "cached_earliest_start_time",
            "cached_latest_end_time",
        )
