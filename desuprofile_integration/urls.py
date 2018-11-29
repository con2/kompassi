from django.conf.urls import include, url
from django.views.generic.base import TemplateView

from .views import (
    CallbackView,
    LoginView,
    ConfirmationView,
    desuprogramme_import_view,
)


urlpatterns = [
    url(
        r'^desuprofile/oauth2/login/?$',
        LoginView.as_view(),
        name='desuprofile_integration_oauth2_login_view',
    ),

    url(
        r'^desuprofile/oauth2/callback/?$',
        CallbackView.as_view(),
        name='desuprofile_integration_oauth2_callback_view',
    ),


    url(
        r'^desuprofile/confirm/?$',
        TemplateView.as_view(template_name='desuprofile_integration_confirmation_required_view.pug'),
        name='desuprofile_integration_confirmation_required_view',
    ),

    url(
        r'^desuprofile/confirm/(?P<code>[a-f0-9]+)/?$',
        ConfirmationView.as_view(),
        name='desuprofile_integration_confirmation_view',
    ),

    url(
        r'^api/v1/events/(?P<event_slug>[a-z0-9-]+)/programme/(?:desu)+/?',
        desuprogramme_import_view,
        name='desuprogramme_import_view',
    )
]
