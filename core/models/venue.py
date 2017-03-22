# encoding: utf-8

from django.db import models


class Venue(models.Model):
    name = models.CharField(max_length=63, verbose_name='Tapahtumapaikan nimi')
    name_inessive = models.CharField(
        max_length=63,
        verbose_name='Tapahtumapaikan nimi inessiivissä',
        help_text='Esimerkki: Paasitornissa',
    )

    class Meta:
        verbose_name = 'Tapahtumapaikka'
        verbose_name_plural = 'Tapahtumapaikat'

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name and not self.name_inessive:
            self.name_inessive = self.name + 'ssa'

        return super(Venue, self).save(*args, **kwargs)

    @classmethod
    def get_or_create_dummy(cls):
        return cls.objects.get_or_create(
            name='Dummy venue'
        )