from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoObjectPermissions

from ..models import Form
from ..serializers import FormSerializer


class FormViewSet(ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    lookup_field = 'slug'
    permission_classes = (DjangoObjectPermissions,)
