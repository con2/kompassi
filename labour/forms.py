from django import forms

from core.models import Person

from .models import Signup


class SignupForm(forms.ModelForm):
    class Meta:
        model = Signup
        exclude = ('event', 'person')