import graphene
from django import forms as django_forms
from graphene.types.generic import GenericScalar

from kompassi.core.middleware import RequestWithCache
from kompassi.core.utils.form_utils import camel_case_keys_to_snake_case
from kompassi.core.utils.model_utils import slugify

from ...models.dimension import Dimension
from ...models.universe import Universe
from ..dimension_full import FullDimensionType


class DimensionForm(django_forms.ModelForm):
    class Meta:
        model = Dimension
        fields = (
            "is_public",
            "is_key_dimension",
            "is_multi_value",
            "is_list_filter",
            "is_shown_in_detail",
            "is_negative_selection",
            "value_ordering",
            # NOTE SUPPORTED_LANGUAGES
            "title_en",
            "title_fi",
            "title_sv",
        )


class PutDimensionInput(graphene.InputObjectType):
    scope_slug = graphene.String(required=True)
    universe_slug = graphene.String(required=True)
    dimension_slug = graphene.String(required=True)
    form_data = GenericScalar(required=True)


class PutDimension(graphene.Mutation):
    class Arguments:
        input = PutDimensionInput(required=True)

    dimension = graphene.Field(FullDimensionType)

    @staticmethod
    def mutate(
        root,
        info,
        input: PutDimensionInput,
    ):
        request: RequestWithCache = info.context
        form_data = camel_case_keys_to_snake_case(input.form_data)  # type: ignore

        universe = Universe.objects.get(
            scope__slug=input.scope_slug,
            slug=input.universe_slug,
        )

        dimension = universe.dimensions.filter(slug=input.dimension_slug).first()

        form = DimensionForm(form_data, instance=dimension)
        if not form.is_valid():
            raise django_forms.ValidationError(form.errors)

        if dimension is None:
            if not universe.can_dimensions_be_created_by(request):
                raise Exception("You cannot create dimensions in this universe.")

            created_dimension = form.save(commit=False)
            created_dimension.universe = universe
            created_dimension.slug = slugify(input.dimension_slug)  # type: ignore
            created_dimension.save()

            dimension = created_dimension
        else:
            if not dimension.can_be_updated_by(request):
                raise Exception("You cannot update this dimension.")

            dimension = form.save()

        dimension.refresh_dependents()

        return PutDimension(dimension=dimension)  # type: ignore
