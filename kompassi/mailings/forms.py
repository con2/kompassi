from django import forms

from kompassi.core.utils import horizontal_form_helper

from .models import Message, RecipientGroup


class MessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop("event")
        app_label = kwargs.pop("app_label")

        super().__init__(*args, **kwargs)

        self.fields["recipient"].queryset = RecipientGroup.objects.filter(
            app_label=app_label,
            event=event,
        )

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    class Meta:
        model = Message
        fields = ("recipient", "subject_template", "body_template")
