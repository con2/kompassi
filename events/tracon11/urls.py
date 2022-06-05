
from .views import tracon11_afterparty_participants_view
from django.urls import re_path


urlpatterns = [
    re_path(
        r"^events/(?P<event_slug>tracon11)/survey/kaatoilmo/results.xlsx$",
        tracon11_afterparty_participants_view,
        name="tracon11_afterparty_participants_view",
    ),
]
