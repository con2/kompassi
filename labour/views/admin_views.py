# encoding: utf-8

from collections import Counter, OrderedDict, namedtuple
import json

import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models.query import Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods, require_safe
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from dateutil.tz import tzlocal

from core.csv_export import csv_response, CSV_EXPORT_FORMATS, EXPORT_FORMATS
from core.sort_and_filter import Filter, Sorter
from core.models import Event, Person
from core.tabs import Tab
from core.utils import initialize_form, url

from ..forms import AdminPersonForm, SignupForm, SignupAdminForm
from ..helpers import labour_admin_required, SignupStateFilter, labour_event_required, labour_supervisor_required
from ..models.constants import SIGNUP_STATE_NAMES
from ..models import (
    JobCategory,
    LabourEventMeta,
    PersonQualification,
    Qualification,
    Signup,
)
from ..proxies.signup.onboarding import SignupOnboardingProxy

from .view_helpers import initialize_signup_forms


MassOperationBase = namedtuple('MassOperation', 'name modal_id text num_candidates')
class MassOperation(MassOperationBase):
    @property
    def disabled_attr(self):
        return 'disabled' if not self.num_candidates else ''


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
@require_http_methods(['GET', 'HEAD', 'POST'])
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

    historic_signups = Signup.objects.filter(person=signup.person).exclude(event=event).order_by('-event__start_time')
    if not person.allow_work_history_sharing:
        # The user has elected to not share their full work history between organizations.
        # Only show work history for the current organization.
        historic_signups = historic_signups.filter(event__organization=event.organization)

    tabs = [
        Tab('labour-admin-signup-state-tab', u'Hakemuksen tila', active=True),
        Tab('labour-admin-signup-person-tab', u'Hakijan tiedot'),
        Tab('labour-admin-signup-application-tab', u'Hakemuksen tiedot'),
        Tab('labour-admin-signup-messages-tab', u'Työvoimaviestit', notifications=signup.person_messages.count()),
        Tab('labour-admin-signup-history-tab', u'Työskentelyhistoria', notifications=historic_signups.count()),
    ]

    vars.update(
        historic_signups=historic_signups,
        next_signup=next_signup,
        person_form=person_form,
        previous_signup=previous_signup,
        signup=signup,
        signup_admin_form=signup_admin_form,
        signup_extra_form=signup_extra_form,
        signup_form=signup_form,
        tabs=tabs,

        # XXX hack: widget customization is very difficult, so apply styles via JS
        non_applied_category_names_json=json.dumps(non_applied_category_names),
        non_qualified_category_names_json=json.dumps(non_qualified_category_names),
    )

    return render(request, 'labour_admin_signup_view.jade', vars)


@labour_admin_required
@require_http_methods(['GET', 'HEAD', 'POST'])
def labour_admin_signups_view(request, vars, event, format='screen'):
    signups = event.signup_set.all()
    signups = signups.select_related('person')
    signups = signups.prefetch_related('job_categories').prefetch_related('job_categories_accepted')

    if format == 'screen':
        num_all_signups = signups.count()

    job_categories = event.jobcategory_set.all()
    personnel_classes = event.personnelclass_set.filter(app_label='labour')

    job_category_filters = Filter(request, "job_category").add_objects("job_categories__slug", job_categories)
    signups = job_category_filters.filter_queryset(signups)
    job_category_accepted_filters = Filter(request, "job_category_accepted").add_objects("job_categories_accepted__slug", job_categories)
    signups = job_category_accepted_filters.filter_queryset(signups)
    personnel_class_filters = Filter(request, "personnel_class").add_objects("personnel_classes__slug", personnel_classes)
    signups = personnel_class_filters.filter_queryset(signups)

    state_filter = SignupStateFilter(request, "state")
    signups = state_filter.filter_queryset(signups)

    sorter = Sorter(request, "sort")
    sorter.add("name", name=u'Sukunimi, Etunimi', definition=('person__surname', 'person__first_name'))
    sorter.add("newest", name=u'Uusin ensin', definition=('-created_at',))
    sorter.add("oldest", name=u'Vanhin ensin', definition=('created_at',))
    signups = sorter.order_queryset(signups)

    if request.method == 'POST':
        action = request.POST.get('action', None)
        if action == 'reject':
            Signup.mass_reject(signups)
        elif action == 'request_confirmation':
            Signup.mass_request_confirmation(signups)
        else:
            messages.error(request, u'Ei semmosta toimintoa oo.')

        return redirect('labour_admin_signups_view', event.slug)

    elif format == 'screen':
        num_would_mass_reject = signups.filter(**Signup.get_state_query_params('new')).count()
        num_would_mass_request_confirmation = signups.filter(**Signup.get_state_query_params('accepted')).count()

        mass_operations = OrderedDict([
            ('reject', MassOperation(
                'reject',
                'labour-admin-mass-reject-modal',
                u'Hylkää kaikki käsittelemättömät...',
                num_would_mass_reject
            )),
            ('request_confirmation', MassOperation(
                'request_confirmation',
                'labour-admin-mass-request-confirmation-modal',
                u'Vaadi vahvistusta kaikilta hyväksytyiltä...',
                num_would_mass_request_confirmation
            )),
        ])

        vars.update(
            export_formats=EXPORT_FORMATS,
            job_category_accepted_filters=job_category_accepted_filters,
            job_category_filters=job_category_filters,
            mass_operations=mass_operations,
            num_all_signups=num_all_signups,
            num_signups=signups.count(),
            personnel_class_filters=personnel_class_filters,
            signups=signups,
            sorter=sorter,
            state_filter=state_filter,
            css_to_show_filter_panel='in' if any(f.selected_slug != f.default for f in [
                job_category_filters,
                job_category_accepted_filters,
                personnel_class_filters,
                state_filter,
                sorter,
            ]) else '',
        )

        return render(request, 'labour_admin_signups_view.jade', vars)
    elif format in CSV_EXPORT_FORMATS:
        filename = "{event.slug}_signups_{timestamp}.{format}".format(
            event=event,
            timestamp=timezone.now().strftime('%Y%m%d%H%M%S'),
            format=format,
        )

        return csv_response(event, Signup, signups,
            dialect='xlsx',
            filename=filename,
            m2m_mode='separate_columns',
        )
    else:
        raise NotImplementedError(format)


