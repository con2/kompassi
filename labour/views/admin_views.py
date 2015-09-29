# encoding: utf-8

import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models.query import Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods, require_GET
from django.utils import timezone

from dateutil.tz import tzlocal

from core.csv_export import csv_response
from core.sort_and_filter import Filter, Sorter
from core.models import Event, Person
from core.utils import initialize_form, url, json_response, render_string

from ..forms import AdminPersonForm, SignupForm, SignupAdminForm
from ..helpers import labour_admin_required
from ..utils import SignupStateFilter
from ..models import (
    JobCategory,
    LabourEventMeta,
    PersonQualification,
    Qualification,
    Signup,
)

from .view_helpers import initialize_signup_forms


@labour_admin_required
def labour_admin_dashboard_view(request, vars, event):
    vars.update(
        # XXX state overhaul
        num_pending=event.signup_set.filter(is_active=True, time_accepted__isnull=True).count(),
        num_accepted=event.signup_set.filter(time_accepted__isnull=False).count(),
        num_rejected=event.signup_set.filter(Q(time_rejected__isnull=False) | Q(time_cancelled__isnull=False)).count(),
        signups=event.signup_set.order_by('-created_at')[:5]
    )

    return render(request, 'labour_admin_dashboard_view.jade', vars)


@labour_admin_required
@require_http_methods(['GET', 'POST'])
def labour_admin_signup_view(request, vars, event, person_id):
    person = get_object_or_404(Person, pk=int(person_id))
    signup = get_object_or_404(Signup, person=person, event=event)

    old_state_flags = signup._state_flags

    signup_form, signup_extra_form, signup_admin_form = initialize_signup_forms(
        request, event, signup,
        admin=True
    )
    person_form = initialize_form(AdminPersonForm, request,
        instance=signup.person,
        prefix='person',
        submit_button=False,
        readonly=True,
        event=event,
    )

    if request.method == 'POST':
        # XXX Need to update state before validation to catch accepting people without accepted job categories
        for state_name in signup.next_states:
            command_name = 'set-state-{state_name}'.format(state_name=state_name)
            if command_name in request.POST:
                old_state_flags = signup._state_flags
                signup.state = state_name
                break

        if signup_form.is_valid() and signup_extra_form.is_valid() and signup_admin_form.is_valid():
            signup_form.save()
            signup_extra_form.save()
            signup_admin_form.save()

            signup.apply_state()
            messages.success(request, u'Tiedot tallennettiin.')

            if 'save-return' in request.POST:
                return redirect('labour_admin_signups_view', event.slug)
            else:
                return redirect('labour_admin_signup_view', event.slug, person.pk)
        else:
            # XXX Restore state just for shows, suboptimal but
            signup._state_flags = old_state_flags

            messages.error(request, u'Ole hyvä ja tarkista lomake.')

    non_qualified_category_names = [
        jc.name for jc in JobCategory.objects.filter(event=event)
        if not jc.is_person_qualified(signup.person)
    ]

    non_applied_categories = list(JobCategory.objects.filter(event=event))
    for applied_category in signup.job_categories.all():
        non_applied_categories.remove(applied_category)
    non_applied_category_names = [cat.name for cat in non_applied_categories]

    previous_signup, next_signup = signup.get_previous_and_next_signup()

    vars.update(
        person_form=person_form,
        signup=signup,
        signup_admin_form=signup_admin_form,
        signup_extra_form=signup_extra_form,
        signup_form=signup_form,

        next_signup=next_signup,
        previous_signup=previous_signup,

        # XXX hack: widget customization is very difficult, so apply styles via JS
        non_applied_category_names_json=json.dumps(non_applied_category_names),
        non_qualified_category_names_json=json.dumps(non_qualified_category_names),
    )

    return render(request, 'labour_admin_signup_view.jade', vars)


@labour_admin_required
def labour_admin_signups_view(request, vars, event):
    signups = event.signup_set.all()

    job_categories = event.jobcategory_set.all()

    job_category_filters = Filter(request, "job_category").add_objects("job_categories__slug", job_categories)
    signups = job_category_filters.filter_queryset(signups)
    job_category_accepted_filters = Filter(request, "job_category_accepted").add_objects("job_categories_accepted__slug", job_categories)
    signups = job_category_accepted_filters.filter_queryset(signups)

    sorter = Sorter(request, "sort")
    sorter.add("name", name=u'Sukunimi, Etunimi', definition=('person__surname', 'person__first_name'))
    sorter.add("newest", name=u'Uusin ensin', definition=('-created_at',))
    sorter.add("oldest", name=u'Vanhin ensin', definition=('created_at',))
    signups = sorter.order_queryset(signups)

    # Must be done after sorting, since `SignupStateFilter` doesn't currently operate in the database
    state_filter = SignupStateFilter(request, "state")
    state_filter.add_state("new", "Haettu")
    state_filter.add_state("accepted", "Odottaa vuoroja")
    state_filter.add_state("finished", "Vuorot lähetetty")
    state_filter.add_state("complained", "Reklamoitu")
    state_filter.add_state("rejected", "Hylätty")
    signups = state_filter.filter_queryset(signups)

    vars.update(
        signups=signups,
        job_category_filters=job_category_filters,
        job_category_accepted_filters=job_category_accepted_filters,
        state_filter=state_filter,
        sorter=sorter
    )

    return render(request, 'labour_admin_signups_view.jade', vars)


