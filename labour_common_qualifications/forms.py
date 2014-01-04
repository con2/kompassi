from django import forms

from .models import JVKortti

class JVKorttiForm(forms.ModelForm):
	class Meta:
		model = JVKortti
		exclude = ('personqualification',)