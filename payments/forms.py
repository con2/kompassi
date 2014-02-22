# encoding: utf-8
# vim: shiftwidth=4 expandtab

from django import forms
from payments.models import *

class PaymentForm(forms.ModelForm):
	class Meta:	    
		model = Payment
