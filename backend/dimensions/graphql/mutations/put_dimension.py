import graphene
from django import forms as django_forms
from graphene.types.generic import GenericScalar

from access.cbac import graphql_check_instance
from core.utils.form_utils import camel_case_keys_to_snake_case

from ...models.dimension import Dimension
from ...models.universe import Universe
from ..dimension_full import FullDimensionType


class DimensionForm(django_forms.ModelForm):
    class Meta:
        model = Dimension
        fields = (
            "slug",
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk is not None:
            del self.fields["slug"]


class PutDimensionInput(graphene.InputObjectType):
    scope_slug = graphene.String(required=True)
    universe_slug = graphene.String(required=True)
    dimension_slug = graphene.String(description="If set, update existing; otherwise, create new")
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
        form_data = camel_case_keys_to_snake_case(input.form_data)  # type: ignore

        universe = Universe.objects.get(
            scope__slug=input.scope_slug,
            slug=input.universe_slug,
        )

        graphql_check_instance(
            universe,  # type: ignore
            info,
            app=universe.app.value,
            field="dimensions",
            operation="update",
        )

        # TODO update_or_create
        dimension: Dimension
        if input.dimension_slug is not None:
            # updating existing Dimension
            dimension = universe.dimensions.get(slug=input.dimension_slug)
            form = DimensionForm(form_data, instance=dimension)

            # TODO dimension.can_be_edited_by
            if dimension.is_technical:
                raise ValueError("Cannot edit technical dimension")
        else:
            form = DimensionForm(form_data)

        if form.is_valid():
            dimension = form.save(commit=False)
            dimension.universe = universe
            dimension.save()
        else:
            raise django_forms.ValidationError(form.errors)

        dimension.refresh_dependents()

        return PutDimension(dimension=dimension)  # type: ignore
