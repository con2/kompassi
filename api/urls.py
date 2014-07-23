from django.conf.urls import patterns, include, url

from .views import api_person_view


urlpatterns = patterns('',
    url(r'^api/v1/people/(?P<username>[a-zA-Z0-9_]+)/?$', api_person_view, name='api_person_view'),
)
