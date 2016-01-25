# encoding: utf-8

from ...models import Programme


PROGRAMME_STATES_HOST_CAN_EDIT = ['idea', 'asked', 'offered', 'accepted']


class ProgrammeProfileProxy(Programme):
    """
    Contains extra methods for Programme used only by profile views.
    """

    @property
    def host_can_edit(self):
        return self.state in PROGRAMME_STATES_HOST_CAN_EDIT

    class Meta:
        proxy = True