from django import forms

from core.utils import horizontal_form_helper

from .models import RecipientGroup, Message

class MessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')

        super(MessageForm, self).__init__(*args, **kwargs)

        self.fields['recipient'].queryset = RecipientGroup.objects.filter(
            app_label='labour',
            event=event,
        )

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    class Meta:
        model = Message
        fields = ('recipient', 'subject_template', 'body_template')
