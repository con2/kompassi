from .public_views import (
    labour_confirm_view,
    labour_event_box_context,
    labour_person_disqualify_view,
    labour_person_qualification_view,
    labour_person_qualify_view,
    labour_profile_menu_items,
    labour_profile_signups_view,
    labour_qualifications_view,
    labour_signup_view,
)

from .admin_views import (
    labour_admin_dashboard_view,
    labour_admin_mail_view,
    labour_admin_roster_view,
)

from .labour_admin_jobcategories_view import labour_admin_jobcategories_view
from .labour_admin_jobcategory_view import labour_admin_jobcategory_view
from .labour_admin_menu_items import labour_admin_menu_items
from .labour_admin_shifts_view import labour_admin_shifts_view
from .labour_admin_shirts_view import labour_admin_shirts_view
from .labour_admin_signup_view import labour_admin_signup_view
from .labour_admin_signups_view import labour_admin_signups_view
from .labour_admin_special_diets_view import labour_admin_special_diets_view
from .labour_admin_startstop_view import labour_admin_startstop_view
from .labour_survey_view import labour_survey_view
from .labour_mail_editor_view import labour_admin_mail_editor_view

from .api_views import (
    labour_api_job_categories_view,
    labour_api_job_category_view,
    labour_api_job_view,
    labour_api_set_job_requirements_view,
    labour_api_shift_view,
)
