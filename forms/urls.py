from django.urls import path

from .views.forms_excel_export_view import forms_excel_export_view
from .views.forms_survey_excel_export_view import forms_survey_excel_export_view

app_name = "forms"
urlpatterns = [
    path(
        "forms/<slug:form_slug>/responses.xlsx",
        forms_excel_export_view,
        name="forms_global_form_excel_export_view",
    ),
    path(
        "events/<slug:event_slug>/forms/<slug:form_slug>/responses.xlsx",
        forms_excel_export_view,
        name="forms_event_form_excel_export_view",
    ),
    path(
        "surveys/<slug:survey_slug>/responses.xlsx",
        forms_survey_excel_export_view,
        name="forms_global_survey_excel_export_view",
    ),
    path(
        "events/<slug:event_slug>/surveys/<slug:survey_slug>/responses.xlsx",
        forms_survey_excel_export_view,
        name="forms_event_survey_excel_export_view",
    ),
]
