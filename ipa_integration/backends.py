import logging

from django.conf import settings
from django.contrib.auth.models import User, Group
from django.db import transaction

from .ipa import IPASession


logger = logging.getLogger('kompassi')


def user_attrs_from_ipa_user_info(user_info):
    groups = set()
    groups.update(user_info['memberof_group'])
    groups.update(user_info['memberofindirect_group'])

    return dict(
        first_name=user_info['givenname'][0],
        last_name=user_info['sn'][0],
        is_active=settings.KOMPASSI_USERS_GROUP in groups,
        is_staff=settings.KOMPASSI_STAFF_GROUP in groups,
        is_superuser=settings.KOMPASSI_SUPERUSERS_GROUP in groups,
        groups=[Group.objects.get_or_create(name=group_name)[0] for group_name in groups],
    )


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

        user_info = user_info['result']['result']

        with transaction.atomic():
            user, created = User.objects.get_or_create(username=username)

            for key, value in user_attrs_from_ipa_user_info(user_info).iteritems():
                setattr(user, key, value)

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
