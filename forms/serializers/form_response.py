from rest_framework import serializers, relations
from rest_framework_nested.relations import NestedHyperlinkedIdentityField

from ..models import Form, FormResponse


class FormResponseSerializer(serializers.HyperlinkedModelSerializer):
    url = NestedHyperlinkedIdentityField(view_name='form-response-detail', lookup_field='id', parent_lookup_kwargs={
        'form_slug': 'form__slug',
    })
    form = relations.HyperlinkedRelatedField(view_name='form-detail', read_only=True, lookup_field='slug')

    def create(self, validated_data):
        form = Form.objects.get(slug=self.context['view'].kwargs['form_slug'])
        validated_data['form'] = form
        return super().create(validated_data)

    class Meta:
        fields = (
            'url',
            'form',
            'values',
            # 'created_by',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'created_at',
            'updated_at',
        )
        model = FormResponse
