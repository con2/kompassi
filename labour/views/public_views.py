# encoding: utf-8

import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
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
)

from ..forms import SignupForm
from ..models import LabourEventMeta, Qualification, PersonQualification, Signup, JobCategory
from ..helpers import labour_event_required


@labour_event_required
@require_http_methods(['GET', 'POST'])
def labour_signup_view(request, event):
    if not request.user.is_authenticated():
        pages = [
            ('core_login_view', u'Sisäänkirjautuminen'),
            ('core_registration_view', u'Rekisteröityminen'),
            ('labour_qualifications_view', u'Pätevyydet'),
            (url('labour_signup_view', event.slug), u'Ilmoittautuminen'),
        ]

        page_wizard_init(request, pages)
        return login_redirect(request)

    try:
        person = request.user.person
    except Person.DoesNotExist:
        pages = [
            ('core_personify_view', u'Perustiedot'),
            ('labour_qualifications_view', u'Pätevyydet'),
            (url('labour_signup_view', event.slug), u'Ilmoittautuminen'),
        ]

        page_wizard_init(request, pages)
        return redirect('core_personify_view')
    else:
        return actual_labour_signup_view(request, event)


def actual_labour_signup_view(request, event):
    # TODO should the user be allowed to change their registration after the registration period is over?
    if not event.labour_event_meta.is_registration_open:
        messages.error(request, u'Ilmoittautuminen tähän tapahtumaan ei ole avoinna.')
        return redirect('core_event_view', event.slug)

    signup = event.labour_event_meta.get_signup_for_person(request.user.person)
    signup_extra = signup.signup_extra
    SignupExtraForm = event.labour_event_meta.signup_extra_model.get_form_class()
    signup_form = initialize_form(SignupForm, request, instance=signup, prefix='signup')
    signup_extra_form = initialize_form(SignupExtraForm, request, instance=signup_extra, prefix='extra')

    if signup.pk is not None:
        submit_text = 'Tallenna muutokset'
    else:
        submit_text = 'Lähetä ilmoittautuminen'

    if request.method == 'POST':
        if signup_form.is_valid() and signup_extra_form.is_valid():
            if signup.pk is None:
                message = u'Kiitos ilmoittautumisestasi!'
            else:
                message = u'Ilmoittautumisesi on päivitetty.'

            signup = signup_form.save()
            signup_extra.signup = signup
            signup_extra_form.save()

            messages.success(request, message)
            page_wizard_clear(request)
            return redirect('core_event_view', event.slug)
        else:
            messages.error(request, u'Ole hyvä ja korjaa virheelliset kentät.')

    job_cats = JobCategory.objects.filter(event=event, public=True)

    vars = dict(
        event=event,
        signup_form=signup_form,
        signup_extra_form=signup_extra_form,
        submit_text=submit_text,

        # XXX HACK descriptions injected using javascript
        job_descriptions_json=json.dumps(dict((cat.pk, cat.description) for cat in job_cats)),
    )

    return render(request, 'labour_signup_view.jade', vars)


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

    vars = dict(
        person_qualification=person_qualification,
        form=form
    )

    return render(request, 'labour_person_qualification_view.jade', vars)

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
    qualifications_url = reverse('labour_qualifications_view')
    qualifications_active = request.path.startswith(qualifications_url)
    qualifications_text = u"Pätevyydet"

    return [(qualifications_active, qualifications_url, qualifications_text)]


def labour_event_box_context(request, event):
    is_signed_up = False
    is_labour_admin = False

    if request.user.is_authenticated():
        try:
            person = request.user.person
        except Person.DoesNotExist:
            pass
        else:
            is_signed_up = event.labour_event_meta.is_person_signed_up(person)
            is_labour_admin = event.labour_event_meta.is_user_admin(request.user)

    return dict(
        is_signed_up=is_signed_up,
        is_labour_admin=is_labour_admin,
    )
