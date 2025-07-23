import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_http_methods

from kompassi.event_log_v2.utils.emit import emit

from ..forms import PasswordForm, PersonForm
from ..helpers import person_required
from ..models import Person
from ..utils import initialize_form

logger = logging.getLogger(__name__)


@person_required
@require_http_methods(["GET", "HEAD", "POST"])
def core_profile_view(request):
    person = request.user.person
    old_email = person.email

    form = initialize_form(PersonForm, request, instance=person, prefix="person")

    if request.method == "POST":
        if form.is_valid():
            person = form.save()

            person.apply_state()

            if form.cleaned_data["email"] != old_email:
                person.setup_email_verification(request)
                messages.info(
                    request,
                    _(
                        "As you changed your e-mail address, you need to verify your e-mail address again. "
                        "Please check your e-mail and proceed with the instructions you will find there. "
                        "Please note that you may experience reduced functionality until you have confirmed "
                        "your e-mail address again. We apologize for the inconvenience."
                    ),
                )

            messages.success(request, _("The changes were saved."))
            return redirect("core_profile_view")
        else:
            messages.error(request, _("Please check the form."))

    vars = dict(form=form)

    return render(request, "core_profile_view.pug", vars)


@sensitive_post_parameters("old_password", "new_password", "new_password_again")
@login_required
@require_http_methods(["GET", "HEAD", "POST"])
def core_password_view(request):
    form = initialize_form(PasswordForm, request, the_request=request)
    user = request.user

    if request.method == "POST":
        if form.is_valid():
            old_password = form.cleaned_data["old_password"]
            new_password = form.cleaned_data["new_password"]

            if not user.check_password(old_password):
                messages.error(request, "Nykyinen salasana ei täsmää.")
                return redirect("core_password_view")

            with transaction.atomic():
                for keypair in user.keypairs.all():
                    keypair.reencrypt_private_key(old_password, new_password)

                user.set_password(new_password)
                user.save(update_fields=["password"])

            messages.success(
                request,
                "Salasanasi on vaihdettu. Voit nyt kirjautua uudestaan sisään uudella salasanallasi.",
            )
            emit("core.password.changed", request=request)
            return redirect("core_frontpage_view")
        else:
            messages.error(request, "Ole hyvä ja korjaa virheelliset kentät.")

    vars = dict(
        form=form,
    )

    return render(request, "core_password_view.pug", vars)


def core_profile_menu_items(request):
    from kompassi.access.views.menu_items import access_profile_menu_items
    from kompassi.labour.views import labour_profile_menu_items
    from kompassi.membership.views import membership_profile_menu_items
    from kompassi.zombies.programme.views.profile_menu_items import programme_profile_menu_items

    items = []

    if not request.user.is_authenticated:
        return items

    profile_url = reverse("core_profile_view")
    profile_active = request.path == profile_url
    profile_text = _("Profile")

    items.append((profile_active, profile_url, profile_text))

    password_url = reverse("core_password_view")
    password_active = request.path == password_url
    password_text = _("Change password")

    items.append((password_active, password_url, password_text))

    try:
        person = request.user.person
    except Person.DoesNotExist:
        pass
    else:
        if not person.is_email_verified:
            email_verification_url = reverse("core_email_verification_request_view")
            email_verification_active = request.path == email_verification_url
            email_verification_text = _("E-mail address verification")
            items.append((email_verification_active, email_verification_url, email_verification_text))

    items.extend(labour_profile_menu_items(request))
    items.extend(programme_profile_menu_items(request))
    items.extend(membership_profile_menu_items(request))
    items.extend(access_profile_menu_items(request))

    tickets_active = False
    tickets_url = f"{settings.KOMPASSI_V2_BASE_URL}/profile/orders"
    tickets_text = _("Ticket orders<sup>v2</sup>…")
    items.append((tickets_active, tickets_url, tickets_text))

    responses_active = False
    responses_url = f"{settings.KOMPASSI_V2_BASE_URL}/profile/responses"
    responses_text = _("Survey responses<sup>v2</sup>…")
    items.append((responses_active, responses_url, responses_text))

    if request.user.is_staff:
        admin_url = "/admin/"
        admin_active = False
        admin_text = _("Site administration")
        items.append((admin_active, admin_url, admin_text))

    return items
