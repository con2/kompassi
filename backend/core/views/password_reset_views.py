from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_http_methods

from event_log_v2.utils.emit import emit

from ..forms import (
    PasswordResetForm,
    PasswordResetRequestForm,
)
from ..models import (
    PasswordResetError,
    PasswordResetToken,
    Person,
)
from ..utils import initialize_form


@sensitive_post_parameters("new_password", "new_password_again")
@require_http_methods(["GET", "HEAD", "POST"])
def core_password_reset_view(request, code):
    if request.user.is_authenticated:
        messages.error(
            request,
            _(
                "You are logged in. In order to use a password reset link, please log out first "
                "or use the Incognito/Private Browsing mode of your browser."
            ),
        )
        return redirect("core_password_view")

    form = initialize_form(PasswordResetForm, request)

    if request.method == "POST":
        if form.is_valid():
            try:
                user = PasswordResetToken.reset_password(code, form.cleaned_data["new_password"])
            except PasswordResetError:
                messages.error(
                    request,
                    "Salasanan nollaus epäonnistui. Ole hyvä ja yritä uudestaan. Tarvittaessa voit "
                    f"ottaa yhteyttä osoitteeseen {settings.DEFAULT_FROM_EMAIL}.",
                )
                return redirect("core_frontpage_view")
            else:
                emit("core.password.changed", request=request, actor=user)

                messages.success(
                    request, "Salasanasi on nyt vaihdettu. Voit nyt kirjautua sisään uudella salasanallasi."
                )
                return redirect("core_login_view")
        else:
            messages.error(request, "Ole hyvä ja korjaa lomakkeen virheet.")

    vars = dict(
        form=form,
        login_page=True,
    )

    return render(request, "core_password_reset_view.pug", vars)


@require_http_methods(["GET", "HEAD", "POST"])
def core_password_reset_request_view(request):
    if request.user.is_authenticated:
        return redirect("core_password_view")

    form = initialize_form(PasswordResetRequestForm, request)

    if request.method == "POST":
        if form.is_valid():
            try:
                person = Person.objects.get(
                    email__iexact=form.cleaned_data["email"].strip(),
                    user__isnull=False,
                )
            except Person.DoesNotExist:
                # Fail silently - do not give information about users

                pass
            else:
                person.setup_password_reset(request)

            messages.success(request, "Ohjeet salasanan vaihtamiseksi on lähetetty antamaasi sähköpostiosoitteeseen.")
        else:
            messages.error(request, "Ole hyvä ja korjaa lomakkeen virheet.")

    vars = dict(
        form=form,
        login_page=True,
    )

    return render(request, "core_password_reset_request_view.pug", vars)
