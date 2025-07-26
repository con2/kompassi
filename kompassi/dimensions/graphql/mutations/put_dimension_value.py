import graphene
from django import forms as django_forms
from graphene.types.generic import GenericScalar

from kompassi.core.middleware import RequestWithCache
from kompassi.core.utils.form_utils import camel_case_keys_to_snake_case
from kompassi.core.utils.model_utils import slugify

from ...models.universe import Universe
from ..dimension_full import DimensionValueType
from ..dimension_value import DimensionValue


class DimensionValueForm(django_forms.ModelForm):
    class Meta:
        model = DimensionValue
        fields = (
            "color",
            "is_subject_locked",
            # NOTE SUPPORTED_LANGUAGES
            "title_en",
            "title_fi",
            "title_sv",
        )


class PutDimensionValueInput(graphene.InputObjectType):
    scope_slug = graphene.String(required=True)
    universe_slug = graphene.String(required=True)
    dimension_slug = graphene.String(required=True)
    value_slug = graphene.String(required=True)
    form_data = GenericScalar(required=True)


class PutDimensionValue(graphene.Mutation):
    class Arguments:
        input = PutDimensionValueInput(required=True)

    value = graphene.Field(DimensionValueType)

    @staticmethod
    def mutate(
        root,
        info,
        input: PutDimensionValueInput,
    ):
        request: RequestWithCache = info.context
        form_data = camel_case_keys_to_snake_case(input.form_data)  # type: ignore

        universe = Universe.objects.get(
            scope__slug=input.scope_slug,
            slug=input.universe_slug,
        )
        dimension = universe.dimensions.get(slug=input.dimension_slug)
        value: DimensionValue | None = dimension.values.filter(slug=input.value_slug).first()

        form = DimensionValueForm(form_data, instance=value)
        if not form.is_valid():
            raise django_forms.ValidationError(form.errors)

        if value is None:
            if not dimension.can_values_be_created_by(request):
                raise Exception("You cannot create values in this dimension.")

            created_value: DimensionValue = form.save(commit=False)
            created_value.dimension = dimension
            created_value.slug = slugify(input.value_slug)  # type: ignore
            created_value.save()

            value = created_value
        else:
            if not value.can_be_updated_by(request):
                raise Exception("You cannot update this value.")

            value = form.save()

        dimension.refresh_dependents()

        return PutDimensionValue(value=value)  # type: ignore
