from collections import defaultdict
from dataclasses import dataclass

from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

from ..helpers import labour_admin_required

NO_SPECIAL_DIET_REPLIES = ["", "-", "N/A", "Ei ole", "Ei ole."]


@dataclass
class DietRow:
    name: str
    count: int = 0


class SpecialDiets(defaultdict):
    def __missing__(self, key):
        value = DietRow(key)
        self[key] = value
        return value


@labour_admin_required
def admin_special_diets_view(request, vars, event):
    meta = event.labour_event_meta
    SignupExtra = meta.signup_extra_model
    special_diet_field = SignupExtra.get_special_diet_field()
    special_diet_other_field = SignupExtra.get_special_diet_other_field()

    if not any((special_diet_field, special_diet_other_field)):
        messages.error(request, _("This event does not record special diets."))
        return redirect("admin_dashboard_view", event.slug)

    # XXX Tracon 11 afterparty participation hack
    if request.GET.get("afterparty_participation"):
        messages.warning(request, "Näytetään vain kaatajaisten osallistujien tiedot.")
        signup_extras = SignupExtra.objects.filter(afterparty_participation=True)
    else:
        signup_extras = SignupExtra.objects.filter(is_active=True)

    if special_diet_field:
        signup_extras_with_standard_special_diets = signup_extras.filter(special_diet__isnull=False).distinct()

        special_diets = SpecialDiets()

        for signup_extra in signup_extras_with_standard_special_diets:
            special_diets[signup_extra.formatted_special_diet].count += 1

        special_diets = list(special_diets.values())
        special_diets.sort(key=lambda sd: sd.name)
    else:
        special_diets = []

    total_count = signup_extras.count()

    if special_diet_other_field:
        # TODO assumes name special_diet_other
        signup_extras_with_other_special_diets = signup_extras.exclude(special_diet_other__in=NO_SPECIAL_DIET_REPLIES)
    else:
        signup_extras_with_other_special_diets = []

    vars.update(
        signup_extras_with_other_special_diets=signup_extras_with_other_special_diets,
        special_diet_field=special_diet_field,
        special_diet_other_field=special_diet_other_field,
        special_diets=special_diets,
        total_count=total_count,
    )

    return render(request, "labour_admin_special_diets_view.pug", vars)
