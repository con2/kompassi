import graphene
from django.db import transaction
from django.http import HttpRequest

from core.models import Event
from event_log_v2.utils.emit import emit

from ...models.product import Product


class DeleteProductInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    product_id = graphene.String(required=True)


class DeleteProduct(graphene.Mutation):
    class Arguments:
        input = DeleteProductInput(required=True)

    id = graphene.NonNull(graphene.String)

    @transaction.atomic
    @staticmethod
    def mutate(
        root,
        info,
        input: DeleteProductInput,
    ):
        request: HttpRequest = info.context

        event = Event.objects.get(slug=input.event_slug)
        product = Product.objects.get(event=event, id=input.product_id, superseded_by=None)

        if not product.can_be_deleted_by(request):
            raise ValueError("Cannot delete product")

        product.delete()

        emit(
            "tickets_v2.product.deleted",
            event=event,
            product=input.product_id,
            request=request,
            context=product.admin_url,
        )

        return DeleteProduct(id=input.product_id)  # type: ignore
