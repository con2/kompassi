from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from ..forms import RemoveJobCategoryForm
from ..helpers import labour_admin_required
from ..proxies.job_category.management import JobCategoryManagementProxy


@labour_admin_required
@require_http_methods(["GET", "HEAD", "POST"])
def admin_jobcategories_view(request, vars, event):
    job_categories = JobCategoryManagementProxy.objects.filter(event=event, app_label="labour")

    if request.method == "POST":
        if "remove" in request.POST:
            remove_job_category_form = RemoveJobCategoryForm(request.POST)
            if remove_job_category_form.is_valid():
                job_category_id = remove_job_category_form.cleaned_data["remove"]
                job_category = get_object_or_404(JobCategoryManagementProxy, event=event, id=job_category_id)

                if job_category.can_remove:
                    job_category.delete()
                    messages.success(request, _("The job category was removed."))
                    return redirect("labour:admin_jobcategories_view", event.slug)

        messages.error(request, _("Invalid request."))
        return redirect("labour:admin_jobcategories_view", event.slug)

    vars.update(job_categories=job_categories)

    return render(request, "labour_admin_jobcategories_view.pug", vars)
