# encoding: utf-8



from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect, render

from core.utils import initialize_form

from ..forms import ProgrammeAdminCreateForm
from ..helpers import programme_admin_required


@programme_admin_required
@require_http_methods(['GET', 'HEAD', 'POST'])
def programme_admin_create_view(request, vars, event):
    form = initialize_form(ProgrammeAdminCreateForm, request, event=event)

    if request.method == 'POST':
        if form.is_valid():
            programme = form.save(commit=False)
            programme.save()
            form.save_m2m()

            messages.success(request, _('The programme was created.'))
            return redirect('programme_admin_detail_view', event.slug, programme.pk)
        else:
            messages.error(request, _('Please check the form.'))

    vars.update(
        form=form,
    )

    return render(request, 'programme_admin_create_view.pug', vars)
