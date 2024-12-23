import graphene
from django import forms as django_forms
from graphene.types.generic import GenericScalar

from access.cbac import graphql_check_model
from core.models import Event

from ...models.product import Product
from ..product_limited import LimitedProductType


class CreateProductInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    form_data = GenericScalar(required=True)


class CreateProductForm(django_forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "title",
            "description",
            "price",
        ]


class CreateProduct(graphene.Mutation):
    class Arguments:
        input = CreateProductInput(required=True)

    product = graphene.Field(LimitedProductType)

    @staticmethod
    def mutate(
        root,
        info,
        input: CreateProductInput,
    ):
        event = Event.objects.get(slug=input.event_slug)
        graphql_check_model(Product, event.scope, info, "create")

        form = CreateProductForm(data=input.form_data)  # type: ignore
        if not form.is_valid():
            raise ValueError(form.errors)

        product = form.save(commit=False)
        product.event = event
        product.save()

        return CreateProduct(product=product)  # type: ignore
