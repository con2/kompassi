from .views import tracon2024_afterparty_participants_view, tracon2024_afterparty_summary_view
from django.urls import re_path


urlpatterns = [
    re_path(
        r"^events/(?P<event_slug>tracon2024)/labour/surveys/kaatoilmo/results.xlsx$",
        tracon2024_afterparty_participants_view,
        name="tracon2024_afterparty_participants_view",
    ),
    re_path(
        r"^events/(?P<event_slug>tracon2024)/labour/surveys/kaatoilmo/summary/?$",
        tracon2024_afterparty_summary_view,
        name="tracon2024_afterparty_summary_view",
    ),
]
