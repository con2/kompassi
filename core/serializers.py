from rest_framework import serializers

from core.utils import slugify, validate_slug

from .models import Event


class SlugDefaultor:
    def __init__(self, source_field="name"):
        self.source_field = source_field

    def set_context(self, field):
        self.source_value = getattr(field.parent.instance, seflf.source_field)

    def __call__(self):
        return slugify(self.source_value)


class EventSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="event-detail", lookup_field="slug")

    class Meta:
        fields = (
            "url",
            "slug",
            "name",
            "start_time",
            "end_time",
            "headline",
            "homepage_url",
        )
        read_only_fields = ("slug",)

        model = Event
