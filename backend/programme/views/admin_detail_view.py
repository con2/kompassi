from collections import namedtuple

from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from core.tabs import Tab
from core.utils import initialize_form

from ..forms import (
    FreeformOrganizerForm,
    IsUsingPaikkalaForm,
    PaikkalaProgramForm,
    ProgrammeInternalForm,
    ProgrammeSelfServiceForm,
    ScheduleForm,
)
from ..helpers import programme_admin_required
from ..models import (
    FreeformOrganizer,
    ProgrammeRole,
)
from ..proxies.programme.management import ProgrammeManagementProxy

PerHostForms = namedtuple("PerHostForms", "change_host_role_form signup_extra_form")


# TODO Split this into multiple views or at refactor it into a CBV
@programme_admin_required
@require_http_methods(["GET", "HEAD", "POST"])
def admin_detail_view(request, vars, event, programme_id):
    programme = get_object_or_404(ProgrammeManagementProxy, category__event=event, pk=int(programme_id))

    if programme.form_used:
        FormClass = programme.form_used.programme_form_class
    else:
        FormClass = ProgrammeSelfServiceForm

    programme_form = initialize_form(
        FormClass, request, instance=programme, event=event, prefix="programme", admin=True
    )
    internal_form = initialize_form(ProgrammeInternalForm, request, instance=programme, event=event, prefix="internal")
    schedule_form = initialize_form(ScheduleForm, request, instance=programme, event=event, prefix="schedule")
    is_using_paikkala_form = initialize_form(
        IsUsingPaikkalaForm,
        request,
        instance=programme,
        prefix="usepaikkala",
        disabled=not programme.can_paikkalize,
    )
    forms = [programme_form, schedule_form, internal_form, is_using_paikkala_form]

    if programme.is_using_paikkala and programme.paikkala_program:
        paikkala_program_form = initialize_form(
            PaikkalaProgramForm, request, instance=programme.paikkala_program, prefix="paikkala"
        )
        forms.append(paikkala_program_form)
    else:
        paikkala_program_form = None

    freeform_organizer_form = initialize_form(FreeformOrganizerForm, request, prefix="freeform")

    SignupExtra = event.programme_event_meta.signup_extra_model
    if SignupExtra and SignupExtra.supports_programme:
        SignupExtraForm = SignupExtra.get_programme_form_class()
    else:
        SignupExtraForm = None

    programme_roles = ProgrammeRole.objects.filter(programme=programme)
    forms_per_host = []
    for role in programme_roles:
        if SignupExtraForm is not None:
            signup_extra_form = initialize_form(
                SignupExtraForm,
                request,
                prefix="sex",
                instance=SignupExtra.for_event_and_person(event, role.person),
            )
        else:
            signup_extra_form = None

        forms_per_host.append(
            PerHostForms(
                change_host_role_form=None,
                signup_extra_form=signup_extra_form,
            )
        )

    feedback = programme.visible_feedback

    tabs = [
        Tab("programme-admin-programme-tab", _("Programme form"), active=True),
        Tab("programme-admin-programme-schedule-tab", _("Schedule information")),
        Tab("programme-admin-programme-internal-tab", _("Internal information")),
        Tab("programme-admin-programme-reservations-tab", _("Seat reservations")),
        Tab("programme-admin-programme-hosts-tab", _("Programme hosts")),
        Tab("programme-admin-programme-feedback-tab", _("Feedback"), notifications=feedback.count()),
    ]

    previous_programme, next_programme = programme.get_previous_and_next_programme()

    vars.update(
        feedback=feedback,
        forms_per_host=forms_per_host,
        freeform_organizer_form=freeform_organizer_form,
        freeform_organizers=FreeformOrganizer.objects.filter(programme=programme),
        internal_form=internal_form,
        is_using_paikkala_form=is_using_paikkala_form,
        next_programme=next_programme,
        overlapping_programmes=programme.get_overlapping_programmes(),
        paikkala_program_form=paikkala_program_form,
        previous_programme=previous_programme,
        programme_form=programme_form,
        programme_roles=programme_roles,
        programme=programme,
        schedule_form=schedule_form,
        tabs=tabs,
    )

    return render(request, "programme_admin_detail_view.pug", vars)
