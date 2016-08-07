# encoding: utf-8

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import EventMetaBase


class IntraEventMeta(EventMetaBase):
    organizer_group = models.ForeignKey('auth.Group', related_name='as_organizer_group_for_intra_event_meta')

    @classmethod
    def get_or_create_dummy(cls):
        from core.models import Event
        event, unused = Event.get_or_create_dummy()
        admin_group, organizer_group = cls.get_or_create_groups(event, ['admins', 'organizers'])
        return cls.objects.get_or_create(event=event, defaults=dict(
            admin_group=admin_group,
            organizer_group=organizer_group,
        ))

    def is_user_organizer(self, user):
        return self.is_user_in_group(user, self.organizer_group)

    def is_user_allowed_to_access(self, user):
        return user.is_authenticated() and (
            user.is_superuser or
            self.is_user_organizer(user) or
            self.is_user_admin(user)
        )
