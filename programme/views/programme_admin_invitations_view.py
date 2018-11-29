# encoding: utf-8

from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404, render
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods

from core.utils import initialize_form

from ..helpers import programme_admin_required
from ..models import Invitation
from ..forms import IdForm


@programme_admin_required
@require_http_methods(["GET", "HEAD", "POST"])
def programme_admin_invitations_view(request, vars, event):
    pending_invitations = Invitation.objects.filter(programme__category__event=event, state='valid')

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'cancel-invitation':
            form = initialize_form(IdForm, request)

            if form.is_valid():
                invitation_id = form.cleaned_data['id']
                invitation = get_object_or_404(Invitation, id=invitation_id, programme__category__event=event)
                invitation.state = 'revoked'
                invitation.save()

                invitation.programme.apply_state()

                messages.success(request, _('The invitation was cancelled.'))
                return redirect('programme_admin_invitations_view', event.slug)

        elif action == 'cancel-all-invitations':
            pending_invitations.update(state='revoked')
            messages.success(request, _('All pending invitations were cancelled.'))
            return redirect('programme_admin_invitations_view', event.slug)

        messages.error(request, _('Invalid request.'))

    vars.update(
        pending_invitations=pending_invitations
    )

    return render(request, 'programme_admin_invitations_view.pug', vars)
