from django.db import models
from django.utils.translation import gettext_lazy as _

from kompassi.core.utils import get_objects_within_period

TARGET_CHOICES = [
    ("", _("Same window")),
    ("_blank", _("New window")),
]


class CarouselSlide(models.Model):
    active_from = models.DateTimeField(blank=True, null=True)
    active_until = models.DateTimeField(blank=True, null=True)
    href = models.CharField(max_length=512, blank=True, default="")
    title = models.CharField(max_length=512, blank=True, default="")
    image_file = models.FileField(upload_to="carousel_slides", blank=True)
    image_credit = models.CharField(max_length=512, blank=True, default="")
    target = models.CharField(
        blank=True,
        choices=TARGET_CHOICES,
        max_length=max(len(key) for (key, label) in TARGET_CHOICES),
        default=TARGET_CHOICES[0][0],
    )
    order = models.IntegerField(default=0)

    @classmethod
    def get_active_slides(cls, t=None, **extra_criteria):
        return get_objects_within_period(cls, t=t, **extra_criteria)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("carousel slide")
        verbose_name_plural = _("carousel slides")
        ordering = ("order", "-active_from")
