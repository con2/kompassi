from csp.decorators import csp_update
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import redirect, render
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_http_methods

from ..forms import RegistrationForm, RegistrationPersonForm, TermsAndConditionsForm
from ..models import Person
from ..utils import get_next, initialize_form
from .login_views import do_login


@sensitive_post_parameters("registration-password", "registration-password_again")
@require_http_methods(["GET", "HEAD", "POST"])
@csp_update({"form-action": settings.KOMPASSI_CSP_ALLOWED_LOGIN_REDIRECTS})
def core_registration_view(request):
    next = get_next(request)

    if request.user.is_authenticated:
        return redirect(next)

    person_form = initialize_form(RegistrationPersonForm, request, prefix="person")
    registration_form = initialize_form(RegistrationForm, request, prefix="registration")
    terms_and_conditions_form = initialize_form(TermsAndConditionsForm, request, prefix="terms")

    if request.method == "POST":
        if person_form.is_valid() and registration_form.is_valid() and terms_and_conditions_form.is_valid():
            username = registration_form.cleaned_data["username"]
            password = registration_form.cleaned_data["password"]

            with transaction.atomic():
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

            person.apply_state_new_user(request, password)

            user = authenticate(username=username, password=password)
            response = do_login(request, user=user, next=next)
            messages.success(
                request,
                f"Käyttäjätunnuksesi on luotu. Tervetuloa {settings.KOMPASSI_INSTALLATION_NAME_ILLATIVE}!",
            )
            return response
        else:
            messages.error(request, "Ole hyvä ja tarkista lomake.")

    vars = dict(
        next=next,
        person_form=person_form,
        registration_form=registration_form,
        terms_and_conditions_form=terms_and_conditions_form,
        login_page=True,
    )

    return render(request, "core_registration_view.pug", vars)


@login_required
@require_http_methods(["GET", "HEAD", "POST"])
def core_personify_view(request):
    try:
        person = request.user.person
    except Person.DoesNotExist:
        pass
    else:
        return redirect("core_profile_view")

    initial = dict(
        first_name=request.user.first_name,
        surname=request.user.last_name,
        email=request.user.email,
    )

    form = initialize_form(RegistrationPersonForm, request, initial=initial, prefix="person")
    next = get_next(request)

    if request.method == "POST":
        if form.is_valid():
            person = form.save(commit=False)
            person.user = request.user
            person.save()
            person.setup_email_verification(request)
            messages.success(
                request,
                "Tietosi on tallennettu. Ole hyvä ja vahvista sähköpostiosoitteesi. Tarkista "
                "postilaatikkosi ja noudata vahvistusviestissä olevia ohjeita.",
            )
            return redirect(next)
        else:
            messages.error(request, "Ole hyvä ja korjaa virheelliset kentät.")
    else:
        messages.info(request, "Tämän toiminnon käyttäminen edellyttää, että täytät yhteystietosi.")

    vars = dict(person_form=form, next=next)

    return render(request, "core_personify_view.pug", vars)
