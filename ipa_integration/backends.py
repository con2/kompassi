import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.db import transaction

from .ipa import IPASession, IPAError
from .utils import set_user_attrs_from_ipa_user_info


logger = logging.getLogger('kompassi')


class KompassiIPABackend(object):
    """
    Authenticates users against FreeIPA.
    """

    def authenticate(self, username, password):
        try:
            with IPASession(username, password) as session:
                user_info = session.get_user_info()
        except IPAError as e:
            return None

        with transaction.atomic():
            user, created = User.objects.get_or_create(username=username)

            set_user_attrs_from_ipa_user_info(user, user_info)
            user.save()

        if user.is_active:
            logger.info(u'Authenticated user %s from IPA', username)
            return user
        else:
            logger.warn(u'Inactive user %s tried to log in', username)
            return None


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesDotExist:
            return None
