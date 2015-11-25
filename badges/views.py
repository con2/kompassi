# encoding: utf-8

from __future__ import print_function


from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_http_methods, require_safe

from core.batches_view import batches_view
from core.utils import url, initialize_form, groupby_strict
from core.csv_export import csv_response, CSV_EXPORT_FORMATS
from labour.models import PersonnelClass

from .forms import CreateBatchForm, BadgeForm, HiddenBadgeCrouchingForm
from .models import Badge, Batch, CountBadgesMixin
from .helpers import badges_admin_required


BADGE_ORDER = ('personnel_class', 'person__surname', 'person__first_name')
BADGE_LIST_TEMPLATES = dict(
    screen=dict(
        normal='badges_admin_badges_view.jade',
        yoink='badges_admin_badges_view.jade',
    ),
    print=dict(
        normal='badges_admin_badges_print.jade',
        yoink='badges_admin_badges_print_yoink.jade',
    ),
)


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


class BadgesToYoinkFakePersonnelClass(object):
    name = u'Yoinkkauslista'
    slug = u'yoink'
badges_to_yoink_fake_personnel_class = BadgesToYoinkFakePersonnelClass()


@badges_admin_required
@require_http_methods(['GET', 'HEAD', 'POST'])
def badges_admin_badges_view(request, vars, event, personnel_class_slug=None):
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
        format = request.GET.get('format', 'screen')
        badge_criteria = dict(personnel_class__event=event)
        active_filter = None
        viewing_yoink_list = False
        template_subtype = 'normal'

        if personnel_class_slug is not None:
            if personnel_class_slug == 'yoink':
                viewing_yoink_list = True
                active_filter = badges_to_yoink_fake_personnel_class
                badge_criteria.update(batch__isnull=False, revoked_at__isnull=False)
                template_subtype = 'yoink'
            else:
                active_filter = get_object_or_404(PersonnelClass, event=event, slug=personnel_class_slug)
                badge_criteria.update(personnel_class=active_filter)

        # Non-yoink paper lists only show non-revoked badges.
        # Yoink list only shows revoked badges.
        if format != 'screen' and personnel_class_slug != 'yoink':
            badge_criteria.update(revoked_at__isnull=True)

        badges = Badge.objects.filter(**badge_criteria).order_by(*BADGE_ORDER)

        if format in CSV_EXPORT_FORMATS:
            filename = "{event.slug}-badges-{badge_filter}{timestamp}.{format}".format(
                event=event,
                badge_filter="{personnel_class_slug}-".format(personnel_class_slug=personnel_class_slug) if personnel_class_slug is not None else '',
                timestamp=timezone.now().strftime('%Y%m%d%H%M%S'),
                format=format,
            )

            return csv_response(event, Badge, badges, filename=filename, dialect=CSV_EXPORT_FORMATS[format])
        elif format in BADGE_LIST_TEMPLATES:
            page_template = BADGE_LIST_TEMPLATES[format][template_subtype]

            title = u"{event.name} &ndash; {qualifier}".format(
                event=event,
                qualifier=active_filter.name if active_filter else u'Nimilista',
            )

            filters = [
                (personnel_class_slug == personnel_class.slug, personnel_class)
                for personnel_class in PersonnelClass.objects.filter(event=event)
            ]

            filters.append(
                (viewing_yoink_list, badges_to_yoink_fake_personnel_class)
            )

            vars.update(
                active_filter=active_filter,
                filters=filters,
                now=timezone.now(),
                title=title,
                should_display_personnel_class=not active_filter or personnel_class_slug == 'yoink',
            )

            if personnel_class_slug == 'yoink' and format == 'print':
                badges_by_personnel_class = groupby_strict(badges, lambda badge: badge.personnel_class)

                vars.update(badges_by_personnel_class=badges_by_personnel_class)
            else:
                vars.update(badges=badges)

            return render(request, page_template, vars)
        else:
            raise NotImplementedError(format)


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


@badges_admin_required
@require_http_methods(['GET', 'HEAD', 'POST'])
def badges_admin_create_view(request, vars, event, personnel_class_slug=None):
    # XXX move this to core
    from programme.forms import ProgrammePersonForm

    initial = dict()

    if personnel_class_slug is not None:
        personnel_class = get_object_or_404(PersonnelClass, event=event, slug=personnel_class_slug)
        initial.update(personnel_class=personnel_class)

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
