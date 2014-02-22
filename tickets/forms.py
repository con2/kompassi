# encoding: utf-8
# vim: shiftwidth=4 expandtab

from django import forms
from django.contrib.localflavor.fi.forms import FIZipCodeField

from crispy_forms.helper import FormHelper

from ticket_sales.models import *

__all__ = [
    "NullForm",
    "OrderProductForm",
    "CustomerForm",
    "SinglePaymentForm",
    "ConfirmSinglePaymentForm",
    "MultiplePaymentsForm",
    "CreateBatchForm",
    "SearchForm",
]

class HappyIntegerField(forms.IntegerField):
    def __init__(self, size=2):
        max_value = 10 ** size - 1

        super(HappyIntegerField, self).__init__(
            widget=forms.TextInput(attrs=dict(size=2, maxlength=size)),
            min_value=0,
            max_value=max_value
        )

    def clean(self, value):
        if not value:
            return 0

        else:
            return super(HappyIntegerField, self).clean(value)

class NullForm(forms.Form):
    pass

class OrderProductForm(forms.ModelForm):
    count = HappyIntegerField(2)

    class Meta:
        exclude = ("order", "product")
        model = OrderProduct
        
class CustomerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    class Meta:
        model = Customer

class SinglePaymentForm(forms.Form):
    ref_number = forms.CharField(max_length=19, label=u"Viitenumero")

class ConfirmSinglePaymentForm(forms.Form):
    order_id = forms.IntegerField()

class MultiplePaymentsForm(forms.Form):
    dump = forms.CharField(widget=forms.Textarea(attrs={'rows':15,'cols':'90'}), label=u"Pastee tähän")

class CreateBatchForm(forms.Form):
    max_orders = forms.IntegerField(label=u"Kuinka monta tilausta (enintään)?")

class SearchForm(forms.Form):
    id = forms.IntegerField(label=u"Tilausnumero", required=False)
    first_name = forms.CharField(label=u"Etunimi", required=False)
    last_name = forms.CharField(label=u"Sukunimi", required=False)
    email = forms.CharField(label=u"Sähköpostiosoite", required=False)
