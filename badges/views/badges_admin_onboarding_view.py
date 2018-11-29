from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from csp.decorators import csp_update

from labour.proxies.signup.onboarding import SignupOnboardingProxy

from ..helpers import badges_admin_required
from ..models import Badge


@badges_admin_required
@require_http_methods(['GET', 'HEAD', 'POST'])
@csp_update(SCRIPT_SRC=['cdn.jsdelivr.net'])
def badges_admin_onboarding_view(request, vars, event):
    if request.method in ('GET', 'HEAD'):
        badges = Badge.objects.filter(
            personnel_class__event=event,
            revoked_at__isnull=True,
        ).select_related('personnel_class').order_by('surname', 'first_name')

        shirt_type_field = None
        shirt_size_field = None


        lem = event.labour_event_meta
        if lem:
            SignupExtra = event.labour_event_meta.signup_extra_model

            shirt_type_field = SignupExtra.get_shirt_type_field()
            shirt_size_field = SignupExtra.get_shirt_size_field()

            # Accessing badge.signup_extra for each badge causes one extra query per badge
            # So cache them.
            if SignupExtra.schema_version >= 2:
                people = [badge.person_id for badge in badges if badge.person]
                signup_extras = SignupExtra.objects.filter(event=event, person_id__in=people)
                signup_extras_by_person_id = dict((sx.person_id, sx) for sx in signup_extras)

                badges = list(badges)
                for badge in badges:
                    badge._signup_extra = signup_extras_by_person_id.get(badge.person_id)

        vars.update(
            badges=badges,
            shirt_type_field=shirt_type_field,
            shirt_size_field=shirt_size_field,
        )

        return render(request, 'badges_admin_onboarding_view.pug', vars)
    elif request.method == 'POST':
        badge_id = request.POST['id']
        is_arrived = request.POST['arrived'] == 'true'

        badge = get_object_or_404(Badge, id=int(badge_id))
        badge.is_arrived = is_arrived
        badge.save()

        if badge.person:
            sop = SignupOnboardingProxy.objects.filter(event=event, person=badge.person, is_active=True).first()
            if sop:
                sop.mark_arrived(is_arrived)

        return HttpResponse()
    else:
        raise NotImplementedError(request.method)
