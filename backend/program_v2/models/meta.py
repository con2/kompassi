from dataclasses import dataclass
from functools import cached_property

from django.conf import settings
from django.db import models

from core.models.contact_email_mixin import ContactEmailMixin, contact_email_validator
from core.models.event import Event
from core.models.event_meta_base import EventMetaBase
from core.models.person import Person
from dimensions.models.universe import Universe
from forms.models.enums import SurveyApp, SurveyPurpose
from forms.models.response import Response
from forms.models.survey import Survey
from involvement.models.involvement import Involvement
from involvement.models.registry import Registry


class ProgramV2EventMeta(ContactEmailMixin, EventMetaBase):
    is_accepting_feedback = models.BooleanField(
        default=True,
        verbose_name="Is accepting feedback",
        help_text="If checked, feedback can be left for programs.",
    )

    contact_email = models.CharField(
        max_length=255,
        blank=True,
        validators=[contact_email_validator],
        help_text="Foo Bar &lt;foo.bar@example.com&gt;",
    )

    guide_v2_embedded_url = models.CharField(
        max_length=255,
        blank=True,
        help_text="URL to the embedded guide. This is used to form program links.",
    )

    default_registry = models.ForeignKey(
        Registry,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    use_cbac = True

    event: models.ForeignKey[Event]

    def __str__(self):
        return str(self.event)

    @classmethod
    def get_or_create_dummy(cls):
        event, _ = Event.get_or_create_dummy()
        return cls.objects.get_or_create(
            event=event,
            defaults=dict(
                admin_group=cls.get_or_create_groups(event, ("admins",))[0],
                is_accepting_feedback=True,
                contact_email="Dummy Program <program@example.com>",
                guide_v2_embedded_url="https://example.com/guide",
                default_registry=Registry.get_or_create_dummy()[0],
            ),
        )

    @cached_property
    def universe(self) -> Universe:
        from program_v2.workflows.program_offer import ProgramOfferWorkflow

        return ProgramOfferWorkflow.get_program_universe(self.event)

    @property
    def program_offers(self):
        """
        NOTE Optimized for frontend/src/app/[locale]/[eventSlug]/program-offers/page.tsx
        """
        return (
            Response.objects.filter(
                form__event=self.event,
                form__survey__app="program_v2",
                form__survey__purpose_slug="DEFAULT",
            )
            .select_related(
                "form",
                "form__event",
                "form__survey",
                "form__survey__event",
                "created_by",
            )
            .prefetch_related(
                "programs",
            )
        )

    @property
    def program_hosts(self) -> models.QuerySet[Involvement]:
        return (
            Involvement.objects.filter(
                universe=self.event.involvement_universe,
                program__isnull=False,
                is_active=True,
            )
            .select_related(
                "person",
                "program",
            )
            .order_by(
                "person__surname",
                "person__first_name",
                "program__cached_first_start_time",
            )
        )

    @property
    def program_offer_forms(self):
        return Survey.objects.filter(
            event=self.event,
            app=SurveyApp.PROGRAM_V2.value,
            purpose_slug=SurveyPurpose.DEFAULT.value,
        )

    @property
    def accept_invitation_forms(self):
        return Survey.objects.filter(
            event=self.event,
            app=SurveyApp.PROGRAM_V2.value,
            purpose_slug=SurveyPurpose.INVITE.value,
        )

    @property
    def schedule_url(self):
        return f"{settings.KOMPASSI_V2_BASE_URL}/{self.event.slug}/program"


@dataclass
class ProgramV2ProfileMeta:
    """
    No need for an actual model for now. This serves as a stand-in for GraphQL.
    """

    person: Person

    @property
    def program_offers(self):
        if self.person.user is None:
            return Response.objects.none()

        return (
            Response.objects.filter(
                form__survey__app="program_v2",
                form__survey__purpose_slug="DEFAULT",
                created_by=self.person.user,
            )
            .select_related(
                "form",
                "form__event",
                "form__survey",
                "form__survey__event",
                "created_by",
            )
            .prefetch_related(
                "programs",
            )
        )
