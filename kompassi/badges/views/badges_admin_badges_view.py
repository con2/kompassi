from typing import Any

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from kompassi.core.csv_export import CSV_EXPORT_FORMATS, csv_response
from kompassi.core.utils import groupby_strict, initialize_form
from kompassi.labour.models import PersonnelClass

from ..forms import HiddenBadgeCrouchingForm
from ..helpers import badges_admin_required
from ..models import Badge
from ..proxies.badge.management import BadgeManagementProxy

BADGE_ORDER = ("personnel_class", "surname", "first_name")
BADGE_LIST_TEMPLATES = dict(
    screen=dict(
        normal="badges_admin_badges_view.pug",
        yoink="badges_admin_badges_view.pug",
    ),
    print=dict(
        normal="badges_admin_badges_print.pug",
        yoink="badges_admin_badges_print_yoink.pug",
    ),
)


class BadgesToYoinkFakePersonnelClass:
    name = "Yoinkkauslista"
    slug = "yoink"


badges_to_yoink_fake_personnel_class = BadgesToYoinkFakePersonnelClass()


@badges_admin_required
@require_http_methods(["GET", "HEAD", "POST"])
def badges_admin_badges_view(request, vars, event, personnel_class_slug=None):
    if request.method == "POST":
        form = initialize_form(HiddenBadgeCrouchingForm, request)

        if form.is_valid():
            badge = get_object_or_404(BadgeManagementProxy, pk=form.cleaned_data["badge_id"])

            if "revoke-badge" in request.POST:
                if not badge.can_revoke:
                    messages.error(
                        request,
                        _(
                            "This badge cannot be revoked here because it is managed "
                            "by either the labour or the programme management system."
                        ),
                    )
                elif badge.is_revoked:
                    messages.warning(request, _("The badge had already been revoked."))
                else:
                    badge.revoke(user=request.user)
                    messages.success(request, _("The badge has now been revoked."))

            elif "clear-revoked" in request.POST:
                if not badge.can_unrevoke:
                    messages.error(
                        request,
                        _(
                            "This revoked badge cannot be un-revoked here because it is managed "
                            "by either the labour or the programme management system."
                        ),
                    )
                if not badge.is_revoked:
                    messages.warning(request, _("The badge was already valid."))
                else:
                    badge.unrevoke()
                    messages.success(request, _("The badge has been restored."))

            elif "mark-printed" in request.POST:
                badge.is_printed_separately = True
                badge.save()
                messages.success(request, "Badge on merkitty erikseen tulostetuksi.")

            elif "clear-printed" in request.POST:
                badge.is_printed_separately = False
                badge.save()
                messages.success(request, "Badgesta on pyyhitty erikseen tulostettu -merkintä.")

            else:
                messages.error(request, "Kelvoton pyyntö.")

            return redirect(request.path)
        raise NotImplementedError("Should never get here.")

    format = request.GET.get("format", "screen")
    badge_criteria = dict(personnel_class__event=event)
    active_filter = None
    viewing_yoink_list = False
    template_subtype = "normal"

    if personnel_class_slug is not None:
        if personnel_class_slug == "yoink":
            viewing_yoink_list = True
            active_filter = badges_to_yoink_fake_personnel_class
            badge_criteria.update(revoked_at__isnull=False)
            template_subtype = "yoink"
        else:
            active_filter = get_object_or_404(PersonnelClass, event=event, slug=personnel_class_slug)
            badge_criteria.update(personnel_class=active_filter)

    # Non-yoink paper lists only show non-revoked badges.
    # Yoink list only shows revoked badges.
    if format != "screen" and personnel_class_slug != "yoink":
        badge_criteria.update(revoked_at__isnull=True)

    badges = BadgeManagementProxy.objects.filter(**badge_criteria).order_by(*BADGE_ORDER)

    if format in CSV_EXPORT_FORMATS:
        filename = "{event.slug}-badges-{badge_filter}{timestamp}.{format}".format(
            event=event,
            badge_filter=f"{personnel_class_slug}-" if personnel_class_slug is not None else "",
            timestamp=timezone.now().strftime("%Y%m%d%H%M%S"),
            format=format,
        )

        return csv_response(event, Badge, badges, filename=filename, dialect=CSV_EXPORT_FORMATS[format])

    if format in BADGE_LIST_TEMPLATES:
        page_template = BADGE_LIST_TEMPLATES[format][template_subtype]

        title = "{event.name} &ndash; {qualifier}".format(
            event=event,
            qualifier=active_filter.name if active_filter else "Nimilista",
        )

        filters: list[tuple[bool, Any]] = [
            (personnel_class_slug == personnel_class.slug, personnel_class)
            for personnel_class in PersonnelClass.objects.filter(event=event)
        ]

        filters.append((viewing_yoink_list, badges_to_yoink_fake_personnel_class))

        vars.update(
            active_filter=active_filter,
            filters=filters,
            now=timezone.now(),
            title=title,
            should_display_personnel_class=not active_filter or personnel_class_slug == "yoink",
            can_manually_add_badge=personnel_class_slug != "yoink",
        )

        if personnel_class_slug == "yoink" and format == "print":
            badges_by_personnel_class = groupby_strict(badges, lambda badge: badge.personnel_class)

            vars.update(badges_by_personnel_class=badges_by_personnel_class)
        else:
            vars.update(badges=badges)

        return render(request, page_template, vars)

    raise NotImplementedError(format)
