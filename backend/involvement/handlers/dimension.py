from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from dimensions.models.dimension import Dimension
from dimensions.models.dimension_value import DimensionValue

from ..models.involvement import Involvement
from ..models.involvement_dimension_value import InvolvementDimensionValue


@receiver(post_delete, sender=Dimension)
@receiver(post_delete, sender=DimensionValue)
def dimension_post_delete(sender, instance: Dimension | DimensionValue, **kwargs):
    universe = instance.universe
    Involvement.refresh_cached_dimensions_qs(universe.involvements.all())


@receiver([post_save, post_delete], sender=InvolvementDimensionValue)
def response_dimension_value_post_save(sender, instance: InvolvementDimensionValue, **kwargs):
    involvement: Involvement = instance.subject
    involvement.refresh_cached_dimensions()
