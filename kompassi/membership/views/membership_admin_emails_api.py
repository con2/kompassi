from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_safe

from kompassi.api.utils import api_login_required, handle_api_errors
from kompassi.core.models import Organization


@handle_api_errors
@api_login_required
@require_safe
def membership_admin_emails_api(request, organization_slug):
    organization = get_object_or_404(Organization, slug=organization_slug)

    return HttpResponse(
        "\n".join(
            membership.person.email
            for membership in organization.memberships.filter(state="in_effect")
            if membership.person.email
        ),
        content_type="text/plain; charset=UTF-8",
    )
