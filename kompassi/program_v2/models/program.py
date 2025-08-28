from __future__ import annotations

import logging
from collections.abc import Collection, Mapping
from datetime import tzinfo
from functools import cached_property
from typing import TYPE_CHECKING, Any, ClassVar, Self
from uuid import UUID

from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.db import models, transaction
from django.http import HttpRequest
from django.urls import reverse
from django.utils.timezone import now

from kompassi.access.cbac import is_graphql_allowed_for_model
from kompassi.core.models import Event
from kompassi.core.utils.model_utils import slugify, validate_slug
from kompassi.dimensions.models.cached_annotations import (
    CachedAnnotations,
    CachedAnnotationsUpdate,
    compact_annotations,
    validate_annotations,
)
from kompassi.dimensions.models.cached_dimensions import CachedDimensions, validate_cached_dimensions
from kompassi.dimensions.models.scope import Scope
from kompassi.dimensions.utils.build_cached_dimensions import build_cached_dimensions
from kompassi.dimensions.utils.dimension_cache import DimensionCache
from kompassi.dimensions.utils.set_dimension_values import set_dimension_values
from kompassi.forms.models.response import Response
from kompassi.forms.models.survey import Survey
from kompassi.forms.utils.extract_annotations import extract_annotations_from_responses
from kompassi.graphql_api.language import DEFAULT_LANGUAGE
from kompassi.involvement.models.enums import InvolvementType
from kompassi.involvement.models.invitation import Invitation
from kompassi.involvement.models.involvement import Involvement

from ..dimensions import get_scheduled_dimension_value
from ..integrations.konsti import get_konsti_signup_url

if TYPE_CHECKING:
    from dimensions.models.universe import Universe

    from .meta import ProgramV2EventMeta
    from .program_dimension_value import ProgramDimensionValue
    from .schedule_item import ScheduleItem


logger = logging.getLogger(__name__)


