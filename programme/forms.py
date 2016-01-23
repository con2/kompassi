# encoding: utf-8

from django import forms
from django.forms.models import modelformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset

from core.models import Person
from core.utils import horizontal_form_helper, format_datetime, indented_without_label, make_horizontal_form_helper

from .models import Programme, Role, Invitation


class ProgrammePublicForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')

        super(ProgrammePublicForm, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.fields['category'].queryset = Category.objects.filter(event=event)

    class Meta:
        model = Programme
        fields = (
            'title',
            'description',
            'category',
        )


class AddHostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')

        super(AddHostForm, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.fields['role'].queryset = Role.objects.filter(event=event)

    class Meta:
        model = Invitation
        fields = (
            'email',
            'role',
        )
