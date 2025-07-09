from csp.decorators import csp_update
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_http_methods

from ..forms import LoginForm
from ..models import Person
from ..utils import get_next, initialize_form
from .email_verification_views import remind_email_verification_if_needed


@sensitive_post_parameters("password")
@require_http_methods(["GET", "POST"])
@csp_update({"form-action": settings.KOMPASSI_CSP_ALLOWED_LOGIN_REDIRECTS})
def core_login_view(request):
    next = get_next(request, "core_frontpage_view")
    form = initialize_form(LoginForm, request, initial=dict(next=next))

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            # Allow login via email address instead of username
            if username and password and "@" in username:
                try:
                    person = Person.objects.get(email=username, user__isnull=False)
                except (Person.DoesNotExist, Person.MultipleObjectsReturned):
                    # TODO warn
                    pass
                else:
                    if person.user:
                        username = person.user.username

            user = authenticate(username=username, password=password)
            if user:
                response = do_login(request, user=user, next=next)
                messages.success(request, "Olet nyt kirjautunut sisään.")
                return response
            else:
                messages.error(request, "Sisäänkirjautuminen epäonnistui.")
        else:
            messages.error(request, "Ole hyvä ja korjaa virheelliset kentät.")

    vars = dict(form=form, login_page=True)

    return render(request, "core_login_view.pug", vars)


def do_login(request, user, next="core_frontpage_view", backend=None):
    """
    Performs Django login and required post-login steps.
    `django.contrib.auth.authenticate` must be called first or `backend` provided.
    """

    if user.groups.filter(name=settings.KOMPASSI_APPLICATION_USER_GROUP).exists():
        messages.error(request, "API-käyttäjätunnuksilla sisäänkirjautuminen on estetty.")
        return redirect("core_frontpage_view")

    login(request, user, backend=backend)
    remind_email_verification_if_needed(request, next)

    return redirect(next)


@require_http_methods(["GET", "HEAD", "POST"])
@csp_update({"form-action": settings.KOMPASSI_CSP_ALLOWED_LOGIN_REDIRECTS})
def core_logout_view(request):
    next = get_next(request)
    logout(request)
    messages.success(request, "Olet nyt kirjautunut ulos.")
    return redirect(next)
