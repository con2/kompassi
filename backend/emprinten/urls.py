from django.conf import settings
from django.urls import path

from . import views

urlpatterns = [
    path("events/<slug:event>/emp/<slug:slug>/", views.project_index, name="emprinten_index"),
    path("events/<slug:event>/emp/<slug:slug>/upload/", views.handle_csv_upload, name="emprinten_upload"),
]

if settings.DEBUG:
    urlpatterns.append(path("emp/<slug:slug>/make", views.handle_debug_request))
