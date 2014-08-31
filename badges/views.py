# encoding: utf-8

from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from core.batches_view import batches_view
from core.utils import url
from core.csv_export import csv_response

from .forms import CreateBadgeBatchForm
from .models import Badge, Batch, Template
from .helpers import badges_admin_required


BADGE_ORDER = ('template', 'person__surname', 'person__first_name')
CSV_EXPORT_FORMATS = dict(
    csv='excel',
    tsv='excel-tab',
)

@badges_admin_required
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
def badges_admin_badges_view(request, vars, event, badge_filter=None):
    badge_criteria = dict(template__event=event)

    if badge_filter is not None:
        badge_criteria.update(template__slug=badge_filter)

    badge_filters = [
        (badge_filter == template.slug, template)
        for template in Template.objects.filter(event=event)
    ]

    badges = Badge.objects.filter(**badge_criteria).order_by(*BADGE_ORDER)

    format = request.GET.get('format', None)

    if format in CSV_EXPORT_FORMATS:
        filename = "{event.slug}-badges-{badge_filter}{timestamp}.{format}".format(
            event=event,
            badge_filter="{badge_filter}-".format(badge_filter=badge_filter) if badge_filter is not None else '',
            timestamp=timezone.now().strftime('%Y%m%d%H%M%S'),
            format=format,
        )

        return csv_response(event, Badge, badges, filename=filename, dialect=CSV_EXPORT_FORMATS[format])
    else:
        vars.update(
            badges=badges,
            filters=badge_filters,
        )

        return render(request, 'badges_admin_badges_view.jade', vars)


badges_admin_batches_view = badges_admin_required(batches_view(
    Batch=Batch,
    CreateBatchForm=CreateBadgeBatchForm,
    template='badges_admin_batches_view.jade',
))


@badges_admin_required
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

def badges_admin_menu_items(request, event):
    dashboard_url = url('badges_admin_dashboard_view', event.slug)
    dashboard_active = request.path == dashboard_url
    dashboard_text = u'Kojelauta'

    batches_url = url('badges_admin_batches_view', event.slug)
    batches_active = request.path.startswith(batches_url)
    batches_text = u'Tulostuserät'

    badges_url = url('badges_admin_badges_view', event.slug)
    badges_active = request.path.startswith(badges_url)
    badges_text = u'Badget'

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
