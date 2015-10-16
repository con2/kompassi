from django.core.management.base import BaseCommand

from ...models import Signup, SIGNUP_STATE_NAMES


class Command(BaseCommand):
    """
    Outputs the labour state diagram in a format that can be processed by GraphViz `dot`.
    See example in `docs/labour_states.png`.
    """

    def handle(self, *opts, **args):
        print 'digraph foo {'
        for originating_state in SIGNUP_STATE_NAMES.keys():
            if originating_state == 'beyond_logic':
                continue

            signup = Signup()
            signup.state = originating_state
            for destination_state in signup.next_states:
                if destination_state == 'beyond_logic':
                    continue

                print "    {src} -> {dest};".format(src=originating_state, dest=destination_state)
            print
        print '}'