from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from dimensions.models.dimension import Dimension
from dimensions.models.dimension_value import DimensionValue

from ..models.form import Form
from ..models.response import Response
from ..models.response_dimension_value import ResponseDimensionValue
from ..models.survey import Survey
from ..models.survey_default_dimension_value import SurveyDefaultDimensionValue


@receiver(post_delete, sender=Dimension)
@receiver(post_delete, sender=DimensionValue)
def dimension_post_delete(sender, instance: Dimension | DimensionValue, **kwargs):
    universe = instance.universe
    surveys = universe.surveys.all()

    Response.refresh_cached_dimensions_qs(Response.objects.filter(form__survey__in=surveys))
    Form.refresh_enriched_fields_qs(Form.objects.filter(survey__in=surveys))


@receiver([post_save, post_delete], sender=ResponseDimensionValue)
def response_dimension_value_post_save(sender, instance: ResponseDimensionValue, **kwargs):
    response: Response = instance.response
    response.refresh_cached_dimensions()


@receiver([post_save, post_delete], sender=SurveyDefaultDimensionValue)
def survey_default_dimension_value_post_save(sender, instance: SurveyDefaultDimensionValue, **kwargs):
    survey: Survey = instance.survey
    survey.refresh_cached_default_dimensions()
