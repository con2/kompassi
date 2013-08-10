from django.conf.urls import patterns, include, url

from .views import programme_view

urlpatterns = patterns('',
    url(r'^$', programme_view, name='programme_view')
)
