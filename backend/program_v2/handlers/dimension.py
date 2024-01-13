from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.forms import ValidationError

from core.utils import slugify

from ..models import Dimension, DimensionValue, Program, ProgramDimensionValue


@receiver(pre_save, sender=ProgramDimensionValue)
def program_dimension_value_pre_save(sender, instance: ProgramDimensionValue, **kwargs):
    if instance.dimension is None:
        instance.dimension = instance.value.dimension
    else:
        if instance.dimension != instance.value.dimension:
            raise ValidationError({"dimension": "Dimension value does not belong to the dimension"})


@receiver([post_save, post_delete], sender=Dimension)
@receiver([post_save, post_delete], sender=DimensionValue)
def dimension_post_save(sender, instance: Dimension | DimensionValue, **kwargs):
    Program.refresh_cached_dimensions(instance.event.programs.all())


@receiver([post_save, post_delete], sender=ProgramDimensionValue)
def program_dimension_value_post_save(sender, instance: ProgramDimensionValue, **kwargs):
    program = instance.program
    program.cached_dimensions = program._dimensions
    program.save(update_fields=["cached_dimensions"])


@receiver(pre_save, sender=(Dimension, DimensionValue))
def dimension_pre_save(sender, instance: Dimension | DimensionValue, **kwargs):
    if instance.slug is None:
        instance.slug = slugify(instance.title.en or instance.title.fi)
