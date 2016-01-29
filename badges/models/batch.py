# encoding: utf-8


from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from core.utils import time_bool_property

from .constants import BADGE_ELIGIBLE_FOR_BATCHING


class Batch(models.Model):
    event = models.ForeignKey('core.Event', related_name='badge_batch_set')

    personnel_class = models.ForeignKey('labour.PersonnelClass', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_(u'Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_(u'Updated at'))
    printed_at = models.DateTimeField(null=True, blank=True)

    is_printed = time_bool_property('printed_at')

    @classmethod
    def create(cls, event, personnel_class=None, max_items=100):
        from .badge import Badge

        if personnel_class is not None:
            assert personnel_class.event == event
            badges = Badge.objects.filter(personnel_class=personnel_class)
        else:
            badges = Badge.objects.filter(personnel_class__event=event)

        badges = badges.filter(**BADGE_ELIGIBLE_FOR_BATCHING).order_by('created_at')

        if max_items is not None:
            badges = badges[:max_items]

        batch = cls(personnel_class=personnel_class, event=event)
        batch.save()

        # Cannot update a query once a slice has been taken.
        # badges.update(batch=batch)
        for badge in badges:
            badge.batch = batch
            badge.save()

        return batch

    def confirm(self):
        self.printed_at = now()
        self.save()

    def cancel(self):
        self.badge_set.update(batch=None)
        self.delete()

    def can_cancel(self):
        return self.printed_at is not None

    def can_confirm(self):
        return self.printed_at is not None

    def __unicode__(self):
        return _(u"Batch %(batch_number)s") % dict(batch_number=self.pk)