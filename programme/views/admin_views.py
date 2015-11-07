# encoding: utf-8

import logging
from pkg_resources import resource_string

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.views.decorators.http import require_http_methods, require_GET

from core.csv_export import csv_response, CSV_EXPORT_FORMATS, EXPORT_FORMATS, ExportFormat
from core.models import Person
from core.sort_and_filter import Filter, Sorter
from core.utils import initialize_form, initialize_form_set, url

from ..models import (
    Category,
    Programme,
    ProgrammeEditToken,
    ProgrammeRole,
    Role,
    Room,
    STATE_CHOICES,
)
from ..helpers import programme_admin_required, group_programmes_by_start_time
from ..forms import (
    AdminProgrammePersonFormSet,
    ProgrammeAdminForm,
    ProgrammeExtraForm,
    ProgrammeForm,
    ProgrammePersonFormHelper,
    SelfServiceProgrammePersonFormSet,
)


EXPORT_FORMATS = EXPORT_FORMATS + [
    ExportFormat(u'Tulostettava versio', 'html', 'html'),
]
logger = logging.getLogger('kompassi')


@programme_admin_required
def programme_admin_view(request, vars, event, format='screen'):
    programmes = Programme.objects.filter(category__event=event)

    categories = Category.objects.filter(event=event)
    category_filters = Filter(request, 'category').add_objects('category__slug', categories)
    programmes = category_filters.filter_queryset(programmes)

    rooms = Room.objects.filter(venue=event.venue)
    room_filters = Filter(request, 'room').add_objects('room__slug', rooms)
    programmes = room_filters.filter_queryset(programmes)

    state_filters = Filter(request, 'state').add_choices('state', STATE_CHOICES)
    state_filters.filter_queryset(programmes)
    programmes = state_filters.filter_queryset(programmes)

    if format != 'html':
        sorter = Sorter(request, 'sort')
        sorter.add('title', name='Otsikko', definition=('title',))
        sorter.add('start_time', name='Alkuaika', definition=('start_time','room'))
        sorter.add('room', name='Sali', definition=('room','start_time'))
        programmes = sorter.order_queryset(programmes)

    if format == 'screen':
        vars.update(
            category_filters=category_filters,
            export_formats=EXPORT_FORMATS,
            programmes=programmes,
            room_filters=room_filters,
            sorter=sorter,
            state_filters=state_filters,
        )

        return render(request, 'programme_admin_view.jade', vars)
    elif format in CSV_EXPORT_FORMATS:
        filename = "{event.slug}_programmes_{timestamp}.xlsx".format(
            event=event,
            timestamp=timezone.now().strftime('%Y%m%d%H%M%S'),
        )

        return csv_response(event, Programme, programmes,
            m2m_mode='comma_separated',
            dialect='xlsx',
            filename=filename,
        )
    elif format == 'html':
        title = u"{event_name}: Ohjelma".format(event_name=event.name)

        if room_filters.selected_slug != None:
            room = Room.objects.get(slug=room_filters.selected_slug)
            title += u' – {room.name}'.format(room=room)

        if state_filters.selected_slug != None:
            state_name = next(name for (slug, name) in STATE_CHOICES if slug == state_filters.selected_slug)
            title += u' ({state_name})'.format(state_name=state_name)

        programmes_by_start_time = group_programmes_by_start_time(programmes)

        vars.update(
            title=title,
            now=timezone.now(),
            programmes=programmes,
            programmes_by_start_time=programmes_by_start_time,
        )

        return render(request, 'programme_admin_print_view.jade', vars)
    else:
        raise NotImplementedError(format)


@programme_admin_required
@require_http_methods(['GET', 'POST'])
def programme_admin_detail_view(request, vars, event, programme_id=None):
    if programme_id:
        programme = get_object_or_404(Programme, category__event=event, pk=int(programme_id))
    else:
        programme = Programme()

    vars.update(overlapping_programmes=programme.get_overlapping_programmes())

    return actual_detail_view(request, vars, event, programme,
        redirect_success=lambda ev, prog: redirect('programme_admin_detail_view', ev.slug, prog.pk),
        self_service=False,
        template='programme_admin_detail_view.jade',
    )


