# encoding: utf-8



from django.contrib import messages
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _

from core.models import Person
from core.utils import initialize_form

from ..forms import TeamMemberForm
from ..helpers import intra_admin_required
from ..models import Team, TeamMember


@intra_admin_required
def intra_admin_team_member_view(request, vars, event, team_slug=None, person_id=None):
    meta = event.intra_event_meta
    initial_data = dict()

    if team_slug is not None:
        team = get_object_or_404(Team, event=event, slug=team_slug)
        initial_data.update(team=team)
    else:
        team = None

    if person_id is not None:
        person = get_object_or_404(Person,
            id=int(person_id),
            user__groups=meta.organizer_group,
        )
        initial_data.update(person=person)
    else:
        person = None

    form = None
    if team and person:
        try:
            team_member = TeamMember.objects.get(team=team, person=person)
        except TeamMember.DoesNotExist:
            pass
        else:
            form = initialize_form(TeamMemberForm, request, event=event, instance=team_member)

    if not form:
        form = initialize_form(TeamMemberForm, request, event=event, initial=initial_data)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'save-return':
            if form.is_valid():
                form.save()
                messages.success(request, _('The member was added to the team.'))
                return redirect('intra_organizer_view', event.slug)
            else:
                messages.error(request, _('Please check the form.'))
        elif action == 'delete':
            if not team_member.pk:
                return HttpResponseNotFound()

            team_member.delete()
            messages.success(request, _('The member was removed from the team.'))
            return redirect('intra_organizer_view', event.slug)
        else:
            messages.error(request, _('Invalid action.'))

    vars.update(
        form=form,
    )

    return render(request, 'intra_admin_team_member_view.jade', vars)
