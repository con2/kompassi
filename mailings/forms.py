from django import forms

from core.utils import horizontal_form_helper

from .models import Message

class MessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    class Meta:
        model = Message
        fields = ('recipient_group', 'subject_template', 'body_template')
