# encoding: utf-8
# vim: shiftwidth=4 expandtab

from django import forms
from payments.models import *

class PaymentForm(forms.ModelForm):
    class Meta:     
        model = Payment
        fields = [
            # XXX What the fuck is this and why the fuck is it here
            'test',

            'VERSION',
            'STAMP',
            'REFERENCE',
            'PAYMENT',
            'STATUS',
            'ALGORITHM',
            'MAC',
        ]