from collections import namedtuple

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from kompassi.core.helpers import person_required
from kompassi.core.utils import initialize_form

from ..helpers import labour_event_required
from ..models import Signup, Survey, SurveyRecord

FakeSignup = namedtuple("FakeSignup", "event")


@labour_event_required
@person_required
@require_http_methods(["GET", "HEAD", "POST"])
def survey_view(request, event, survey_slug):
    survey = get_object_or_404(Survey, slug=survey_slug, event=event)
    person = request.user.person

    Form = survey.form_class

    try:
        signup = Signup.objects.get(event=event, person=person)
    except Signup.DoesNotExist:
        signup = FakeSignup(event)

    try:
        instance = Form.get_instance_for_event_and_person(event, person)
    except ObjectDoesNotExist:
        instance = None

    if instance is None:
        messages.error(request, survey.does_not_apply_message)
        return redirect("core_event_view", event.slug)

    if not survey.is_active:
        if SurveyRecord.objects.filter(survey=survey, person=person).exists():
            messages.warning(
                request,
                _(
                    "You have previously answered this survey that is no longer active. You may view "
                    "your answers below, but you cannot alter them any more."
                ),
            )
        else:
            messages.error(request, _("This survey is not currently active."))
            return redirect("core_event_view", event.slug)

    form = initialize_form(
        Form,
        request,
        instance=instance,
        event=event,
        readonly=not survey.is_active,
    )

    if request.method == "POST":
        if form.is_valid() and survey.is_active:
            SurveyRecord.objects.get_or_create(survey=survey, person=person)
            form.save()
            messages.success(request, _("Thank you for your answers."))
            return redirect("core_event_view", event.slug)
        else:
            messages.error(request, _("Please check the form."))

    vars = dict(
        event=event,
        signup=signup,
        instance=instance,
        survey=survey,
        form=form,
    )

    return render(request, "labour_survey_view.pug", vars)
