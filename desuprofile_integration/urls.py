from django.urls import re_path
from django.views.generic.base import TemplateView

from .views import (
    CallbackView,
    ConfirmationView,
    LoginView,
    desuprogramme_feedback_view,
)

urlpatterns = [
    re_path(
        r"^desuprofile/oauth2/login/?$",
        LoginView.as_view(),
        name="desuprofile_integration_oauth2_login_view",
    ),
    re_path(
        r"^desuprofile/oauth2/callback/?$",
        CallbackView.as_view(),
        name="desuprofile_integration_oauth2_callback_view",
    ),
    re_path(
        r"^desuprofile/confirm/?$",
        TemplateView.as_view(template_name="desuprofile_integration_confirmation_required_view.pug"),
        name="desuprofile_integration_confirmation_required_view",
    ),
    re_path(
        r"^desuprofile/confirm/(?P<code>[a-f0-9]+)/?$",
        ConfirmationView.as_view(),
        name="desuprofile_integration_confirmation_view",
    ),
    re_path(
        r"^api/v1/events/(?P<event_slug>[a-z0-9-]+)/programme/(?P<programme_slug>[a-z0-9-]+)/feedback/?$",
        desuprogramme_feedback_view,
        name="desuprogramme_feedback_view",
    ),
]
