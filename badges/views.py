# encoding: utf-8

from django.shortcuts import render

from .models import Badge, Batch
from .helpers import badges_admin_required


BADGE_ORDER = ('template', 'person__surname', 'person__first_name')


@badges_admin_required
def badges_admin_index_view(request, vars, event, badge_filter=None):
    badge_criteria = dict(template__event=event)

    if badge_filter is not None:
        badge_criteria.update(template__slug=badge_filter)

    vars.update(
        badges=Badge.objects.filter(**badge_criteria).order_by(*BADGE_ORDER),
    )

    return render(request, 'badges_index_view', vars)


@badges_admin_required
def badges_admin_batches_view(request, vars, event):
    raise NotImplemented()


@badges_admin_required
def badges_admin_batch_view(request, vars, event, batch_id):
    raise NotImplemented()


def badges_admin_menu_items(request, event):
    index_url = reverse('badges_admin_index_view', event.slug)
    index_active = request.path == index_url
    index_text = u'Badget'

    batches_url = reverse('badges_admin_batches_view', event.slug)
    batches_active = request.path.startswith(batches_url)
    batches_text = u'Tulostuserät'

    lists_url = reverse('badges_admin_lists_view', event.slug)
    lists_active = request.path.startswith(lists_url)
    lists_text = u'Nimilistat'

    return [
        (index_active, index_url, index_text),
        (batches_active, batches_url, batches_text),
        (lists_url, lists_active, lists_text),
    ]
