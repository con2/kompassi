from rest_framework import serializers

from ..models import Form


class FormSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='form-detail', lookup_field='slug')

    class Meta:
        fields = (
            'url',
            'slug',
            'title',
            'fields',
            'layout',
            'login_required',
            'active',
            'standalone',
        )
        model = Form