def actual_detail_view(request, vars, event, programme, template, self_service, redirect_success):
    hosts = Person.objects.filter(programmerole__programme=programme)

    if self_service:
        PersonFormSetClass = SelfServiceProgrammePersonFormSet
    else:
        PersonFormSetClass = AdminProgrammePersonFormSet

    programme_person_form_set = initialize_form_set(PersonFormSetClass, request,
        queryset=hosts,
        prefix='programme_person',
    )
    programme_person_form_helper = ProgrammePersonFormHelper()

    programme_form = initialize_form(ProgrammeForm, request,
        instance=programme,
        prefix='programme_basic',
        self_service=self_service,
    )

    forms = [programme_form, programme_person_form_set]

    if not self_service:
        programme_admin_form = initialize_form(ProgrammeAdminForm, request,
            instance=programme,
            prefix='programme_admin',
            event=event,
        )

        forms.append(programme_admin_form)

        vars.update(programme_admin_form=programme_admin_form)

    vars.update(
        programme=programme,
        programme_form=programme_form,
        programme_person_form_set=programme_person_form_set,
        programme_person_form_helper=programme_person_form_helper,
        self_service=self_service,
    )

    def determine_can_send_link():
        return not self_service and programme.pk and any(p.email for p in programme.organizers.all())

    if programme.pk:
        programme_extra_form = initialize_form(ProgrammeExtraForm, request,
            instance=programme,
            prefix='programme_extra',
            self_service=self_service,
        )
        vars.update(
            programme_extra_form=programme_extra_form
        )

        forms.append(programme_extra_form)
    else:
        programme_extra_form = None

    if request.method == 'POST':
        if 'save' in request.POST or 'save-sendlink' in request.POST:
            if all(form.is_valid() for form in forms):
                programme_form.save()

                if programme_extra_form:
                    programme_extra_form.save()

                if not self_service:
                    programme_admin_form.save()

                hosts = programme_person_form_set.save(commit=False)

                for person in hosts:
                    if person.pk and not ProgrammeRole.objects.filter(
                        programme=programme,
                        person=person,
                    ).exists():
                        # XXX better reporting
                        raise RuntimeError('Manipulation of form set id fields detected')

                    person.save()

                # XXX
                role = Role.objects.get(is_default=True)

                for person in hosts:
                    ProgrammeRole.objects.get_or_create(
                        programme=programme,
                        person=person,
                        defaults=dict(
                            role=role,
                        ),
                    )

                messages.success(request, u'Ohjelmanumeron tiedot tallennettiin.')

                if 'save-sendlink' in request.POST and determine_can_send_link():
                    programme.send_edit_codes(request)
                    messages.success(request, u'Linkki ohjelmanumeron tietojen päivityksiin lähetettiin ohjelmanjärjestäjille.')

                return redirect_success(event, programme)
            else:
                messages.error(request, u'Ole hyvä ja tarkista lomake.')

        elif not self_service and 'delete' in request.POST:
            programme.delete()
            messages.success(request, u'Ohjelmanumero poistettiin.')
            return redirect('programme_admin_view', event.slug)

        else:
            messages.error(request, u'Tunnistamaton pyyntö')

    vars.update(can_send_link=determine_can_send_link())

    return render(request, template, vars)


@programme_admin_required
@require_GET
def programme_admin_timetable_view(request, vars, event):
    from .public_views import actual_timetable_view

    return actual_timetable_view(
        request,
        event,
        internal_programmes=True,
        template='programme_admin_timetable_view.jade',
        vars=vars,
    )


@programme_admin_required
@require_GET
def programme_admin_special_view(request, vars, event):
    from .public_views import actual_special_view

    return actual_special_view(
        request,
        event,
        template='programme_admin_special_view.jade',
        vars=vars,
    )


def programme_admin_menu_items(request, event):
    timetable_url = url('programme_admin_timetable_view', event.slug)
    timetable_active = request.path == timetable_url
    timetable_text = u'Ohjelmakartan esikatselu'

    special_url = url('programme_admin_special_view', event.slug)
    special_active = request.path == special_url
    special_text = u'Ohjelmakartan ulkopuolisten esikatselu'

    index_url = url('programme_admin_view', event.slug)
    index_active = request.path.startswith(index_url) and not any((
        timetable_active,
        special_active,
    ))
    index_text = u'Ohjelmaluettelo'


    return [
        (index_active, index_url, index_text),
        (timetable_active, timetable_url, timetable_text),
        (special_active, special_url, special_text),
    ]


@programme_admin_required
def programme_admin_email_list_view(request, vars, event):
    addresses = Person.objects.filter(programme__category__event=event).order_by('email').values_list('email', flat=True).distinct()

    return HttpResponse("\n".join(addr for addr in addresses if addr), content_type='text/plain')
