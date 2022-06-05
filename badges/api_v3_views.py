from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoObjectPermissions


from .models import Badge
from .serializers import BadgeSerializer


class BadgeViewSet(ModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    lookup_field = "id"
    permission_classes = (DjangoObjectPermissions,)
