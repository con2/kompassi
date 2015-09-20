# encoding: utf-8

import json
from datetime import datetime

from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import redirect
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages

from requests_oauthlib import OAuth2Session

from core.models import Person
from core.views import do_login
from core.utils import create_temporary_password, get_next

from .models import Connection, ConfirmationCode


def get_session(request, **kwargs):
    return OAuth2Session(settings.KOMPASSI_DESUPROFILE_OAUTH2_CLIENT_ID,
        redirect_uri=request.build_absolute_uri(reverse('desuprofile_integration_oauth2_callback_view')),
        scope=settings.KOMPASSI_DESUPROFILE_OAUTH2_SCOPE, # XXX hardcoded scope
        **kwargs
    )


def get_desuprofile(oauth2_session):
    print vars(oauth2_session)
    print settings.KOMPASSI_DESUPROFILE_API_URL
    response = oauth2_session.get(settings.KOMPASSI_DESUPROFILE_API_URL)
    response.raise_for_status()
    return response.json()


class LoginView(View):
    def get(self, request):
        authorization_url, state = get_session(request).authorization_url(settings.KOMPASSI_DESUPROFILE_OAUTH2_AUTHORIZATION_URL)
        request.session['oauth_state'] = state
        request.session['oauth_next'] = request.GET.get('next', None)
        return redirect(authorization_url)


class CallbackView(View):
    def get(self, request):
        if 'oauth_state' not in request.session or 'oauth_next' not in request.session:
            return HttpResponse('OAuth2 callback accessed outside OAuth2 authorization flow', status=400)

        session = get_session(request, state=request.session['oauth_state'])
        token = session.fetch_token(settings.KOMPASSI_DESUPROFILE_OAUTH2_TOKEN_URL,
            client_secret=settings.KOMPASSI_DESUPROFILE_OAUTH2_CLIENT_SECRET,
            authorization_response=request.build_absolute_uri(),
        )

        next_url = request.session['oauth_next']

        del request.session['oauth_state']
        del request.session['oauth_next']

        desuprofile = get_desuprofile(session)

        try:
            connection = Connection.objects.get(id=int(desuprofile['id']))
        except Connection.DoesNotExist:
            # No Desuprofile connection for this Desuprofile username yet.
            # Create new user or connect to existing one.
            return self.respond_with_new_connection(request, desuprofile)
        else:
            return respond_with_connection(request, connection)

    def respond_with_new_connection(self, request, desuprofile):
        User = get_user_model()

        try:
            user = User.objects.get(email=desuprofile['email'])
        except User.DoesNotExist:
            return self.respond_with_new_user(request, desuprofile)
        else:
            return self.respond_with_existing_user(request, desuprofile, user)

    def respond_with_new_user(self, request, desuprofile):
        User = get_user_model()
        username = "desuprofile_{id}".format(id=desuprofile['id'])
        password = create_temporary_password()

        user = User(
            username=username,
            is_active=True,
            is_staff=False,
            is_superuser=False,
        )

        user.set_password(password)
        user.save()

        person = Person(
            first_name=desuprofile['first_name'],
            surname=desuprofile['last_name'],
            nick=desuprofile['nickname'],
            email=desuprofile['email'],
            phone=desuprofile['phone'],
            birth_date=datetime.strptime(desuprofile['birth_date'], '%Y-%m-%d').date() if desuprofile.get('birth_date', None) else None,
            notes=u'Luotu Desuprofiilista',
            user=user,
        )

        person.save()
        person.setup_email_verification(request)

        if 'external_auth' in settings.INSTALLED_APPS:
            from external_auth.utils import create_user
            create_user(user, password)

        connection = Connection(
            id=int(desuprofile['id']),
            user=user,
        )
        connection.save()

        messages.success(request, u'Sinulle on luotu Desuprofiiliisi liitetty Kompassi-tunnus. Tervetuloa Kompassiin!')

        return respond_with_connection(request, connection)

    def respond_with_existing_user(self, request, desuprofile, user):
        desuprofile_json = json.dumps(desuprofile)

        code, created = ConfirmationCode.objects.get_or_create(
            person=user.person,
            state='valid',
            defaults=dict(
                desuprofile_json=desuprofile_json,
            ),
        )

        if not created:
            code.desuprofile_json = desuprofile_json
            code.save()

        code.send(request)

        return redirect('desuprofile_integration_confirmation_required_view')


def respond_with_connection(request, connection):
    user = connection.user
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    next = get_next(request, 'core_frontpage_view')
    return do_login(request, user, next=next)


class ConfirmationView(View):
    def get(self, request, code):
        code = get_object_or_404(ConfirmationCode, code)

        try:
            connection = code.confirm(request)
        except ConfirmationError as e:
            messages.error(request, e.args[0])
            return respond_with_connection(connection)
        else:
            messages.success(request, u'Desuprofiilisi on liitetty Kompassi-tunnukseesi. Voit nyt kirjautua sisään Kompassiin käyttäen Desuprofiiliasi.')

            return respond_with_connection(request, connection)
