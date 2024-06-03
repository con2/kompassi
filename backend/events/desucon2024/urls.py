from django.urls import re_path

from .views import desucon2024_afterparty_summary_view

urlpatterns = [
    re_path(
        r"^events/(?P<event_slug>desucon2024)/labour/surveys/kaatoilmo/summary/?$",
        desucon2024_afterparty_summary_view,
        name="desucon2024_afterparty_summary_view",
    ),
]
