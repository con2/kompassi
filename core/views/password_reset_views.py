# encoding: utf-8

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_http_methods, require_safe

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
    url,
    change_user_password,
)
from ..helpers import person_required


@sensitive_post_parameters('new_password', 'new_password_again')
@require_http_methods(['GET', 'HEAD', 'POST'])
def core_password_reset_view(request, code):
    if request.user.is_authenticated:
        return redirect('core_password_view')

    form = initialize_form(PasswordResetForm, request)

    if request.method == 'POST':
        if form.is_valid():
            try:
                PasswordResetToken.reset_password(code, form.cleaned_data['new_password'])
            except PasswordResetError as e:
                messages.error(request,
                    'Salasanan nollaus epäonnistui. Ole hyvä ja yritä uudestaan. Tarvittaessa voit '
                    'ottaa yhteyttä osoitteeseen {settings.DEFAULT_FROM_EMAIL}.'
                    .format(settings=settings)
                )
                return redirect('core_frontpage_view')

            messages.success(request,
                'Salasanasi on nyt vaihdettu. Voit nyt kirjautua sisään uudella salasanallasi.'
            )
            return redirect('core_login_view')
        else:
            messages.error(request, 'Ole hyvä ja korjaa lomakkeen virheet.')

    vars = dict(
        form=form,
        login_page=True,
    )

    return render(request, 'core_password_reset_view.pug', vars)


@require_http_methods(['GET', 'HEAD', 'POST'])
def core_password_reset_request_view(request):
    if request.user.is_authenticated:
        return redirect('core_password_view')

    form = initialize_form(PasswordResetRequestForm, request)

    if request.method == 'POST':
        if form.is_valid():
            try:
                person = Person.objects.get(
                    email__iexact=form.cleaned_data['email'].strip(),
                    user__isnull=False,
                )
            except Person.DoesNotExist:
                # Fail silently - do not give information about users

                pass
            else:
                person.setup_password_reset(request)

            messages.success(request,
                'Ohjeet salasanan vaihtamiseksi on lähetetty antamaasi sähköpostiosoitteeseen.'
            )
        else:
            messages.error(request, 'Ole hyvä ja korjaa lomakkeen virheet.')

    vars = dict(
        form=form,
        login_page=True,
    )

    return render(request, 'core_password_reset_request_view.pug', vars)
