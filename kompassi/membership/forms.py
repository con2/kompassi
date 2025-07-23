from crispy_forms.layout import Layout
from django import forms

from kompassi.core.forms import PersonForm
from kompassi.core.models import Person
from kompassi.core.utils import horizontal_form_helper

from .models import Membership, MembershipFeePayment, Term


class MemberForm(PersonForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper.form_tag = False
        self.helper.layout = Layout(
            "first_name",
            "surname",
            "nick",
            "official_first_names",
            "muncipality",
            "birth_date",
            "phone",
            "email",
        )

        self.fields[
            "muncipality"
        ].help_text = "Yhdistyslaki vaatii yhdistystä pitämään jäsenistään luetteloa, josta ilmenevät jäsenen täydellinen nimi ja kotikunta."
        self.fields["phone"].help_text = None
        self.fields["email"].help_text = self.fields["email"].help_text.replace("tapahtumaan", "yhdistykseen")

        for field_name, field in self.fields.items():
            field.required = field_name in ["first_name", "surname"]

    class Meta:
        model = Person
        fields = [
            "first_name",
            "surname",
            "nick",
            "official_first_names",
            "muncipality",
            "birth_date",
            "phone",
            "email",
        ]


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ("message",)


class MembershipForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.layout = Layout(
            "state",
            "message",
        )

    class Meta:
        model = Membership
        fields = (
            "state",
            "message",
        )


class MembershipFeePaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = MembershipFeePayment
        fields = ("payment_type", "payment_method", "payment_date", "amount_cents")


class TermForm(forms.ModelForm):
    class Meta:
        model = Term
        # TODO: support entrance_fee_cents
        fields = ("title", "start_date", "end_date", "membership_fee_cents", "payment_method")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not (self.instance.organization.payments_organization_meta):
            # if not chekkout, get the hekk out
            self.fields["payment_method"].choices = [
                (key, label) for (key, label) in self.fields["payment_method"].choices if key != "checkout"
            ]