class Program(models.Model):
    id: int

    event: models.ForeignKey[Event] = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="programs")
    title = models.CharField(max_length=1023)
    slug = models.CharField(max_length=1023, validators=[validate_slug])
    description = models.TextField(blank=True)
    annotations: models.JSONField[dict[str, Any]] = models.JSONField(blank=True, default=dict)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # denormalized fields
    cached_dimensions = models.JSONField(default=dict, blank=True)
    cached_combined_dimensions = models.JSONField(default=dict, blank=True)
    cached_earliest_start_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text=(
            "The earliest start time of any schedule item of this program. "
            "NOTE: This is not the same as the program's start time. "
            "The intended purpose of this field is to exclude programs that have not yet started. "
            "Always use `scheduleItems` for the purpose of displaying program times."
        ),
    )
    cached_latest_end_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text=(
            "The latest end time of any schedule item of this program. "
            "NOTE: This is not the same as the program's start end. "
            "The intended purpose of this field is to exclude programs that have already ended. "
            "Always use `scheduleItems` for the purpose of displaying program times."
        ),
    )
    cached_color = models.CharField(max_length=15, blank=True, default="")

    program_offer: models.ForeignKey[Response] | None = models.ForeignKey(
        Response,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="programs",
        help_text="If this program was created from a program offer, this field will be set to the program offer.",
    )
    program_offer_id: UUID | None

    @property
    def is_cancelled(self) -> bool:
        # Program items generally should not end up in the rejected state, but we check for it just in case.
        return bool(set(self.cached_dimensions.get("state", [])).intersection({"cancelled", "rejected"}))

    @property
    def is_active(self) -> bool:
        return not self.is_cancelled

    @property
    def universe(self) -> Universe:
        return self.event.program_universe

    # related fields
    dimensions: models.QuerySet[ProgramDimensionValue]
    involvements: models.QuerySet[Involvement]
    schedule_items: models.QuerySet[ScheduleItem]
    event_id: int

    class Meta:
        unique_together = ("event", "slug")
        indexes = [
            GinIndex(
                fields=["cached_combined_dimensions"],
                name="program_v2_program_gin",
                opclasses=["jsonb_path_ops"],
            ),
        ]

    def __str__(self):
        return str(self.title)

    def refresh_technical_dimensions(self):
        cache = self.meta.universe.preload_dimensions(["scheduled"])

        values = get_scheduled_dimension_value(self.schedule_items.count())
        self.set_dimension_values({"scheduled": values}, cache=cache)

    @classmethod
    def refresh_technical_dimensions_qs(
        cls,
        queryset: models.QuerySet[Self],
        cache: DimensionCache | None = None,
    ):
        for program in queryset.annotate(count_schedule_items=models.Count("schedule_items")):
            cur_cache = cache or program.meta.universe.preload_dimensions(["scheduled"])
            values = get_scheduled_dimension_value(program.count_schedule_items)  # type: ignore
            program.set_dimension_values({"scheduled": values}, cache=cur_cache)

    def refresh_cached_fields(self):
        self.refresh_technical_dimensions()
        self.refresh_cached_dimensions()
        self.refresh_cached_times()
        self.refresh_annotations()

    @classmethod
    def refresh_cached_fields_qs(
        cls,
        queryset: models.QuerySet[Self],
        cache: DimensionCache | None = None,
    ):
        cls.refresh_technical_dimensions_qs(queryset, cache=cache)
        cls.refresh_cached_dimensions_qs(queryset)
        cls.refresh_cached_times_qs(queryset)
        cls.refresh_annotations_qs(queryset)

    def with_cached_dimensions(self):
        from .schedule_item_dimension_value import ScheduleItemDimensionValue

        self.cached_dimensions = build_cached_dimensions(self.dimensions.all())
        self.cached_combined_dimensions = build_cached_dimensions(
            self.dimensions.all(),
            ScheduleItemDimensionValue.objects.filter(subject__program=self),
        )

        self.cached_color = (
            first_pdv_with_color.value.color
            if (first_pdv_with_color := self.dimensions.exclude(value__color="").first())
            else ""
        )

        return self

    def refresh_cached_dimensions(self):
        self.with_cached_dimensions().save(
            update_fields=[
                "cached_dimensions",
                "cached_combined_dimensions",
                "cached_color",
            ]
        )

    program_batch_size: ClassVar[int] = 100
    schedule_item_batch_size: ClassVar[int] = 100

    @classmethod
    def refresh_cached_dimensions_qs(cls, queryset: models.QuerySet[Self]):
        num_programs_updated = cls.objects.bulk_update(
            (
                program.with_cached_dimensions()
                for program in queryset.select_for_update(of=("self",), no_key=True).only(
                    "id",
                    "cached_dimensions",
                    "cached_combined_dimensions",
                    "cached_color",
                )
            ),
            [
                "cached_dimensions",
                "cached_combined_dimensions",
                "cached_color",
            ],
            batch_size=cls.program_batch_size,
        )
        logger.info("Refreshed cached dimensions for %s programs", num_programs_updated)

    def with_cached_times(self):
        earliest_schedule_item = self.schedule_items.order_by("start_time").first()
        latest_schedule_item = self.schedule_items.order_by("cached_end_time").last()

        self.cached_earliest_start_time = earliest_schedule_item.start_time if earliest_schedule_item else None
        self.cached_latest_end_time = latest_schedule_item.cached_end_time if latest_schedule_item else None

        return self

    def refresh_cached_times(self):
        self.with_cached_times().save(
            update_fields=[
                "cached_earliest_start_time",
                "cached_latest_end_time",
                "updated_at",
            ],
        )

    @classmethod
    def refresh_cached_times_qs(cls, queryset: models.QuerySet[Self]):
        with transaction.atomic():
            num_updated = cls.objects.bulk_update(
                (
                    program.with_cached_times()
                    for program in queryset.select_for_update(of=("self",), no_key=True).only(
                        "id",
                        "cached_earliest_start_time",
                        "cached_latest_end_time",
                        "updated_at",
                    )
                ),
                ["cached_earliest_start_time", "cached_latest_end_time", "updated_at"],
                batch_size=cls.program_batch_size,
            )
            logger.info("Refreshed cached times for %s programs", num_updated)

    def with_annotations(self, update: CachedAnnotationsUpdate | CachedAnnotations | None = None) -> Self:
        self.annotations = dict(self.annotations)
        if update:
            self.annotations.update(update)

        # TODO(#728): if soft delete of program hosts is implemented, this should be updated to
        # include only active program hosts
        default_formatted_hosts = ", ".join(host.person.display_name for host in self.all_program_hosts)
        formatted_hosts = self.annotations.get("internal:overrideFormattedHosts", "") or default_formatted_hosts
        self.annotations.update(
            {
                "internal:defaultFormattedHosts": default_formatted_hosts,
                "internal:formattedHosts": formatted_hosts,
            }
        )

        # TODO(#801) Should be separately on each schedule item
        if not self.annotations.get("internal:links:signup") and (konsti_url := get_konsti_signup_url(self)):
            self.annotations["internal:links:signup"] = konsti_url

        self.annotations = compact_annotations(self.annotations)

        return self

    def refresh_annotations(self, update: CachedAnnotationsUpdate | CachedAnnotations | None = None):
        self.with_annotations(update).save(update_fields=["annotations"])

    @classmethod
    def refresh_annotations_qs(cls, queryset: models.QuerySet[Self]):
        with transaction.atomic():
            num_updated = queryset.bulk_update(
                (
                    program.with_annotations()
                    for program in queryset.select_for_update(of=("self",), no_key=True).only("id", "annotations")
                ),
                ["annotations"],
                batch_size=cls.program_batch_size,
            )
            logger.info("Refreshed cached annotations for %s programs", num_updated)

    def refresh_dependents(self):
        from .schedule_item import ScheduleItem

        ScheduleItem.refresh_cached_fields_qs(self.schedule_items.all())

        if self.cached_combined_dimensions.get("paikkala", []):
            for item in self.schedule_items.all():
                item.ensure_paikkala()

    @property
    def _effective_annotations(self):
        """
        For use by resolve_cached_annotations, to allow treating Program and ScheduleItem the same.
        Other users should usually query .annotations directly.
        """
        return self.annotations

    @cached_property
    def meta(self) -> ProgramV2EventMeta:
        if (meta := self.event.program_v2_event_meta) is None:
            raise TypeError(f"Event {self.event.slug} does not have program_v2_event_meta but Programs are present")

        return meta

    @cached_property
    def timezone(self) -> tzinfo:
        return self.event.timezone

    def get_calendar_export_link(self, request: HttpRequest):
        return request.build_absolute_uri(
            reverse(
                "program_v2:single_program_calendar_export_view",
                kwargs=dict(
                    event_slug=self.event.slug,
                    program_slug=self.slug,
                ),
            )
        )

    @property
    def is_accepting_feedback(self) -> bool:
        return bool(
            self.meta.is_accepting_feedback
            and self.cached_earliest_start_time
            and now() >= self.cached_earliest_start_time
        )

    @property
    def scope(self) -> Scope:
        return self.event.scope

    @transaction.atomic
    def set_dimension_values(self, values_to_set: Mapping[str, Collection[str]], cache: DimensionCache):
        """
        Changes only those dimension values that are present in dimension_values.

        NOTE: Caller must call refresh_cached_dimensions() or refresh_cached_dimensions_qs()
        afterwards to update the cached_dimensions field.

        :param values_to_set: Mapping of dimension slug to list of value slugs.
        :param cache: Cache from Universe.preload_dimensions()
        """
        from .program_dimension_value import ProgramDimensionValue

        set_dimension_values(ProgramDimensionValue, self, values_to_set, cache)

    @classmethod
    def from_program_offer(
        cls,
        program_offer: Response,
        slug: str = "",
        title: str = "",
        program_dimension_values: CachedDimensions | None = None,
        involvement_dimension_values: CachedDimensions | None = None,
        created_by: Any | None = None,  # User
    ) -> Self:
        """
        Accept a program offer and return the new Program instance.
        """
        event = program_offer.event
        meta = event.program_v2_event_meta
        if meta is None:
            raise TypeError(f"Event {event.slug} does not have program_v2_event_meta")
        cache = event.program_universe.preload_dimensions()

        combined_dimension_values = validate_cached_dimensions(program_offer.survey.cached_default_response_dimensions)
        combined_dimension_values.update(validate_cached_dimensions(program_offer.cached_dimensions))
        if program_dimension_values:
            combined_dimension_values.update(validate_cached_dimensions(program_dimension_values))
        combined_dimension_values.update(
            state=["accepted"],
        )

        values, warnings = program_offer.get_processed_form_data()
        if warnings:
            logger.warning("Program offer %s had form data warnings: %s", program_offer.id, warnings)

        if not title:
            title = values.get("title", "")

        if not slug:
            slug = slugify(title)

        annotations = extract_annotations_from_responses(
            [program_offer],
            meta.universe.active_universe_annotations.all(),
        )

        program = cls(
            event=program_offer.event,
            slug=slug,
            title=title,
            description=values.get("description", ""),
            annotations=annotations,
            created_by=created_by,
            cached_dimensions={},
            program_offer=program_offer,
        )
        program.full_clean()
        program.save()
        program.set_dimension_values(combined_dimension_values, cache=cache)
        program.refresh_cached_fields()

        program_offer.set_dimension_values(program.cached_dimensions, cache=cache)
        program_offer.refresh_cached_fields()

        Involvement.from_accepted_program_offer(
            program_offer,
            program,
            cache=event.involvement_universe.preload_dimensions(),
            dimension_values=involvement_dimension_values or {},
        )

        return program

    @property
    def active_program_hosts(self) -> models.QuerySet[Involvement]:
        return (
            Involvement.objects.filter(
                program=self,
                is_active=True,
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

    @property
    def all_program_hosts(self) -> models.QuerySet[Involvement]:
        return (
            Involvement.objects.filter(
                program=self,
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

    def invite_program_host(
        self,
        email: str,
        survey: Survey,
        involvement_dimensions: CachedDimensions,
        language: str = DEFAULT_LANGUAGE,
        created_by: Any | None = None,  # User
    ) -> Invitation:
        if survey.involvement_type != InvolvementType.PROGRAM_HOST:
            raise ValueError(f"Survey {survey} cannot be used to invite program hosts")

        invitation = Invitation(
            survey=survey,
            program=self,
            email=email,
            created_by=created_by,
            language=language,
            cached_dimensions=validate_cached_dimensions(involvement_dimensions),
        )
        invitation.full_clean()
        invitation.save()
        invitation.send()

        return invitation

    @property
    def invitations(self) -> models.QuerySet[Invitation]:
        return (
            Invitation.objects.filter(
                program=self,
                used_at__isnull=True,
            )
            .select_related(
                "survey",
                "program",
            )
            .order_by("created_at")
        )

    @property
    def responses(self) -> models.QuerySet[Response]:
        response_ids = self.all_program_hosts.filter(response__isnull=False).values_list("response_id", flat=True)
        return Response.objects.filter(id__in=response_ids).order_by("revision_created_at")

    @property
    def validated_annotations(self) -> CachedAnnotations:
        """
        Returns the annotations of this program, validated against the event's schema.
        """

        return validate_annotations(self.annotations, self.meta.annotations_with_fallback.all())

    def can_be_cancelled_by(
        self,
        request: HttpRequest,
    ) -> bool:
        return not self.is_cancelled and self.can_be_deleted_by(request)

    def can_be_deleted_by(
        self,
        request: HttpRequest,
    ) -> bool:
        return is_graphql_allowed_for_model(
            request.user,
            instance=self,
            app="program_v2",
            operation="delete",
        )

    def can_be_restored_by(
        self,
        request: HttpRequest,
    ) -> bool:
        return self.is_cancelled and is_graphql_allowed_for_model(
            request.user,
            instance=self,
            app="program_v2",
            operation="update",
        )

    def can_program_host_be_invited_by(
        self,
        request: HttpRequest,
    ) -> bool:
        return not self.is_cancelled and is_graphql_allowed_for_model(
            request.user,
            instance=self,
            app="program_v2",
            operation="create",
            field="program_hosts",
        )
