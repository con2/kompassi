from django.urls import path

from .views.forms_projection_view import forms_projection_view
from .views.forms_survey_excel_export_view import forms_survey_excel_export_view
from .views.forms_survey_zip_export_view import forms_survey_zip_export_view

app_name = "forms"
urlpatterns = [
    path(
        "events/<slug:event_slug>/surveys/<slug:survey_slug>/responses.xlsx",
        forms_survey_excel_export_view,
        name="forms_survey_excel_export_view",
    ),
    path(
        "events/<slug:scope_slug>/surveys/<slug:survey_slug>/responses.zip",
        forms_survey_zip_export_view,
        name="forms_survey_zip_export_view",
    ),
    path(
        "api/v1/scopes/<slug:scope_slug>/projections/<slug:projection_slug>",
        forms_projection_view,
        name="forms_projection_view",
    ),
    path(
        "events/<slug:scope_slug>/projections/<slug:projection_slug>.xlsx",
        forms_projection_view,
        name="forms_projection_excel_view",
        kwargs={"format": "xlsx"},
    ),
]
