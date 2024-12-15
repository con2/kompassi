from django.db.models import QuerySet
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from dimensions.models.dimension import Dimension
from dimensions.models.dimension_value import DimensionValue

from ..models.dimension_values import ProgramDimensionValue
from ..models.program import Program


@receiver(post_delete, sender=Dimension)
@receiver(post_delete, sender=DimensionValue)
def dimension_post_save(sender, instance: Dimension | DimensionValue, **kwargs):
    if isinstance(kwargs["origin"], QuerySet):
        # should not run on bulk delete :)
        return

    if kwargs.get("update_fields", []):
        return

    universe = instance.universe
    if universe.app != "program_v2":
        return

    event = universe.scope.event
    if event is None:
        raise ValueError(f"Universe {universe} is has app=program_v2 but no event")

    Program.refresh_cached_dimensions_qs(event.programs.all())


@receiver([post_save, post_delete], sender=ProgramDimensionValue)
def program_dimension_value_post_save(sender, instance: ProgramDimensionValue, **kwargs):
    if isinstance(kwargs["origin"], QuerySet):
        # should not run on bulk delete :)
        return

    if kwargs.get("update_fields", []):
        return

    program = instance.program
    program.refresh_cached_dimensions()

    for schedule_item in program.schedule_items.all():
        schedule_item.refresh_cached_fields()
