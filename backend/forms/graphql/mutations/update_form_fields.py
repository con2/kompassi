import graphene
import pydantic
from graphene.types.generic import GenericScalar

from access.cbac import graphql_check_instance

from ...models.field import Field
from ...models.survey import Survey
from ..survey_full import SurveyType


class UpdateFormFieldsInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    survey_slug = graphene.String(required=True)
    language = graphene.String(required=True)
    fields = GenericScalar(required=True)


class Fields(pydantic.BaseModel):
    fields: list[Field]


class UpdateFormFields(graphene.Mutation):
    class Arguments:
        input = UpdateFormFieldsInput(required=True)

    survey = graphene.Field(SurveyType)

    @staticmethod
    def mutate(
        root,
        info,
        input: UpdateFormFieldsInput,
    ):
        survey = Survey.objects.get(event__slug=input.event_slug, slug=input.survey_slug)
        form = survey.languages.get(language=input.language)
        fields = Fields.model_validate(dict(fields=input.fields))

        # TODO(#324) rethink
        graphql_check_instance(survey, info, "languages", "mutation")

        form.fields = [field.model_dump(mode="json", by_alias=True) for field in fields.fields]
        form.save(update_fields=["fields"])

        return UpdateFormFields(survey=survey)  # type: ignore
