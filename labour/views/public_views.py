import json

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods, require_POST, require_safe

from core.helpers import person_required
from core.models import Person
from core.utils import (
    initialize_form,
    login_redirect,
    url,
    set_attrs,
)
from core.page_wizard import (
    page_wizard_init,
    page_wizard_vars,
)
from event_log.utils import emit

from ..models import (
    AlternativeSignupForm,
    JobCategory,
    PersonQualification,
    Qualification,
    Signup,
)
from ..helpers import labour_event_required

from .view_helpers import initialize_signup_forms


def login_related():
    related = ['core_registration_view']

    if 'desuprofile_integration' in settings.INSTALLED_APPS:
        related.extend([
            'desuprofile_integration_oauth2_login_view',
            'desuprofile_integration_oauth2_callback_view',
            'desuprofile_integration_confirmation_required_view',
        ])

    return related


# XXX hackish
def qualifications_related():
    result = []

    for qual in Qualification.objects.all():
        # wouldn't need labour_person_(dis)qualify_view if they used POST as they should
        for view_name in ['labour_person_qualification_view', 'labour_person_qualify_view', 'labour_person_disqualify_view']:
            result.append(url(view_name, qual.slug))

    return result


@labour_event_required
@require_http_methods(['GET', 'HEAD', 'POST'])
def labour_signup_view(request, event, alternative_form_slug=None):
    """
    This is the "gate" function. The implementation is in
    `actual_labour_signup_view`.

    The purpose of this function is to redirect new users through the process
    of registering an account, entering qualifications and only then signing up.
    Existing users are welcomed to sign up right away.
    """

    if alternative_form_slug:
        actual_signup_url = url('labour_special_signup_view', event.slug, alternative_form_slug)
    else:
        actual_signup_url = url('labour_signup_view', event.slug)

    if not request.user.is_authenticated():
        pages = [
            ('core_login_view', _('Sign up or sign in...'), login_related()),
            ('labour_qualifications_view', _('Revise qualifications'), qualifications_related()),
            (actual_signup_url, _('Apply for volunteer work')),
        ]

        page_wizard_init(request, pages)
        return login_redirect(request)

    try:
        person = request.user.person
    except Person.DoesNotExist:
        pages = [
            ('core_personify_view', _('Complete contact information')),
            ('labour_qualifications_view', _('Revise qualifications'), qualifications_related()),
            (actual_signup_url, _('Apply for volunteer work')),
        ]

        page_wizard_init(request, pages)
        return redirect('core_personify_view')

    return actual_labour_signup_view(request, event, alternative_form_slug=alternative_form_slug)


