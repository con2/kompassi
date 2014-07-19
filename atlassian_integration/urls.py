from django.conf.urls import patterns, include, url

from .views import crowd_session_view


urlpatterns = patterns('',
    url(r'^crowd$', crowd_session_view, name='crowd_session_view'),
)