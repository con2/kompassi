from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from dimensions.models.dimension import Dimension
from dimensions.models.dimension_value import DimensionValue

from ..models.form import Form
from ..models.response import Response
from ..models.response_dimension_value import ResponseDimensionValue


@receiver(post_delete, sender=Dimension)
@receiver(post_delete, sender=DimensionValue)
def dimension_post_delete(sender, instance: Dimension | DimensionValue, **kwargs):
    universe = instance.universe
    if universe.app != "forms":
        return

    survey = universe.survey
    if survey is None:
        raise ValueError(f"Universe {universe} is has app=forms but no survey")

    Response.refresh_cached_dimensions_qs(survey.responses.all())
    Form.refresh_enriched_fields_qs(survey.languages.all())


@receiver([post_save, post_delete], sender=ResponseDimensionValue)
def response_dimension_value_post_save(sender, instance: ResponseDimensionValue, **kwargs):
    response = instance.response
    response.refresh_cached_dimensions()
