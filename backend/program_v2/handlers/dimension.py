from django.db.models import QuerySet
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.forms import ValidationError

from core.utils import slugify
from core.utils.locale_utils import get_message_in_language
from graphql_api.language import DEFAULT_LANGUAGE

from ..models import Dimension, DimensionValue, Program, ProgramDimensionValue


@receiver(pre_save, sender=ProgramDimensionValue)
def program_dimension_value_pre_save(sender, instance: ProgramDimensionValue, **kwargs):
    if instance.dimension is None:
        instance.dimension = instance.value.dimension
    elif instance.dimension != instance.value.dimension:
        raise ValidationError({"dimension": "Dimension value does not belong to the dimension"})


@receiver([post_save, post_delete], sender=Dimension)
@receiver([post_save, post_delete], sender=DimensionValue)
def dimension_post_save(sender, instance: Dimension | DimensionValue, **kwargs):
    if isinstance(kwargs["origin"], QuerySet):
        # should not run on bulk delete :)
        return

    if kwargs.get("update_fields", {}):
        return

    Program.refresh_cached_dimensions_qs(instance.event.programs.all())


@receiver([post_save, post_delete], sender=ProgramDimensionValue)
def program_dimension_value_post_save(sender, instance: ProgramDimensionValue, **kwargs):
    if isinstance(kwargs["origin"], QuerySet):
        # should not run on bulk delete :)
        return

    if kwargs.get("update_fields", {}):
        return

    program = instance.program
    program.refresh_cached_dimensions()

    for schedule_item in program.schedule_items.all():
        schedule_item.refresh_cached_fields()


@receiver(pre_save, sender=(Dimension, DimensionValue))
def dimension_pre_save(sender, instance: Dimension | DimensionValue, **kwargs):
    if instance.slug is None and (title := get_message_in_language(instance.title, DEFAULT_LANGUAGE)):
        instance.slug = slugify(title)
