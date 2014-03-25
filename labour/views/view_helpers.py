from ..models import JobCategory
from ..forms import SignupForm

from core.utils import initialize_form

def initialize_signup_forms(request, event, signup, **initialize_form_kwargs):
    job_categories = JobCategory.objects.filter(event=event, public=True)
    jcs_qualified = [jc.pk for jc in job_categories if jc.is_person_qualified(signup.person)]
    job_categories = JobCategory.objects.filter(id__in=jcs_qualified).order_by('name') # bc it needs to be a queryset

    signup_extra = signup.signup_extra
    SignupExtraForm = event.labour_event_meta.signup_extra_model.get_form_class()
    signup_form = initialize_form(SignupForm, request,
        job_categories=job_categories,
        instance=signup,
        prefix='signup',
        **initialize_form_kwargs
    )
    signup_extra_form = initialize_form(SignupExtraForm, request,
        instance=signup_extra,
        prefix='extra',
        **initialize_form_kwargs
    )

    return signup_form, signup_extra_form