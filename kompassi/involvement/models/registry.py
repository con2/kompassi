from __future__ import annotations

from functools import cache
from typing import Self

from django.db import models
from django.http import HttpRequest

from kompassi.access.cbac import is_graphql_allowed_for_model
from kompassi.core.models.organization import Organization
from kompassi.dimensions.models.scope import Scope
from kompassi.graphql_api.language import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGE_CODES, getattr_message_in_language


class Registry(models.Model):
    scope = models.ForeignKey(
        Scope,
        on_delete=models.CASCADE,
        related_name="registries",
    )

    slug = models.SlugField(unique=False)

    # NOTE SUPPORTED_LANGUAGES
    title_en = models.CharField(max_length=255)
    title_fi = models.CharField(max_length=255)
    title_sv = models.CharField(max_length=255)

    policy_url_en = models.URLField(blank=True)
    policy_url_fi = models.URLField(blank=True)
    policy_url_sv = models.URLField(blank=True)

    default_retention_period = models.DurationField(
        null=True,
        blank=True,
        help_text=(
            "The default retention period for personal data in this registry, counted from the end of the year "
            "in which the event ends (or, lacking that, in which the record was created). If unset, personal data "
            "in this registry is retained indefinitely. Can be overridden per survey."
        ),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("scope", "slug")
        unique_together = ("scope", "slug")

    def __str__(self):
        return getattr_message_in_language(self, "title", DEFAULT_LANGUAGE)

    @classmethod
    def get_or_create_dummy(cls):
        organization, _ = Organization.get_or_create_dummy()

        return cls.objects.get_or_create(
            scope=organization.scope,
            slug="dummy",
            defaults=dict(
                title_en="Dummy registry",
                title_fi="Dummy-rekisteri",
                title_sv="Dummy register",
            ),
        )

    @classmethod
    @cache
    def get_user_registry(cls) -> Self:
        return cls.objects.get(
            scope=Scope.get_root_scope(),
            slug="users",
        )

    def get_title_dict(self) -> dict[str, str]:
        return {
            language_code: title
            for language_code in SUPPORTED_LANGUAGE_CODES
            if (title := getattr(self, f"title_{language_code}"))
        }

    def can_be_deleted_by(self, request: HttpRequest) -> bool:
        return (
            not self.involvements.exists()
            and not self.surveys.exists()
            and not self.involvement_event_metas.exists()
            and not self.program_v2_event_metas.exists()
            and not self.badges_event_metas.exists()
            and is_graphql_allowed_for_model(
                request.user,
                instance=self,
                operation="delete",
                field="self",
            )
        )
