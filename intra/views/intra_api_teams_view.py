from django.http import JsonResponse

from ..helpers import intra_event_required
from ..models import Team


@intra_event_required
def intra_api_teams_view(request, event):
    meta = event.intra_event_meta
    teams = Team.objects.filter(event=event, is_public=True).prefetch_related("members")

    return JsonResponse(dict(teams=[team.as_dict(include_members=True) for team in teams]))
