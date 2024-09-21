from django.urls import path

from .views.public_api import create_order, get_products

urlpatterns = [
    path(
        "api/tickets-v2/events/<slug:event_slug>/products/",
        get_products,
        name="tickets_v2_get_products",
    ),
    path(
        "api/tickets-v2/events/<slug:event_slug>/orders/",
        create_order,
        name="tickets_v2_create_order",
    ),
]
