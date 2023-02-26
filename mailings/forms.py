from django import forms

from core.utils import horizontal_form_helper

from .models import RecipientGroup, Message


class MessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop("event")
        app_label = kwargs.pop("app_label")

        super().__init__(*args, **kwargs)

        if not event.sms_event_meta and self.instance.channel != "sms":
            self.fields["channel"].choices = [
                (key, value) for (key, value) in self.fields["channel"].choices if key != "sms"
            ]

        self.fields["recipient"].queryset = RecipientGroup.objects.filter(
            app_label=app_label,
            event=event,
        )

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    class Meta:
        model = Message
        fields = ("channel", "recipient", "subject_template", "body_template")
