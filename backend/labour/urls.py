from django.urls import re_path
from django.views.generic.base import RedirectView

from .views import (
    admin_dashboard_view,
    admin_jobcategories_view,
    admin_jobcategory_view,
    admin_mail_editor_view,
    admin_mail_view,
    admin_roster_view,
    admin_shifts_view,
    admin_shirts_view,
    admin_signup_view,
    admin_signups_view,
    admin_special_diets_view,
    admin_startstop_view,
    api_job_categories_view,
    api_job_category_view,
    api_job_view,
    api_set_job_requirements_view,
    api_shift_view,
    confirm_view,
    person_disqualify_view,
    person_qualification_view,
    person_qualify_view,
    profile_signups_view,
    profile_work_reference,
    qualifications_view,
    signup_view,
    survey_view,
)

app_name = "labour"
urlpatterns = [
    re_path(r"^events/(?P<event_slug>[a-z0-9-]+)/signup/?$", signup_view, name="signup_view"),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/signup/(?P<alternative_form_slug>[a-z0-9-]+)/?$",
        signup_view,
        name="special_signup_view",
    ),
    re_path(r"^profile/qualifications/?$", qualifications_view, name="qualifications_view"),
    re_path(
        r"^profile/qualifications/(?P<qualification>[a-z0-9-]+)/?$",
        person_qualification_view,
        name="person_qualification_view",
    ),
    # XXX make these DELETE and POST of person_qualification_view
    re_path(
        r"^profile/qualifications/(?P<qualification>[a-z0-9-]+)/delete/?$",
        person_disqualify_view,
        name="person_disqualify_view",
    ),
    re_path(
        r"^profile/qualifications/(?P<qualification>[a-z0-9-]+)/add/?$", person_qualify_view, name="person_qualify_view"
    ),
    re_path(
        r"^profile/signups/?$",
        profile_signups_view,
        name="profile_signups_view",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/reference/?$",
        profile_work_reference,
        name="profile_work_reference",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/confirm/?$",
        confirm_view,
        name="confirm_view",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/labour/surveys/(?P<survey_slug>[a-z0-9-]+)/?$",
        survey_view,
        name="survey_view",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/admin(?P<suffix>.*)",
        RedirectView.as_view(url="/events/%(event_slug)s/labour/admin%(suffix)s", permanent=False),
        name="labour_admin_old_urls_redirect",
    ),
    re_path(r"^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/?$", admin_dashboard_view, name="admin_dashboard_view"),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/signups/?$", admin_signups_view, name="admin_signups_view"
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/signups\.(?P<format>xlsx|csv|tsv|html)/?$",
        admin_signups_view,
        name="admin_export_view",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/signups/(?P<person_id>\d+)/?$",
        admin_signup_view,
        name="admin_signup_view",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/jobcategories/?$",
        admin_jobcategories_view,
        name="admin_jobcategories_view",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/jobcategories/new/?$",
        admin_jobcategory_view,
        dict(job_category_slug=None),
        name="admin_create_jobcategory_view",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/jobcategories/(?P<job_category_slug>[a-z0-9-]+)/?$",
        admin_jobcategory_view,
        name="admin_jobcategory_view",
    ),
    re_path(r"^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/roster/?$", admin_roster_view, name="admin_roster_view"),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/roster/(?P<job_category_slug>[a-z0-9-]+)/?$",
        admin_roster_view,
        name="admin_roster_job_category_view",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/start/?$", admin_startstop_view, name="admin_startstop_view"
    ),
    re_path(r"^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/mail/?$", admin_mail_view, name="admin_mail_view"),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/mail/new/?$",
        admin_mail_editor_view,
        name="admin_mail_new_view",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/mail/(?P<message_id>\d+)/?$",
        admin_mail_editor_view,
        name="admin_mail_editor_view",
    ),
    re_path(r"^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/shirts/?$", admin_shirts_view, name="admin_shirts_view"),
    re_path(r"^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/shifts/?$", admin_shifts_view, name="admin_shifts_view"),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/shifts\.(?P<format>\w+)?$",
        admin_shifts_view,
        name="admin_export_shifts_view",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/labour/admin/specialdiets/?$",
        admin_special_diets_view,
        name="admin_special_diets_view",
    ),
    re_path(
        r"^api/v1/events/(?P<event_slug>[a-z0-9-]+)/jobcategories/?$",
        api_job_categories_view,
        name="api_job_categories_view",
    ),
    re_path(
        r"^api/v1/events/(?P<event_slug>[a-z0-9-]+)/jobcategories/(?P<job_category_slug>[a-z0-9-]+)/?$",
        api_job_category_view,
        name="api_job_category_view",
    ),
    re_path(
        r"^api/v1/events/(?P<event_slug>[a-z0-9-]+)/jobcategories/(?P<job_category_slug>[a-z0-9-]+)/jobs/?$",
        api_job_view,
        name="api_create_job_view",
    ),
    re_path(
        r"^api/v1/events/(?P<event_slug>[a-z0-9-]+)/jobcategories/(?P<job_category_slug>[a-z0-9-]+)/jobs/(?P<job_slug>[a-z0-9-]+)/?$",
        api_job_view,
        name="api_edit_job_view",
    ),
    re_path(
        r"^api/v1/events/(?P<event_slug>[a-z0-9-]+)/jobcategories/(?P<job_category_slug>[a-z0-9-]+)/jobs/(?P<job_slug>[a-z0-9-]+)/requirements/?$",
        api_set_job_requirements_view,
        name="api_set_job_requirements_view",
    ),
    re_path(
        r"^api/v1/events/(?P<event_slug>[a-z0-9-]+)/jobcategories/(?P<job_category_slug>[a-z0-9-]+)/shifts/?$",
        api_shift_view,
        name="api_create_shift_view",
    ),
    re_path(
        r"^api/v1/events/(?P<event_slug>[a-z0-9-]+)/jobcategories/(?P<job_category_slug>[a-z0-9-]+)/shifts/(?P<shift_id>\d+)/?$",
        api_shift_view,
        name="api_edit_shift_view",
    ),
]
