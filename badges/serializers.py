from rest_framework import serializers

from .models import Badge


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'first_name',
            'nick',
            'surname',
            'job_title',
        )

        model = Badge
