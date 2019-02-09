from rest_framework import serializers

from core.models import Person


class UserSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    @classmethod
    def get_username(self, person):
        return person.user.username

    class Meta:
        model = Person
        fields = ('username', 'email', 'first_name', 'surname', 'display_name')
