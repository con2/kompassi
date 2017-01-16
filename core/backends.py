from django.contrib.auth.models import User


# Sentinel object
YES_PLEASE_ALLOW_PASSWORDLESS_LOGIN = object()


class PasswordlessLoginBackend(object):
    """
    Supports authentication without password for the impersonation feature.

    Pass a username and allow_passwordless_login=YES_PLEASE_ALLOW_PASSWORDLESS_LOGIN to authenticate() to invoke
    this backend.

    All authentication attempts that have a password are forwarded to the next backend.
    """

    def authenticate(self, username, password=None, allow_passwordless_login=None):
        if password is not None:
            return None

        if allow_passwordless_login is not YES_PLEASE_ALLOW_PASSWORDLESS_LOGIN:
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
