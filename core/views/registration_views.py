# encoding: utf-8

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.views.decorators.http import require_http_methods, require_GET

from ..models import (
    EmailVerificationError,
    EmailVerificationToken,
    Event,
    Organization,
    PasswordResetError,
    PasswordResetToken,
    Person,
)
from ..forms import (
    LoginForm,
    PasswordForm,
    PasswordResetForm,
    PasswordResetRequestForm,
    PersonForm,
    RegistrationForm,
)
from ..utils import (
    get_next,
    groups_of_n,
    initialize_form,
    next_redirect,
    page_wizard_clear,
    page_wizard_vars,
    url,
)
from ..helpers import person_required


@require_http_methods(['GET','POST'])
def core_registration_view(request):
    vars = page_wizard_vars(request)
    next = vars['next']

    if request.user.is_authenticated():
        return redirect(next)

    person_form = initialize_form(PersonForm, request, prefix='person')
    person_form.helper.form_tag = False
    registration_form = initialize_form(RegistrationForm, request, prefix='registration')

    if request.method == 'POST':
        if person_form.is_valid() and registration_form.is_valid():
            username = registration_form.cleaned_data['username']
            password = registration_form.cleaned_data['password']

            person = person_form.save(commit=False)
            user = User(
                username=username,
                is_active=True,
                is_staff=False,
                is_superuser=False,
            )

            user.set_password(password)
            user.save()

            person.user = user
            person.save()
            person.setup_email_verification(request)

            if 'external_auth' in settings.INSTALLED_APPS:
                from external_auth.utils import create_user
                create_user(user, password)

            user = authenticate(username=username, password=password)

            response = do_login(request, user=user, password=password, next=next)
            messages.success(request,
                u'Käyttäjätunnuksesi on luotu. Tervetuloa {kompassiin}!'
                .format(kompassiin=settings.KOMPASSI_INSTALLATION_NAME_ILLATIVE)
            )
            return response
        else:
            messages.error(request, u'Ole hyvä ja tarkista lomake.')

    vars.update(
        next=next,
        person_form=person_form,
        registration_form=registration_form,
        login_page=True
    )

    return render(request, 'core_registration_view.jade', vars)


@login_required
@require_http_methods(['GET', 'POST'])
def core_personify_view(request):
    try:
        person = request.user.person
    except Person.DoesNotExist:
        pass
    else:
        return redirect('core_profile_view')

    initial = dict(
        first_name=request.user.first_name,
        surname=request.user.last_name,
        email=request.user.email,
    )

    form = initialize_form(PersonForm, request, initial=initial, prefix='person')
    next = get_next(request)

    if request.method == 'POST':
        if form.is_valid():
            person = form.save(commit=False)
            person.user = request.user
            person.save()
            person.setup_email_verification(request)
            messages.success(request,
                u'Tietosi on tallennettu. Ole hyvä ja vahvista sähköpostiosoitteesi. Tarkista '
                u'postilaatikkosi ja noudata vahvistusviestissä olevia ohjeita.'
            )
            return redirect(next)
        else:
            messages.error(request, u'Ole hyvä ja korjaa virheelliset kentät.')
    else:
        messages.info(request, u'Tämän toiminnon käyttäminen edellyttää, että täytät yhteystietosi.')

    vars = dict(
        person_form=form,
        next=next
    )

    return render(request, 'core_personify_view.jade', vars)
