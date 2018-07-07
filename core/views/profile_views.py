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
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods, require_safe
from django.views.decorators.debug import sensitive_post_parameters

from event_log.utils import emit

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
from ..page_wizard import (
    page_wizard_clear,
    page_wizard_vars,
)
from ..helpers import person_required


@person_required
@require_http_methods(['GET', 'HEAD', 'POST'])
def core_profile_view(request):
    person = request.user.person
    old_email = person.email

    form = initialize_form(PersonForm, request, instance=person, prefix='person')

    if request.method == 'POST':
        if form.is_valid():
            person = form.save()

            person.apply_state()

            if form.cleaned_data['email'] != old_email:
                person.setup_email_verification(request)
                messages.info(request, _(
                    "As you changed your e-mail address, you need to verify your e-mail address again. "
                    "Please check your e-mail and proceed with the instructions you will find there. "
                    "Please note that you may experience reduced functionality until you have confirmed "
                    "your e-mail address again. We apologize for the inconvenience."
                ))

            messages.success(request, _("The changes were saved."))
            return redirect('core_profile_view')
        else:
            messages.error(request, _("Please check the form."))

    vars = dict(
        form=form
    )

    return render(request, 'core_profile_view.jade', vars)


@sensitive_post_parameters('old_password', 'new_password', 'new_password_again')
@login_required
@require_http_methods(['GET', 'HEAD', 'POST'])
def core_password_view(request):
    form = initialize_form(PasswordForm, request, the_request=request)

    if request.method == 'POST':
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']

            try:
                change_user_password(request.user, old_password=old_password, new_password=new_password)
            except RuntimeError:
                logger.exception('Failed to change password')
                messages.error(request, 'Salasanan vaihto epäonnistui. Ole hyvä ja yritä myöhemmin uudelleen.')
                return redirect('core_password_view')
            else:
                messages.success(request, 'Salasanasi on vaihdettu. Voit nyt kirjautua uudestaan sisään uudella salasanallasi.')
                emit('core.password.changed', request=request)
                return redirect('core_frontpage_view')
        else:
            messages.error(request, 'Ole hyvä ja korjaa virheelliset kentät.')

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
    profile_text = _('Profile')

    items.append((profile_active, profile_url, profile_text))

    password_url = reverse('core_password_view')
    password_active = request.path == password_url
    password_text = _('Change password')

    items.append((password_active, password_url, password_text))

    try:
        person = request.user.person
    except Person.DoesNotExist:
        pass
    else:
        if not person.is_email_verified:
            email_verification_url = reverse('core_email_verification_request_view')
            email_verification_active = request.path == email_verification_url
            email_verification_text = _('E-mail address verification')
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
        admin_text = _('Site administration')
        items.append((admin_active, admin_url, admin_text))

    return items
