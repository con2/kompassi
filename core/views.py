# encoding: utf-8

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.views.decorators.http import require_http_methods, require_GET

from .models import Event, Person, PasswordResetError, PasswordResetToken, EmailVerificationError, EmailVerificationToken
from .forms import PersonForm, RegistrationForm, PasswordForm, LoginForm, PasswordResetForm, PasswordResetRequestForm
from .utils import initialize_form, get_next, next_redirect, page_wizard_clear, page_wizard_vars, url
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


def core_event_view(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug)

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

    if event.tickets_event_meta:
        from tickets.views import tickets_event_box_context
        vars.update(tickets_event_box_context(request, event))

    return render(request, 'core_event_view.jade', vars)


def remind_email_verification_if_needed(request, next=None):
    try:
        person = request.user.person
    except Person.DoesNotExist:
        return

    if person.is_email_verified:
        return
    elif next and next.startswith('/profile/email/verify'): # XXX hardcoded url fragment
        return
    elif person.pending_email_verification:
        messages.warning(request,
            u'Muistathan vahvistaa sähköpostiosoitteesi! Sinulle on lähetetty vahvistusviesti '
            u'sähköpostiisi. Jos viesti ei ole tullut perille, voit myös <a href="{}">pyytää '
            u'uuden vahvistusviestin</a>.'.format(url('core_email_verification_request_view'))
        )
    else:
        messages.warning(request,
            u'Pyydämme kaikkia käyttäjiämme vahvistamaan sähköpostiosoitteensa. Jotkin '
            u'{settings.TURSKA_INSTALLATION_NAME_GENITIVE} toiminnot edellyttävät vahvistettua '
            u'sähköpostiosoitetta. Saat vahvistuslinkin sähköpostiisi '
            u'<a href="{request_page_url}">vahvistussivulta</a>.'.format(
                request_page_url=url('core_email_verification_request_view'),
                settings=settings
            )
        )


@require_http_methods(['GET','POST'])
def core_login_view(request):
    next = get_next(request, 'core_frontpage_view')
    form = initialize_form(LoginForm, request, initial=dict(next=next))

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                page_wizard_clear(request)
                messages.success(request, u'Olet nyt kirjautunut sisään.')
                remind_email_verification_if_needed(request, next)
                return redirect(next)
            else:
                messages.error(request, u'Sisäänkirjautuminen epäonnistui.')
        else:
            messages.error(request, u'Ole hyvä ja korjaa virheelliset kentät.')

    vars = page_wizard_vars(request)

    vars.update(
        form=form,
        login_page=True
    )

    return render(request, 'core_login_view.jade', vars)


