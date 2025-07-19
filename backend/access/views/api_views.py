import logging

from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_safe

from api.utils import api_login_required, cbac_api_view, handle_api_errors
from core.models import Person
from core.utils import pick_attrs
from involvement.models import Involvement
from labour.helpers import labour_event_required

from ..models import EmailAliasDomain, InternalEmailAlias

logger = logging.getLogger("kompassi")


@require_safe
@cbac_api_view
@labour_event_required
def api_discord_view(request, event):
    """
    Supplies discord handles for role bot integration.
    https://outline.con2.fi/doc/discord-role-bot-3IYyCqALLI
    """
    roles_by_handle: dict[str, set[str]] = {}

    # Labour V1
    if meta := event.labour_event_meta:
        SignupExtra = meta.signup_extra_model
        for extra in SignupExtra.objects.filter(is_active=True).select_related("person"):
            if discord_handle := extra.person.discord_handle:
                roles_by_handle.setdefault(discord_handle.removeprefix("@"), set()).update(extra.discord_roles)

    # Program V2
    for discord_handle in Involvement.objects.filter(
        universe=event.involvement_universe,
        is_active=True,
        person__discord_handle__isnull=False,
        program__isnull=False,
    ).values_list("person__discord_handle", flat=True):
        roles_by_handle.setdefault(discord_handle.removeprefix("@"), set()).add("Ohjelma")

    return [dict(handle=handle, roles=list(roles)) for handle, roles in roles_by_handle.items()]


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
