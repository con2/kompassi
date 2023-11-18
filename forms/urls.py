from django.urls import path

from .views import forms_excel_export_view

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
]
