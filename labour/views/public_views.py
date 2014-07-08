# encoding: utf-8

import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.timezone import now
from django.views.decorators.http import require_http_methods

from core.helpers import person_required
from core.models import Event, Person
from core.utils import (
    initialize_form,
    login_redirect,
    page_wizard_clear,
    page_wizard_init,
    page_wizard_vars,
    url,
    set_attrs,
)

from ..forms import SignupForm
from ..models import (
    AlternativeSignupForm,
    JobCategory,
    LabourEventMeta,
    PersonQualification,
    PROCESSED_STATES,
    Qualification,
    Signup,
)
from ..helpers import labour_event_required

from .view_helpers import initialize_signup_forms

# XXX hackish
def qualifications_related():
    result = []

    for qual in Qualification.objects.all():
        # wouldn't need labour_person_(dis)qualify_view if they used POST as they should
        for view_name in ['labour_person_qualification_view', 'labour_person_qualify_view', 'labour_person_disqualify_view']:
            result.append(url(view_name, qual.slug))

    return result


@labour_event_required
@require_http_methods(['GET', 'POST'])
def labour_signup_view(request, event, alternative_form_slug=None):
    """
    This is the "gate" function. The implementation is in
    `actual_labour_signup_view`.

    The purpose of this function is to redirect new users through the process
    of registering an account, entering qualifications and only then signing up.
    Existing users are welcomed to sign up right away.
    """
    if not request.user.is_authenticated():
        pages = [
            ('core_login_view', u'Sisäänkirjautuminen'),
            ('core_registration_view', u'Rekisteröityminen'),
            ('labour_qualifications_view', u'Pätevyydet', qualifications_related()),
            (url('labour_signup_view', event.slug), u'Ilmoittautuminen'),
        ]

        page_wizard_init(request, pages)
        return login_redirect(request)

    try:
        person = request.user.person
    except Person.DoesNotExist:
        pages = [
            ('core_personify_view', u'Perustiedot'),
            ('labour_qualifications_view', u'Pätevyydet', qualifications_related()),
            (url('labour_signup_view', event.slug), u'Ilmoittautuminen'),
        ]

        page_wizard_init(request, pages)
        return redirect('core_personify_view')
    else:
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
            messages.error(request, u'Hakemusta ei ole tehty käyttäen tätä lomaketta.')
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
            messages.error(request, u'Pyytämäsi ilmoittautumislomake ei ole käytössä.')
            return redirect('core_event_view', event.slug)

        SignupFormClass = alternative_signup_form.signup_form_class
        SignupExtraFormClass = alternative_signup_form.signup_extra_form_class
    else:
        # Using default signup form

        if not event.labour_event_meta.is_registration_open:
            messages.error(request, u'Ilmoittautuminen tähän tapahtumaan ei ole avoinna.')
            return redirect('core_event_view', event.slug)

        SignupFormClass = None
        SignupExtraFormClass = None

    if signup.state in PROCESSED_STATES:
        messages.error(request,
            u'Hakemuksesi on jo käsitelty, joten et voi enää muokata sitä. '
            u'Tarvittaessa ota yhteyttä työvoimatiimiin.'
        )
        return redirect('core_event_view', event.slug)

    if signup.pk is not None:
        old_state = signup.state
        submit_text = 'Tallenna muutokset'
    else:
        old_state = None
        submit_text = 'Lähetä ilmoittautuminen'

    signup_extra = signup.signup_extra
    signup_form, signup_extra_form = initialize_signup_forms(request, event, signup,
        SignupFormClass=SignupFormClass,
        SignupExtraFormClass=SignupExtraFormClass,
    )

    if request.method == 'POST':
        if signup_form.is_valid() and signup_extra_form.is_valid():
            if signup.pk is None:
                message = u'Kiitos ilmoittautumisestasi!'
            else:
                message = u'Ilmoittautumisesi on päivitetty.'

            if alternative_signup_form is not None:
                signup.alternative_signup_form_used = alternative_signup_form

                set_attrs(signup, **signup_form.get_excluded_field_defaults())
                set_attrs(signup_extra, **signup_form.get_excluded_field_defaults())

            signup = signup_form.save()

            signup_extra.signup = signup
            signup_extra_form.save()

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

            signup.state_change_from(old_state)

            messages.success(request, message)
            return redirect('core_event_view', event.slug)
        else:
            messages.error(request, u'Ole hyvä ja korjaa virheelliset kentät.')

    all_job_cats = JobCategory.objects.filter(event=event)
    job_cats = JobCategory.objects.filter(event=event, public=True)

    # FIXME use id and data attr instead of category name
    non_qualified_category_names = [
        jc.name for jc in job_cats
        if not jc.is_person_qualified(request.user.person)
    ]

    vars.update(
        event=event,
        signup_form=signup_form,
        signup_extra_form=signup_extra_form,
        submit_text=submit_text,
        alternative_signup_form=alternative_signup_form,

        # XXX HACK descriptions injected using javascript
        job_descriptions_json=json.dumps(dict((cat.pk, cat.description) for cat in all_job_cats)),
        non_qualified_category_names_json=json.dumps(non_qualified_category_names),
    )

    return render(request, 'labour_signup_view.jade', vars)


