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
    url,
)
from ..page_wizard import (
    page_wizard_clear,
    page_wizard_vars,
)
from ..helpers import person_required


@person_required
@require_http_methods(['GET', 'POST'])
def core_profile_view(request):
    person = request.user.person
    old_email = person.email

    form = initialize_form(PersonForm, request, instance=person, prefix='person')

    if request.method == 'POST':
        if form.is_valid():
            person = form.save()

            if form.cleaned_data['email'] != old_email:
                person.setup_email_verification(request)
                messages.info(request,
                    u'Tietosi on tallennettu. Koska muutit sähköpostiosoitettasi, sinun täytyy '
                    u'vahvistaa sähköpostiosoitteesi uudelleen. Tarkista postilaatikkosi ja '
                    u'noudata vahvistusviestissä olevia ohjeita.'
                )
            else:
                messages.success(request, u'Tietosi on tallennettu.')
        else:
            messages.error(request, u'Ole hyvä ja korjaa virheelliset kentät.')

    vars = dict(
        form=form
    )

    return render(request, 'core_profile_view.jade', vars)


@login_required
@require_http_methods(['GET', 'POST'])
def core_password_view(request):
    form = initialize_form(PasswordForm, request, the_request=request)

    if request.method == 'POST':
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']

            ldap_user = getattr(request.user, 'ldap_user', None)
            if ldap_user:
                from external_auth.utils import change_current_user_password
                from external_auth.ipa import IPAError

                try:
                    change_current_user_password(request,
                        old_password=old_password,
                        new_password=new_password,
                    )
                except IPAError, e:
                    # TODO need to tell the user if this is due to too simple pw
                    messages.error(request, u'Salasanan vaihto epäonnistui.')
                else:
                    messages.success(request, u'Salasanasi on vaihdettu.')

            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, u'Salasanasi on vaihdettu.')
        else:
            messages.error(request, u'Ole hyvä ja korjaa virheelliset kentät.')

    vars = dict(
        form=form,
    )

    return render(request, 'core_password_view.jade', vars)


def core_profile_menu_items(request):
    items = []

    if not request.user.is_authenticated():
        return items

    profile_url = reverse('core_profile_view')
    profile_active = request.path == profile_url
    profile_text = u'Omat tiedot'

    items.append((profile_active, profile_url, profile_text))

    password_url = reverse('core_password_view')
    password_active = request.path == password_url
    password_text = u'Salasanan vaihto'

    items.append((password_active, password_url, password_text))

    try:
        person = request.user.person
    except Person.DoesNotExist:
        pass
    else:
        if not person.is_email_verified:
            email_verification_url = reverse('core_email_verification_request_view')
            email_verification_active = request.path == email_verification_url
            email_verification_text = u'Sähköpostiosoitteen vahvistaminen'
            items.append((email_verification_active, email_verification_url, email_verification_text))

    if 'labour' in settings.INSTALLED_APPS:
        from labour.views import labour_profile_menu_items
        items.extend(labour_profile_menu_items(request))

    if 'programme' in settings.INSTALLED_APPS:
        from programme.views import programme_profile_menu_items
        items.extend(programme_profile_menu_items(request))

    if 'membership' in settings.INSTALLED_APPS:
        from membership.views import membership_profile_menu_items
        items.extend(membership_profile_menu_items(request))

    if 'access' in settings.INSTALLED_APPS:
        from access.views import access_profile_menu_items
        items.extend(access_profile_menu_items(request))

    if 'django.contrib.admin' in settings.INSTALLED_APPS and request.user.is_staff:
        admin_url = '/admin/' # XXX hardcoded
        admin_active = False
        admin_text = 'Sivuston ylläpito'
        items.append((admin_active, admin_url, admin_text))

    return items
