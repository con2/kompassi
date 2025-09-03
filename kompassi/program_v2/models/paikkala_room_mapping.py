from django.db import models
from paikkala.models.rooms import Room as PaikkalaRoom

from kompassi.dimensions.models.dimension_value import DimensionValue


class PaikkalaRoomMapping(models.Model):
    room_dimension_value: models.OneToOneField[DimensionValue] = models.OneToOneField(
        DimensionValue,
        on_delete=models.CASCADE,
        related_name="paikkala_room_mapping",
        primary_key=True,
    )

    paikkala_room: models.OneToOneField[PaikkalaRoom] = models.OneToOneField(
        PaikkalaRoom,
        on_delete=models.CASCADE,
        related_name="kompassi_v2_room_mapping",
        unique=True,
    )
