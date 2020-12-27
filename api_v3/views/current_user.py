from rest_framework.generics import RetrieveAPIView

from core.models import Person

from ..serializers import UserSerializer
from ..permissions import IsPerson


class CurrentUserView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = Person.objects.none()
    permission_classes = [IsPerson]

    def get_object(self):
        return self.request.user.person
