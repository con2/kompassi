from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoObjectPermissions

from ..models import Form, FormResponse
from ..serializers import FormSerializer, FormResponseSerializer


class FormViewSet(ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    lookup_field = "slug"
    permission_classes = (DjangoObjectPermissions,)


class FormResponseViewSet(ModelViewSet):
    serializer_class = FormResponseSerializer
    lookup_field = "id"
    permission_classes = (DjangoObjectPermissions,)

    def get_queryset(self):
        return FormResponse.objects.filter(form__slug=self.kwargs["form_slug"])
