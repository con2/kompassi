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
from .email_verification_views import remind_email_verification_if_needed


@require_http_methods(['GET','POST'])
def core_login_view(request):
    next = get_next(request, 'core_frontpage_view')
    form = initialize_form(LoginForm, request, initial=dict(next=next))

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Allow login via email address instead of username
            if username and password and '@' in username:
                try:
                    person = Person.objects.get(email=username, user__isnull=False)
                    username = person.user.username
                except (Person.DoesNotExist, Person.MultipleObjectsReturned) as e:
                    # TODO warn
                    pass

            user = authenticate(username=username, password=password)
            if user:
                response = do_login(request, user=user, password=password, next=next)
                page_wizard_clear(request)
                messages.success(request, u'Olet nyt kirjautunut sisään.')
                return response
            else:
                messages.error(request, u'Sisäänkirjautuminen epäonnistui.')
        else:
            messages.error(request, u'Ole hyvä ja korjaa virheelliset kentät.')

    vars = page_wizard_vars(request)

    vars.update(
        form=form,
        login_page=True
    )

    return render(request, 'core_login_view.jade', vars)


def do_login(request, user, password=None, next='core_frontpage_view'):
    """
    Performs Django login, possible Crowd login and required post-login steps.

    `django.contrib.auth.authenticate` must be called first.
    """

    if 'api' in settings.INSTALLED_APPS:
        if user.groups.filter(name=settings.KOMPASSI_APPLICATION_USER_GROUP).exists():
            messages.error(request,
                u'API-käyttäjätunnuksilla sisäänkirjautuminen on estetty.'
            )
            return redirect('core_frontpage_view')

    if 'external_auth' in settings.INSTALLED_APPS:
        # Also set password locally to facilitate future architecture change
        if not user.password:
            user.set_password(password)
            user.save()

    login(request, user)

    remind_email_verification_if_needed(request, next)

    return redirect(next)


@require_http_methods(['GET', 'POST'])
def core_logout_view(request):
    next = get_next(request)
    logout(request)
    messages.success(request, u'Olet nyt kirjautunut ulos.')
    return redirect(next)
