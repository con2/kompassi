from rest_framework import serializers

from core.models import Person


class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api_v3_current_user_view', lookup_field='slug')
    username = serializers.SerializerMethodField()

    @classmethod
    def get_username(self, person):
        return person.user.username

    class Meta:
        model = Person
        fields = ('username', 'email', 'first_name', 'surname', 'display_name')
