# encoding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _


class InfoLink(models.Model):
    event = models.ForeignKey('core.Event', verbose_name=u'Tapahtuma')
    group = models.ForeignKey('auth.Group',
        verbose_name=u'Ryhmä',
        help_text=u'Linkki näytetään vain tämän ryhmän jäsenille.',
    )

    url = models.CharField(
        max_length=255,
        verbose_name=u'Osoite',
        help_text=u'Muista aloittaa ulkoiset linkit <i>http://</i> tai <i>https://</i>.'
    )

    title = models.CharField(max_length=255, verbose_name=u'Teksti')

    class Meta:
        verbose_name = _(u'info link')
        verbose_name_plural = _(u'info links')

    def __unicode__(self):
        return self.title