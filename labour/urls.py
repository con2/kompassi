from django.conf.urls import include, url
from django.views.generic.base import RedirectView

from .views import (
    labour_admin_dashboard_view,
    labour_admin_jobcategories_view,
    labour_admin_jobcategory_view,
    labour_admin_mail_editor_view,
    labour_admin_mail_view,
    labour_admin_roster_view,
    labour_admin_shifts_view,
    labour_admin_shirts_view,
    labour_admin_signup_view,
    labour_admin_signups_view,
    labour_admin_special_diets_view,
    labour_admin_startstop_view,
    labour_api_job_categories_view,
    labour_api_job_category_view,
    labour_api_job_view,
    labour_api_shift_view,
    labour_api_set_job_requirements_view,
    labour_confirm_view,
    labour_person_disqualify_view,
    labour_person_qualification_view,
    labour_person_qualify_view,
    labour_profile_signups_view,
    labour_qualifications_view,
    labour_signup_view,
    labour_survey_view,
)


urlpatterns = [
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
        r'^events/(?P<event_slug>[a-z0-9-]+)/confirm/?$',
        labour_confirm_view,
        name='labour_confirm_view',
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/labour/surveys/(?P<survey_slug>[a-z0-9-]+)/?$',
        labour_survey_view,
        name='labour_survey_view',
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/admin(?P<suffix>.*)',
        RedirectView.as_view(url='/events/%(event_slug)s/labour/admin%(suffix)s', permanent=False),
        name='labour_admin_old_urls_redirect'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/labour/admin$',
        labour_admin_dashboard_view,
        name='labour_admin_dashboard_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/signups$',
        labour_admin_signups_view,
        name='labour_admin_signups_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/signups\.(?P<format>xlsx|csv|tsv|html)$',
        labour_admin_signups_view,
        name='labour_admin_export_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/signups/(?P<person_id>\d+)$',
        labour_admin_signup_view,
        name='labour_admin_signup_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/jobcategories/?$',
        labour_admin_jobcategories_view,
        name='labour_admin_jobcategories_view',
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/jobcategories/new/?$',
        labour_admin_jobcategory_view,
        dict(job_category_slug=None),
        name='labour_admin_create_jobcategory_view',
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/jobcategories/(?P<job_category_slug>[a-z0-9-]+)/?$',
        labour_admin_jobcategory_view,
        name='labour_admin_jobcategory_view',
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/roster/?$',
        labour_admin_roster_view,
        name='labour_admin_roster_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/roster/(?P<job_category_slug>[a-z0-9-]+)/?$',
        labour_admin_roster_view,
        name='labour_admin_roster_job_category_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/start/?$',
        labour_admin_startstop_view,
        name='labour_admin_startstop_view'
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
        r'^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/shirts/?$',
        labour_admin_shirts_view,
        name='labour_admin_shirts_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/shifts/?$',
        labour_admin_shifts_view,
        name='labour_admin_shifts_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/shifts\.(?P<format>\w+)?$',
        labour_admin_shifts_view,
        name='labour_admin_export_shifts_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/specialdiets/?$',
        labour_admin_special_diets_view,
        name='labour_admin_special_diets_view'
    ),

    url(
        r'^api/v1/events/(?P<event_slug>[a-z0-9-]+)/jobcategories/?$',
        labour_api_job_categories_view,
        name='labour_api_job_categories_view'
    ),
    url(
        r'^api/v1/events/(?P<event_slug>[a-z0-9-]+)/jobcategories/(?P<job_category_slug>[a-z0-9-]+)/?$',
        labour_api_job_category_view,
        name='labour_api_job_category_view'
    ),
    url(
        r'^api/v1/events/(?P<event_slug>[a-z0-9-]+)/jobcategories/(?P<job_category_slug>[a-z0-9-]+)/jobs/?$',
        labour_api_job_view,
        name='labour_api_create_job_view'
    ),
    url(
        r'^api/v1/events/(?P<event_slug>[a-z0-9-]+)/jobcategories/(?P<job_category_slug>[a-z0-9-]+)/jobs/(?P<job_slug>[a-z0-9-]+)/?$',
        labour_api_job_view,
        name='labour_api_edit_job_view'
    ),
    url(
        r'^api/v1/events/(?P<event_slug>[a-z0-9-]+)/jobcategories/(?P<job_category_slug>[a-z0-9-]+)/jobs/(?P<job_slug>[a-z0-9-]+)/requirements/?$',
        labour_api_set_job_requirements_view,
        name='labour_api_set_job_requirements_view'
    ),
    url(
        r'^api/v1/events/(?P<event_slug>[a-z0-9-]+)/jobcategories/(?P<job_category_slug>[a-z0-9-]+)/shifts/?$',
        labour_api_shift_view,
        name='labour_api_create_shift_view'
    ),
    url(
        r'^api/v1/events/(?P<event_slug>[a-z0-9-]+)/jobcategories/(?P<job_category_slug>[a-z0-9-]+)/shifts/(?P<shift_id>\d+)/?$',
        labour_api_shift_view,
        name='labour_api_edit_shift_view'
    ),
]
