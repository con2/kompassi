# encoding: utf-8



from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class SimpleChoice(models.Model):
    """
    Abstract base model for generic simple M2M fields.
    """

    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class SpecialDiet(SimpleChoice):
    pass
