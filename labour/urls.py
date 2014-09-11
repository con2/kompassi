from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from .views import *

urlpatterns = patterns('',
    url(r'^events/(?P<event_slug>[a-z0-9-]+)/signup/?$', labour_signup_view, name='labour_signup_view'),
    url(r'^events/(?P<event_slug>[a-z0-9-]+)/signup/(?P<alternative_form_slug>[a-z0-9-]+)/?$', labour_signup_view, name='labour_special_signup_view'),

    url(r'^profile/qualifications$', labour_qualifications_view, name='labour_qualifications_view'),
    url(r'^profile/qualifications/(?P<qualification>[a-z0-9-]+)$', labour_person_qualification_view, name='labour_person_qualification_view'),

    # XXX make these DELETE and POST of labour_person_qualification_view
    url(r'^profile/qualifications/(?P<qualification>[a-z0-9-]+)/delete$', labour_person_disqualify_view, name='labour_person_disqualify_view'),
    url(r'^profile/qualifications/(?P<qualification>[a-z0-9-]+)/add$', labour_person_qualify_view, name='labour_person_qualify_view'),

    url(
        r'^profile/signups$',
        labour_profile_signups_view,
        name='labour_profile_signups_view',
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/admin(?P<suffix>.*)',
        RedirectView.as_view(url='/events/%(event_slug)s/labour/admin%(suffix)s'),
        name='labour_admin_old_urls_redirect'
    ),

    url(r'^events/(?P<event_slug>[a-z0-9-]+)/labour/admin$', labour_admin_dashboard_view, name='labour_admin_dashboard_view'),
    url(r'^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/signups$', labour_admin_signups_view, name='labour_admin_signups_view'),
    url(r'^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/signups/(?P<person_id>\d+)$', labour_admin_signup_view, name='labour_admin_signup_view'),
    url(r'^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/signups\.xlsx$', labour_admin_export_view, name='labour_admin_export_view'),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/roster$',
        labour_admin_roster_view,
        name='labour_admin_roster_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/roster/jobcategories/(?P<job_category>\d+).json$',
        labour_admin_roster_job_category_fragment,
        name='labour_admin_roster_job_category_fragment'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/mail$',
        labour_admin_mail_view,
        name='labour_admin_mail_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/mail/new$',
        labour_admin_mail_editor_view,
        name='labour_admin_mail_new_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/mail/(?P<message_id>\d+)$',
        labour_admin_mail_editor_view,
        name='labour_admin_mail_editor_view'
    ),
    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/query$',
        query_index,
        name='labour_admin_query'
    ),
    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/query/data$',
        query_exec,
        name='labour_admin_query_exec'
    ),
)
