from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from kompassi.core.utils import initialize_form

from ..forms import JobCategoryForm
from ..helpers import labour_admin_required
from ..proxies.job_category.management import JobCategoryManagementProxy


@labour_admin_required
@require_http_methods(["GET", "HEAD", "POST"])
def admin_jobcategory_view(request, vars, event, job_category_slug=None):
    meta = event.labour_event_meta

    if job_category_slug is not None:
        # Edit existing
        job_category = get_object_or_404(JobCategoryManagementProxy, event=event, slug=job_category_slug)
    else:
        # Add new
        job_category = JobCategoryManagementProxy(event=event, app_label="labour")

    form = initialize_form(JobCategoryForm, request, instance=job_category, event=event)

    if request.method == "POST":
        action = request.POST.get("action")
        if action in ("save-return", "save-edit"):
            if form.is_valid():
                job_category = form.save()
                meta.create_groups_async()
                messages.success(request, _("The job category was saved."))

                if action == "save-return":
                    return redirect("labour:admin_jobcategories_view", event.slug)
                elif action == "save-edit":
                    return redirect("labour:admin_jobcategory_view", event.slug, job_category.slug)
                else:
                    raise NotImplementedError(action)
            else:
                messages.error(request, _("Please check the form."))
        elif action == "remove" and job_category.can_remove:
            job_category.delete()
            messages.success(request, _("The job category was removed."))
            return redirect("labour:admin_jobcategories_view", event.slug)
        else:
            messages.error(request, _("Invalid request."))

    vars.update(
        form=form,
        job_category=job_category,
    )

    return render(request, "labour_admin_jobcategory_view.pug", vars)
