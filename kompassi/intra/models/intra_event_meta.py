from collections import namedtuple

from django.db import models

from kompassi.core.models import EventMetaBase, Person
from kompassi.labour.models import Signup

from ..constants import SUPPORTED_APPS

UnassignedOrganizer = namedtuple("UnassignedOrganizer", "person signup")


class IntraEventMeta(EventMetaBase):
    organizer_group = models.ForeignKey(
        "auth.Group", on_delete=models.CASCADE, related_name="as_organizer_group_for_intra_event_meta"
    )

    is_organizer_list_public = models.BooleanField(
        help_text="If set, the organizer list (name and job title) can be accessed via the GraphQL API.",
        default=False,
    )

    use_cbac = True

    @classmethod
    def get_or_create_dummy(cls):
        from kompassi.core.models import Event

        event, unused = Event.get_or_create_dummy()
        admin_group, organizer_group = cls.get_or_create_groups(event, ["admins", "organizers"])
        return cls.objects.get_or_create(
            event=event,
            defaults=dict(
                admin_group=admin_group,
                organizer_group=organizer_group,
            ),
        )

    def is_user_organizer(self, user):
        return self.is_user_in_group(user, self.organizer_group)

    def is_user_allowed_to_access(self, user):
        return user.is_authenticated and (user.is_superuser or self.is_user_organizer(user) or self.is_user_admin(user))

    @property
    def unassigned_organizers(self):
        if not hasattr(self, "_unassigned_organizers"):
            self._unassigned_organizers = []
            for person in Person.objects.filter(
                user__groups=self.organizer_group,
            ).exclude(
                user__person__team_memberships__team__event_id=self.event.id,
            ):
                signup = Signup.objects.filter(event=self.event, person=person).first()
                if signup:
                    self._unassigned_organizers.append(UnassignedOrganizer(person=person, signup=signup))

        return self._unassigned_organizers

    def get_active_apps(self):
        return [app_label for app_label in SUPPORTED_APPS if self.event.get_app_event_meta(app_label)]
