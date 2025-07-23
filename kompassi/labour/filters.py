from kompassi.core.sort_and_filter import Filter

from .models import Signup
from .models.constants import SIGNUP_STATE_NAMES


class SignupStateFilter(Filter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for state_slug in SIGNUP_STATE_NAMES:
            if state_slug != "archived":
                self._add_state(state_slug)

    def _add_state(self, state):
        """
        Add a state to the filter. Name defaults to the long name for the state.

        :param state: State mnemonic.
        :param name: Name, or None.
        :return: This object.
        """
        self.add(state, SIGNUP_STATE_NAMES[state], Signup.get_state_query_params(state))
