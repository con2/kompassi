from dataclasses import dataclass
from functools import cached_property

from django.conf import settings
from django.db import models

from core.models.contact_email_mixin import ContactEmailMixin, contact_email_validator
from core.models.event_meta_base import EventMetaBase
from core.models.person import Person
from dimensions.models.universe import Universe
from forms.models.response import Response


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

    use_cbac = True

    def __str__(self):
        return str(self.event)

    @cached_property
    def universe(self) -> Universe:
        from program_v2.workflow import ProgramOfferWorkflow

        return ProgramOfferWorkflow.get_program_universe(self.event)

    @property
    def program_offers(self):
        return Response.objects.filter(
            form__event=self.event,
            form__survey__app="program_v2",
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
