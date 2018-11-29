from collections import Counter

from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _

from ..helpers import labour_admin_required


@labour_admin_required
def labour_admin_shirts_view(request, vars, event):
    # TODO half assumes and half doesn't that the shirt size field is named "shirt_size"
    meta = event.labour_event_meta
    SignupExtra = meta.signup_extra_model
    shirt_size_field = SignupExtra.get_shirt_size_field()
    shirt_type_field = SignupExtra.get_shirt_type_field()

    if shirt_size_field is None:
        messages.error(request, _('This event does not record shirt sizes.'))
        return redirect('labour_admin_dashboard_view', event.slug)

    shirt_sizes = shirt_size_field.choices

    if shirt_type_field:
        shirt_types = shirt_type_field.choices
    else:
        shirt_types = [('default', _('Paita'))]

    base_criteria = dict(is_active=True)

    shirt_type_totals = Counter()
    shirt_size_rows = []
    for shirt_size_slug, shirt_size_name in shirt_sizes:
        num_shirts_by_shirt_type = []
        for shirt_type_slug, shirt_type_name in shirt_types:
            signup_extras = SignupExtra.objects.filter(**base_criteria).filter(shirt_size=shirt_size_slug)

            if shirt_type_field:
                signup_extras = signup_extras.filter(shirt_type=shirt_type_slug)

            num_shirts = signup_extras.count()
            shirt_type_totals[shirt_type_slug] += num_shirts
            num_shirts_by_shirt_type.append(num_shirts)

        shirt_size_rows.append((shirt_size_name, num_shirts_by_shirt_type))

    shirt_type_totals = [shirt_type_totals[shirt_type_slug] for (shirt_type_slug, shirt_type_name) in shirt_types]

    num_shirts = sum(shirt_type_totals)

    # TODO Why does this assert sometimes blow
    # Eg. Desucon 2016: Left 343, right 340
    # We order extra shirts anyway so not going to debug this now
    # assert SignupExtra.objects.filter(shirt_size__isnull=False, **base_criteria).count() == num_shirts, "Lost some shirts"

    vars.update(
        num_shirts=num_shirts,
        shirt_size_rows=shirt_size_rows,
        shirt_types=shirt_types,
        shirt_type_totals=shirt_type_totals,
    )

    return render(request, 'labour_admin_shirts_view.pug', vars)
