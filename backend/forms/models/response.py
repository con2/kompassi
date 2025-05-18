from __future__ import annotations

import logging
import uuid
from collections import defaultdict
from collections.abc import Callable, Collection, Iterable, Mapping, Sequence
from typing import TYPE_CHECKING, Any, Literal

from django.conf import settings
from django.db import models, transaction
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _

from core.models.event import Event
from core.utils.model_utils import slugify, slugify_underscore
from dimensions.models.scope import Scope
from dimensions.utils.dimension_cache import DimensionCache
from graphql_api.language import SUPPORTED_LANGUAGES

from .attachment import Attachment
from .field import Field, FieldType
from .form import Form
from .survey import Survey, SurveyApp

if TYPE_CHECKING:
    from program_v2.models.program import Program

    from ..utils.process_form_data import FieldWarning
    from .response_dimension_value import ResponseDimensionValue


logger = logging.getLogger("kompassi")


class Response(models.Model):
    # TODO UUID7
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="responses")
    form_data = JSONField()

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

    # related fields
    dimensions: models.QuerySet[ResponseDimensionValue]
    programs: models.QuerySet[Program]

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
                    "Refusing to operate on attachments of field %s of responpse %s due to warnings: %s",
                    field.slug,
                    self.id,
                    field_warnings,
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
        new_cached_dimensions = {}
        for sdv in self.dimensions.all():
            new_cached_dimensions.setdefault(sdv.value.dimension.slug, []).append(sdv.value.slug)

        return new_cached_dimensions

    @classmethod
    @transaction.atomic
    def refresh_cached_fields_qs(
        cls,
        responses: models.QuerySet[Response],
        batch_size: int = 100,
    ):
        bulk_update = []
        for response in (
            responses.select_for_update(of=("self",))
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
            bulk_update.append(response)
        cls.objects.bulk_update(bulk_update, ["cached_dimensions", "cached_key_fields"], batch_size=batch_size)

    def refresh_cached_fields(self):
        self.cached_dimensions = self._build_cached_dimensions()
        self.cached_key_fields = self._build_cached_key_fields()
        self.save(update_fields=["cached_dimensions", "cached_key_fields"])

    def lift_dimension_values(self, *, dimension_slugs: list[str] | None = None, cache: DimensionCache):
        """
        Lifts the values of dimensions from form data into proper dimension values.
        This makes sense only for responses that are related to a survey.

        NOTE: Caller must call refresh_cached_fields() or refresh_cached_fields_qs()
        afterwards to update the cached_dimensions field.

        :param dimension_slugs: If provided, only these dimensions will be lifted.
        """
        survey = self.survey

        # only these fields have the potential of being dimension fields
        # TODO support single checkbox as dimension field?
        # get_processed_form_data expects enriched, validated form of fields
        fields: list[Field] = [field for field in self.form.validated_fields if field.type.is_dimension_field]

        if dimension_slugs is not None:
            # filter out fields that are not in dimension_slugs
            fields = [field for field in fields if field.dimension in dimension_slugs]

        values, warnings = self.get_processed_form_data(fields)
        values_to_set: defaultdict[str, set[str]] = defaultdict(set)

        for field in fields:
            log_context = dict(
                survey=survey.id,
                language=self.form.language,
                response=self.id,
                field=field.slug,
                dimension=field.dimension,
                field_type=field.type,
            )

            if not field.dimension:
                logger.warning("Dimension field has no dimension: %s", log_context)
                continue

            dimension = cache.dimensions.get(field.dimension)
            if dimension is None:
                logger.warning(
                    "Dimension field refers to non-existing dimension: %s",
                    dict(log_context),
                )
                continue

            if field_warnings := warnings.get(field.slug):
                # this dimension has validation warnings
                logger.warning(
                    "Cowardly refusing to lift dimension values from field with warnings: %s",
                    dict(log_context, warnings=field_warnings),
                )
                continue

            value_slugs: list[str]
            match field.type:
                case FieldType.DIMENSION_MULTI_SELECT:
                    value_slugs = values.get(field.slug, [])
                case FieldType.DIMENSION_SINGLE_SELECT:
                    value_slugs = [value_slug] if (value_slug := values.get(field.slug)) else []
                case _:
                    logger.warning("Unexpected field type for dimension field: %s", log_context)
                    continue

            if not isinstance(value_slugs, list):
                logger.warning(
                    "Expected list of value slugs for dimension field: %s",
                    dict(log_context, value_slugs=value_slugs),
                )
                continue

            for value_slug in value_slugs:
                value = cache.values_by_dimension[dimension.slug][value_slug]
                if value is None:
                    logger.warning(
                        "Response refers to a dimension value that doesn't exist: %s",
                        dict(log_context, value_slug=value_slug),
                    )
                    continue

                values_to_set[dimension.slug].add(value_slug)

        if values_to_set:
            self.set_dimension_values(values_to_set, cache)

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

        bulk_delete = self.dimensions.filter(value__dimension__slug__in=values_to_set.keys())
        bulk_create: list[ResponseDimensionValue] = []

        for dimension_slug, value_slugs in values_to_set.items():
            bulk_delete = bulk_delete.exclude(
                value__dimension__slug=dimension_slug,
                value__slug__in=value_slugs,
            )

            for value_slug in value_slugs:
                if value_slug not in self.cached_dimensions.get(dimension_slug, []):
                    bulk_create.append(
                        ResponseDimensionValue(
                            response=self,
                            value=cache.values_by_dimension[dimension_slug][value_slug],
                        )
                    )

        bulk_delete.delete()
        ResponseDimensionValue.objects.bulk_create(bulk_create)

    def get_processed_form_data(
        self,
        fields: Sequence[Field] | None = None,
        field_slugs: Sequence[str] | None = None,
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

    notification_templates = {
        language.code: f"survey_response_notification_email/{language.code}.eml" for language in SUPPORTED_LANGUAGES
    }

    subject_templates = {
        "fi": "{survey_title} ({event_name}): Uusi vastaus",
        "en": "{survey_title} ({event_name}): New response",
        "sv": "{survey_title} ({event_name}): Nytt svar",
    }

    @property
    def admin_url(self) -> str:
        match SurveyApp(self.survey.app):
            case SurveyApp.FORMS:
                return f"{settings.KOMPASSI_V2_BASE_URL}/{self.survey.event.slug}/surveys/{self.survey.slug}/responses/{self.id}"
            case SurveyApp.PROGRAM_V2:
                return f"{settings.KOMPASSI_V2_BASE_URL}/{self.survey.event.slug}/program-offers/{self.id}"
            case _:
                raise ValueError(f"Unknown app type: {self.survey.app}")

    @staticmethod
    def _reslugify_pair(
        pair: tuple[str, Any],
        field_slug: str,
        slugifier: Callable[[str], str],
    ) -> tuple[str, Any]:
        key, value = pair
        if not isinstance(value, str):
            # FileUpload
            return key, value

        if key == field_slug:
            # SingleSelect -> DimensionSingleSelect
            return key, slugifier(value)
        elif key.startswith(f"{field_slug}."):
            # MultiSelect -> DimensionMultiSelect
            _, subkey = key.split(".", 1)
            subkey = slugifier(subkey)
            return f"{key}.{subkey}", value

        return key, value

    def reslugify_field(self, field_slug: str, separator: Literal["-", "_"]):
        """
        When promoting a form field to dimension, we need to account for possible
        differences in the slugification of the field and the dimension values.

        NOTE: Caller is responsible for calling save(["form_data"]) afterwards.
        """
        slugifier = slugify if separator == "-" else slugify_underscore
        self.form_data = dict(self._reslugify_pair(pair, field_slug, slugifier) for pair in self.form_data.items())