@require_http_methods(['GET','POST'])
def core_registration_view(request):
    vars = page_wizard_vars(request)
    next = vars['next']

    if request.user.is_authenticated():
        return redirect(next)

    person_form = initialize_form(PersonForm, request, prefix='person')
    person_form.helper.form_tag = False
    registration_form = initialize_form(RegistrationForm, request, prefix='registration')

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
            person.setup_email_verification(request)

            if 'external_auth' in settings.INSTALLED_APPS:
                from external_auth.utils import create_user
                create_user(user, password)

            user = authenticate(username=username, password=password)
            login(request, user)

            messages.success(request,
                u'Käyttäjätunnuksesi on luotu. Tervetuloa {site_name_illative}!'
                .format(site_name_illative=settings.TURSKA_INSTALLATION_NAME_ILLATIVE)
            )
            return redirect(next)
        else:
            messages.error(request, u'Ole hyvä ja tarkista lomake.')

    vars.update(
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
    old_email = person.email

    form = initialize_form(PersonForm, request, instance=person, prefix='person')

    if request.method == 'POST':
        if form.is_valid():
            person = form.save()

            if form.cleaned_data['email'] != old_email:
                person.setup_email_verification(request)
                messages.info(request,
                    u'Tietosi on tallennettu. Koska muutit sähköpostiosoitettasi, sinun täytyy '
                    u'vahvistaa sähköpostiosoitteesi uudelleen. Tarkista postilaatikkosi ja '
                    u'noudata vahvistusviestissä olevia ohjeita.'
                )
            else:
                messages.success(request, u'Tietosi on tallennettu.')
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
    except Person.DoesNotExist:
        pass
    else:
        return redirect('core_profile_view')

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
            person.setup_email_verification(request)
            messages.success(request,
                u'Tietosi on tallennettu. Ole hyvä ja vahvista sähköpostiosoitteesi. Tarkista '
                u'postilaatikkosi ja noudata vahvistusviestissä olevia ohjeita.'
            )
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
                    # TODO need to tell the user if this is due to too simple pw
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

    try:
        person = request.user.person
    except Person.DoesNotExist:
        pass
    else:
        if not person.is_email_verified:
            email_verification_url = reverse('core_email_verification_request_view')
            email_verification_active = request.path == email_verification_url
            email_verification_text = u'Sähköpostiosoitteen vahvistaminen'
            items.append((email_verification_active, email_verification_url, email_verification_text))

    if 'labour' in settings.INSTALLED_APPS:
        from labour.views import labour_profile_menu_items
        items.extend(labour_profile_menu_items(request))

    if 'programme' in settings.INSTALLED_APPS:
        from programme.views import programme_profile_menu_items
        items.extend(programme_profile_menu_items(request))

    return items


EMAIL_VERIFICATION_ERROR_MESSAGES = dict(
    default=u'Sähköpostiosoitteen vahvistus epäonnistui. Tarkista koodi.',
    wrong_person=
        u'Ole hyvä ja kirjaudu ulos ja uudestaan sisään sillä käyttäjällä, jonka '
        u'sähköpostiosoitetta yrität vahvistaa, ja yritä sitten uudelleen.',
    code_not_valid=u'Tämä vahvistuslinkki on jo käytetty tai mitätöity.',
    email_changed=
        u'Sähköpostiosoitteesi on muuttunut sitten vahvistuslinkin lähetyksen. '
        u'Ole hyvä ja käytä uusinta saamaasi vahvistuslinkkiä.',
    already_verified=u'Sähköpostiosoitteesi on jo vahvistettu.',
)


@person_required
@require_GET
def core_email_verification_view(request, code):
    person = request.user.person

    try:
        person.verify_email(code)
    except EmailVerificationError, e:
        reason = e.args[0]
        error_message = EMAIL_VERIFICATION_ERROR_MESSAGES.get(reason,
            EMAIL_VERIFICATION_ERROR_MESSAGES['default']
        )
        messages.error(request, error_message)
    else:
        messages.success(request, u'Kiitos! Sähköpostiosoitteesi on nyt vahvistettu.')

    return redirect('core_frontpage_view')


@person_required
@require_http_methods(['GET', 'POST'])
def core_email_verification_request_view(request):
    person = request.user.person

    if person.is_email_verified:
        messages.error(request, u'Sähköpostiosoitteesi on jo vahvistettu.')
        return redirect('core_profile_view')

    if request.method == 'POST':
        person.setup_email_verification(request)
        messages.info(request,
            u'Sinulle lähetettiin uusi vahvistuslinkki. Ole hyvä ja tarkista sähköpostisi.'
        )

    vars = dict(
        code=person.pending_email_verification,
    )

    return render(request, 'core_email_verification_request_view.jade', vars)


@require_http_methods(['GET', 'POST'])
def core_password_reset_view(request, code):
    if request.user.is_authenticated():
        return redirect('core_password_view')

    form = initialize_form(PasswordResetForm, request)

    if request.method == 'POST':
        if form.is_valid():
            try:
                PasswordResetToken.reset_password(code, form.cleaned_data['new_password'])
            except PasswordResetError, e:
                messages.error(request,
                    u'Salasanan nollaus epäonnistui. Ole hyvä ja yritä uudestaan. Tarvittaessa voit '
                    u'ottaa yhteyttä osoitteeseen {settings.DEFAULT_FROM_EMAIL}.'
                    .format(settings=settings)
                )
                return redirect('core_frontpage_view')

            messages.success(request,
                u'Salasanasi on nyt vaihdettu. Voit nyt kirjautua sisään uudella salasanallasi.'
            )
            return redirect('core_login_view')
        else:
            messages.error(request, u'Ole hyvä ja korjaa lomakkeen virheet.')

    vars = dict(
        form=form,
        login_page=True,
    )

    return render(request, 'core_password_reset_view.jade', vars)


@require_http_methods(['GET', 'POST'])
def core_password_reset_request_view(request):
    if request.user.is_authenticated():
        return redirect('core_password_view')

    form = initialize_form(PasswordResetRequestForm, request)

    if request.method == 'POST':
        if form.is_valid():
            try:
                person = Person.objects.get(email=form.cleaned_data['email'])
            except Person.DoesNotExist:
                # Fail silently - do not give information about users

                pass
            else:
                person.setup_password_reset(request)

            messages.success(request,
                u'Ohjeet salasanan vaihtamiseksi on lähetetty antamaasi sähköpostiosoitteeseen.'
            )
        else:
            messages.error(request, u'Ole hyvä ja korjaa lomakkeen virheet.')

    vars = dict(
        form=form,
        login_page=True,
    )

    return render(request, 'core_password_reset_request_view.jade', vars)
