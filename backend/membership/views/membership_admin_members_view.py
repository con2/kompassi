from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.timezone import now
from django.views.decorators.http import require_http_methods

from core.csv_export import CSV_EXPORT_FORMATS, csv_response
from core.sort_and_filter import Filter
from event_log_v2.utils.emit import emit

from ..helpers import membership_admin_required
from ..models import STATE_CHOICES, Membership

EXPORT_FORMATS = [
    ("html", "Tulostettava versio"),
    ("xlsx", "Excel"),
    ("csv", "CSV"),
]

EXPORT_TYPE_VERBOSE = dict(
    approval="Hyväksyntää odottavat hakemukset",
    discharged="Erotetut jäsenet",
    declined="Hylätyt jäsenhakemukset",
    in_effect="Jäsenluettelo",
    all="Jäsenluettelo",
)

HTML_TEMPLATES = dict(
    screen="membership_admin_members_view.pug",
    html="membership_admin_export_html_view.pug",
)


@membership_admin_required
@require_http_methods(["GET", "HEAD", "POST"])
def membership_admin_members_view(request, vars, organization, format="screen"):
    memberships = organization.memberships.all().select_related("person")
    num_all_members = memberships.count()

    state_filters = Filter(request, "state").add_choices("state", STATE_CHOICES)
    memberships = state_filters.filter_queryset(memberships)

    memberships = memberships.order_by("person__surname", "person__official_first_names")

    all_filters = [state_filters]

    current_term = organization.membership_organization_meta.get_current_term()
    if current_term:
        payment_filters = Filter(request, "paid")
        paymentinator = (
            lambda is_paid: lambda member: (term := member.get_payment_for_term()) and term.is_paid == is_paid
        )
        payment_filters.add("1", "Maksettu", paymentinator(True))
        payment_filters.add("0", "Ei maksettu", paymentinator(False))
        memberships = payment_filters.filter_queryset(memberships)

        all_filters.append(payment_filters)
    else:
        messages.warning(request, "Nykyisen toimikauden tiedot puuttuvat. Syötä tiedot Toimikauden tiedot -näkymässä.")
        payment_filters = None

    filter_active = any(f.selected_slug != f.default for f in all_filters)

    if request.method == "POST" and state_filters.selected_slug == "approval":
        # PLEASE DON'T: locally cached objects do not get updated and apply_state does not do the needful
        # memberships.update(state='in_effect')

        # TODO encap in Membership
        for membership in memberships:
            membership.state = "in_effect"
            membership.save()
            membership.apply_state()

        messages.success(request, "Hyväksyntää odottavat jäsenhakemukset hyväksyttiin.")
        return redirect("membership_admin_members_view", organization.slug)

    export_type = state_filters.selected_slug or "all"
    export_type_verbose = EXPORT_TYPE_VERBOSE[export_type]

    title = f"{organization.name} – {export_type_verbose}"

    vars.update(
        show_approve_all_button=state_filters.selected_slug == "approval",
        memberships=memberships,
        num_members=len(memberships),
        num_all_members=num_all_members,
        state_filters=state_filters,
        payment_filters=payment_filters,
        filter_active=filter_active,
        css_to_show_filter_panel="in" if filter_active else "",
        export_formats=EXPORT_FORMATS,
        now=now(),
        title=title,
        current_term=current_term,
    )

    if format in HTML_TEMPLATES:
        return render(request, HTML_TEMPLATES[format], vars)
    elif format in CSV_EXPORT_FORMATS:
        filename = "{organization.slug}_members_{timestamp}.{format}".format(
            organization=organization,
            timestamp=now().strftime("%Y%m%d%H%M%S"),
            format=format,
        )

        emit("core.person.exported", request=request)

        return csv_response(
            organization,
            Membership,
            memberships,
            dialect=format,
            filename=filename,
            m2m_mode="separate_columns",
        )
    else:
        raise NotImplementedError(format)