@labour_admin_required
def labour_admin_roster_view(request, vars, event):
    # use javaScriptCase because this gets directly embedded in <script> as json
    tz = tzlocal()

    config = dict(
        event=event.as_dict(),
        workHours=[
            dict(timestamp=hour.astimezone(tz).isoformat())
            for hour in event.labour_event_meta.work_hours
        ],
        lang='fi', # XXX I18N hardcoded
        urls=dict(
            base=url('labour_admin_roster_view', event.slug),
            jobCategoryApi=url('labour_api_job_categories_view', event.slug),
        )
    )

    vars.update(
        config_json=json.dumps(config),
    )

    return render(request, 'labour_admin_roster_view.jade', vars)


@labour_admin_required
@require_GET
def labour_admin_mail_view(request, vars, event):
    from mailings.models import Message

    messages = Message.objects.filter(recipient__event=event, recipient__app_label='labour')

    vars.update(
        labour_messages=messages
    )

    return render(request, 'labour_admin_mail_view.jade', vars)


@labour_admin_required
@require_http_methods(['GET', 'POST'])
def labour_admin_mail_editor_view(request, vars, event, message_id=None):
    from mailings.models import Message
    from mailings.forms import MessageForm

    if message_id:
        message = get_object_or_404(Message, recipient__event=event, pk=int(message_id))
    else:
        message = None

    form = initialize_form(MessageForm, request, event=event, instance=message)

    if request.method == 'POST':
        if 'delete' in request.POST:
            assert not message.sent_at
            message.delete()
            messages.success(request, u'Viesti poistettiin.')
            return redirect('labour_admin_mail_view', event.slug)

        else:
            if form.is_valid():
                message = form.save(commit=False)

                if 'save-send' in request.POST:
                    message.save()
                    message.send()
                    messages.success(request, u'Viesti lähetettiin. Se lähetetään automaattisesti myös kaikille uusille vastaanottajille.')

                elif 'save-expire' in request.POST:
                    message.save()
                    message.expire()
                    messages.success(request, u'Viesti merkittiin vanhentuneeksi. Sitä ei lähetetä enää uusille vastaanottajille.')

                elif 'save-unexpire' in request.POST:
                    message.save()
                    message.unexpire()
                    messages.success(request, u'Viesti otettiin uudelleen käyttöön. Se lähetetään automaattisesti myös kaikille uusille vastaanottajille.')

                elif 'save-return' in request.POST:
                    message.save()
                    messages.success(request, u'Muutokset viestiin tallennettiin.')
                    return redirect('labour_admin_mail_view', event.slug)

                elif 'save-edit' in request.POST:
                    message.save()
                    messages.success(request, u'Muutokset viestiin tallennettiin.')

                else:
                    messages.error(request, u'Tuntematon toiminto.')

                return redirect('labour_admin_mail_editor_view', event.slug, message.pk)

            else:
                messages.error(request, u'Ole hyvä ja tarkasta lomake.')

    vars.update(
        message=message,
        form=form,
        sender="TODO",
    )

    return render(request, 'labour_admin_mail_editor_view.jade', vars)


@labour_admin_required
@require_GET
def labour_admin_export_view(request, vars, event):
    signup_ids = request.GET.get('signup_ids', None)

    if signup_ids == "":
        # fmh
        signups = []
    elif signup_ids is not None:
        signup_ids = [int(id) for id in signup_ids.split(',')]
        signups = Signup.objects.filter(event=event, pk__in=signup_ids)
    else:
        signups = Signup.objects.filter(event=event)

    signups = signups.select_related('person').select_related('event').select_related('event__laboureventmeta')

    filename="{event.slug}_signups_{timestamp}.xlsx".format(
        event=event,
        timestamp=timezone.now().strftime('%Y%m%d%H%M%S'),
    )

    return csv_response(event, Signup, signups,
        dialect='xlsx',
        filename=filename,
        m2m_mode='separate_columns',
    )


def labour_admin_menu_items(request, event):
    dashboard_url = url('labour_admin_dashboard_view', event.slug)
    dashboard_active = request.path == dashboard_url
    dashboard_text = u"Kojelauta"

    signups_url = url('labour_admin_signups_view', event.slug)
    signups_active = request.path.startswith(signups_url)
    signups_text = u"Tapahtumaan ilmoittautuneet henkilöt"

    mail_url = url('labour_admin_mail_view', event.slug)
    mail_active = request.path.startswith(mail_url)
    mail_text = u"Työvoimaviestit"

    roster_url = url('labour_admin_roster_view', event.slug)
    roster_active = request.path.startswith(roster_url)
    roster_text = u"Työvuorojen suunnittelu"

    query_url = url('labour_admin_query', event.slug)
    query_active = request.path == query_url
    query_text = u"Hakemusten suodatus"

    menu_items = [
        (dashboard_active, dashboard_url, dashboard_text),
        (signups_active, signups_url, signups_text),
        (mail_active, mail_url, mail_text),
    ]

    # unstable / development features
    if settings.DEBUG:
        menu_items.extend((
            (roster_active, roster_url, roster_text),
            (query_active, query_url, query_text),
        ))

    return menu_items
