from __future__ import annotations

from functools import cache
from typing import Self

from django.db import models

from core.models.organization import Organization
from dimensions.models.scope import Scope
from graphql_api.language import DEFAULT_LANGUAGE, getattr_message_in_language


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
