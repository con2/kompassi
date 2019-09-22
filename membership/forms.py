from datetime import date

from django import forms

from crispy_forms.layout import Layout, Fieldset

from core.forms import PersonForm
from core.models import Person
from core.utils import indented_without_label, horizontal_form_helper

from .models import Membership, MembershipFeePayment, Term


class MemberForm(PersonForm):
    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)

        self.helper.form_tag = False
        self.helper.layout = Layout(
            'first_name',
            'surname',
            'nick',
            'official_first_names',
            'muncipality',
            'birth_date',
            'phone',
            'email',
        )

        self.fields['muncipality'].help_text = 'Yhdistyslaki vaatii yhdistystä pitämään jäsenistään luetteloa, josta ilmenevät jäsenen täydellinen nimi ja kotikunta.'
        self.fields['phone'].help_text = None
        self.fields['email'].help_text = self.fields['email'].help_text.replace('tapahtumaan', 'yhdistykseen')

        for field_name, field in self.fields.items():
            field.required = field_name in ['first_name', 'surname']

    class Meta:
        model = Person
        fields = [
            'first_name',
            'surname',
            'nick',
            'official_first_names',
            'muncipality',
            'birth_date',
            'phone',
            'email',
        ]


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ('message',)


class MembershipForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MembershipForm, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.layout = Layout(
            'state',
            'message',
        )

    class Meta:
        model = Membership
        fields = ('state', 'message',)


class MembershipFeePaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        current_term = kwargs.pop('current_term')
        initial = kwargs.setdefault('initial', {})
        initial.update(
            term=current_term.id,
            amount_cents=current_term.membership_fee_cents,
            payment_type='membership_fee',
        )

        super().__init__(*args, **kwargs)

        self.fields['term'].queryset = current_term.organization.terms.all()

    class Meta:
        model = MembershipFeePayment
        fields = ('term', 'payment_type', 'payment_method', 'amount_cents')


class TermForm(forms.ModelForm):
    class Meta:
        model = Term
        fields = ('title', 'start_date', 'end_date', 'entrance_fee_cents', 'membership_fee_cents')
