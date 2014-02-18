# encoding: utf-8

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.views.decorators.http import require_http_methods

from .models import Event, Person
from .forms import PersonForm, RegistrationForm, PasswordForm, LoginForm
from .utils import initialize_form, get_next, next_redirect
from .helpers import person_required


def core_frontpage_view(request):
    t = now()

    vars = dict(
        settings=settings,
        past_events=Event.objects.filter(public=True, end_time__lte=t).order_by('-start_time'),
        current_events=Event.objects.filter(public=True, start_time__lte=t, end_time__gt=t).order_by('-start_time'),
        future_events=Event.objects.filter(public=True, start_time__gt=t).order_by('-start_time'),
    )

    return render(request, 'core_frontpage_view.jade', vars)


def core_event_view(request, event):
    event = get_object_or_404(Event, slug=event)

    vars = dict(
        event=event,
        settings=settings,
    )

    if event.labour_event_meta:
        from labour.views import labour_event_box_context
        vars.update(labour_event_box_context(request, event))

    if event.programme_event_meta:
        from programme.views import programme_event_box_context
        vars.update(programme_event_box_context(request, event))

    return render(request, 'core_event_view.jade', vars)


@require_http_methods(['GET','POST'])
def core_login_view(request):
    form = initialize_form(LoginForm, request)
    next = get_next(request, 'core_frontpage_view')

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, u'Olet nyt kirjautunut sisään.')
                return redirect(next)
            else:
                messages.error(request, u'Sisäänkirjautuminen epäonnistui.')
        else:
            messages.error(request, u'Ole hyvä ja korjaa virheelliset kentät.')

    vars = dict(
        form=form,
        next=next,
        login_page=True
    )

    return render(request, 'core_login_view.jade', vars)


@require_http_methods(['GET','POST'])
def core_registration_view(request):
    person_form = initialize_form(PersonForm, request, prefix='person')
    person_form.helper.form_tag = False
    registration_form = initialize_form(RegistrationForm, request, prefix='registration')
    next = get_next(request)

    if request.method == 'POST':
        if person_form.is_valid() and registration_form.is_valid():
            username = registration_form.cleaned_data['username']
            password = registration_form.cleaned_data['password']

            person = person_form.save(commit=False)
            user = User(
                username=username,
                is_active=True,
                is_staff=False,
                is_superuser=False,
            )

            if 'external_auth' not in settings.INSTALLED_APPS:
                user.set_password(password)

            user.save()

            person.user = user
            person.save()

            if 'external_auth' in settings.INSTALLED_APPS:
                from external_auth.utils import create_user
                create_user(user, password)

            user = authenticate(username=username, password=password)
            login(request, user)

            messages.success(request,
                u'Käyttäjätunnuksesi on luotu. Tervetuloa {{ site_name_illative }}!'
                .format(site_name_illative=settings.TURSKA_INSTALLATION_NAME_ILLATIVE)
            )
            return redirect(next)
        else:
            messages.error(request, u'Ole hyvä ja tarkista lomake.')

    vars = dict(
        next=next,
        person_form=person_form,
        registration_form=registration_form,
        login_page=True
    )

    return render(request, 'core_registration_view.jade', vars)


@person_required
@require_http_methods(['GET', 'POST'])
def core_profile_view(request):
    person = request.user.person
    form = initialize_form(PersonForm, request, instance=person, prefix='person')

    if request.method == 'POST':
        if form.is_valid():
            person = form.save()
            messages.success(request, u'Tiedot tallennettiin.')
        else:
            messages.error(request, u'Ole hyvä ja korjaa virheelliset kentät.')

    vars = dict(
        form=form
    )

    return render(request, 'core_profile_view.jade', vars)


@login_required
@require_http_methods(['GET', 'POST'])
def core_personify_view(request):
    try:
        person = request.user.person
        return redirect('core_profile_view')
    except Person.DoesNotExist:
        pass

    initial = dict(
        first_name=request.user.first_name,
        surname=request.user.last_name,
        email=request.user.email,
    )

    form = initialize_form(PersonForm, request, initial=initial, prefix='person')
    next = get_next(request)

    if request.method == 'POST':
        if form.is_valid():
            person = form.save(commit=False)
            person.user = request.user
            person.save()
            messages.success(request, u'Tiedot tallennettiin.')
            return redirect(next)
        else:
            messages.error(request, u'Ole hyvä ja korjaa virheelliset kentät.')
    else:
        messages.info(request, u'Tämän toiminnon käyttäminen edellyttää, että täytät yhteystietosi.')

    vars = dict(
        person_form=form,
        next=next
    )

    return render(request, 'core_personify_view.jade', vars)


@login_required
@require_http_methods(['GET', 'POST'])
def core_password_view(request):
    form = initialize_form(PasswordForm, request, the_request=request)

    if request.method == 'POST':
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']

            ldap_user = getattr(request.user, 'ldap_user', None)
            if ldap_user:
                from external_auth.utils import change_current_user_password
                from external_auth.ipa import IPAError

                try:
                    change_current_user_password(request,
                        old_password=old_password,
                        new_password=new_password,
                    )
                except IPAError, e:
                    # XXX need to tell the user if this is due to too simple pw
                    messages.error(request, u'Salasanan vaihto epäonnistui.')
                else:
                    messages.success(request, u'Salasanasi on vaihdettu.')
            else:
                request.user.set_password(new_password)
                request.user.save()
                messages.success(request, u'Salasanasi on vaihdettu.')
        else:
            messages.error(request, u'Ole hyvä ja korjaa virheelliset kentät.')

    vars = dict(
        form=form,
    )

    return render(request, 'core_password_view.jade', vars)


def core_profile_menu_items(request):
    items = []

    if not request.user.is_authenticated():
        return items

    profile_url = reverse('core_profile_view')
    profile_active = request.path == profile_url
    profile_text = u'Omat tiedot'

    items.append((profile_active, profile_url, profile_text))

    password_url = reverse('core_password_view')
    password_active = request.path == password_url
    password_text = u'Salasanan vaihto'

    items.append((password_active, password_url, password_text))

    if 'labour' in settings.INSTALLED_APPS:
        from labour.views import labour_profile_menu_items
        items.extend(labour_profile_menu_items(request))

    if 'programme' in settings.INSTALLED_APPS:
        from programme.views import programme_profile_menu_items
        items.extend(programme_profile_menu_items(request))

    return items