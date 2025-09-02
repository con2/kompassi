from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from kompassi.core.utils import initialize_form
from kompassi.labour.models import PersonnelClass

from ..forms import BadgeForm
from ..helpers import badges_admin_required


@badges_admin_required
@require_http_methods(["GET", "HEAD", "POST"])
def badges_admin_create_view(request, vars, event, personnel_class_slug=None):
    initial = dict()

    if personnel_class_slug is not None:
        personnel_class = get_object_or_404(PersonnelClass, event=event, slug=personnel_class_slug)
        initial.update(personnel_class=personnel_class)

    form = initialize_form(BadgeForm, request, prefix="badge_type", event=event, initial=initial)

    if request.method == "POST":
        if form.is_valid():
            badge = form.save(commit=False)

            badge.is_first_name_visible = bool(badge.first_name)
            badge.is_surname_visible = bool(badge.surname)
            badge.is_nick_visible = bool(badge.nick)
            badge.perks = {"internal:formattedPerks": form.cleaned_data["formatted_perks"]}

            badge.created_by = request.user

            try:
                badge.full_clean()
            except ValidationError as e:
                messages.error(request, e.message)
            else:
                badge.save()

                messages.success(request, _("The badge has been added."))
                return redirect("badges_admin_dashboard_view", event.slug)
        else:
            messages.error(request, _("Please check the form."))

    vars.update(
        form=form,
    )

    return render(request, "badges_admin_create_view.pug", vars)
