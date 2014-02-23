from django.conf.urls import patterns, include, url
from django.shortcuts import redirect
from django.contrib.auth.views import logout

from .forms import LoginForm
from .views import (
    core_event_view,
    core_frontpage_view,
    core_login_view,
    core_password_view,
    core_personify_view,
    core_profile_view,
    core_registration_view,
)


urlpatterns = patterns(
    '',

    url(r'^$', core_frontpage_view, name='core_frontpage_view'),
    url(r'^events/(?P<event_id>[a-z0-9-]+)$', core_event_view, name='core_event_view'),
    url(r'^login$', core_login_view, name='core_login_view'),
    url(r'^register$', core_registration_view, name='core_registration_view'),
    url(r'^logout$', logout, dict(next_page='/'), name='core_logout_view'),
    url(r'^profile$', core_profile_view, name='core_profile_view'),
    url(r'^profile/new$', core_personify_view, name='core_personify_view'),
    url(r'^profile/password$', core_password_view, name='core_password_view'),
)
