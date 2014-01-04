from django import forms

from .models import SignupExtra

class SignupExtraForm(forms.ModelForm):
	class Meta:
		model = SignupExtra
		exclude = ('signup')