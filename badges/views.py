# encoding: utf-8

from __future__ import print_function

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_http_methods, require_GET

from core.batches_view import batches_view
from core.utils import url, initialize_form
from core.csv_export import csv_response

from .forms import CreateBatchForm, BadgeForm, HiddenBadgeCrouchingForm
from .models import Badge, Batch, Template
from .helpers import badges_admin_required


BADGE_ORDER = ('template', 'person__surname', 'person__first_name')
CSV_EXPORT_FORMATS = dict(
    csv='excel',
    tsv='excel-tab',
)
BADGE_LIST_TEMPLATES = dict(
    screen='badges_admin_badges_view.jade',
    print='badges_admin_badges_print.jade',
)

@badges_admin_required
@require_GET
def badges_admin_dashboard_view(request, vars, event):
    meta = event.badges_event_meta

    vars.update(
        templates=Template.objects.filter(event=event),
        num_badges_total=meta.count_badges(),
        num_badges_printed=meta.count_printed_badges(),
        num_badges_waiting_in_batch=meta.count_badges_waiting_in_batch(),
        num_badges_awaiting_batch=meta.count_badges_awaiting_batch(),
    )

    return render(request, 'badges_admin_dashboard_view.jade', vars)

@badges_admin_required
@require_http_methods(['GET', 'POST'])
def badges_admin_badges_view(request, vars, event, template_slug=None):
    if request.method == 'POST':
        form = initialize_form(HiddenBadgeCrouchingForm, request)

        if form.is_valid():
            badge = get_object_or_404(Badge, pk=form.cleaned_data['badge_id'])

            if 'revoke-badge' in request.POST:
                badge.is_revoked = True
                badge.save()
                messages.success(request, u'Badge on mitätöity.')

            elif 'clear-revoked' in request.POST:
                badge.is_revoked = False
                badge.save()
                messages.success(request, u'Badge on palautettu.')

            elif 'mark-printed' in request.POST:
                badge.is_printed_separately = True
                badge.save()
                messages.success(request, u'Badge on merkitty erikseen tulostetuksi.')

            elif 'clear-printed' in request.POST:
                badge.is_printed_separately = False
                badge.save()
                messages.success(request, u'Badgesta on pyyhitty erikseen tulostettu -merkintä.')

            else:
                messages.error(request, u'Tuntematon pyyntö.')

            return redirect(request.path)

    else:
        badge_criteria = dict(template__event=event)
        active_filter = None

        if template_slug is not None:
            active_filter = get_object_or_404(Template, event=event, slug=template_slug)
            badge_criteria.update(template=active_filter)

        badges = Badge.objects.filter(**badge_criteria).order_by(*BADGE_ORDER)

        format = request.GET.get('format', 'screen')

        if format in CSV_EXPORT_FORMATS:
            filename = "{event.slug}-badges-{badge_filter}{timestamp}.{format}".format(
                event=event,
                badge_filter="{template_slug}-".format(template_slug=template_slug) if template_slug is not None else '',
                timestamp=timezone.now().strftime('%Y%m%d%H%M%S'),
                format=format,
            )

            return csv_response(event, Badge, badges, filename=filename, dialect=CSV_EXPORT_FORMATS[format])
        elif format in BADGE_LIST_TEMPLATES:
            page_template = BADGE_LIST_TEMPLATES[format]

            title = u"{event.name} &ndash; {qualifier}".format(
                event=event,
                qualifier=active_filter.name if active_filter else u'Nimilista',
            )

            badge_filters = [
                (template_slug == badge_template.slug, badge_template)
                for badge_template in Template.objects.filter(event=event)
            ]

            vars.update(
                active_filter=active_filter,
                badges=badges,
                filters=badge_filters,
                now=timezone.now(),
                title=title,
            )

            return render(request, page_template, vars)
        else:
            raise NotImplemented(format)


badges_admin_batches_view = badges_admin_required(batches_view(
    Batch=Batch,
    CreateBatchForm=CreateBatchForm,
    template='badges_admin_batches_view.jade',
))


@badges_admin_required
@require_GET
def badges_admin_export_view(request, vars, event, batch_id, format='csv'):
    if format not in CSV_EXPORT_FORMATS:
        raise NotImplemented(format)

    batch = get_object_or_404(Batch, pk=int(batch_id), event=event)
    badges = batch.badge_set.all()

    filename = "{event.slug}-badges-batch{batch.pk}.{format}".format(
        event=event,
        batch=batch,
        format=format,
    )

    return csv_response(event, Badge, badges, filename=filename, dialect=CSV_EXPORT_FORMATS[format])


@badges_admin_required
@require_http_methods(['GET', 'POST'])
def badges_admin_create_view(request, vars, event, template_slug=None):
    # XXX move this to core
    from programme.forms import ProgrammePersonForm

    initial = dict()

    if template_slug is not None:
        template = get_object_or_404(Template, event=event, slug=template_slug)
        initial.update(template=template)

    badge_form = initialize_form(BadgeForm, request, prefix='badge_type', event=event, initial=initial)
    person_form = initialize_form(ProgrammePersonForm, request, prefix='person')

    if request.method == 'POST':
        if badge_form.is_valid() and person_form.is_valid():
            person = person_form.save()
            badge = badge_form.save(commit=False)

            badge.person = person
            badge.save()

            messages.success(request, u'Henkilö on lisätty onnistuneesti.')
            return redirect('badges_admin_dashboard_view', event.slug)
        else:
            messages.error(request, u'Ole hyvä ja tarkista lomake.')

    vars.update(
        badge_form=badge_form,
        person_form=person_form,
    )

    return render(request, 'badges_admin_create_view.jade', vars)


def badges_admin_menu_items(request, event):
    dashboard_url = url('badges_admin_dashboard_view', event.slug)
    dashboard_active = request.path == dashboard_url
    dashboard_text = u'Kojelauta'

    batches_url = url('badges_admin_batches_view', event.slug)
    batches_active = request.path.startswith(batches_url)
    batches_text = u'Tulostuserät'

    badges_url = url('badges_admin_badges_view', event.slug)
    badges_active = request.path.startswith(badges_url)
    badges_text = u'Nimilistat'

    return [
        (dashboard_active, dashboard_url, dashboard_text),
        (badges_active, badges_url, badges_text),
        (batches_active, batches_url, batches_text),
    ]


def badges_event_box_context(request, event):
    is_badges_admin = False

    if request.user.is_authenticated():
        is_badges_admin = event.badges_event_meta.is_user_admin(request.user)

    return dict(
        is_badges_admin=is_badges_admin,
    )
