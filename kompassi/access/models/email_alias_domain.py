from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from kompassi.core.models.organization import Organization


class EmailAliasDomain(models.Model):
    domain_name = models.CharField(
        max_length=255,
        unique=True,
        help_text="eg. example.com",
    )
    organization: models.ForeignKey[Organization] = models.ForeignKey(
        "core.Organization",
        on_delete=models.CASCADE,
    )
    has_internal_aliases = models.BooleanField(default=False)

    @classmethod
    def get_or_create_dummy(
        cls,
        domain_name="example.com",
        has_internal_aliases: bool = True,
    ):
        from kompassi.access.models.internal_email_alias import InternalEmailAlias
        from kompassi.core.models.organization import Organization

        organization, unused = Organization.get_or_create_dummy()

        domain, created = cls.objects.get_or_create(
            domain_name=domain_name,
            defaults=dict(
                organization=organization,
                has_internal_aliases=has_internal_aliases,
            ),
        )

        if has_internal_aliases:
            InternalEmailAlias.ensure_internal_email_aliases()

        return domain, created

    def __str__(self):
        return self.domain_name
