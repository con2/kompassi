from django.conf.urls import patterns, include, url

from .views import schedule_view

urlpatterns = patterns('',
    url(r'^$', schedule_view, name='schedule_view')
)
