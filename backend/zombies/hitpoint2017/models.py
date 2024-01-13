from django.db import models

NIGHT_WORK_CHOICES = [
    ("miel", "Työskentelen mielelläni yövuorossa"),
    ("tarv", "Voin tarvittaessa työskennellä yövuorossa"),
    ("ei", "En vaan voi työskennellä yövuorossa"),
]

SHIFT_TYPE_CHOICES = [
    ("yksipitka", "Yksi pitkä vuoro"),
    ("montalyhytta", "Monta lyhyempää vuoroa"),
    ("kaikkikay", "Kumpi tahansa käy"),
]

TOTAL_WORK_CHOICES = [
    ("8h", "Minimi - 8 tuntia"),
    ("12h", "10–12 tuntia"),
    ("yli12h", "Työn Sankari! Yli 12 tuntia!"),
]


# NOTE: these are foolishly referred to in programme core and newer events, so they cannot be removed :(
class SimpleChoice(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class SpecialDiet(SimpleChoice):
    pass


class TimeSlot(SimpleChoice):
    pass