def actual_labour_signup_view(request, event, alternative_form_slug):
    vars = page_wizard_vars(request)

    signup = event.labour_event_meta.get_signup_for_person(request.user.person)

    if alternative_form_slug is not None:
        # Alternative signup form specified via URL

        alternative_signup_form = get_object_or_404(AlternativeSignupForm, event=event, slug=alternative_form_slug)

        if (
            signup.alternative_signup_form_used is not None and \
            signup.alternative_signup_form_used.pk != alternative_signup_form.pk
        ):
            messages.error(request, _('Your application has not been submitted using this form.'))
            return redirect('core_event_view', event.slug)
    elif signup.pk is not None and signup.alternative_signup_form_used is not None:
        # Alternative signup form used to sign up
        alternative_signup_form = signup.alternative_signup_form_used
    else:
        # Use default signup form
        alternative_signup_form = None

    if alternative_signup_form is not None:
        # Using an alternative signup form

        if not alternative_signup_form.is_active:
            messages.error(request, _('The signup form you have requested is not currently active.'))
            return redirect('core_event_view', event.slug)

        if alternative_signup_form.signup_message:
            messages.warning(request, alternative_signup_form.signup_message)

        SignupFormClass = alternative_signup_form.signup_form_class
        SignupExtraFormClass = alternative_signup_form.signup_extra_form_class
    else:
        # Using default signup form

        if not event.labour_event_meta.is_registration_open:
            messages.error(request, _('This event is not currently accepting applications.'))
            return redirect('core_event_view', event.slug)

        if event.labour_event_meta.signup_message:
            messages.warning(request, event.labour_event_meta.signup_message)

        SignupFormClass = None
        SignupExtraFormClass = None

    if signup.is_processed:
        messages.error(request, _(
            'Your application has already been processed, so you can no longer edit it. '
            'Please contact the volunteer coordinator for any further changes.'
        ))
        return redirect('core_event_view', event.slug)

    if signup.pk is not None:
        old_state = signup.state
        submit_text = _('Update application')
    else:
        old_state = None
        submit_text = _('Submit application')

    signup_extra = signup.signup_extra
    signup_form, signup_extra_form = initialize_signup_forms(request, event, signup,
        SignupFormClass=SignupFormClass,
        SignupExtraFormClass=SignupExtraFormClass,
    )

    if request.method == 'POST':
        if signup_form.is_valid() and signup_extra_form.is_valid():
            if signup.pk is None:
                message = _('Thank you for your application!')
                event_type = 'labour.signup.created'
            else:
                message = _('Your application has been updated.')
                event_type = 'labour.signup.updated'

            if alternative_signup_form is not None:
                signup.alternative_signup_form_used = alternative_signup_form

                set_attrs(signup, **signup_form.get_excluded_field_defaults())
                set_attrs(signup_extra, **signup_extra_form.get_excluded_field_defaults())

            with transaction.atomic():
                signup = signup_form.save()

                signup_extra.signup = signup
                signup_extra = signup_extra_form.save()

                if alternative_signup_form is not None:
                    # Save m2m field defaults
                    for obj, form in [
                        (signup, signup_form),
                        (signup_extra, signup_extra_form),
                    ]:
                        defaults = form.get_excluded_m2m_field_defaults()
                        if defaults:
                            set_attrs(obj, **defaults)
                            obj.save()

            emit(event_type, request=request, person=request.user.person, event=event)

            signup.apply_state()

            messages.success(request, message)
            return redirect('core_event_view', event.slug)
        else:
            messages.error(request, _('Please check the form.'))

    available_job_categories = signup_form.get_job_categories(event=event)
    all_job_categories = JobCategory.objects.filter(event=event)

    # FIXME use id and data attr instead of category name
    non_qualified_category_names = [
        jc.name for jc in available_job_categories
        if not jc.is_person_qualified(request.user.person)
    ]

    vars.update(
        alternative_signup_form=alternative_signup_form,
        event=event,
        signup_extra_form=signup_extra_form,
        signup_form=signup_form,
        signup=signup,
        submit_text=submit_text,

        # XXX HACK descriptions injected using javascript
        job_descriptions_json=json.dumps(dict((cat.pk, cat.description) for cat in all_job_categories)),
        non_qualified_category_names_json=json.dumps(non_qualified_category_names),
    )

    return render(request, 'labour_signup_view.jade', vars)


@person_required
def labour_profile_signups_view(request):
    person = request.user.person

    t = now()

    signups_past_events = person.signups.filter(event__end_time__lte=t).order_by('-event__start_time')
    signups_current_events = person.signups.filter(event__start_time__lte=t, event__end_time__gt=t).order_by('-event__start_time')
    signups_future_events = person.signups.filter(event__start_time__gt=t).order_by('-event__start_time')

    vars = dict(
        person=person,
        signups_past_events=signups_past_events,
        signups_current_events=signups_current_events,
        signups_future_events=signups_future_events,
        no_signups=not any(signups.exists() for signups in [signups_past_events, signups_current_events, signups_future_events]),
        all_signups=person.signups.all(),
    )

    return render(request, 'labour_profile_signups_view.jade', vars)


@person_required
@labour_event_required
@require_POST
def labour_confirm_view(request, event):
    signup = get_object_or_404(Signup, event=event, person=request.user.person)

    if not signup.state == 'confirmation':
        messages.error(request, _('Your application does not currently need to be confirmed.'))
        return redirect('labour_profile_signups_view')

    signup.confirm()
    messages.success(request, _('Your application has been confirmed.'))

    return redirect('labour_profile_signups_view')


