from django.contrib.auth.models import User


class KompassiImpersonationBackend(object):
    """
    Supports authentication without password for the impersonation feature. All authentication 
    attempts that have a password are forwarded to the next backend.
    """

    def authenticate(self, username, password=None):
        if password is not None:
            return None

        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesDotExist:
            return None
