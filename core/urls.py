from django.conf.urls import patterns, include, url
from django.shortcuts import redirect
from django.contrib.auth.views import login, logout

from .forms import LoginForm
from .views import core_frontpage_view, core_event_view, core_profile_view


urlpatterns = patterns(
    '',

    url(r'^$', core_frontpage_view, name='core_frontpage_view'),
    url(r'^events/(?P<event>[a-z0-9-]+)$', core_event_view, name='core_event_view'),
    url(r'^login$', login,
        dict(
            template_name='core_login_view.jade',
            authentication_form=LoginForm,
            extra_context=dict(login_page=True)
        ),
        name='core_login_view'
    ),
    url(r'^logout$', logout, dict(next_page='/'), name='core_logout_view'),
    url(r'^profile$', core_profile_view, name='core_profile_view'),
)