@person_required
@require_safe
def labour_qualifications_view(request):
    vars = page_wizard_vars(request)

    person_qualifications = request.user.person.personqualification_set.all()
    qualification_pks = [q.qualification.pk for q in person_qualifications]
    available_qualifications = Qualification.objects.exclude(pk__in=qualification_pks)

    vars.update(
        person_qualifications=person_qualifications,
        available_qualifications=available_qualifications
    )

    if 'page_wizard' in vars:
        template_name = 'labour_new_user_qualifications_view.jade'
    else:
        template_name = 'labour_profile_qualifications_view.jade'

    return render(request, template_name, vars)


@person_required
@require_http_methods(['GET', 'HEAD', 'POST'])
def labour_person_qualification_view(request, qualification):
    vars = page_wizard_vars(request)

    person = request.user.person
    qualification = get_object_or_404(Qualification, slug=qualification)

    try:
        person_qualification = qualification.personqualification_set.get(person=person)
    except PersonQualification.DoesNotExist:
        person_qualification = PersonQualification(
            person=person,
            qualification=qualification
        )

    QualificationExtra = qualification.qualification_extra_model
    if QualificationExtra:
        QualificationExtraForm = QualificationExtra.get_form_class()
        qualification_extra = person_qualification.qualification_extra
        form = initialize_form(QualificationExtraForm, request, instance=qualification_extra)
    else:
        qualification_extra = None
        form = None

    if request.method == 'POST':
        form_valid = not form or (form and form.is_valid())
        if form_valid:
            person_qualification.save()

            if form:
                qualification_extra.personqualification = person_qualification
                form.save()

            messages.success(request, _('The qualification has been updated.'))
            return redirect('labour_qualifications_view')
        else:
            messages.error(request, _('Please check the form.'))

    vars.update(
        person_qualification=person_qualification,
        form=form
    )

    if 'page_wizard' in vars:
        template_name = 'labour_new_user_person_qualification_view.jade'
    else:
        template_name = 'labour_profile_person_qualification_view.jade'

    return render(request, template_name, vars)


@person_required
def labour_person_qualify_view(request, qualification):
    person = request.user.person
    qualification = get_object_or_404(Qualification, slug=qualification)

    if qualification.qualification_extra_model:
        return redirect('labour_person_qualification_view', qualification.slug)

    person_qualification, created = PersonQualification.objects.get_or_create(
        person=person,
        qualification=qualification
    )

    if created:
        messages.success(request, _('The qualification has been added.'))

    return redirect('labour_qualifications_view')


@person_required
def labour_person_disqualify_view(request, qualification):
    person = request.user.person
    qualification = get_object_or_404(Qualification, slug=qualification)

    try:
        person_qualification = get_object_or_404(PersonQualification,
            person=person, qualification=qualification)
        person_qualification.delete()
        messages.success(request, _('The qualification has been removed.'))
    except:
        pass

    return redirect('labour_qualifications_view')


def labour_profile_menu_items(request):
    signups_url = reverse('labour_profile_signups_view')
    signups_active = request.path.startswith(signups_url)
    signups_text = _('Volunteer work applications')

    qualifications_url = reverse('labour_qualifications_view')
    qualifications_active = request.path.startswith(qualifications_url)
    qualifications_text = _('Qualifications')

    return [
        (signups_active, signups_url, signups_text),
        (qualifications_active, qualifications_url, qualifications_text),
    ]


def labour_event_box_context(request, event):
    signup = None
    is_labour_admin = False

    if request.user.is_authenticated():
        is_labour_admin = event.labour_event_meta.is_user_admin(request.user)

        try:
            person = request.user.person
            signup = Signup.objects.get(event=event, person=person)
        except (Person.DoesNotExist, Signup.DoesNotExist):
            pass

    return dict(
        signup=signup,
        is_labour_admin=is_labour_admin,
    )
