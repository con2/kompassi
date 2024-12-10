from django.urls import path

from .views.etickets_view import etickets_view

app_name = "tickets_v2"
urlpatterns = [
    path(
        "events/<slug:event_slug>/orders/<slug:order_id>/e-ticket.pdf",
        etickets_view,
        name="etickets_view",
    ),
    # NOTE: These are served by optimized_server
    # path(
    #     "api/tickets-v2/events/<slug:event_slug>/products/",
    #     get_products,
    #     name="tickets_v2_get_products",
    # ),
    # path(
    #     "api/tickets-v2/events/<slug:event_slug>/orders/",
    #     create_order,
    #     name="tickets_v2_create_order",
    # ),
]
