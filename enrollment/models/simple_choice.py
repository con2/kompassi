from django.db import models


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


class ConconPart(SimpleChoice):
    pass
