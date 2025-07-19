from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from typing import Any

from django.conf import settings
from django.db import models

from core.models.contact_email_mixin import ContactEmailMixin, contact_email_validator
from core.models.event import Event
from core.models.event_meta_base import EventMetaBase
from core.models.person import Person
from dimensions.filters import DimensionFilters
from dimensions.models.enums import DimensionApp
from dimensions.models.scope import Scope
from dimensions.models.universe import Universe
from forms.models.enums import SurveyPurpose
from forms.models.response import Response
from forms.models.survey import Survey
from involvement.models.involvement import Involvement
from involvement.models.registry import Registry

from .annotation import Annotation
from .event_annotation import EventAnnotation


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

    # NOTE: currently this being set has the side effect of is_program_published being True.
    # In the future, is_program_published will be time based.
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
    all_event_annotations: models.QuerySet[EventAnnotation]

    def __str__(self):
        return str(self.event)

    @property
    def annotations(self) -> models.QuerySet[Annotation]:
        annotation_ids = self.active_event_annotations.values_list("annotation_id", flat=True)
        return Annotation.objects.filter(id__in=annotation_ids)

    @property
    def active_event_annotations(self) -> models.QuerySet[EventAnnotation]:
        return self.all_event_annotations.filter(is_active=True)

    @property
    def annotations_with_fallback(self) -> models.QuerySet[Annotation]:
        if self.all_event_annotations.exists():
            annotation_ids = self.active_event_annotations.all().values_list("annotation_id", flat=True)
            queryset = Annotation.objects.filter(id__in=annotation_ids)
        else:
            # Legacy event without event annotations
            # TODO Backfill them and remove this
            queryset = Annotation.objects.all()

        return queryset.order_by("slug")

    @cached_property
    def scope(self) -> Scope:
        return self.event.scope

    @classmethod
    def get_or_create_dummy(cls):
        event, _ = Event.get_or_create_dummy()
        meta, created = cls.objects.get_or_create(
            event=event,
            defaults=dict(
                admin_group=cls.get_or_create_groups(event, ("admins",))[0],
                is_accepting_feedback=True,
                contact_email="Dummy Program <program@example.com>",
                guide_v2_embedded_url="https://example.com/guide",
                default_registry=Registry.get_or_create_dummy()[0],
            ),
        )
        if created:
            meta.ensure()
        return meta, created

    @cached_property
    def universe(self) -> Universe:
        from program_v2.dimensions import get_program_universe

        return get_program_universe(self.event)

    @property
    def programs(self):
        from .program import Program

        return Program.objects.filter(event=self.event)

    @property
    def schedule_items(self):
        from .schedule_item import ScheduleItem

        return ScheduleItem.objects.filter(cached_event=self.event)

    @property
    def current_program_offers(self):
        return self._get_program_offers(superseded_by=None)

    @property
    def all_program_offers(self):
        return self._get_program_offers()

    @property
    def is_program_published(self) -> bool:
        # TODO
        return bool(self.guide_v2_embedded_url)

    def _get_program_offers(self, **extra_criteria: Any) -> models.QuerySet[Response]:
        """
        NOTE Optimized for frontend/src/app/[locale]/[eventSlug]/program-offers/page.tsx
        """
        return (
            Response.objects.filter(
                form__event=self.event,
                form__survey__app_name=DimensionApp.PROGRAM_V2.value,
                form__survey__purpose_slug=SurveyPurpose.DEFAULT.value,
                **extra_criteria,
            )
            .select_related(
                "form",
                "form__event",
                "form__survey",
                "form__survey__event",
                "revision_created_by",
            )
            .prefetch_related(
                "programs",
            )
            .order_by("-original_created_at")
        )

    def get_active_program_hosts(
        self,
        program_filters: DimensionFilters | None = None,
        involvement_filters: DimensionFilters | None = None,
    ) -> models.QuerySet[Involvement]:
        if program_filters:
            program_ids = program_filters.filter(self.programs.all()).values_list("id", flat=True)
            program_criteria = {"program__in": program_ids}
        else:
            program_criteria = {"program__isnull": False}

        involvements = (
            Involvement.objects.filter(
                universe=self.event.involvement_universe,
                is_active=True,
                **program_criteria,
            )
            .select_related(
                "person",
                "program",
            )
            .order_by(
                "person__surname",
                "person__first_name",
                "program__cached_earliest_start_time",
            )
        )

        if involvement_filters:
            involvements = involvement_filters.filter(involvements)

        return involvements

    @property
    def program_offer_forms(self):
        return Survey.objects.filter(
            event=self.event,
            app_name=DimensionApp.PROGRAM_V2.value,
            purpose_slug=SurveyPurpose.DEFAULT.value,
        )

    @property
    def accept_invitation_forms(self):
        return Survey.objects.filter(
            event=self.event,
            app_name=DimensionApp.PROGRAM_V2.value,
            purpose_slug=SurveyPurpose.INVITE.value,
        )

    @property
    def schedule_url(self):
        return f"{settings.KOMPASSI_V2_BASE_URL}/{self.event.slug}/program"

    def ensure(self):
        """
        Idempotent way to ensure all required structures are set up for this event.
        """
        EventAnnotation.ensure(self)


@dataclass
class ProgramV2ProfileMeta:
    """
    No need for an actual model for now. This serves as a stand-in for GraphQL.
    """

    person: Person

    @property
    def current_program_offers(self):
        if self.person.user is None:
            return Response.objects.none()

        return (
            Response.objects.filter(
                form__survey__app_name=DimensionApp.PROGRAM_V2.value,
                form__survey__purpose_slug=SurveyPurpose.DEFAULT.value,
                original_created_by=self.person.user,
                superseded_by=None,
            )
            .select_related(
                "form",
                "form__event",
                "form__survey",
                "form__survey__event",
                "revision_created_by",
                "original_created_by",
            )
            .prefetch_related(
                "programs",
            )
            .order_by("-revision_created_at")
        )
