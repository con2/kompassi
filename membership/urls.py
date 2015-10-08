from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from .views import *

urlpatterns = patterns('',
    url(
        r'^organizations/(?P<organization_slug>[a-z0-9-]+)/apply/?$',
        membership_apply_view,
        name='membership_apply_view'
    ),

    url(
        r'^organizations/(?P<organization_slug>[a-z0-9-]+)/admin/members/?$',
        membership_admin_members_view,
        name='membeship_admin_members_view'
    ),

    url(
        r'^organizations/(?P<organization_slug>[a-z0-9-]+)/admin/members/(?P<person_id>[0-9]+)/?$',
        membership_admin_member_view,
        name='membeship_admin_member_view'
    ),
)
