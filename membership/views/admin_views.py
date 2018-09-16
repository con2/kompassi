from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.views.decorators.http import require_safe, require_http_methods

from api.utils import handle_api_errors, api_login_required
from core.csv_export import csv_response, CSV_EXPORT_FORMATS
from core.models import Organization
from core.sort_and_filter import Filter
from core.tabs import Tab
from core.utils import url, initialize_form
from event_log.utils import emit

from ..forms import MemberForm, MembershipForm
from ..helpers import membership_admin_required
from ..models import STATE_CHOICES, Membership


EXPORT_FORMATS = [
    ('html', 'Tulostettava versio'),
    ('xlsx', 'Excel'),
    ('csv', 'CSV'),
]


EXPORT_TYPE_VERBOSE = dict(
    approval='Hyväksyntää odottavat hakemukset',
    discharged='Erotetut jäsenet',
    declined='Hylätyt jäsenhakemukset',
    in_effect='Jäsenluettelo',
    all='Jäsenluettelo',
)


HTML_TEMPLATES = dict(
    screen='membership_admin_members_view.jade',
    html='membership_admin_export_html_view.jade',
)


@membership_admin_required
@require_http_methods(['GET', 'HEAD', 'POST'])
def membership_admin_members_view(request, vars, organization, format='screen'):
    memberships = organization.memberships.all().select_related('person')
    num_all_members = memberships.count()

    state_filters = Filter(request, 'state').add_choices('state', STATE_CHOICES)
    memberships = state_filters.filter_queryset(memberships)

    filter_active = any(f.selected_slug != f.default for f in [
        state_filters,
    ])

    memberships = memberships.order_by('person__surname', 'person__official_first_names')

    if request.method == 'POST' and state_filters.selected_slug == 'approval':
        # PLEASE DON'T: locally cached objects do not get updated and apply_state does not do the needful
        # memberships.update(state='in_effect')

        # TODO encap in Membership
        for membership in memberships:
            membership.state = 'in_effect'
            membership.save()
            membership.apply_state()

        messages.success(request, 'Hyväksyntää odottavat jäsenhakemukset hyväksyttiin.')
        return redirect('membership_admin_members_view', organization.slug)

    export_type = state_filters.selected_slug or 'all'
    export_type_verbose = EXPORT_TYPE_VERBOSE[export_type]

    title = '{organization.name} – {export_type_verbose}'.format(
        organization=organization,
        export_type_verbose=export_type_verbose,
    )

    vars.update(
        show_approve_all_button=state_filters.selected_slug == 'approval',
        memberships=memberships,
        num_members=memberships.count(),
        num_all_members=num_all_members,
        state_filters=state_filters,
        filter_active=filter_active,
        css_to_show_filter_panel='in' if filter_active else '',
        export_formats=EXPORT_FORMATS,
        now=now(),
        title=title,
    )

    if format in HTML_TEMPLATES:
        return render(request, HTML_TEMPLATES[format], vars)
    elif format in CSV_EXPORT_FORMATS:
        filename = "{organization.slug}_members_{timestamp}.{format}".format(
            organization=organization,
            timestamp=now().strftime('%Y%m%d%H%M%S'),
            format=format,
        )

        emit('core.person.exported', request=request, organization=organization)

        return csv_response(organization, Membership, memberships,
            dialect=format,
            filename=filename,
            m2m_mode='separate_columns',
        )
    else:
        raise NotImplementedError(format)


@membership_admin_required
@require_http_methods(['GET', 'HEAD', 'POST'])
def membership_admin_member_view(request, vars, organization, person_id):
    membership = get_object_or_404(Membership, organization=organization, person=int(person_id))
    read_only = membership.person.user is not None
    member_form = initialize_form(MemberForm, request, instance=membership.person, readonly=read_only, prefix='member')
    membership_form = initialize_form(MembershipForm, request, instance=membership, prefix='membership')

    forms = [membership_form] if read_only else [membership_form, member_form]

    if request.method == 'POST':
        action = request.POST['action']

        if action in ['save-edit', 'save-return']:
            if all(form.is_valid() for form in forms):
                for form in forms:
                    form.save()

                membership.apply_state()

                messages.success(request, 'Jäsenen tiedot tallennettiin.')

                if action == 'save-return':
                    return redirect('membership_admin_members_view', organization.slug)

            else:
                messages.error(request, 'Tarkista lomakkeen tiedot.')
        else:
            raise NotImplementedError(action)

    previous_membership, next_membership = membership.get_previous_and_next()

    tabs = [
        Tab('membership-admin-person-tab', 'Jäsenen tiedot', active=True),
        Tab('membership-admin-state-tab', 'Jäsenyyden tila'),
        # Tab('membership-admin-events-tab', 'Jäsenyyteen liittyvät tapahtumat'),
        # Tab('membership-admin-payments-tab', 'Jäsenmaksut'),
    ]

    vars.update(
        member=membership.person,
        member_form=member_form,
        membership=membership,
        membership_form=membership_form,
        next_membership=next_membership,
        previous_membership=previous_membership,
        read_only=read_only,
        tabs=tabs,
    )

    membership.person.log_view(request)

    return render(request, 'membership_admin_member_view.jade', vars)


@handle_api_errors
@api_login_required
@require_safe
def membership_admin_emails_api(request, organization_slug):
    organization = get_object_or_404(Organization, slug=organization_slug)

    return HttpResponse(
        '\n'.join(
            membership.person.email
            for membership in organization.memberships.filter(state='in_effect')
            if membership.person.email
        ),
        content_type='text/plain; charset=UTF-8'
    )


def membership_admin_menu_items(request, organization):
    members_url = url('membership_admin_members_view', organization.slug)
    members_active = request.path.startswith(members_url)
    members_text = 'Jäsenrekisteri'

    return [(members_active, members_url, members_text)]
