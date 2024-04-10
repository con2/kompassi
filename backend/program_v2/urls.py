from django.urls import path

from .views.calendar_export_view import calendar_export_view, single_program_calendar_export_view

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
]
