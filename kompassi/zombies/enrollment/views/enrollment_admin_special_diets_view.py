from django.shortcuts import render

from kompassi.labour.views.admin_special_diets_view import NO_SPECIAL_DIET_REPLIES, SpecialDiets

from ..helpers import enrollment_admin_required
from ..models import Enrollment


@enrollment_admin_required
def enrollment_admin_special_diets_view(request, vars, event):
    enrollments = Enrollment.objects.filter(event=event)

    enrollments_with_standard_special_diets = enrollments.filter(special_diet__isnull=False).distinct()

    special_diets = SpecialDiets()

    for signup_extra in enrollments_with_standard_special_diets:
        special_diets[signup_extra.formatted_special_diet].count += 1

    special_diets = list(special_diets.values())
    special_diets.sort(key=lambda sd: sd.name)

    enrollments_with_other_special_diets = enrollments.exclude(special_diet_other__in=NO_SPECIAL_DIET_REPLIES)

    vars.update(
        enrollments_with_other_special_diets=enrollments_with_other_special_diets,
        special_diets=special_diets,
    )

    return render(request, "enrollment_admin_special_diets_view.pug", vars)
