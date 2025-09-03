from django.urls import path, re_path

from .views.calendar_export_view import calendar_export_view, single_program_calendar_export_view
from .views.paikkala_views import (
    paikkala_inspection_view,
    paikkala_profile_reservations_view,
    paikkala_relinquish_view,
    paikkala_reservation_view,
    paikkala_special_reservation_view,
)
from .views.program_hosts_excel_export_view import program_hosts_excel_export_view
from .views.program_offers_excel_export_view import program_offers_excel_export_view
from .views.schedule_items_excel_export_view import schedule_items_excel_export_view

app_name = "program_v2"
urlpatterns = [
    path(
        "events/<slug:event_slug>/program.ics",
        calendar_export_view,
        name="calendar_export_view",
    ),
    path(
        "events/<slug:event_slug>/programs/<slug:program_slug>.ics",
        single_program_calendar_export_view,
        name="single_program_calendar_export_view",
    ),
    path(
        "events/<slug:event_slug>/program-offers.xlsx",
        program_offers_excel_export_view,
        name="program_offers_excel_export_view",
    ),
    path(
        "events/<slug:event_slug>/program-hosts.xlsx",
        program_hosts_excel_export_view,
        name="program_hosts_excel_export_view",
    ),
    path(
        "events/<slug:event_slug>/schedule-items.xlsx",
        schedule_items_excel_export_view,
        name="schedule_items_excel_export_view",
    ),
    # paikkala (semi-legacy v1 views ported to v2)
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/reservations/(?P<schedule_item_slug>[a-z0-9-]+)/(?P<pk>\d+)/relinquish/?$",
        paikkala_relinquish_view,  # type: ignore
        name="paikkala_relinquish_view",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/reservations/(?P<schedule_item_slug>[a-z0-9-]+)/(?P<pk>\d+)/inspect/(?P<key>.+?)/?$",
        paikkala_inspection_view,  # type: ignore
        name="paikkala_inspection_view",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/reservations/(?P<schedule_item_slug>[a-z0-9-]+)/?$",
        paikkala_reservation_view,  # type: ignore
        name="paikkala_reservation_view",
    ),
    re_path(
        r"^reservations/(?P<code>[a-z0-9-]+)/?$",
        paikkala_special_reservation_view,
        name="paikkala_special_reservation_view",
    ),
    re_path(
        r"^profile/reservations/?",
        paikkala_profile_reservations_view,
        name="paikkala_profile_reservations_view",
    ),
]
