from __future__ import annotations

import logging
import uuid
from collections.abc import Collection, Iterable, Mapping, Sequence
from functools import cached_property
from typing import TYPE_CHECKING, Any, ClassVar

from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.db import models, transaction
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _

from core.models.event import Event
from dimensions.models.scope import Scope
from dimensions.utils.build_cached_dimensions import build_cached_dimensions
from dimensions.utils.dimension_cache import DimensionCache
from dimensions.utils.set_dimension_values import set_dimension_values
from graphql_api.language import SUPPORTED_LANGUAGES

from .attachment import Attachment
from .field import Field
from .form import Form
from .survey import DimensionApp, Survey

if TYPE_CHECKING:
    from program_v2.models.program import Program

    from ..utils.process_form_data import FieldWarning
    from .response_dimension_value import ResponseDimensionValue


logger = logging.getLogger("kompassi")


class Response(models.Model):
    # TODO UUID7
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    form: models.ForeignKey[Form] = models.ForeignKey(
        Form,
        on_delete=models.CASCADE,
        related_name="all_responses",
    )
    form_data = JSONField()

    revision_created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    original_created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )

    revision_created_at = models.DateTimeField(
        auto_now_add=True,
    )
    original_created_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    ip_address = models.CharField(
        max_length=48,
        blank=True,
        default="",
        verbose_name=_("IP address"),
    )

    sequence_number = models.PositiveIntegerField(
        default=0,
        help_text="Sequence number of this response within the use case (eg. survey).",
    )

    # denormalized fields
    cached_dimensions = models.JSONField(
        default=dict,
        help_text="dimension slug -> list of value slugs",
    )
    cached_key_fields = models.JSONField(
        default=dict,
        help_text="key field slug -> value as in values",
    )

    superseded_by = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    # related fields
    dimensions: models.QuerySet[ResponseDimensionValue]
    programs: models.QuerySet[Program]

    class Meta:
        indexes = [
            GinIndex(
                fields=["cached_dimensions"],
                name="forms_response_gin",
                opclasses=["jsonb_path_ops"],
            ),
        ]

    @property
    def survey(self) -> Survey:
        return self.form.survey

    @property
    def scope(self) -> Scope:
        return self.survey.scope

    @property
    def event(self) -> Event:
        return self.form.event

    @property
    def timezone(self):
        return self.event.timezone

    @property
    def old_versions(self) -> models.QuerySet[Response]:
        return Response.objects.filter(
            superseded_by=self.current_version,
        ).order_by("-revision_created_at")

    @property
    def current_version(self) -> Response:
        return self.superseded_by or self

    @cached_property
    def original(self) -> Response:
        return self.old_versions.last() or self

    @property
    def is_current_version(self) -> bool:
        return self.superseded_by is None

    @property
    def is_original(self) -> bool:
        return self.original == self

    def get_attachments(
        self,
        fields: Sequence[Field] | None = None,
    ):
        if fields is None:
            form: Form = self.form
            fields = form.validated_fields

        return list(self._get_attachments(fields))

    def _get_attachments(
        self,
        fields: Sequence[Field],
    ) -> Iterable[Attachment]:
        form: Form = self.form
        values, warnings = self.get_processed_form_data(fields=fields)
        for field in form.validated_fields:
            if not field.type.are_attachments_allowed:
                continue

            if field_warnings := warnings.get(field.slug, []):
                logger.warning(
                    "Cowardly refusing to operate on attachments of field that has warnings: %s",
                    dict(
                        response=self.id,
                        field=field.slug,
                        warnings=field_warnings,
                    ),
                )

            urls: list[str] = values.get(field.slug, [])
            for attachment_url in urls:
                yield Attachment(presigned_url=attachment_url, field_slug=field.slug)

    def _build_cached_key_fields(self, fields: list[Field] | None = None) -> dict[str, Any]:
        if fields is None:
            fields = self.form.validated_fields

        if fields is None:
            raise AssertionError("This should never happen (appease type checker)")

        values, warnings = self.get_processed_form_data(fields, field_slugs=self.survey.key_fields)
        return {
            field_slug: field_value
            for field_slug, field_value in values.items()
            if field_slug in self.survey.key_fields and field_slug not in warnings and field_value is not None
        }

    def _build_cached_dimensions(self) -> dict[str, list[str]]:
        """
        Used by ..handlers/dimension.py to populate cached_dimensions
        """
        return build_cached_dimensions(self.dimensions.all())

    @classmethod
    def refresh_cached_fields_qs(
        cls,
        responses: models.QuerySet[Response],
        batch_size: int = 100,
    ):
        bulk_update = []
        for response in (
            responses.select_for_update(of=("self",), no_key=True)
            .prefetch_related(
                "dimensions__value__dimension",
                "dimensions__value",
            )
            .only(
                "id",
                "dimensions__value__dimension__slug",
                "dimensions__value__slug",
            )
        ):
            response.cached_dimensions = response._build_cached_dimensions()
            response.cached_key_fields = response._build_cached_key_fields()

            if response.original_created_by is None:
                response.original_created_by = response.original.revision_created_by
            if response.original_created_at is None:
                response.original_created_at = response.original.revision_created_at

            bulk_update.append(response)
        cls.objects.bulk_update(
            bulk_update,
            [
                "cached_dimensions",
                "cached_key_fields",
                "original_created_at",
                "original_created_by",
            ],
            batch_size=batch_size,
        )

    def refresh_cached_fields(self):
        update_fields = ["cached_dimensions", "cached_key_fields"]
        self.cached_dimensions = self._build_cached_dimensions()
        self.cached_key_fields = self._build_cached_key_fields()

        if self.original_created_by is None:
            self.original_created_by = self.original.revision_created_by
            update_fields.append("original_created_by")

        if self.original_created_at is None:
            self.original_created_at = self.original.revision_created_at
            update_fields.append("original_created_at")

        self.save(update_fields=update_fields)

    @transaction.atomic
    def set_dimension_values(self, values_to_set: Mapping[str, Collection[str]], cache: DimensionCache):
        """
        Changes only those dimension values that are present in dimension_values.

        NOTE: Caller must call refresh_cached_dimensions() or refresh_cached_dimensions_qs()
        afterwards to update the cached_dimensions field.

        :param values_to_set: Mapping of dimension slug to list of value slugs.
        :param cache: Cache from Universe.preload_dimensions()
        """
        from .response_dimension_value import ResponseDimensionValue

        set_dimension_values(ResponseDimensionValue, self, values_to_set, cache)

    def get_processed_form_data(
        self,
        fields: Sequence[Field] | None = None,
        field_slugs: Collection[str] | None = None,
    ) -> tuple[dict[str, Any], dict[str, list[FieldWarning]]]:
        """
        If you only need a subset of fields, pass them in as fields or field_slugs.
        Returns a tuple of (values, warnings).
        """
        from ..utils.process_form_data import process_form_data

        if fields is None:
            fields = self.form.validated_fields

        if fields is None:
            raise AssertionError("This should never happen (appease type checker)")

        if field_slugs is not None:
            fields = [field for field in fields if field.slug in field_slugs]

        return process_form_data(
            fields,  # type: ignore
            self.form_data,
        )

    new_response_message_templates: ClassVar[dict[str, str]] = {
        language.code: f"survey_response_notification_email_{language.code}.eml" for language in SUPPORTED_LANGUAGES
    }

    new_response_subject_templates: ClassVar[dict[str, str]] = {
        "fi": "{survey_title} ({event_name}): Uusi vastaus",
        "en": "{survey_title} ({event_name}): New response",
        "sv": "{survey_title} ({event_name}): Nytt svar",
    }

    edited_response_message_templates: ClassVar[dict[str, str]] = {
        language.code: f"survey_response_edited_notification_email_{language.code}.eml"
        for language in SUPPORTED_LANGUAGES
    }

    edited_response_subject_templates: ClassVar[dict[str, str]] = {
        "fi": "{survey_title} ({event_name}): Vastausta muokattu",
        "en": "{survey_title} ({event_name}): Response edited",
        "sv": "{survey_title} ({event_name}): Svar redigerat",
    }

    @property
    def admin_url(self) -> str:
        match DimensionApp(self.survey.app_name):
            case DimensionApp.FORMS:
                return f"{settings.KOMPASSI_V2_BASE_URL}/{self.survey.event.slug}/surveys/{self.survey.slug}/responses/{self.id}"
            case DimensionApp.PROGRAM_V2:
                return f"{settings.KOMPASSI_V2_BASE_URL}/{self.survey.event.slug}/program-offers/{self.id}"
            case _:
                raise ValueError(f"Unknown app type: {self.survey.app_name}")
