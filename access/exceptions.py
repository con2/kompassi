from django.core.exceptions import PermissionDenied


class CBACPermissionDenied(PermissionDenied):
    def __init__(self, claims):
        super()
        self.claims = claims
