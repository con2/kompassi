from ..models import JobCategory
from ..forms import SignupForm, SignupAdminForm

from core.utils import initialize_form

def initialize_signup_forms(request, event, signup, admin=False):
    job_categories = JobCategory.objects.filter(event=event, public=True)

    signup_extra = signup.signup_extra
    SignupExtraForm = event.labour_event_meta.signup_extra_model.get_form_class()

    # Signup form and signup extra form not editable in admin mode
    signup_form = initialize_form(SignupForm, request,
        job_categories=job_categories,
        instance=signup,
        prefix='signup',
        readonly=admin
    )
    signup_extra_form = initialize_form(SignupExtraForm, request,
        instance=signup_extra,
        prefix='extra',
        readonly=admin
    )

    if admin:
        signup_admin_form = initialize_form(SignupAdminForm, request,
            job_categories=job_categories,
            instance=signup,
            prefix='admin',
        )

        return signup_form, signup_extra_form, signup_admin_form
    else:
        return signup_form, signup_extra_form
