from csp.decorators import csp_update
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from kompassi.core.utils.view_utils import login_redirect
from kompassi.labour.models.personnel_class import PersonnelClass
from kompassi.labour.proxies.signup.onboarding import SignupOnboardingProxy

from ..helpers import badges_event_required
from ..models import Badge


@require_http_methods(["GET", "HEAD", "POST"])
@csp_update({"script-src": ["cdn.jsdelivr.net"]})  # type: ignore
@badges_event_required
def badges_admin_onboarding_view(request, event):
    meta = event.badges_event_meta

    if not meta.is_user_allowed_onboarding_access(request.user):
        return login_redirect(request)

    if request.method in ("GET", "HEAD"):
        personnel_classes = PersonnelClass.objects.filter(event=event)
        badges = (
            Badge.objects.filter(
                personnel_class__in=personnel_classes,
                revoked_at__isnull=True,
            )
            .select_related("personnel_class")
            .order_by("surname", "first_name")
        )

        shirt_type_field = None
        shirt_size_field = None

        lem = event.labour_event_meta
        emp = event.involvement_event_meta.emperkelator_class if event.involvement_event_meta else None
        if lem and not emp:
            SignupExtra = event.labour_event_meta.signup_extra_model

            if SignupExtra:
                shirt_type_field = SignupExtra.get_shirt_type_field()
                shirt_size_field = SignupExtra.get_shirt_size_field()
            else:
                shirt_type_field = None
                shirt_size_field = None

            # Accessing badge.signup_extra for each badge causes one extra query per badge
            # So cache them.
            if SignupExtra and SignupExtra.schema_version >= 2:
                people = [badge.person_id for badge in badges if badge.person]
                signup_extras = SignupExtra.objects.filter(event=event, person_id__in=people)
                signup_extras_by_person_id = {sx.person_id: sx for sx in signup_extras}

                badges = list(badges)
                for badge in badges:
                    badge._signup_extra = signup_extras_by_person_id.get(badge.person_id)

        is_perks_column_shown = True

        vars = dict(
            event=event,
            badges=badges,
            shirt_type_field=shirt_type_field,
            shirt_size_field=shirt_size_field,
            is_perks_column_shown=is_perks_column_shown,
            personnel_classes=personnel_classes,
        )

        return render(request, "badges_admin_onboarding_view.pug", vars)
    elif request.method == "POST":
        badge_id = request.POST["id"]
        is_arrived = request.POST["arrived"] == "true"

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
