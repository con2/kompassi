# -- encoding: UTF-8 --

from core.sort_and_filter import Filter
from labour.models import SIGNUP_STATE_NAMES


class SignupStateFilter(Filter):
    # TODO: This should use the database instead of "software" filtering
    def add_state(self, state, name=None):
        """
        Add a state to the filter. Name defaults to the long name for the state.

        :param state: State mnemonic.
        :param name: Name, or None.
        :return: This object.
        """
        if state not in SIGNUP_STATE_NAMES:
            raise ValueError("Unknown state: %s" % state)
        if not name:
            name = SIGNUP_STATE_NAMES[state]
        self.add(state, name, (lambda obj: obj.state == state))