@person_required
def labour_profile_signups_view(request):
    person = request.user.person

    t = now()

    signups_past_events = person.signup_set.filter(event__end_time__lte=t).order_by('-event__start_time')
    signups_current_events = person.signup_set.filter(event__start_time__lte=t, event__end_time__gt=t).order_by('-event__start_time')
    signups_future_events = person.signup_set.filter(event__start_time__gt=t).order_by('-event__start_time')

    vars = dict(
        signups_past_events=signups_past_events,
        signups_current_events=signups_current_events,
        signups_future_events=signups_future_events,
        no_signups=not any(signups.exists() for signups in [signups_past_events, signups_current_events, signups_future_events]),
        all_signups=person.signup_set.all(),
    )

    return render(request, 'labour_profile_signups_view.jade', vars)

@person_required
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
@require_http_methods(['GET', 'POST'])
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

            messages.success(request, u'Pätevyys tallennettiin.')
            return redirect('labour_qualifications_view')
        else:
            messages.error(request, u'Ole hyvä ja korjaa lomakkeen virheet.')

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
        messages.success(request, u"Pätevyys lisättiin.")

    return redirect('labour_qualifications_view')


@person_required
def labour_person_disqualify_view(request, qualification):
    person = request.user.person
    qualification = get_object_or_404(Qualification, slug=qualification)

    try:
        person_qualification = get_object_or_404(PersonQualification,
            person=person, qualification=qualification)
        person_qualification.delete()
        messages.success(request, u"Pätevyys poistettiin.")
    except:
        pass

    return redirect('labour_qualifications_view')


def labour_profile_menu_items(request):
    signups_url = reverse('labour_profile_signups_view')
    signups_active = request.path.startswith(signups_url)
    signups_text = u"Työvoimahakemukset"

    qualifications_url = reverse('labour_qualifications_view')
    qualifications_active = request.path.startswith(qualifications_url)
    qualifications_text = u"Pätevyydet"

    return [
        (signups_active, signups_url, signups_text),
        (qualifications_active, qualifications_url, qualifications_text),
    ]


def labour_event_box_context(request, event):
    signup = None
    is_labour_admin = False

    if request.user.is_authenticated():
        try:
            person = request.user.person
        except Person.DoesNotExist:
            pass
        else:
            is_labour_admin = event.labour_event_meta.is_user_admin(request.user)

            try:
                signup = Signup.objects.get(event=event, person=person)
            except Signup.DoesNotExist:
                pass

    return dict(
        signup=signup,
        is_labour_admin=is_labour_admin,
    )
