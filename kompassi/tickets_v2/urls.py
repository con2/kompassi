from django.urls import path, re_path

from .views.etickets_view import etickets_view
from .views.pos_view import pos_view

app_name = "tickets_v2"
urlpatterns = [
    path(
        "events/<slug:event_slug>/orders/<slug:order_id>/e-ticket.pdf",
        etickets_view,
        name="etickets_view",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/pos/?$",
        pos_view,
        name="pos_view",
    ),
]
