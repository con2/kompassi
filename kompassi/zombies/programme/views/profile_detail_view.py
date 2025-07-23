import logging

from django.shortcuts import get_object_or_404, render

from kompassi.core.helpers import person_required
from kompassi.core.utils import initialize_form

from ..forms import ProgrammeSelfServiceForm
from ..models import FreeformOrganizer, ProgrammeRole

logger = logging.getLogger(__name__)


@person_required
def profile_detail_view(request, programme_id):
    programme_role_qs = ProgrammeRole.objects.filter(person=request.user.person, programme=int(programme_id))
    try:
        programme_role = get_object_or_404(programme_role_qs)
    except ProgrammeRole.MultipleObjectsReturned as e:
        programme_role = programme_role_qs.first()
        if programme_role is None:
            raise AssertionError("This shouldn't happen (appease typechecker)") from e
        logger.warning("Multiple roles for same programme/person: %s", programme_role.programme)

    programme = programme_role.programme
    event = programme.category.event

    if programme.form_used:
        alternative_programme_form = programme.form_used
        FormClass = alternative_programme_form.programme_form_class
    else:
        # implicit default form
        alternative_programme_form = None
        FormClass = ProgrammeSelfServiceForm

    form = initialize_form(
        FormClass,
        request,
        instance=programme,
        event=event,
        readonly=not programme.host_can_edit,
    )

    forms = [form]

    SignupExtra = event.programme_event_meta.signup_extra_model
    if SignupExtra and SignupExtra.supports_programme:
        SignupExtraForm = SignupExtra.get_programme_form_class()
        signup_extra = SignupExtra.for_event_and_person(event, request.user.person)
        signup_extra_form = initialize_form(
            SignupExtraForm,
            request,
            instance=signup_extra,
            prefix="extra",
        )
        forms.append(signup_extra_form)
    else:
        signup_extra = None
        signup_extra_form = None

    vars = dict(
        alternative_programme_form=alternative_programme_form,
        event=event,
        form=form,
        freeform_organizers=FreeformOrganizer.objects.filter(programme=programme),
        programme_role=programme_role,
        programme_roles=ProgrammeRole.objects.filter(programme=programme),
        programme=programme,
        signup_extra_form=signup_extra_form,
    )

    return render(request, "programme_profile_detail_view.pug", vars)
