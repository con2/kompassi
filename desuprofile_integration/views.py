# encoding: utf-8

import json
import logging
from datetime import datetime

from django.db import transaction
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import redirect
from django.conf import settings
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from django.utils.timezone import now

from jsonschema import ValidationError as JSONSchemaValidationError
from requests_oauthlib import OAuth2Session

from core.forms import valid_username
from core.models import Person
from core.views import do_login
from core.utils import create_temporary_password, get_next

from .models import Connection, ConfirmationCode, Desuprofile


logger = logging.getLogger('kompassi')


def get_session(request, **kwargs):
    return OAuth2Session(settings.KOMPASSI_DESUPROFILE_OAUTH2_CLIENT_ID,
        redirect_uri=request.build_absolute_uri(reverse('desuprofile_integration_oauth2_callback_view')),
        scope=settings.KOMPASSI_DESUPROFILE_OAUTH2_SCOPE, # XXX hardcoded scope
        **kwargs
    )


def get_desuprofile(oauth2_session):
    response = oauth2_session.get(settings.KOMPASSI_DESUPROFILE_API_URL)
    response.raise_for_status()
    return Desuprofile.from_dict(response.json())


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

        try:
            desuprofile = get_desuprofile(session)
        except JSONSchemaValidationError as e:
            logging.exception('Desuprofile {username} failed validation'.format(username=e.instance.get('username', None)))
            messages.error(request, u'Etunimi, sukunimi ja vahvistettu sähköpostiosoite ovat Kompassin kannalta välttämättömiä '
                u'kenttiä Desuprofiilissa. Kirjaudu <a href="https://desucon.fi/desuprofiili" target="_blank">Desuprofiiliisi</a> '
                u'ja korjaa nämä kentät, ja yritä sitten uudelleen.')
            return redirect('core_login_view')

        try:
            connection = Connection.objects.get(id=int(desuprofile.id))
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
            user = User.objects.get(email=desuprofile.email)
        except User.DoesNotExist:
            # Case 3
            return self.respond_with_new_user(request, next_url, desuprofile)
        else:
            # Case 2
            return self.respond_with_existing_user(request, next_url, desuprofile, user)

    def respond_with_new_user(self, request, next_url, desuprofile):
        User = get_user_model()
        password = create_temporary_password()

        # Kompassi has stricter rules for username validation than Desusite
        username = desuprofile.username.lower()
        try:
            valid_username(username)
        except DjangoValidationError:
            username = None

        with transaction.atomic():
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                # Username is free
                pass
            else:
                # Username clash with an existing account, use safe username
                username = None

            if username is None:
                username = "desuprofile_{id}".format(id=desuprofile.id)

            user = User(
                username=username,
                is_active=True,
                is_staff=False,
                is_superuser=False,
            )

            user.set_password(password)
            user.save()

            person = Person(
                first_name=desuprofile.first_name,
                surname=desuprofile.last_name,
                nick=desuprofile.nickname,
                email=desuprofile.email,
                phone=desuprofile.phone,
                birth_date=datetime.strptime(desuprofile.birth_date, '%Y-%m-%d').date() if desuprofile.birth_date else None,
                notes=u'Luotu Desuprofiilista',
                user=user,
            )

            person.save()

            connection = Connection(
                id=int(desuprofile.id),
                user=user,
            )
            connection.save()

        person.setup_email_verification(request)

        if 'external_auth' in settings.INSTALLED_APPS:
            from external_auth.utils import create_user
            create_user(user, password)

        messages.success(request, u'Sinulle on luotu Desuprofiiliisi liitetty Kompassi-tunnus. Tervetuloa Kompassiin!')

        return respond_with_connection(request, next_url, connection)

    def respond_with_existing_user(self, request, next_url, desuprofile, user):
        code, created = ConfirmationCode.objects.get_or_create(
            person=user.person,
            state='valid',
            desuprofile_id=int(desuprofile.id),
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

        # We just effectively verified their email, so reflect that in the Person.
        if not code.person.is_email_verified:
            code.person.verify_email()

        messages.success(request, u'Desuprofiilisi on liitetty Kompassi-tunnukseesi ja sinut on kirjattu sisään. Jatkossa voit kirjautua sisään Kompassiin käyttäen Desuprofiiliasi.')
        return respond_with_connection(request, code.next_url, connection)
