from django.db import models
from django.utils.translation import gettext_lazy as _


class EmailAliasDomain(models.Model):
    domain_name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("domain"),
        help_text=_("eg. example.com"),
    )
    organization = models.ForeignKey("core.Organization", on_delete=models.CASCADE, verbose_name=_("organization"))
    has_internal_aliases = models.BooleanField(default=False)

    @classmethod
    def get_or_create_dummy(
        cls,
        domain_name="example.com",
        has_internal_aliases: bool = True,
    ):
        from access.models.internal_email_alias import InternalEmailAlias
        from core.models.organization import Organization

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

    class Meta:
        verbose_name = _("e-mail alias domain")
        verbose_name_plural = _("e-mail alias domains")
