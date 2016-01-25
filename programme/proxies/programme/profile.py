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

    @property
    def host_cannot_edit_explanation(self):
        assert not self.host_can_edit

        if self.state == 'published':
            return _(u'This programme has been published. You can no longer edit it yourself. '
                'If you need edits to be made, please contact the programme manager.')
        elif self.state == 'cancelled':
            return _(u'You have cancelled this programme.')
        elif self.state == 'rejected':
            return _(u'This programme has been rejected by the programme manager.')
        else:
            raise NotImplementedError(self.state)

    class Meta:
        proxy = True