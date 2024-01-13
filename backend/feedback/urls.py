from django.urls import path, re_path
from django.views.generic import TemplateView

from .views import feedback_view

urlpatterns = [
    path(
        "feedback",
        feedback_view,
        name="feedback_view",
    ),
    re_path(
        r"^feedback.js$",
        TemplateView.as_view(template_name="feedback.js"),
        name="feedback_js_view",
    ),
]
