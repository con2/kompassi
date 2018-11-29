# encoding: utf-8

from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_http_methods, require_safe
from django.db.models import Count
from django.conf import settings

from core.utils import url, initialize_form

from .models import VoteCategory, Vote, Hotword, Nominee, SMSMessageIn
from .helpers import sms_admin_required


@sms_admin_required
@require_safe
def sms_admin_votes_view(request, vars, event):
    vars.update(
        hotwords=Hotword.objects.filter(assigned_event=event),
        categories=VoteCategory.objects.filter(hotword__assigned_event=event),
        nominees=Nominee.objects.filter(category__hotword__assigned_event=event).values('category','name','number').annotate(votes=Count('vote__vote__category')).order_by('-votes'),
        total_votes=Vote.objects.filter(category__hotword__assigned_event=event).values('category').annotate(votes=Count('vote')),
        number=settings.NEXMO_FROM
    )

    return render(request, 'sms_admin_votes_view.pug', vars)


@sms_admin_required
@require_safe
def sms_admin_received_view(request, vars, event):
    vars.update(
        received_messages=SMSMessageIn.objects.filter(SMSEventMeta__event=event),
    )
    return render(request, 'sms_admin_received_view.pug', vars)


def sms_admin_menu_items(request, event):
    votes_url = url('sms_admin_votes_view', event.slug)
    votes_active = request.path == votes_url
    votes_text = 'Äänestykset'

    received_url = url('sms_admin_received_view', event.slug)
    received_active = request.path == received_url
    received_text = 'Vastaanotetut viestit'

    return [
        (votes_active, votes_url, votes_text),
        (received_active, received_url, received_text),
    ]


def sms_event_box_context(request, event):
    is_sms_admin = False

    if request.user.is_authenticated:
        is_sms_admin = event.sms_event_meta.is_user_admin(request.user)

    return dict(
        is_sms_admin=is_sms_admin,
    )
