# encoding: utf-8

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods

from core.models import Event
from core.helpers import initialize_form

from .models import LabourEventMeta, Qualification, PersonQualification
from .forms import SignupForm


@login_required
@require_http_methods(['GET', 'POST'])
def labour_signup_view(request, event):
    event = get_object_or_404(Event, slug=event)

    # TODO should the user be allowed to change their registration after the registration period is over?
    if not event.laboureventmeta.is_registration_open:
        messages.error(request, u'Ilmoittautuminen tähän tapahtumaan ei ole avoinna.')
        return redirect('core_event_view', event.slug)

    signup = event.laboureventmeta.get_signup_for_person(request.user.person)
    signup_extra = signup.signup_extra
    SignupExtraForm = event.laboureventmeta.signup_extra_model.get_form_class()
    signup_form = initialize_form(SignupForm, request, instance=signup, prefix='signup')
    signup_extra_form = initialize_form(SignupExtraForm, request, instance=signup_extra, prefix='extra')

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
            return redirect('core_event_view', event.slug)
        else:
            messages.error(request, u'Ole hyvä ja korjaa virheelliset kentät.')

    vars = dict(
        event=event,
        signup_form=signup_form,
        signup_extra_form=signup_extra_form,
    )

    return render(request, 'labour_signup_view.jade', vars)


def labour_event_box_context(request, event):
    if request.user.is_authenticated():
        current_user_signed_up = event.laboureventmeta.is_person_signed_up(request.user.person)
    else:
        current_user_signed_up = False

    return dict(current_user_signed_up=current_user_signed_up)


@login_required
def labour_qualifications_view(request):
    person_qualifications = request.user.person.personqualification_set.all()
    qualification_pks = [q.qualification.pk for q in person_qualifications]
    available_qualifications = Qualification.objects.exclude(pk__in=qualification_pks)

    vars = dict(
        person_qualifications=person_qualifications,
        available_qualifications=available_qualifications
    )

    return render(request, 'labour_qualifications_view.jade', vars)


@login_required
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

def labour_profile_menu_items(request):
    qualifications_url = reverse('labour_qualifications_view')
    qualifications_active = request.path.startswith(qualifications_url)
    qualifications_text = u"Pätevyydet"

    return [(qualifications_active, qualifications_url, qualifications_text)]