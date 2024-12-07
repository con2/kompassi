import graphene
from graphene.types.generic import GenericScalar

from access.cbac import graphql_check_instance

from ...models.dimension_dto import DimensionValueDTO
from ...models.survey import Survey
from ..dimension import SurveyDimensionValueType


class PutSurveyDimensionValueInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    survey_slug = graphene.String(required=True)
    dimension_slug = graphene.String(required=True)
    value_slug = graphene.String(description="If set, update existing; otherwise, create new")
    form_data = GenericScalar(required=True)


class PutSurveyDimensionValue(graphene.Mutation):
    class Arguments:
        input = PutSurveyDimensionValueInput(required=True)

    value = graphene.Field(SurveyDimensionValueType)

    @staticmethod
    def mutate(
        root,
        info,
        input: PutSurveyDimensionValueInput,
    ):
        survey = Survey.objects.get(event__slug=input.event_slug, slug=input.survey_slug)
        form_data: dict[str, str] = input.form_data  # type: ignore

        # TODO bastardization of graphql_check_access, rethink
        graphql_check_instance(survey, info, "dimensions", "mutation")

        dimension = survey.dimensions.get(slug=input.dimension_slug)

        if input.value_slug is None:
            if survey.dimensions.filter(slug=form_data["slug"]).exists():
                raise ValueError("Dimension value with this slug already exists")
        else:
            form_data["slug"] = input.value_slug  # type: ignore

        value = DimensionValueDTO.from_form_data(form_data).save(dimension)

        return PutSurveyDimensionValue(value=value)  # type: ignore
