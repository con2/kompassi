import csv
import logging

from django import forms
from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect, render
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from core.utils.form_utils import horizontal_form_helper
from labour.models.personnel_class import PersonnelClass

from ..helpers import badges_admin_required
from ..models import Badge

logger = logging.getLogger(__name__)


class BadgeImportForm(forms.Form):
    file = forms.FileField(
        label=_("CSV file"),
        help_text=_(
            "CSV file with columns first_name, surname, job_title, nick and personnel_class. "
            "A truthy value in a field called printed will mark the badge as such. "
            "Any of these may be missing or empty. "
            "Use semicolon as field delimiter (default in Excel)."
        ),
    )
    default_personnel_class = forms.ModelChoiceField(
        queryset=PersonnelClass.objects.all(),
        label=_("Default personnel class"),
        required=False,
        help_text=_(
            "Personnel class to use for badges that don't have one specified in the CSV file. If you don't set a default personnel class, you must specify personnel_class on each row."
        ),
    )

    def __init__(self, *args, **kwargs):
        event = kwargs.pop("event")
        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()

        self.fields["default_personnel_class"].queryset = PersonnelClass.objects.filter(event=event)  # type: ignore


@badges_admin_required
@require_http_methods(["GET", "HEAD", "POST"])
def badges_admin_import_view(request, vars, event):
    if request.method == "POST":
        form = BadgeImportForm(request.POST, request.FILES, event=event)
        vars.update(form=form)
        if not form.is_valid():
            messages.error(request, _("Please check the form"))
            return render(request, "badges_admin_import_view.pug", vars)

        csv_file = request.FILES.get("file")
        if not csv_file:
            messages.error(request, _("No file uploaded"))
            return redirect("badges_admin_import_view", event.slug)

        try:
            decoded_file = csv_file.read().decode("utf-8-sig").splitlines()
            reader = csv.DictReader(decoded_file, dialect="excel", delimiter=";")

            with transaction.atomic():
                for row in reader:
                    first_name = row.get("first_name", "")
                    surname = row.get("surname", "")
                    job_title = row.get("job_title", "")
                    nick = row.get("nick", "")

                    if not any([first_name, surname, job_title, nick]):
                        continue

                    personnel_class_name = row.get("personnel_class")
                    if personnel_class_name:
                        personnel_class = PersonnelClass.objects.get(event=event, name=personnel_class_name)
                    else:
                        personnel_class = form.cleaned_data["default_personnel_class"]

                    if personnel_class is None:
                        messages.error(
                            request,
                            "If you do not set a default personnel class, you must specify personnel_class on each row.",
                        )
                        return redirect("badges_admin_import_view", event.slug)

                    badge = Badge.objects.create(
                        personnel_class=personnel_class,
                        first_name=first_name,
                        surname=surname,
                        job_title=job_title,
                        nick=nick,
                    )

                    if row.get("printed"):
                        badge.printed_separately_at = now()
                        badge.save()

            messages.success(request, _("Badges imported successfully"))
        except Exception as e:
            logger.error("Error processing file", exc_info=e)
            messages.error(request, _("Error processing file: ") + str(e))
        return redirect("badges_admin_import_view", event.slug)

    form = BadgeImportForm(event=event)
    vars.update(form=form)

    return render(request, "badges_admin_import_view.pug", vars)
