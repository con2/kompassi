from django.conf import settings
from django.conf.urls import include, url
from django.views.generic import RedirectView

from .views import (
    programme_accept_invitation_view,
    programme_admin_change_host_role_view,
    programme_admin_change_invitation_role_view,
    programme_admin_create_view,
    programme_admin_detail_view,
    programme_admin_email_list_view,
    programme_admin_invitations_view,
    programme_admin_publish_view,
    programme_admin_special_view,
    programme_admin_timetable_view,
    programme_admin_view,
    programme_feedback_view,
    programme_internal_adobe_taggedtext_view,
    programme_internal_timetable_view,
    programme_json_view,
    programme_mobile_timetable_view,
    programme_profile_detail_view,
    programme_profile_view,
    programme_special_view,
    programme_timetable_view,
)

urlpatterns = [
    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/timetable(?P<suffix>.*)',
        RedirectView.as_view(url='/events/%(event_slug)s/programme%(suffix)s', permanent=False),
        name='programme_old_urls_redirect'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/programme/?$',
        programme_timetable_view,
        dict(show_programme_actions=True),
        name='programme_timetable_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/programme/special/?$',
        programme_special_view,
        dict(show_programme_actions=True),
        name='programme_special_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/programme/publish/?$',
        RedirectView.as_view(url='/events/%(event_slug)s/programme/admin/publish/', permanent=False),
        name='programme_admin_old_publish_view_redirect'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/programme/special/fragment/?$',
        programme_special_view,
        dict(template='programme_list.jade'),
        name='programme_special_fragment_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/programme/fragment?$',
        programme_timetable_view,
        dict(template='programme_timetable_fragment.jade'),
        name='programme_timetable_fragment'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/programme/mobile/?$',
        programme_mobile_timetable_view,
        name='programme_mobile_timetable_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/programme/full/?$',
        programme_internal_timetable_view,
        name='programme_internal_timetable_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/programme/(?P<programme_id>\d+)/feedback/?$',
        programme_feedback_view,
        name='programme_feedback_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/programme\.taggedtext$',
        programme_internal_adobe_taggedtext_view,
        name='programme_internal_adobe_taggedtext_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/programme\.json$',
        programme_json_view,
        name='programme_json_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/programme/desucon\.json$',
        programme_json_view,
        dict(format='desucon'),
        name='programme_moe_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/programme/invitation/(?P<code>[a-f0-9]+)/?$',
        programme_accept_invitation_view,
        name='programme_accept_invitation_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/programme/admin/?$',
        programme_admin_view,
        name='programme_admin_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/programme/admin/new/?$',
        programme_admin_create_view,
        name='programme_admin_create_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/programme/admin/(?P<programme_id>\d+)/?$',
        programme_admin_detail_view,
        name='programme_admin_detail_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/programme/admin/(?P<programme_id>\d+)/invitations/(?P<invitation_id>\d+)/?$',
        programme_admin_change_invitation_role_view,
        name='programme_admin_change_invitation_role_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/programme/admin/(?P<programme_id>\d+)/hosts/(?P<programme_role_id>\d+)/?$',
        programme_admin_change_host_role_view,
        name='programme_admin_change_host_role_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/programme/admin/invitations/?$',
        programme_admin_invitations_view,
        name='programme_admin_invitations_view',
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/programme/admin/timetable/?$',
        programme_admin_timetable_view,
        name='programme_admin_timetable_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/programme/admin/special/?$',
        programme_admin_special_view,
        name='programme_admin_special_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/programme/admin/publish/?$',
        programme_admin_publish_view,
        name='programme_admin_publish_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/programme/admin/programme\.(?P<format>xlsx|csv|tsv|html)$',
        programme_admin_view,
        name='programme_admin_export_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/programme/admin/emails\.txt$',
        programme_admin_email_list_view,
        name='programme_admin_email_list_view'
    ),

    url(
        r'^profile/programmes/?$',
        programme_profile_view,
        name='programme_profile_view',
    ),

    url(
        r'^profile/programmes/(?P<programme_id>\d+)/?$',
        programme_profile_detail_view,
        name='programme_profile_detail_view',
    ),
]
