from collections import OrderedDict, namedtuple

from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from kompassi.core.csv_export import CSV_EXPORT_FORMATS, EXPORT_FORMATS, csv_response
from kompassi.core.sort_and_filter import Filter, Sorter
from kompassi.event_log_v2.utils.emit import emit

from ..filters import SignupStateFilter
from ..helpers import labour_admin_required
from ..models import ArchivedSignup, Signup
from ..proxies.signup.certificate import SignupCertificateProxy

HTML_TEMPLATES = dict(
    screen="labour_admin_signups_view.pug",
    html="labour_admin_work_certificate_print.pug",
)


MassOperationBase = namedtuple("MassOperation", "name modal_id text num_candidates")


class MassOperation(MassOperationBase):
    @property
    def disabled_attr(self):
        return "disabled" if not self.num_candidates else ""


@labour_admin_required
@require_http_methods(["GET", "HEAD", "POST"])
def admin_signups_view(request, vars, event, format="screen"):
    meta = event.labour_event_meta
    SignupClass = SignupCertificateProxy if format == "html" else Signup
    SignupExtra = meta.signup_extra_model
    signups = SignupClass.objects.filter(event=event)
    signups = signups.select_related("person").select_related("event")
    signups = signups.prefetch_related("job_categories").prefetch_related("job_categories_accepted")

    archived_signups = ArchivedSignup.objects.filter(event=event)
    archive_mode = archived_signups.exists()

    if format in HTML_TEMPLATES:
        num_all_signups = signups.count()

    job_categories = event.jobcategory_set.all()
    personnel_classes = event.personnelclass_set.filter(app_label="labour")

    if archive_mode:
        signups = archived_signups
        messages.warning(
            request,
            _(
                "The applications for this event have been archived. Functionality is limited. "
                "Only people who worked at the event are displayed below. "
                "Note that as only a positive record is maintained, people who were reprimanded "
                "for their performance may also have been omitted."
            ),
        )

    all_filters = []

    job_category_accepted_filters = Filter(request, "job_category_accepted").add_objects(
        "job_categories_accepted__slug", job_categories
    )
    signups = job_category_accepted_filters.filter_queryset(signups)
    all_filters.append(job_category_accepted_filters)

    personnel_class_filters = Filter(request, "personnel_class").add_objects(
        "personnel_classes__slug", personnel_classes
    )
    signups = personnel_class_filters.filter_queryset(signups)
    all_filters.append(personnel_class_filters)

    if not archive_mode:
        job_category_filters = Filter(request, "job_category").add_objects("job_categories__slug", job_categories)
        signups = job_category_filters.filter_queryset(signups)
        all_filters.append(job_category_filters)

        state_filter = SignupStateFilter(request, "state")
        signups = state_filter.filter_queryset(signups)
        all_filters.append(state_filter)

    if SignupExtra and SignupExtra.get_field("night_work"):
        night_work_path = "{prefix}{app_label}_signup_extra__night_work".format(
            prefix="person__" if SignupExtra.schema_version >= 2 else "",
            app_label=SignupExtra._meta.app_label,
        )
        night_work_filter = Filter(request, "night_work").add_booleans(night_work_path)
        signups = night_work_filter.filter_queryset(signups)
        all_filters.append(night_work_filter)
    else:
        night_work_filter = None

    sorter = Sorter(request, "sort")
    sorter.add("name", name="Sukunimi, Etunimi", definition=("person__surname", "person__first_name"))
    all_filters.append(sorter)

    if not archive_mode:
        sorter.add("newest", name="Uusin ensin", definition=("-created_at",))
        sorter.add("oldest", name="Vanhin ensin", definition=("created_at",))

    signups = sorter.order_queryset(signups)

    if request.method == "POST" and not archive_mode:
        action = request.POST.get("action", None)
        if action == "reject":
            SignupClass.mass_reject(signups)
        elif action == "request_confirmation":
            SignupClass.mass_request_confirmation(signups)
        elif action == "send_shifts":
            SignupClass.mass_send_shifts(signups)
        else:
            messages.error(request, "Ei semmosta toimintoa oo.")

        return redirect("labour:admin_signups_view", event.slug)

    elif format in HTML_TEMPLATES:
        if archive_mode:
            num_would_mass_reject = 0
            num_would_mass_request_confirmation = 0
            num_would_send_shifts = 0
            mass_operations = OrderedDict()
        else:
            num_would_mass_reject = signups.filter(**SignupClass.get_state_query_params("new")).count()
            num_would_mass_request_confirmation = signups.filter(
                **SignupClass.get_state_query_params("accepted")
            ).count()
            num_would_send_shifts = SignupClass.filter_signups_for_mass_send_shifts(signups).count()
            mass_operations = OrderedDict(
                [
                    (
                        "reject",
                        MassOperation(
                            "reject",
                            "labour-admin-mass-reject-modal",
                            "Hylkää kaikki käsittelemättömät...",
                            num_would_mass_reject,
                        ),
                    ),
                    (
                        "request_confirmation",
                        MassOperation(
                            "request_confirmation",
                            "labour-admin-mass-request-confirmation-modal",
                            "Vaadi vahvistusta kaikilta hyväksytyiltä...",
                            num_would_mass_request_confirmation,
                        ),
                    ),
                    (
                        "send_shifts",
                        MassOperation(
                            "send_shifts",
                            "labour-admin-mass-send-shifts-modal",
                            "Lähetä vuorot kaikille vuoroja odottaville, joille ne on määritelty...",
                            num_would_send_shifts,
                        ),
                    ),
                ]
            )

        vars.update(
            archive_mode=archive_mode,
            export_formats=EXPORT_FORMATS,
            job_category_accepted_filters=job_category_accepted_filters,
            job_category_filters=job_category_filters if not archive_mode else None,
            mass_operations=mass_operations,
            night_work_filter=night_work_filter,
            num_all_signups=num_all_signups,
            num_signups=signups.count(),
            personnel_class_filters=personnel_class_filters,
            signups=signups,
            sorter=sorter,
            state_filter=state_filter if not archive_mode else None,
            css_to_show_filter_panel="in" if any(f.selected_slug != f.default for f in all_filters) else "",
            now=now(),
        )

        html_template = HTML_TEMPLATES[format]

        return render(request, html_template, vars)
    elif format in CSV_EXPORT_FORMATS:
        filename = f"{event.slug}_signups_{now().strftime('%Y%m%d%H%M%S')}.{format}"

        emit("core.person.exported", request=request)

        return csv_response(
            event,
            SignupClass,
            signups,
            dialect=CSV_EXPORT_FORMATS[format],
            filename=filename,
            m2m_mode="separate_columns",
        )
    else:
        raise NotImplementedError(format)
