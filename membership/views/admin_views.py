# encoding: utf-8

from django.contrib import messages
from django.core.urlresolvers import reverse
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

from ..forms import MemberForm, MembershipForm
from ..helpers import membership_admin_required
from ..models import STATE_CHOICES, Membership


EXPORT_FORMATS = [
    ('html', u'Tulostettava versio'),
    ('xlsx', u'Excel'),
    ('csv', u'CSV'),
]


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
        memberships.update(state='in_effect')
        messages.success(request, u'Hyväksyntää odottavat jäsenhakemukset hyväksyttiin.')
        return redirect('membership_admin_members_view', organization.slug)

    export_type = state_filters.selected_slug
    if export_type == 'approval':
        export_type_verbose = u'Hyväksyntää odottavat hakemukset'
    elif export_type == 'discharged':
        export_type_verbose = u'Erotetut jäsenet'
    elif export_type == 'declined':
        export_type_verbose = u'Hylätyt jäsenhakemukset'
    elif export_type == 'in_effect':
        export_type_verbose = u'Jäsenluettelo'
    elif not export_type:
        export_type = 'all'
        export_type_verbose = u'Jäsenluettelo'

    title = u'{organization.name} – {export_type_verbose}'.format(
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

    if format == 'screen':
        return render(request, 'membership_admin_members_view.jade', vars)
    elif format == 'html':
        return render(request, 'membership_admin_export_html_view.jade', vars)
    elif format in CSV_EXPORT_FORMATS:
        filename = "{organization.slug}_members_{timestamp}.{format}".format(
            organization=organization,
            timestamp=now().strftime('%Y%m%d%H%M%S'),
            format=format,
        )

        return csv_response(organization, Membership, memberships,
            dialect='xlsx',
            filename=filename,
            m2m_mode='separate_columns',
        )

@membership_admin_required
@require_http_methods(['GET', 'HEAD', 'POST'])
def membership_admin_member_view(request, vars, organization, person_id):
    membership = get_object_or_404(Membership, organization=organization, person=int(person_id))
    read_only = membership.person.user is not None
    member_form = initialize_form(MemberForm, request, instance=membership.person, readonly=read_only, prefix='member')
    membership_form = initialize_form(MembershipForm, request, instance=membership, prefix='membership')

    if request.method == 'POST':
        action = request.POST['action']

        if action in ['save-edit', 'save-return']:
            if read_only:
                valid = membership_form.is_valid()
            else:
                valid = membership_form.is_valid() and member_form.is_valid()

            if valid:
                membership_form.save()
                if not read_only:
                    member_form.save()

                membership.apply_state()

                messages.success(request, u'Jäsenen tiedot tallennettiin.')

                if action == 'save-return':
                    return redirect('membership_admin_members_view', organization.slug)

            else:
                messages.error(request, u'Tarkista lomakkeen tiedot.')
        else:
            raise NotImplementedError(action)

    previous_membership, next_membership = membership.get_previous_and_next()

    tabs = [
        Tab('membership-admin-person-tab', u'Jäsenen tiedot', active=True),
        Tab('membership-admin-state-tab', u'Jäsenyyden tila'),
        #Tab('membership-admin-events-tab', u'Jäsenyyteen liittyvät tapahtumat'),
        #Tab('membership-admin-payments-tab', u'Jäsenmaksut'),
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

    return render(request, 'membership_admin_member_view.jade', vars)


@handle_api_errors
@api_login_required
@require_safe
def membership_admin_emails_api(request, organization_slug):
    organization = get_object_or_404(Organization, slug=organization_slug)

    return HttpResponse(
        u'\n'.join(membership.person.email for membership in organization.memberships.all() if membership.person.email),
        content_type='text/plain; charset=UTF-8'
    )


def membership_admin_menu_items(request, organization):
    members_url = url('membership_admin_members_view', organization.slug)
    members_active = request.path.startswith(members_url)
    members_text = u'Jäsenrekisteri'

    return [(members_active, members_url, members_text)]
