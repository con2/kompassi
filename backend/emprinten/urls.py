from django.conf import settings
from django.urls import path

from . import views

urlpatterns = []

if settings.DEBUG:
    urlpatterns.append(path("emp/<slug:slug>/make", views.handle_debug_request))
