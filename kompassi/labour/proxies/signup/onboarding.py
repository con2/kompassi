from ...models import Signup

STATE_ARRIVED = "arrived"
STATE_NOT_ARRIVED = "finished"


class SignupOnboardingProxy(Signup):
    """
    Contains methods used for onboarding, ie. marking workers as having arrived in the event.

    Whether or not a worker has arrived is currently embedded in the Grand Order clusterfuck.
    That is to say, "is_arrived" is a state flag, and only certain combinations of state flags are allowed.
    We can currently enter the "arrived" state from multiple different states, but at the moment it implies
    certain other state flags (such as "shifts finished" and not "complained"). Marking someone arrived
    will now lose information about these, and we have no way of restoring them to the previous state,
    should the labour supervisor have made a mistake.

    For now, we accept that information about state flags is lost when entering the "arrived" state,
    and returning people to the non-arrived state places them in the "finished" state. May those affected
    have patience and forgiveness. Once the Grand Order is abolished, this will be revisited.
    """

    class Meta:
        proxy = True

    def mark_arrived(self, is_arrived):
        if not self.is_active:
            raise AssertionError("Will not mark an inactive Signup as arrived")

        if is_arrived:
            self.state = STATE_ARRIVED
        else:
            self.state = STATE_NOT_ARRIVED

        self.save()

        return self
