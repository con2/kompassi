from django import forms
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from kompassi.core.utils import horizontal_form_helper

from ..models import Room, View, ViewRoom
from ..models.room import ROOM_NAME_MAX_LENGTH


class ViewRoomIdForm(forms.Form):
    view_room_id = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop("event")
        super().__init__(*args, **kwargs)

    def get_view_room(self):
        return get_object_or_404(
            ViewRoom,
            id=self.cleaned_data["view_room_id"],
            room__event=self.event,
            view__event=self.event,
        )


class MoveViewRoomForm(ViewRoomIdForm):
    direction = forms.ChoiceField(choices=[("left", _("Left")), ("right", _("Right"))])

    def save(self):
        view_room = self.get_view_room()
        view_room.move(view_room.view.view_rooms.all(), self.cleaned_data["direction"])


class RemoveViewRoomForm(ViewRoomIdForm):
    def save(self):
        view_room = self.get_view_room()
        view_room.delete()


class ViewIdForm(forms.Form):
    view_id = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop("event")
        super().__init__(*args, **kwargs)

    def get_view(self):
        return get_object_or_404(View, id=self.cleaned_data["view_id"], event=self.event)


class MoveViewForm(ViewIdForm):
    direction = forms.ChoiceField(choices=[("up", _("Up")), ("down", _("Down"))])

    def save(self):
        view = self.get_view()
        view.move(self.event.views.all(), self.cleaned_data["direction"])


class DeleteViewForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop("instance")
        super().__init__(*args, **kwargs)

    def save(self):
        self.instance.delete()


class ViewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop("event", None)

        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    def save(self, commit=True):
        view = super().save(commit=False)

        if self.event:
            view.event = self.event

        if commit:
            view.save()
        return view

    class Meta:
        model = View
        fields = ("name", "start_time", "end_time", "public")


NEW_ROOM_HELP_TEXT = _(
    "You can either select an existing room or choose to create a new one by typing its " "name here, but not both."
)


class AddRoomForm(forms.Form):
    """
    Implements the "Add room to view" action in the Schedule Admin view.
    """

    existing_room = forms.ModelChoiceField(
        queryset=Room.objects.none(),
        label=_("Existing room"),
        required=False,
    )

    new_room_name = forms.CharField(
        max_length=ROOM_NAME_MAX_LENGTH, label=_("New room name"), required=False, help_text=NEW_ROOM_HELP_TEXT
    )

    def __init__(self, *args, **kwargs):
        self.view = kwargs.pop("instance")

        super().__init__(*args, **kwargs)

        self.fields["existing_room"].queryset = Room.objects.filter(event=self.view.event)
        self.fields["existing_room"].label = _("Existing room")
        self.fields["existing_room"].required = False

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    def clean(self):
        existing_room = self.cleaned_data["existing_room"]
        new_room_name = self.cleaned_data["new_room_name"]

        if not existing_room and not new_room_name:
            raise forms.ValidationError(NEW_ROOM_HELP_TEXT)

        if existing_room and new_room_name:
            raise forms.ValidationError(NEW_ROOM_HELP_TEXT)

    def save(self, *args, **kwargs):
        new_room_name = self.cleaned_data["new_room_name"]
        if new_room_name:
            room = Room.objects.create(event=self.view.event, name=new_room_name)
        else:
            room = self.cleaned_data["existing_room"]

        return ViewRoom.objects.create(view=self.view, room=room)


class RoomIdForm(forms.Form):
    room_id = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop("event")
        super().__init__(*args, **kwargs)

    def get_room(self):
        return get_object_or_404(Room, id=self.cleaned_data["room_id"], event=self.event)


class DeleteRoomForm(RoomIdForm):
    def save(self):
        room = self.get_room()
        if not room.can_delete:
            raise ValueError(f"Cannot delete Room: {room}")

        room.delete()
