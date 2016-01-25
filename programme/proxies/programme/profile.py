# encoding: utf-8

from ...models import Programme


PROGRAMME_STATES_HOST_CAN_EDIT = ['idea', 'asked', 'offered', 'accepted']
PROGRAMME_STATES_REJECTED = ['rejected', 'cancelled']


class ProgrammeProfileProxy(Programme):
    """
    Contains extra methods for Programme used only by profile views.
    """

    @classmethod
    def _get_in_states(cls, person, states):
        return (
            cls.objects.filter(state__in=states, organizers=person)
                .order_by('category__event__start_time', 'start_time', 'title')
        )

    @classmethod
    def get_editable_programmes(cls, person):
        return cls._get_in_states(person, PROGRAMME_STATES_HOST_CAN_EDIT)

    @classmethod
    def get_rejected_programmes(cls, person):
        return cls._get_in_states(person, PROGRAMME_STATES_REJECTED)

    @classmethod
    def get_published_programmes(cls, person):
        return cls._get_in_states(person, ['published'])

    @property
    def host_can_edit(self):
        return self.state in PROGRAMME_STATES_HOST_CAN_EDIT

    class Meta:
        proxy = True