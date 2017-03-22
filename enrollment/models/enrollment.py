# encoding: utf-8



from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Enrollment(models.Model):
    """
    Holds all the possible fields an enrollment instance may have
    """
    event = models.ForeignKey('core.event')
    person = models.ForeignKey('core.person')

    special_diet = models.ManyToManyField(
        'enrollment.SpecialDiet',
        blank=True,
        verbose_name=_("Diet")
    )

    special_diet_other = models.TextField(
        blank=True,
        verbose_name=_('Other diets'),
        help_text=_(
            'If you\'re on a diet that\'s not included in the list, '
            'please detail your diet here. Event organizer will try '
            'to take dietary needs into consideration, but all diets '
            'may not be catered for.'
        )
    )

    @property
    def formatted_special_diet(self):
        return ', '.join(sd.name for sd in self.special_diet.all())

    def __str__(self):
        return '{event}: {person}'.format(
            event=self.event,
            person=self.person,
        )
