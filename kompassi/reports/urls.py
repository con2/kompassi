from django.urls import re_path

from .views import REPORT_SOURCES, event_report_export_view, stats_report_export_view

app_name = "reports"
urlpatterns = [
    re_path(
        rf"^events/(?P<event_slug>[a-z0-9-]+)/(?P<source>{'|'.join(REPORT_SOURCES)})/reports/"
        r"(?P<report_slug>[a-z0-9_-]+)\.(?P<format>csv|xlsx)$",
        event_report_export_view,
        name="event_report_export_view",
    ),
    re_path(
        r"^stats/reports/(?P<report_slug>[a-z0-9_-]+)\.(?P<format>csv|xlsx)$",
        stats_report_export_view,
        name="stats_report_export_view",
    ),
]
