from django.contrib import messages
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from core.utils import initialize_form

from ..forms import PrivilegesForm
from ..helpers import intra_admin_required
from ..models.intra_event_meta import APP_NAMES


@intra_admin_required
def intra_admin_privileges_view(request, vars, event):
    meta = event.intra_event_meta
    users = meta.organizer_group.user_set.all().order_by('last_name', 'first_name')

    privileges_forms = [
        initialize_form(PrivilegesForm, request, event=event, user=user, prefix=f'u{user.id}')
        for user in users
    ]

    if request.method == 'POST':
        if all(form.is_valid() for form in privileges_forms):
            for form in privileges_forms:
                form.save()
            messages.success(request, _('The privileges were updated.'))
        else:
            messages.error(request, _('Please check the form.'))

    vars.update(
        app_names=[APP_NAMES[app_label] for app_label in meta.get_active_apps()],
        privileges_forms=privileges_forms,
    )

    return render(request, 'intra_admin_privileges_view.pug', vars)
