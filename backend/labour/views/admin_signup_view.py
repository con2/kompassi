import json

from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from core.models import Person
from core.tabs import Tab
from core.utils import initialize_form
from event_log_v2.utils.emit import emit

from ..forms import AdminPersonForm
from ..helpers import labour_admin_required
from ..models import (
    JobCategory,
    Signup,
)
from .view_helpers import initialize_signup_forms


@labour_admin_required
@require_http_methods(["GET", "HEAD", "POST"])
def admin_signup_view(request, vars, event, person_id):
    person = get_object_or_404(Person, pk=int(person_id))
    signup = get_object_or_404(Signup, person=person, event=event)
    signup_extra = signup.signup_extra

    old_state_flags = signup._state_flags

    signup_form, signup_extra_form, signup_admin_form, override_working_hours_form = initialize_signup_forms(
        request,
        event,
        signup,
        admin=True,
    )
    person_form = initialize_form(
        AdminPersonForm,
        request,
        instance=signup.person,
        prefix="person",
        readonly=True,
        event=event,
    )

    if request.method == "POST":
        # XXX Need to update state before validation to catch accepting people without accepted job categories
        for state_name in signup.next_states:
            command_name = f"set-state-{state_name}"
            if command_name in request.POST:
                old_state_flags = signup._state_flags
                signup.state = state_name
                break

        old_shirt_size = getattr(signup_extra, "shirt_size", None)

        if (
            signup_form.is_valid()
            and signup_extra_form.is_valid()
            and signup_admin_form.is_valid()
            and override_working_hours_form.is_valid()
        ):
            signup_form.save()
            signup_extra_form.save()
            signup_admin_form.save()
            override_working_hours_form.save()

            new_shirt_size = getattr(signup_extra, "shirt_size", None)

            signup.apply_state()
            messages.success(request, "Tiedot tallennettiin.")

            emit(
                "labour.signup.updated",
                person=signup.person.pk,
                request=request,
                old_shirt_size=old_shirt_size,
                new_shirt_size=new_shirt_size,
            )

            if "save-return" in request.POST:
                return redirect("labour:admin_signups_view", event.slug)
            else:
                return redirect("labour:admin_signup_view", event.slug, person.pk)
        else:
            # XXX Restore state just for shows, suboptimal but
            signup._state_flags = old_state_flags

            messages.error(request, "Ole hyvä ja tarkista lomake.")

    non_qualified_category_names = [
        jc.name for jc in JobCategory.objects.filter(event=event) if not jc.is_person_qualified(signup.person)
    ]

    non_applied_categories = list(JobCategory.objects.filter(event=event))
    for applied_category in signup.job_categories.all():
        non_applied_categories.remove(applied_category)
    non_applied_category_names = [cat.name for cat in non_applied_categories]

    previous_signup, next_signup = signup.get_previous_and_next_signup()

    unarchived_signups = Signup.objects.filter(person=signup.person).exclude(event=event).order_by("-event__start_time")
    archived_signups = person.archived_signups.all()
    if not person.allow_work_history_sharing:
        # The user has elected to not share their full work history between organizations.
        # Only show work history for the current organization.
        unarchived_signups = unarchived_signups.filter(event__organization=event.organization)
        archived_signups = archived_signups.filter(event__organization=event.organization)

    historic_signups = sorted(
        list(archived_signups) + list(unarchived_signups),
        key=lambda signup: signup.event.start_time,
        reverse=True,
    )

    tabs = [
        Tab("labour-admin-signup-state-tab", "Hakemuksen tila", active=True),
        Tab("labour-admin-signup-person-tab", "Hakijan tiedot"),
        Tab("labour-admin-signup-application-tab", "Hakemuksen tiedot"),
        Tab("labour-admin-signup-messages-tab", "Työvoimaviestit", notifications=signup.person_messages.count()),
        Tab("labour-admin-signup-shifts-tab", "Työvuorot"),
        Tab("labour-admin-signup-history-tab", "Työskentelyhistoria", notifications=len(historic_signups)),
    ]

    vars.update(
        historic_signups=historic_signups,
        next_signup=next_signup,
        person_form=person_form,
        previous_signup=previous_signup,
        signup=signup,
        signup_admin_form=signup_admin_form,
        signup_extra_form=signup_extra_form,
        signup_form=signup_form,
        override_working_hours_form=override_working_hours_form,
        tabs=tabs,
        total_hours=signup.shifts.all().aggregate(Sum("hours"))["hours__sum"],
        # XXX hack: widget customization is very difficult, so apply styles via JS
        non_applied_category_names_json=json.dumps(non_applied_category_names),
        non_qualified_category_names_json=json.dumps(non_qualified_category_names),
    )

    person.log_view(request)

    return render(request, "labour_admin_signup_view.pug", vars)
