from typing import TYPE_CHECKING

from django.db import models, transaction
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from kompassi.core.utils import time_bool_property
from kompassi.core.utils.cleanup import register_cleanup

from .constants import BADGE_ELIGIBLE_FOR_BATCHING

if TYPE_CHECKING:
    from .badge import Badge


def contains_moon_runes(unicode_str):
    try:
        unicode_str.encode("ISO-8859-1")
    except UnicodeEncodeError:
        return True
    else:
        return False


@register_cleanup(lambda qs: qs.filter(badges__isnull=True))
class Batch(models.Model):
    event = models.ForeignKey(
        "core.Event",
        on_delete=models.CASCADE,
        related_name="badge_batch_set",
    )

    personnel_class = models.ForeignKey(
        "labour.PersonnelClass",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))
    printed_at = models.DateTimeField(null=True, blank=True)

    is_printed = time_bool_property("printed_at")

    badges: models.QuerySet["Badge"]

    @classmethod
    def create(cls, event, personnel_class=None, max_items=100, moon_rune_policy="dontcare"):
        from .badge import Badge

        if personnel_class is not None:
            if personnel_class.event != event:
                raise AssertionError("personnel_class in wrong event")
            badges = Badge.objects.filter(personnel_class=personnel_class)
        else:
            badges = Badge.objects.filter(personnel_class__event=event)

        if moon_rune_policy == "onlyinclude":
            fields = Badge.get_csv_fields(event)
            test = lambda badge: contains_moon_runes(badge.get_printable_text(fields))
        elif moon_rune_policy == "exclude":
            fields = Badge.get_csv_fields(event)
            test = lambda badge: not contains_moon_runes(badge.get_printable_text(fields))
        elif moon_rune_policy == "dontcare":
            test = lambda badge: True
        else:
            raise NotImplementedError(moon_rune_policy)

        with transaction.atomic():
            batch = cls(personnel_class=personnel_class, event=event)
            batch.save()

            badges = badges.filter(**BADGE_ELIGIBLE_FOR_BATCHING).order_by("created_at")
            num_selected_badges = 0

            for badge in badges:
                if test(badge):
                    badge.batch = batch
                    badge.save()

                    num_selected_badges += 1
                    if max_items is not None and num_selected_badges >= max_items:
                        break

        return batch

    def confirm(self):
        self.printed_at = now()
        self.save()

    def cancel(self):
        self.badges.update(batch=None)
        self.delete()

    def can_cancel(self):
        return self.printed_at is not None

    def can_confirm(self):
        return self.printed_at is not None

    def __str__(self):
        return _("Batch %(batch_number)s") % dict(batch_number=self.pk)

    def admin_get_number(self):
        return str(self)

    admin_get_number.short_description = _("Batch number")
    admin_get_number.admin_order_field = "id"

    def admin_get_num_badges(self):
        return self.badges.count()

    admin_get_num_badges.short_description = _("Number of badges")

    class Meta:
        verbose_name = _("Batch")
        verbose_name_plural = _("Batches")
