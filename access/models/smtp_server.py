# encoding: utf-8



from django.db import models
from django.utils.translation import ugettext_lazy as _


class SMTPServer(models.Model):
    hostname = models.CharField(
        max_length=255,
        verbose_name=_('SMTP server'),
    )

    crypto = models.CharField(
        max_length=5,
        verbose_name=_('encryption'),
        default='tls',
        choices=[('plain', 'Ei salausta'), ('ssl', 'SSL'), ('tls', 'TLS')],
    )

    port = models.IntegerField(
        verbose_name=_('port number'),
        default=587,
    )

    domains = models.ManyToManyField('access.EmailAliasDomain',
        verbose_name=_('domains'),
        related_name='smtp_servers',
    )

    def __unicode__(self):
        return self.hostname

    class Meta:
        verbose_name = _('SMTP server')
        verbose_name_plural = _('SMTP servers')
