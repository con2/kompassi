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
    response = oauth2_session.get(settings.KOMPASSI_DESUPROFILE_API_URL)
    response.raise_for_status()
    return response.json()


class LoginView(View):
    """
    This view initiates the OAuth2 login flow when a user clicks the "Log in with Desuprofile" button on the login page.
    The user is redirected to Desusite to log in there.
    """

    def get(self, request):
        authorization_url, state = get_session(request).authorization_url(settings.KOMPASSI_DESUPROFILE_OAUTH2_AUTHORIZATION_URL)
        request.session['oauth_state'] = state
        request.session['oauth_next'] = request.GET.get('next', None)
        return redirect(authorization_url)


class CallbackView(View):
    """
    The user, having requested login via Desuprofile to Kompassi, has visited the Desusite and logged in there, and
    now they are redirected back to Kompassi with an authorization token. The token is exchanged into an access token
    and the access token is used to retrieve the Desuprofile information for the user.

    There are three possible paths we might take here:

    1. A Kompassi account with a linked Desuprofile already exists. This user account is logged in.

    2. No Kompassi account is linked to this Desuprofile, and no Kompassi account matches the Desuprofile by email address.
       A new Kompassi account is created and logged in.

    3. No Kompassi account is linked to this Desuprofile, but there is a Kompassi account that matches by email address.
       E-mail confirmation is requested before linking the accounts.
    """

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
            # Cases 2 and 3
            # No Desuprofile connection for this Desuprofile username yet.
            # Create new user or connect to existing one.
            return self.respond_with_new_connection(request, next_url, desuprofile)
        else:
            # Case 1
            return respond_with_connection(request, next_url, connection)

    def respond_with_new_connection(self, request, next_url, desuprofile):
        User = get_user_model()

        try:
            user = User.objects.get(email=desuprofile['email'])
        except User.DoesNotExist:
            # Case 3
            return self.respond_with_new_user(request, next_url, desuprofile)
        else:
            # Case 2
            return self.respond_with_existing_user(request, next_url, desuprofile, user)

    def respond_with_new_user(self, request, next_url, desuprofile):
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

        return respond_with_connection(request, next_url, connection)

    def respond_with_existing_user(self, request, next_url, desuprofile, user):
        code, created = ConfirmationCode.objects.get_or_create(
            person=user.person,
            state='valid',
            desuprofile_id=int(desuprofile['id']),
            next_url=next_url,
        )

        code.send(request)

        return redirect('desuprofile_integration_confirmation_required_view')


def respond_with_connection(request, next_url, connection):
    user = connection.user
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    return do_login(request, user, next=next_url)


class ConfirmationView(View):
    """
    This view is used when a user has requested login via Desuprofiili and there is already a Kompassi user account
    by the same email address. A confirmation code has been sent to the registered email address and the user visits
    this view to redeem the confirmation code and link the accounts.
    """

    def get(self, request, code):
        try:
            code = ConfirmationCode.objects.get(code=code, state='valid')
        except ConfirmationCode.DoesNotExist:
            messages.error(request, u'Vahvistuskoodi ei kelpaa.')
            return redirect('core_frontpage_view')

        code.mark_used()

        if Connection.objects.filter(user=code.person.user).exists():
            messages.error(request, u'Kompassi-tunnukseesi on jo liitetty Desuprofiili. Jos haluat vaihtaa '
                u'Kompassi-tunnukseesi liitettyä Desuprofiilia, ota yhteyttä ylläpitoon: {email}'.format(
                    email=settings.DEFAULT_FROM_EMAIL,
                )
            )
            return redirect('core_frontpage_view')

        connection = Connection(
            id=code.desuprofile_id,
            user=code.person.user,
        )
        connection.save()

        messages.success(request, u'Desuprofiilisi on liitetty Kompassi-tunnukseesi ja sinut on kirjattu sisään. Jatkossa voit kirjautua sisään Kompassiin käyttäen Desuprofiiliasi.')
        return respond_with_connection(request, code.next_url, connection)
