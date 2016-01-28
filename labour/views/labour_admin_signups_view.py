# encoding: utf-8

from collections import OrderedDict, namedtuple

from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from core.sort_and_filter import Sorter, Filter
from core.csv_export import CSV_EXPORT_FORMATS, EXPORT_FORMATS

from ..helpers import labour_admin_required
from ..filters import SignupStateFilter
from ..models import Signup
from ..proxies.signup.certificate import SignupCertificateProxy


HTML_TEMPLATES = dict(
    screen="labour_admin_signups_view.jade",
    html="labour_admin_work_certificate_print.jade",
)


MassOperationBase = namedtuple('MassOperation', 'name modal_id text num_candidates')
class MassOperation(MassOperationBase):
    @property
    def disabled_attr(self):
        return 'disabled' if not self.num_candidates else ''


@labour_admin_required
@require_http_methods(['GET', 'HEAD', 'POST'])
def labour_admin_signups_view(request, vars, event, format='screen'):
    SignupClass = SignupCertificateProxy if format == 'html' else Signup
    signups = SignupClass.objects.filter(event=event)
    signups = signups.select_related('person')
    signups = signups.prefetch_related('job_categories').prefetch_related('job_categories_accepted')

    if format in HTML_TEMPLATES:
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
            SignupClass.mass_reject(signups)
        elif action == 'request_confirmation':
            SignupClass.mass_request_confirmation(signups)
        else:
            messages.error(request, u'Ei semmosta toimintoa oo.')

        return redirect('labour_admin_signups_view', event.slug)

    elif format in HTML_TEMPLATES:
        num_would_mass_reject = signups.filter(**SignupClass.get_state_query_params('new')).count()
        num_would_mass_request_confirmation = signups.filter(**SignupClass.get_state_query_params('accepted')).count()

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
            now=now(),
        )

        html_template = HTML_TEMPLATES[format]

        return render(request, html_template, vars)
    elif format in CSV_EXPORT_FORMATS:
        filename = "{event.slug}_signups_{timestamp}.{format}".format(
            event=event,
            timestamp=timezone.now().strftime('%Y%m%d%H%M%S'),
            format=format,
        )

        return csv_response(event, SignupClass, signups,
            dialect='xlsx',
            filename=filename,
            m2m_mode='separate_columns',
        )
    else:
        raise NotImplementedError(format)