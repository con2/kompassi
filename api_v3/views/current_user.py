from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from core.models import Person

from ..serializers import UserSerializer


class IsPerson(IsAuthenticated):
    def has_permission(self, request, view):
        try:
            return super().has_permission(request, view) and request.user.person
        except Person.DoesNotExist:
            return False


class CurrentUserView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = Person.objects.none()
    permission_classes = [IsPerson]

    def get_object(self):
        return self.request.user.person
