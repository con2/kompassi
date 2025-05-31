import graphene
from django import forms as django_forms
from graphene.types.generic import GenericScalar

from access.cbac import graphql_check_instance
from core.utils.form_utils import camel_case_keys_to_snake_case

from ...models.universe import Universe
from ..dimension import DimensionValueType
from ..dimension_value import DimensionValue


class DimensionValueForm(django_forms.ModelForm):
    class Meta:
        model = DimensionValue
        fields = (
            "slug",
            "color",
            "is_subject_locked",
            # NOTE SUPPORTED_LANGUAGES
            "title_en",
            "title_fi",
            "title_sv",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk is not None:
            del self.fields["slug"]


class PutDimensionValueInput(graphene.InputObjectType):
    scope_slug = graphene.String(required=True)
    universe_slug = graphene.String(required=True)
    dimension_slug = graphene.String(required=True)
    value_slug = graphene.String(description="If set, update existing; otherwise, create new")
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
        form_data = camel_case_keys_to_snake_case(input.form_data)  # type: ignore

        universe = Universe.objects.get(
            scope__slug=input.scope_slug,
            slug=input.universe_slug,
        )

        graphql_check_instance(
            universe,  # type: ignore
            info,
            app=universe.app,
            field="dimensions",
            operation="update",
        )

        dimension = universe.dimensions.get(slug=input.dimension_slug)

        if input.value_slug is not None:
            value = dimension.values.get(slug=input.value_slug)

            # TODO value.can_be_edited_by
            if value.is_technical:
                raise ValueError("Cannot edit technical dimension")

            form = DimensionValueForm(form_data, instance=value)
        else:
            form = DimensionValueForm(form_data)

        if form.is_valid():
            value = form.save(commit=False)
            value.dimension = dimension
            value.save()
        else:
            raise django_forms.ValidationError(form.errors)

        return PutDimensionValue(value=value)  # type: ignore
