import graphene
import pydantic
from django.db import transaction
from graphene.types.generic import GenericScalar

from kompassi.access.cbac import graphql_check_instance

from ...models.field import Field
from ...models.survey import Survey
from ..survey_full import FullSurveyType


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

    survey = graphene.Field(FullSurveyType)

    @staticmethod
    def mutate(
        root,
        info,
        input: UpdateFormFieldsInput,
    ):
        with transaction.atomic():
            survey = Survey.objects.get(event__slug=input.event_slug, slug=input.survey_slug)
            form = survey.languages.get(language=input.language)
            fields = Fields.model_validate(dict(fields=input.fields))

            graphql_check_instance(
                survey,
                info,
                app=survey.app,
                field="languages",
                operation="update",
            )

            # Dimension fields' choices are only ever derived from the dimension at read time
            # (see Form._enrich_field). Persisting client-supplied choices for them would freeze
            # stale values and translations in place, so they must never be saved.
            form.fields = [
                field.model_dump(
                    mode="json",
                    by_alias=True,
                    exclude={"choices"} if field.type.is_dimension_field else None,
                )
                for field in fields.fields
            ]
            form.save(update_fields=["fields", "cached_enriched_fields"])

            survey.refresh_cached_key_fields(form)

            return UpdateFormFields(survey=survey)  # type: ignore
