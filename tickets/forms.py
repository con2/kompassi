from django import forms
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit

from core.utils import horizontal_form_helper, indented_without_label, initialize_form

from .models import (
    AccommodationInformation,
    Customer,
    Order,
    OrderProduct,
    Product,
    ShirtOrder,
)


class NullForm(forms.Form):
    pass


class AccommodationInformationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        for field_name, field in self.fields.items():
            if field_name != "email":
                field.required = True

    @classmethod
    def get_for_order(cls, request, order, admin=False):
        ais = AccommodationInformation.get_for_order(order)
        return [cls.get_for_accommodation_information(request, ai) for ai in ais]

    @classmethod
    def get_for_accommodation_information(cls, request, ai):
        return initialize_form(
            cls,
            request,
            instance=ai,
            prefix="a%d" % ai.pk,
        )

    class Meta:
        model = AccommodationInformation
        fields = ("first_name", "last_name", "phone_number", "email")


class AccommodationPresenceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = "sr-only"
        self.helper.form_tag = False

    class Meta:
        model = AccommodationInformation
        fields = ("room_name",)


class OrderProductForm(forms.ModelForm):
    count = forms.IntegerField(label="Määrä", min_value=0, max_value=99)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = "sr-only"
        self.helper.field_class = "col-md-12"
        self.helper.form_tag = False

    @classmethod
    def get_for_order(cls, request, order, admin=False):
        product_criteria = dict(event=order.event)

        if not admin:
            product_criteria.update(available=True)

        return [
            cls.get_for_order_and_product(request, order, product, admin=admin)
            for product in Product.objects.filter(**product_criteria).order_by("ordering")
        ]

    @classmethod
    def get_for_order_and_product(cls, request, order, product, admin=False):
        order_product, unused = OrderProduct.objects.get_or_create(order=order, product=product)

        return initialize_form(
            OrderProductForm,
            request,
            instance=order_product,
            prefix="o%d" % order_product.pk,
            # XXX disallow changing amounts of electronic tickets for now
            readonly=admin
            and (
                (order.batch is not None and product.requires_shipping) or (order.is_paid and product.electronic_ticket)
            ),
        )

    class Meta:
        exclude = ("order", "product")
        model = OrderProduct


class CustomerForm(forms.ModelForm):
    accept_terms_and_conditions = forms.BooleanField(required=True)

    def __init__(self, *args, **kwargs):
        order = kwargs.pop("order")
        meta = order.event.tickets_event_meta

        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        layout_fields = [
            "first_name",
            "last_name",
            "phone_number",
            "email",
            indented_without_label("allow_marketing_email"),
        ]

        terms_and_conditions_url = meta.terms_and_conditions_url.translate()
        if terms_and_conditions_url:
            layout_fields.append(
                "accept_terms_and_conditions",
            )
            self.fields["accept_terms_and_conditions"].label = _(
                "I accept the <a href='{}' target='_blank' rel='noreferer noopener'>terms and conditions</a> (required)."
            ).format(terms_and_conditions_url)
        else:
            del self.fields["accept_terms_and_conditions"]

        self.helper.layout = Layout(*layout_fields)

    class Meta:
        model = Customer
        fields = [
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "allow_marketing_email",
        ]


class SinglePaymentForm(forms.Form):
    ref_number = forms.CharField(max_length=19, label="Viitenumero")


class ConfirmSinglePaymentForm(forms.Form):
    order_id = forms.IntegerField()


class SearchForm(forms.Form):
    id = forms.IntegerField(label="Tilausnumero", required=False)
    first_name = forms.CharField(label="Etunimi", required=False)
    last_name = forms.CharField(label="Sukunimi", required=False)
    email = forms.CharField(label="Sähköpostiosoite", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.layout = Layout(
            "id",
            "first_name",
            "last_name",
            "email",
            indented_without_label(Submit("submit", "Hae tilauksia", css_class="btn-primary")),
        )


class AdminOrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            "reference_number",
            # 'start_time',
            "confirm_time",
            "payment_date",
            "cancellation_time",
            "ip_address",
            "batch",
        )

    class Meta:
        model = Order
        fields = (
            "batch",
            "cancellation_time",
            "confirm_time",
            "ip_address",
            "payment_date",
            "reference_number",
            # 'start_time',
        )


class CreateBatchForm(forms.Form):
    max_items = forms.IntegerField(label="Kuinka monta tilausta (enintään)?", initial=100)
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        required=False,
        label="Tuote",
        help_text="Jos valitset tästä kentästä tuotteen, saat erän jossa on ainoastaan sellaisia "
        "tilauksia jotka sisältävät vähintään yhden kappaleen valittua tuotetta.",
    )

    def __init__(self, *args, **kwargs):
        event = kwargs.pop("event")

        super().__init__(*args, **kwargs)

        self.fields["product"].queryset = Product.objects.filter(event=event)


class ShirtOrderForm(forms.ModelForm):
    class Meta:
        model = ShirtOrder
        fields = ("count",)
