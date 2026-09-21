from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_safe


@require_safe
def core_stats_view(request):
    return HttpResponseRedirect(f"{settings.KOMPASSI_V2_BASE_URL}/stats")
