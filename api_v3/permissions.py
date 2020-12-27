from rest_framework.permissions import IsAuthenticated, BasePermission

from access.cbac import get_default_claims
from access.models import CBACEntry
from core.models import Person


class IsPerson(IsAuthenticated):
    def has_permission(self, request, view):
        try:
            return super().has_permission(request, view) and request.user.person
        except Person.DoesNotExist:
            return False


class CBACPermissions(BasePermission):
    def has_permission(self, request, view):
        claims = get_default_claims(request)
        return CBACEntry.is_allowed(request.user, claims)
