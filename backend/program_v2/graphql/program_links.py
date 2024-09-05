import graphene
from django.conf import settings
from django.http import HttpRequest
from django.utils.timezone import now

from core.utils.locale_utils import get_message_in_language
from graphql_api.language import DEFAULT_LANGUAGE

from ..models import Program

# imported for side effects (register object type used by django object type fields)
from .schedule_item_limited import LimitedScheduleItemType  # noqa: F401


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
                href = (
                    program.annotations.get(
                        link_annotation,
                        settings.KOMPASSI_V2_BASE_URL
                        + f"/events/{program.event.slug}/programs/{program.slug}/feedback",
                    )
                    if program.is_accepting_feedback
                    else ""
                )

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

        return cls(type=link_type, href=href, title=title)  # type: ignore[call-arg]
