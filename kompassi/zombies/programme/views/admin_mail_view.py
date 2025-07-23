from django.shortcuts import render
from django.views.decorators.http import require_safe

from ..helpers import programme_admin_required


@programme_admin_required
@require_safe
def admin_mail_view(request, vars, event):
    from kompassi.mailings.models import Message

    messages = Message.objects.filter(recipient__event=event, recipient__app_label="programme")

    vars.update(not_messages=messages)

    return render(request, "programme_admin_mail_view.pug", vars)
