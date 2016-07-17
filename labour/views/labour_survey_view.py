# encoding: utf-8

from __future__ import unicode_literals

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods

from core.helpers import person_required
from core.utils import initialize_form

from ..models import Signup, Survey
from ..helpers import labour_event_required


@labour_event_required
@person_required
@require_http_methods(['GET', 'HEAD', 'POST'])
def labour_survey_view(request, event, survey_slug):
    survey = get_object_or_404(Survey, slug=survey_slug, event=event)

    try:
        signup = Signup.objects.get(event=event, person=request.user.person)
    except Signup.DoesNotExist:
        messages.error(request, _('You have not signed up for this event.'))
        return redirect('core_event_view', event.slug)

    Form = survey.form_class

    try:
        instance = Form.get_instance_for_signup(signup)
    except ObjectDoesNotExist:
        messages.error(request, _('This survey does not apply to you.'))
        return redirect('core_event_view', event.slug)

    form = initialize_form(Form, request, instance=instance, event=event)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, _('Thank you for your answers.'))
            return redirect('core_event_view', event.slug)
        else:
            messages.error(request, _('Please check the form.'))

    vars = dict(
        event=event,
        signup=signup,
        instance=instance,
        survey=survey,
        form=form,
    )

    return render(request, 'labour_survey_view.jade', vars)
