import logging
from datetime import timedelta

from csp.decorators import csp_update
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.timezone import now
from django.views.decorators.http import require_http_methods, require_POST, require_safe

from api.utils import api_login_required, cbac_api_view, handle_api_errors
from core.helpers import person_required
from core.models import Person
from core.utils import groupby_strict, pick_attrs, url
from event_log_v2.utils.emit import emit

from .constants import CBAC_SUDO_CLAIMS, CBAC_SUDO_VALID_MINUTES
from .exceptions import CBACPermissionDenied
from .helpers import access_admin_required
from .models import CBACEntry, EmailAlias, EmailAliasDomain, InternalEmailAlias, Privilege, SMTPPassword, SMTPServer

logger = logging.getLogger("kompassi")

SLACK_INVITE_ORIGIN = "https://join.slack.com"


@person_required
@csp_update({"form-action": [SLACK_INVITE_ORIGIN]})  # type: ignore
def access_profile_privileges_view(request):
    person = request.user.person

    vars = dict(
        granted_privileges=person.granted_privileges.all(),
        potential_privileges=Privilege.get_potential_privileges(person),
    )

    return render(request, "access_profile_privileges_view.pug", vars)


@person_required
def access_profile_privilege_view(request, privilege_slug):
    person = request.user.person
    privilege = get_object_or_404(Privilege, slug=privilege_slug)

    granted_privilege = person.granted_privileges.filter(privilege=privilege).first()
    potential_privilege = Privilege.get_potential_privileges(person, id=privilege.id).first()

    if not granted_privilege and not potential_privilege:
        messages.error(
            request,
            (
                "Et voi tällä hetkellä hankkia tätä käyttöoikeutta itsepalveluna. "
                "Mikäli epäilet tässä olevan virheen, ota yhteys käyttöoikeudesta vastaavan tapahtuman järjestäjiin."
            ),
        )
        return redirect("access_profile_privileges_view")

    vars = dict(
        granted_privilege=granted_privilege,
        privilege=potential_privilege,
    )

    return render(request, "access_profile_privilege_view.pug", vars)


@person_required
@require_POST
@csp_update({"form-action": [SLACK_INVITE_ORIGIN]})  # type: ignore
def access_profile_request_privilege_view(request, privilege_slug):
    if not request.user.person.is_email_verified:
        messages.error(request, "Käyttöoikeuden pyytäminen edellyttää vahvistettua sähköpostiosoitetta.")
        return redirect("access_profile_privileges_view")

    # People belonging to both Hitpoint and Tracon concoms were getting MultipleObjectsReturned here.
    # Cannot use get_object_or_404 due to the same object being returned multiple times via multiple groups.
    # get_object_or_404 uses .get which has no way to provide .distinct() from outside.
    privilege = Privilege.objects.filter(
        slug=privilege_slug,
        group_privileges__group__in=request.user.groups.all(),
    ).first()
    if privilege is None:
        raise Http404("Privilege not found")

    privilege.grant(request.user.person)

    if privilege.request_success_message:
        success_message = privilege.request_success_message
    else:
        success_message = "Käyttöoikeuden pyytäminen onnistui."

    messages.success(request, success_message)

    if privilege.slack_access:
        return redirect(privilege.slack_access.invite_link)
    else:
        return redirect("access_profile_privileges_view")


@person_required
@require_http_methods(["GET", "HEAD", "POST"])
def access_profile_aliases_view(request):
    person = request.user.person

    if request.method == "POST":
        domain = get_object_or_404(
            EmailAliasDomain.objects.all().distinct(),
            domain_name=request.POST.get("create_new_password_for_domain"),
            emailaliastype__email_aliases__person=request.user.person,
        )

        newly_created_password, unused = SMTPPassword.create_for_domain_and_person(domain, request.user.person)
    else:
        newly_created_password = None

    aliases_by_domain = [
        (
            domain,
            SMTPServer.objects.filter(domains=domain).exists(),
            SMTPPassword.objects.filter(person=request.user.person, smtp_server__domains=domain),
            aliases,
        )
        for (domain, aliases) in groupby_strict(
            person.email_aliases.all().order_by("domain__domain_name"), lambda alias: alias.domain
        )
    ]

    vars = dict(
        aliases_by_domain=aliases_by_domain,
        newly_created_password=newly_created_password,
        person=person,
    )

    return render(request, "access_profile_aliases_view.pug", vars)


