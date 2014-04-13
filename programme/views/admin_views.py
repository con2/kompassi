# encoding: utf-8

from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods, require_GET

from core.models import Person
from core.utils import initialize_form, initialize_form_set, url

from ..models import (
    Programme,
    ProgrammeEditToken,
    ProgrammeRole,
    Role,
)
from ..helpers import programme_admin_required
from ..forms import (
    ProgrammeAdminForm,
    ProgrammeExtraForm,
    ProgrammeForm,
    ProgrammePersonFormHelper,
    ProgrammePersonFormSet,
)


@programme_admin_required
def programme_admin_view(request, vars, event):
    programmes = Programme.objects.filter(category__event=event)

    vars.update(
        programmes=programmes
    )

    return render(request, 'programme_admin_view.jade', vars)


@programme_admin_required
@require_http_methods(['GET', 'POST'])
def programme_admin_detail_view(request, vars, event, programme_id=None):
    if programme_id:
        programme = get_object_or_404(Programme, category__event=event, pk=int(programme_id))
    else:
        programme = Programme()

    hosts = Person.objects.filter(programmerole__programme=programme)

    programme_person_form_set = initialize_form_set(ProgrammePersonFormSet, request,
        queryset=hosts,
        prefix='programme_person',
    )
    programme_person_form_helper = ProgrammePersonFormHelper()

    programme_form = initialize_form(ProgrammeForm, request,
        instance=programme,
        prefix='programme_basic',
    )
    programme_admin_form = initialize_form(ProgrammeAdminForm, request,
        instance=programme,
        prefix='programme_admin',
        event=event,
    )

    vars.update(
        programme=programme,
        programme_admin_form=programme_admin_form,
        programme_form=programme_form,
        programme_person_form_set=programme_person_form_set,
        programme_person_form_helper=programme_person_form_helper,
    )

    forms = [programme_form, programme_admin_form, programme_person_form_set]

    def determine_can_send_link():
        return programme.pk and any(p.email for p in programme.organizers.all())

    if programme.pk:
        programme_extra_form = initialize_form(ProgrammeExtraForm, request,
            instance=programme,
            prefix='programme_extra',
            self_service=False,
        )
        vars.update(
            programme_extra_form=programme_extra_form
        )

        forms.append(programme_extra_form)

    if request.method == 'POST':
        if 'save' in request.POST or 'save-sendlink' in request.POST:
            if all(form.is_valid() for form in forms):
                programme_form.save(commit=False)
                programme_admin_form.save(commit=False)

                if programme.pk:
                    programme_extra_form.save(commit=False)

                programme.save()

                hosts = programme_person_form_set.save()

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

                return redirect('programme_admin_detail_view', event.slug, programme.pk)
            else:
                messages.error(request, u'Ole hyvä ja tarkista lomake.')

        elif 'delete' in request.POST:
            programme.delete()
            messages.success(request, u'Ohjelmanumero poistettiin.')
            return redirect('programme_admin_view', event.slug)

        else:
            messages.error(request, u'Tunnistamaton pyyntö')

    vars.update(can_send_link=determine_can_send_link())

    return render(request, 'programme_admin_detail_view.jade', vars)


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


def programme_admin_menu_items(request, event):
    timetable_url = url('programme_admin_timetable_view', event.slug)
    timetable_active = request.path == timetable_url
    timetable_text = u'Ohjelmakartan esikatselu'

    index_url = url('programme_admin_view', event.slug)
    index_active = request.path.startswith(index_url) and not timetable_active # XXX
    index_text = u'Ohjelmaluettelo'

    return [
        (index_active, index_url, index_text),
        (timetable_active, timetable_url, timetable_text),
    ]
