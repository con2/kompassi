import graphene
from django.http import HttpRequest
from django.utils.timezone import now
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType

from core.utils.locale_utils import get_message_in_language
from core.utils.text_utils import normalize_whitespace
from graphql_api.language import DEFAULT_LANGUAGE

from ..models import Program

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
DEFAULT_TITLES = dict(
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
    ):
        """
        TODO should this be pushed into the Program model?
        TODO should this be cached? (probably not, as some links are time-sensitive)
        """
        link_type_str = link_type.value  # type: ignore[attr-defined]
        title_specifier = ""

        match link_type:
            case ProgramLinkType.CALENDAR:
                # Do not show these links if the program has ended
                if program.cached_latest_end_time and now() > program.cached_latest_end_time:
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
                if program.cached_latest_end_time and now() > program.cached_latest_end_time:
                    href = ""
                else:
                    href = program.other_fields.get(f"{link_type_str.lower()}_link", "")
            case ProgramLinkType.FEEDBACK:
                # Do not show feedback link if the program has not started yet
                if program.cached_earliest_start_time and now() < program.cached_earliest_start_time:
                    href = ""
                else:
                    href = program.other_fields.get("feedback_link", "")
            case _:
                href = program.other_fields.get(f"{link_type_str.lower()}_link", "")

        if not href:
            return None

        titles = get_message_in_language(DEFAULT_TITLES, language) or {}
        title = program.other_fields.get(
            f"{link_type_str.lower()}_link_title",
            titles.get(link_type_str, ""),
        )

        if title_specifier:
            title = f"{title} ({title_specifier})"

        return cls(
            type=link_type,
            href=href,
            title=title,
        )


class ProgramType(DjangoObjectType):
    cached_dimensions = graphene.Field(GenericScalar)

    @staticmethod
    def resolve_cached_hosts(parent: Program, info):
        return parent.other_fields.get("formatted_hosts", "")

    cached_hosts = graphene.NonNull(graphene.String)

    @staticmethod
    def resolve_location(parent: Program, info, lang=DEFAULT_LANGUAGE):
        """
        Get the location of the program in the format it should be displayed in to the participant.
        Currently this simply returns the value of the location dimension in the language specified.
        In the future, also a freeform location field could be supported.
        """
        return parent.get_location(lang) or ""

    location = graphene.NonNull(
        graphene.String,
        description=normalize_whitespace(resolve_location.__doc__ or ""),
    )

    @staticmethod
    def resolve_links(
        parent: Program,
        info,
        types: list[ProgramLinkType] | None = None,
        lang=DEFAULT_LANGUAGE,
    ):
        """
        Get the links associated with the program. If types are not specified, all links are returned.
        """
        if types is None:
            types = list(ProgramLinkType)

        return [
            program_link
            for link_type in types
            if (program_link := ProgramLink.from_program(info.context, parent, link_type, lang))
        ]

    links = graphene.NonNull(
        graphene.List(graphene.NonNull(ProgramLink)),
        description=normalize_whitespace(resolve_links.__doc__ or ""),
        types=graphene.List(ProgramLinkType),
        lang=graphene.String(),
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

    class Meta:
        model = Program
        fields = (
            "title",
            "slug",
            "description",
            "dimensions",
            "cached_dimensions",
            "schedule_items",
            "cached_earliest_start_time",
            "cached_latest_end_time",
        )
