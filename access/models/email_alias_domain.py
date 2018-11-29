from django.db import models
from django.utils.translation import ugettext_lazy as _


class EmailAliasDomain(models.Model):
    domain_name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_('domain'),
        help_text=_('eg. example.com'),
    )
    organization = models.ForeignKey('core.Organization', on_delete=models.CASCADE, verbose_name=_('organization'))
    has_internal_aliases = models.BooleanField(default=False)

    @classmethod
    def get_or_create_dummy(cls, domain_name='example.com'):
        from core.models.organization import Organization
        organization, unused = Organization.get_or_create_dummy()

        return cls.objects.get_or_create(domain_name=domain_name, defaults=dict(organization=organization))

    def __str__(self):
        return self.domain_name

    class Meta:
        verbose_name = _('e-mail alias domain')
        verbose_name_plural = _('e-mail alias domains')
