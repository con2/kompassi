# encoding: utf-8

from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from core.utils import url
from core.csv_export import csv_response

from .models import Badge, Batch, Template
from .helpers import badges_admin_required


BADGE_ORDER = ('template', 'person__surname', 'person__first_name')


@badges_admin_required
def badges_admin_index_view(request, vars, event, badge_filter=None):
    badge_criteria = dict(template__event=event)

    if badge_filter is not None:
        badge_criteria.update(template__slug=badge_filter)

    badge_filters = [
        (badge_filter == template.slug, template)
        for template in Template.objects.filter(event=event)
    ]

    badges = Badge.objects.filter(**badge_criteria).order_by(*BADGE_ORDER)

    if request.GET.get('format', None) == 'tsv':
        filename = "{event.slug}-badges-{badge_filter}{timestamp}".format(
            event=event,
            badge_filter="{badge_filter}-".format(badge_filter=badge_filter) if badge_filter is not None else '',
            timestamp=timezone.now().strftime('%Y%m%d%H%M%S'),
        )

        return csv_response(event, Badge, badges, filename=filename)
    else:
        vars.update(
            badges=badges,
            filters=badge_filters,
        )

        return render(request, 'badges_admin_index_view.jade', vars)


@badges_admin_required
def badges_admin_batches_view(request, vars, event):
    raise NotImplemented()


@badges_admin_required
def badges_admin_batch_view(request, vars, event, batch_id):
    raise NotImplemented()


@badges_admin_required
def badges_admin_export_view(request, vars, event, badge_filter=None, batch_id=None):
    raise NotImplemented()


def badges_admin_menu_items(request, event):
    batches_url = url('badges_admin_batches_view', event.slug)
    batches_active = request.path.startswith(batches_url)
    batches_text = u'Tulostuserät'

    index_url = url('badges_admin_index_view', event.slug)
    index_active = request.path.startswith(index_url) and not batches_active
    index_text = u'Badget'    

    return [
        (index_active, index_url, index_text),
        (batches_active, batches_url, batches_text),
    ]
