# encoding: utf-8



from collections import defaultdict, namedtuple

from django.contrib import messages
from django.db.models import Count, Case, When
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _

from labour.views.labour_admin_special_diets_view import (
    NO_SPECIAL_DIET_REPLIES,
    SpecialDiets
)

from ..models import Enrollment, SpecialDiet
from ..helpers import enrollment_admin_required


@enrollment_admin_required
def enrollment_admin_special_diets_view(request, vars, event):
    meta = event.enrollment_event_meta
    enrollments = Enrollment.objects.filter(event=event)

    enrollments_with_standard_special_diets = enrollments.filter(
        special_diet__isnull=False
    ).distinct()

    special_diets = SpecialDiets()

    for signup_extra in enrollments_with_standard_special_diets:
        special_diets[signup_extra.formatted_special_diet].count += 1

    special_diets = list(special_diets.values())
    special_diets.sort(key=lambda sd: sd.name)

    enrollments_with_other_special_diets = enrollments.exclude(
        special_diet_other__in=NO_SPECIAL_DIET_REPLIES
    )

    vars.update(
        enrollments_with_other_special_diets=enrollments_with_other_special_diets,
        special_diets=special_diets,
    )

    return render(request, 'enrollment_admin_special_diets_view.pug', vars)
