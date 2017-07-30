from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods

from membership.models import Membership

from ..helpers import directory_access_required


@directory_access_required
@require_http_methods(['GET', 'HEAD', 'POST'])
def directory_person_view(request, vars, organization, person_id):
    person = get_object_or_404(organization.people, id=int(person_id))
    membership = Membership.objects.filter(organization=organization, person=person).first()

    vars.update(
        person=person,
        membership=membership,
    )

    return render(request, 'directory_person_view.jade', vars)