@labour_admin_required
def labour_admin_roster_view(request, vars, event):
    # use javaScriptCase because this gets directly embedded in <script> as json
    tz = tzlocal()

    config = dict(
        event=event.as_dict(),
        workHours=[
            dict(startTime=hour.astimezone(tz).isoformat())
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
@require_safe
def labour_admin_mail_view(request, vars, event):
    from mailings.models import Message

    messages = Message.objects.filter(recipient__event=event, recipient__app_label='labour')

    vars.update(
        labour_messages=messages
    )

    return render(request, 'labour_admin_mail_view.jade', vars)


@labour_admin_required
@require_http_methods(['GET', 'HEAD', 'POST'])
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
def labour_admin_shirts_view(request, vars, event):
    # TODO half assumes and half doesn't that the shirt size field is named "shirt_size"
    meta = event.labour_event_meta
    SignupExtra = meta.signup_extra_model
    shirt_size_field = SignupExtra.get_shirt_size_field()
    shirt_type_field = SignupExtra.get_shirt_type_field()

    if shirt_size_field is None:
        messages.error(request, u'Tämä tapahtuma ei kerää paitakokoja.')
        return redirect('labour_admin_dashboard_view', event.slug)

    shirt_sizes = shirt_size_field.choices

    if shirt_type_field:
        shirt_types = shirt_type_field.choices
    else:
        shirt_types = [(u'default', u'Paita')]

    base_criteria = dict(
        signup__event=event,
        signup__is_active=True,
        signup__time_accepted__isnull=False,
    )

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
    assert SignupExtra.objects.filter(shirt_size__isnull=False, **base_criteria).count() == num_shirts, "Lost some shirts"

    vars.update(
        num_shirts=num_shirts,
        shirt_size_rows=shirt_size_rows,
        shirt_types=shirt_types,
        shirt_type_totals=shirt_type_totals,
    )

    return render(request, 'labour_admin_shirts_view.jade', vars)


@labour_supervisor_required
@require_http_methods(['GET', 'HEAD', 'POST'])
def labour_onboarding_view(request, event):
    if request.method in ('GET', 'HEAD'):
        signups = event.signup_set.filter(is_active=True)

        vars = dict(
            event=event,
            signups=signups,
        )

        return render(request, 'labour_admin_onboarding_view.jade', vars)
    elif request.method == 'POST':
        signup_id = request.POST['id']
        is_arrived = request.POST['arrived'] == 'true'

        signup = get_object_or_404(SignupOnboardingProxy, id=int(signup_id), is_active=True)
        signup.mark_arrived(is_arrived)

        return HttpResponse()
    else:
        raise NotImplementedError(request.method)


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

    onboarding_url = url('labour_onboarding_view', event.slug)
    onboarding_active = request.path == onboarding_url
    onboarding_text = _(u'Onboarding')

    menu_items = [
        (dashboard_active, dashboard_url, dashboard_text),
        (signups_active, signups_url, signups_text),
        (mail_active, mail_url, mail_text),
        (roster_active, roster_url, roster_text),
        (onboarding_active, onboarding_url, onboarding_text),
    ]

    if event.labour_event_meta.signup_extra_model.get_shirt_size_field():
        shirts_url = url('labour_admin_shirts_view', event.slug)
        shirts_active = request.path == shirts_url
        shirts_text = u'Paitakoot'

        menu_items.append((shirts_active, shirts_url, shirts_text))

    # unstable / development features
    if settings.DEBUG:
        menu_items.extend((
            (query_active, query_url, query_text),
        ))

    return menu_items
