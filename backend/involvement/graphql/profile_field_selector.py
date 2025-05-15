import graphene_pydantic

from ..models.profile_field_selector import ProfileFieldSelector


class ProfileFieldSelectorType(graphene_pydantic.PydanticObjectType):
    class Meta:
        model = ProfileFieldSelector
        fields = (
            "first_name",
            "last_name",
            "nick",
            "email",
            "phone_number",
            "discord_handle",
        )
