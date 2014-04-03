from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

from .views import (
    programme_admin_detail_view,
    programme_admin_view,
    programme_internal_adobe_taggedtext_view,
    programme_internal_timetable_view,
    programme_mobile_detail_view,
    programme_mobile_timetable_view,
    programme_self_service_view,
    programme_timetable_view,
)

urlpatterns = patterns('',
    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/timetable(?P<suffix>.*)',
        RedirectView.as_view(url='/events/%(event_slug)s/programme%(suffix)s'),
        name='programme_old_urls_redirect'
    ),

    url(r'^events/(?P<event_slug>[a-z0-9-]+)/programme/?$', programme_timetable_view, name='programme_timetable_view'),
    url(r'^events/(?P<event_slug>[a-z0-9-]+)/programme/fragment?$', programme_timetable_view, dict(template='programme_timetable_fragment.jade'), name='programme_timetable_fragment'),
    url(r'^events/(?P<event_slug>[a-z0-9-]+)/programme/mobile/?$', programme_mobile_timetable_view, name='programme_mobile_timetable_view'),
    url(r'^events/(?P<event_slug>[a-z0-9-]+)/programme/mobile/(\d{1,4})', programme_mobile_detail_view, name='programme_mobile_detail_view'),
    url(r'^events/(?P<event_slug>[a-z0-9-]+)/programme/full$', programme_internal_timetable_view, name='programme_internal_timetable_view'),
    url(r'^events/(?P<event_slug>[a-z0-9-]+)/programme.taggedtext$', programme_internal_adobe_taggedtext_view, name='programme_internal_adobe_taggedtext_view'),

    url(r'^events/(?P<event_slug>[a-z0-9-]+)/programme/admin$', programme_admin_view, name='programme_admin_view'),
    url(r'^events/(?P<event_slug>[a-z0-9-]+)/programme/admin/new$', programme_admin_detail_view, name='programme_admin_new_view'),
    url(r'^events/(?P<event_slug>[a-z0-9-]+)/programme/admin/(?P<programme_id>\d{1,4})$', programme_admin_detail_view, name='programme_admin_detail_view'),
    url(r'^events/(?P<event_slug>[a-z0-9-]+)/programme/token/(?P<programme_edit_code>[0-9a-f]+)$', programme_self_service_view, name='programme_self_service_view'),
)