def access_profile_menu_items(request):
    privileges_url = reverse("access_profile_privileges_view")
    privileges_active = request.path.startswith(privileges_url)
    privileges_text = "Käyttöoikeudet"

    items: list[tuple[bool, str, str]] = [
        (privileges_active, privileges_url, privileges_text),
    ]

    try:
        aliases_visible = request.user.person.email_aliases.exists()
    except Person.DoesNotExist:
        aliases_visible = False

    if aliases_visible:
        aliases_url = reverse("access_profile_aliases_view")
        aliases_active = request.path == aliases_url
        aliases_text = "Sähköpostialiakset"

        items.append((aliases_active, aliases_url, aliases_text))

    return items


@handle_api_errors
@api_login_required
def access_admin_aliases_api(request, domain_name):
    domain = get_object_or_404(EmailAliasDomain, domain_name=domain_name)

    lines = []

    # Personal aliases
    for person in Person.objects.filter(email_aliases__domain=domain).distinct():
        lines.append(f"# {person.full_name}")
        lines.extend(f"{alias.account_name}: {person.email}" for alias in person.email_aliases.filter(domain=domain))
        lines.append("")

    # Technical aliases
    for alias in InternalEmailAlias.objects.filter(domain=domain):
        if alias.normalized_target_emails:
            lines.append(f"{alias.account_name}: {alias.normalized_target_emails}")
        else:
            logger.warning("Internal alias %s does not have target emails", alias)

    return HttpResponse("\n".join(lines), content_type="text/plain; charset=UTF-8")


@access_admin_required
def access_admin_aliases_view(request, vars, organization):
    aliases = EmailAlias.objects.filter(domain__organization=organization).order_by("person")

    vars.update(
        aliases=aliases,
    )

    return render(request, "access_admin_aliases_view.pug", vars)


@handle_api_errors
@api_login_required
def access_admin_group_emails_api(request, group_name):
    group = get_object_or_404(Group, name=group_name)

    return HttpResponse(
        "\n".join(user.email for user in group.user_set.all() if user.email),  # type: ignore
        content_type="text/plain; charset=UTF-8",
    )


@require_safe
@cbac_api_view
def access_admin_group_members_api(request, group_name):
    group = get_object_or_404(Group, name=group_name)

    return [
        pick_attrs(user.person, "first_name", "surname", "nick", "email", "phone")
        for user in group.user_set.all()  # type: ignore
    ]


def access_admin_menu_items(request, organization):
    aliases_url = url("access_admin_aliases_view", organization.slug)
    aliases_active = request.path == aliases_url
    aliases_text = "Sähköpostialiakset"

    return [(aliases_active, aliases_url, aliases_text)]


def permission_denied_view(request, exception=None):
    sudo_claims = {}

    if request.user.is_superuser and isinstance(exception, CBACPermissionDenied):
        sudo_claims = {k: v for (k, v) in exception.claims.items() if k in CBAC_SUDO_CLAIMS}

    vars = dict(
        sudo_claims=sudo_claims,
        next=request.path,
    )

    return render(request, "403.pug", vars)


def not_found_view(request, exception=None):
    return render(
        request,
        "404.pug",
        {
            "event": None,
            "login_page": True,
        },
    )


@user_passes_test(lambda u: u.is_superuser)  # type: ignore
def sudo_view(request):
    next = request.GET.get("next") or "/"
    claims = {k: v for (k, v) in request.POST.items() if k in CBAC_SUDO_CLAIMS}

    cbac_entry = CBACEntry(
        user=request.user,
        valid_until=now() + timedelta(minutes=CBAC_SUDO_VALID_MINUTES),
        claims=claims,
        created_by=request.user,
    )
    cbac_entry.save()

    messages.warning(
        request,
        f"Käyttöoikeustarkastus ohitettu pääkäyttäjän oikeuksin. "
        f"Väliaikainen käyttöoikeus on voimassa {CBAC_SUDO_VALID_MINUTES} minuuttia.",
    )

    emit("access.cbac.sudo", request=request, other_fields=cbac_entry.as_dict())
    emit("access.cbacentry.created", request=request, other_fields=cbac_entry.as_dict())

    return redirect(next)
