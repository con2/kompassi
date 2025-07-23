from django.urls import re_path

from .views import tracon2025_afterparty_participants_view, tracon2025_afterparty_summary_view

urlpatterns = [
    re_path(
        r"^events/(?P<event_slug>tracon2025)/labour/surveys/kaatoilmo/results.xlsx$",
        tracon2025_afterparty_participants_view,
        name="tracon2025_afterparty_participants_view",
    ),
    re_path(
        r"^events/(?P<event_slug>tracon2025)/labour/surveys/kaatoilmo/summary/?$",
        tracon2025_afterparty_summary_view,
        name="tracon2025_afterparty_summary_view",
    ),
]
