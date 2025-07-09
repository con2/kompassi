from core.utils import initialize_form


def initialize_signup_forms(request, event, signup, admin=False, SignupFormClass=None, SignupExtraFormClass=None):
    assert (  # noqa: S101
        all([SignupFormClass, SignupExtraFormClass]) or not any([SignupFormClass, SignupExtraFormClass])
    )

    signup_extra = signup.signup_extra

    if SignupFormClass is None:  # and SignupExtraFormClass is None
        from ..forms import SignupForm

        SignupFormClass = SignupForm
        SignupExtraFormClass = event.labour_event_meta.signup_extra_model.get_form_class()

    if signup is not None and signup.alternative_signup_form_used is not None:
        # SignupFormClass = signup.alternative_signup_form_used.signup_form_class
        SignupExtraFormClass = signup.alternative_signup_form_used.signup_extra_form_class

    # Signup form and signup extra form not editable in admin mode
    signup_form = initialize_form(
        SignupFormClass,
        request,
        event=event,
        admin=admin,
        instance=signup,
        prefix="signup",
    )
    signup_extra_form = initialize_form(
        SignupExtraFormClass,
        request,
        instance=signup_extra,
        prefix="extra",
    )

    if admin:
        from ..forms import OverrideWorkingHoursForm, SignupAdminForm

        signup_admin_form = initialize_form(
            SignupAdminForm,
            request,
            event=event,
            instance=signup,
            prefix="admin",
        )

        override_working_hours_form = initialize_form(
            OverrideWorkingHoursForm,
            request,
            instance=signup,
            prefix="hours",
        )

        return signup_form, signup_extra_form, signup_admin_form, override_working_hours_form
    else:
        return signup_form, signup_extra_form
