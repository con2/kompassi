# encoding: utf-8

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now

from core.utils import url, initialize_form
from core.sort_and_filter import Filter
from core.csv_export import csv_response, CSV_EXPORT_FORMATS

from ..forms import MemberForm, MembershipForm
from ..helpers import membership_admin_required
from ..models import STATE_CHOICES, Membership


EXPORT_FORMATS = [
    ('html', u'Tulostettava versio'),
    ('xlsx', u'Excel'),
    ('csv', u'CSV'),
]


@membership_admin_required
def membership_admin_members_view(request, vars, organization, format='screen'):
    members = organization.members.all().select_related('person')
    num_all_members = members.count()

    state_filters = Filter(request, 'state').add_choices('state', STATE_CHOICES)
    members = state_filters.filter_queryset(members)

    filter_active = any(f.selected_slug != f.default for f in [
        state_filters,
    ])

    members = members.order_by('person__surname', 'person__official_first_names')

    export_type = state_filters.selected_slug
    if export_type == 'approval':
        export_type_verbose = u'Hyväksyntää odottavat hakemukset'
    elif export_type == 'discharged':
        export_type_verbose = u'Erotetut jäsenet'
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
        members=members,
        num_members=members.count(),
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

        return csv_response(organization, Membership, members,
            dialect='xlsx',
            filename=filename,
            m2m_mode='separate_columns',
        )

@membership_admin_required
def membership_admin_member_view(request, vars, organization, person_id):
    membership = get_object_or_404(Membership, organization=organization, person=int(person_id))
    read_only = membership.person.user is not None
    form = initialize_form(MemberForm, request, instance=membership.person, readonly=read_only)

    if request.method == 'POST':
        action = request.POST['action']

        if read_only:
            messages.error(request, u'Koska jäsenellä on Kompassi-tunnus, vain jäsen itse voi muokata näitä tietoja.')
        elif action in ['save-edit', 'save-return']:
            if form.is_valid():
                form.save()

                messages.success(request, u'Jäsenen tiedot tallennettiin.')

                if action == 'save-return':
                    return redirect('membership_admin_members_view', organization.slug)
        else:
            raise NotImplementedError(action)

    vars.update(
        membership=membership,
        member=membership.person,
        form=form,
        read_only=read_only,
    )

    return render(request, 'membership_admin_member_view.jade', vars)


def membership_admin_menu_items(request, organization):
    members_url = url('membership_admin_members_view', organization.slug)
    members_active = request.path.startswith(members_url)
    members_text = u'Jäsenrekisteri'

    return [(members_active, members_url, members_text)]
