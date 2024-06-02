from django.http import JsonResponse

from ..helpers import intra_event_required
from ..models import Team


@intra_event_required
def intra_api_teams_view(request, event):
    if not event.intra_event_meta.is_organizer_list_public and not event.intra_event_meta.is_user_allowed_to_access(
        request.user
    ):
        return JsonResponse({"error": "Unauthorized"}, status=403)

    teams = Team.objects.filter(event=event, is_public=True).prefetch_related("members")

    return JsonResponse(dict(teams=[team.as_dict(include_members=True) for team in teams]))
