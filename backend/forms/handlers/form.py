from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models.form import Form


@receiver(post_save, sender=Form)
def form_post_save(sender, instance: Form, *, created: bool, update_fields: list[str] | None, **kwargs):
    """
    We can't call build_enriched_fields on an unsaved form.
    This will cause a second save, but forms are changed seldom so this should
    not cause a performance issue.

    Explicit update_fields=["cached_enriched_fields"] is used to signal that the
    has just been rebuilt and need not be rebuilt again.
    """
    if created:
        # need to postpone until after the form has been associated with a survey
        # see Form.enriched_fields
        return

    if update_fields is not None and "cached_enriched_fields" in update_fields:
        return

    instance.cached_enriched_fields = instance._build_enriched_fields()
    instance.save(update_fields=["cached_enriched_fields"])
