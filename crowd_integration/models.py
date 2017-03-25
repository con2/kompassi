# encoding: utf-8



from collections import namedtuple


BaseJustEnoughUser = namedtuple('JustEnoughUser', 'username first_name last_name email')
class JustEnoughUser(BaseJustEnoughUser):
    """
        JustEnoughUser can be passed to most IPA functions instead of an actual User if one is not available at
        the time of the call of create_user.
    """
    pass