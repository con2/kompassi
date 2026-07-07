from django.test import TestCase

from kompassi.access.models import CBACEntry
from kompassi.core.models import Person
from kompassi.event_log_v2.models.entry import Entry
from kompassi.involvement.models.meta import InvolvementEventMeta

from .forms import PrivilegesForm
from .models import IntraEventMeta, TeamMember


class TeamMembersTestCase(TestCase):
    def setUp(self):
        self.meta, unused = IntraEventMeta.get_or_create_dummy()
        self.event = self.meta.event

    def test_team_group_membership(self):
        team_member, unused = TeamMember.get_or_create_dummy()
        team = team_member.team
        person = team_member.person
        group = team.group

        assert person.user.groups.filter(id=group.id).exists()

        team_member.delete()

        assert not person.user.groups.filter(id=group.id).exists()


class InvolvementPrivilegeTestCase(TestCase):
    def setUp(self):
        Entry.ensure_partitions()
        self.meta, _ = IntraEventMeta.get_or_create_dummy()
        self.event = self.meta.event
        self.involvement_meta = InvolvementEventMeta.ensure(self.event)
        self.person, _ = Person.get_or_create_dummy(superuser=False)
        self.user = self.person.user

    def _save_privileges(self, involvement_admin: bool):
        active_apps = self.meta.get_active_apps()
        assert "involvement" in active_apps
        cleaned_data = {app_label: (app_label == "involvement" and involvement_admin) for app_label in active_apps}
        PrivilegesForm._save(self.event, [(self.user, cleaned_data)])

    def _involvement_cbac_entries(self):
        return CBACEntry.objects.filter(
            user=self.user,
            claims__app="involvement",
            claims__organization=self.event.organization.slug,
        )

    def test_field_order_matches_active_apps(self):
        # The privileges template pairs column headers (get_active_apps() order) with
        # checkboxes (form field iteration order) positionally, so the two must agree.
        form = PrivilegesForm(event=self.event, user=self.user)
        assert [bound_field.name for bound_field in form] == self.meta.get_active_apps()

    def test_grant_and_revoke_involvement_privilege(self):
        admin_group = self.event.involvement_event_meta.admin_group

        assert not admin_group.user_set.filter(id=self.user.id).exists()
        assert not self._involvement_cbac_entries().exists()

        # grant
        self._save_privileges(involvement_admin=True)
        assert admin_group.user_set.filter(id=self.user.id).exists()
        assert self._involvement_cbac_entries().exists()

        # revoke
        self._save_privileges(involvement_admin=False)
        assert not admin_group.user_set.filter(id=self.user.id).exists()
        assert not self._involvement_cbac_entries().exists()
