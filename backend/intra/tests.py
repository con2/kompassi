from django.test import TestCase

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
