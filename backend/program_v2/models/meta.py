from dataclasses import dataclass
from functools import cached_property

from django.conf import settings
from django.db import models

from core.models.contact_email_mixin import ContactEmailMixin, contact_email_validator
from core.models.event import Event
from core.models.event_meta_base import EventMetaBase
from core.models.person import Person
from dimensions.models.universe import Universe
from forms.models.response import Response
from involvement.models.involvement import Involvement, InvolvementApp
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

    @cached_property
    def universe(self) -> Universe:
        from program_v2.workflow import ProgramWorkflow

        return ProgramWorkflow.get_program_universe(self.event)

    @property
    def program_offers(self):
        """
        NOTE Optimized for frontend/src/app/[locale]/[eventSlug]/program-offers/page.tsx
        """
        return (
            Response.objects.filter(
                form__event=self.event,
                form__survey__app="program_v2",
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
    def program_hosts(self):
        return (
            Involvement.objects.filter(
                universe=self.event.involvement_universe,
                is_active=True,
                app_name=InvolvementApp.PROGRAM.value,
                program__isnull=False,
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
    def schedule_url(self):
        return f"{settings.KOMPASSI_V2_BASE_URL}/{self.event.slug}/program"


@dataclass
class ProgramV2ProfileMeta:
    """
    No need for an actual model for now. This serves as a stand-in for GraphQL.
    """

    person: Person
