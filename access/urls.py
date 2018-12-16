from django.conf.urls import url

from .views import (
    access_admin_aliases_api,
    access_admin_aliases_view,
    access_admin_group_emails_api,
    access_admin_smtppasswd_api,
    access_profile_aliases_view,
    access_profile_privilege_view,
    access_profile_privileges_view,
    access_profile_request_privilege_view,
)


urlpatterns = [
    url(
        r'^profile/aliases/?$',
        access_profile_aliases_view,
        name='access_profile_aliases_view',
    ),

    url(
        r'^profile/privileges/?$',
        access_profile_privileges_view,
        name='access_profile_privileges_view',
    ),

    url(
        r'^profile/privileges/(?P<privilege_slug>[a-z0-9-]+)/?$',
        access_profile_privilege_view,
        name='access_profile_privilege_view',
    ),

    url(
        r'^profile/privileges/(?P<privilege_slug>[a-z0-9-]+)/request/?$',
        access_profile_request_privilege_view,
        name='access_profile_request_privilege_view',
    ),

    url(
        r'^api/v1/domains/(?P<domain_name>[a-z0-9-\.]+)/aliases.txt$',
        access_admin_aliases_api,
        name='access_admin_aliases_api',
    ),

    url(
        r'^api/v1/smtpservers/(?P<smtp_server_hostname>[a-z0-9-\.]+)/smtppasswd.txt$',
        access_admin_smtppasswd_api,
        name='access_admin_smtppasswd_api',
    ),

    url(
        r'^api/v1/groups/(?P<group_name>[a-z0-9-]+)/emails.txt$',
        access_admin_group_emails_api,
        name='access_admin_group_emails_api',
    ),

    url(
        r'^organizations/(?P<organization_slug>[a-z0-9-]+)/admin/aliases/?$',
        access_admin_aliases_view,
        name='access_admin_aliases_view',
    ),
]
