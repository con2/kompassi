import logging

from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from kompassi.core.helpers import person_required
from kompassi.core.utils import groupby_strict

from ..helpers import access_admin_required
from ..models import EmailAlias, EmailAliasDomain, SMTPPassword, SMTPServer

logger = logging.getLogger(__name__)


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


@access_admin_required
def access_admin_aliases_view(request, vars, organization):
    aliases = EmailAlias.objects.filter(domain__organization=organization).order_by("person")

    vars.update(
        aliases=aliases,
    )

    return render(request, "access_admin_aliases_view.pug", vars)
