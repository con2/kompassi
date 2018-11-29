# encoding: utf-8

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.debug import sensitive_post_parameters

from csp.decorators import csp_exempt

from ..models import Person
from ..forms import LoginForm
from ..utils import get_next, initialize_form
from ..page_wizard import page_wizard_clear, page_wizard_vars
from .email_verification_views import remind_email_verification_if_needed


@sensitive_post_parameters('password')
@require_http_methods(['GET', 'POST'])
@csp_exempt  # FIXME
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
                messages.success(request, 'Olet nyt kirjautunut sisään.')
                return response
            else:
                messages.error(request, 'Sisäänkirjautuminen epäonnistui.')
        else:
            messages.error(request, 'Ole hyvä ja korjaa virheelliset kentät.')

    vars = page_wizard_vars(request)

    vars.update(
        form=form,
        login_page=True
    )

    return render(request, 'core_login_view.pug', vars)


def do_login(request, user, password=None, next='core_frontpage_view'):
    """
    Performs Django login, possible Crowd login and required post-login steps.

    `django.contrib.auth.authenticate` must be called first.
    """

    if 'api' in settings.INSTALLED_APPS:
        if user.groups.filter(name=settings.KOMPASSI_APPLICATION_USER_GROUP).exists():
            messages.error(request,
                'API-käyttäjätunnuksilla sisäänkirjautuminen on estetty.'
            )
            return redirect('core_frontpage_view')

    login(request, user)

    # Most users do not have up to date passwords in Crowd. Fix that.
    # FIXME Commented out to explore possible race condition in Crowd between Kompassi & Atlasso

    # if password and 'crowd_integration' in settings.INSTALLED_APPS:
    #     if 'background_tasks' in settings.INSTALLED_APPS:
    #         from crowd_integration.tasks import change_user_password
    #         change_user_password.delay(user.pk, password)
    #     else:
    #         from crowd_integration.utils import change_user_password
    #         change_user_password(user, password)

    remind_email_verification_if_needed(request, next)

    return redirect(next)


@require_http_methods(['GET', 'HEAD', 'POST'])
@csp_exempt  # FIXME
def core_logout_view(request):
    next = get_next(request)
    logout(request)
    messages.success(request, 'Olet nyt kirjautunut ulos.')
    return redirect(next)
