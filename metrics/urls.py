from django.urls import re_path

from .views import dummy_metrics_view

urlpatterns = [
    re_path(r"metrics/?", dummy_metrics_view),
]
