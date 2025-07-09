from django.urls import re_path

from .views import frostbite2025_afterparty_summary_view

urlpatterns = [
    re_path(
        r"^events/(?P<event_slug>frostbite2025)/labour/surveys/kaatoilmo/summary/?$",
        frostbite2025_afterparty_summary_view,
        name="frostbite2025_afterparty_summary_view",
    ),
]
