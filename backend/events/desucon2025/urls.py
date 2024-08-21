from django.urls import re_path

from .views import desucon2025_afterparty_summary_view

urlpatterns = [
    re_path(
        r"^events/(?P<event_slug>desucon2025)/labour/surveys/kaatoilmo/summary/?$",
        desucon2025_afterparty_summary_view,
        name="desucon2025_afterparty_summary_view",
    ),
]
