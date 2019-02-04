from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='event-detail', lookup_field='slug')

    class Meta:
        fields = (
            'url',
            'slug',
            'name',
            'start_time',
            'end_time',
            'headline',
            'homepage_url',
        )
        model = Event
