# encoding: utf-8

from __future__ import print_function


from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods, require_safe

from core.batches_view import batches_view
from core.utils import url, initialize_form, groupby_strict
from core.csv_export import csv_response, CSV_EXPORT_FORMATS
from labour.models import PersonnelClass

from ..forms import CreateBatchForm, BadgeForm, HiddenBadgeCrouchingForm
from ..models import Badge, Batch, CountBadgesMixin
from ..helpers import badges_admin_required


# TODO use a generic proxy or have PersonnelClass inherit CountBadgesMixin directly
class PersonnelClassProxy(CountBadgesMixin):
    def __init__(self, target):
        self.target = target

    @property
    def badge_set(self):
        return self.target.badge_set

    @property
    def name(self):
        return self.target.name

    @property
    def slug(self):
        return self.target.slug


@badges_admin_required
@require_safe
def badges_admin_dashboard_view(request, vars, event):
    meta = event.badges_event_meta

    vars.update(
        personnel_classes=[
            PersonnelClassProxy(personnel_class)
            for personnel_class in PersonnelClass.objects.filter(event=event)
        ],
        num_badges_total=meta.count_badges(),
        num_badges_printed=meta.count_printed_badges(),
        num_badges_waiting_in_batch=meta.count_badges_waiting_in_batch(),
        num_badges_awaiting_batch=meta.count_badges_awaiting_batch(),
        num_badges_revoked=meta.count_revoked_badges(),
    )

    return render(request, 'badges_admin_dashboard_view.jade', vars)


badges_admin_batches_view = badges_admin_required(batches_view(
    Batch=Batch,
    CreateBatchForm=CreateBatchForm,
    template='badges_admin_batches_view.jade',
))


@badges_admin_required
@require_safe
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
