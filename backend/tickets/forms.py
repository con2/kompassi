from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit
from django import forms
from django.core import validators
from django.utils.translation import gettext_lazy as _

from core.utils import horizontal_form_helper, indented_without_label, initialize_form
from core.utils.locale_utils import get_message_in_language

from .models import Customer, Order, OrderProduct, Product


class OrderProductForm(forms.ModelForm):
    count = forms.IntegerField(label="Määrä", min_value=0)

    def __init__(self, *args, **kwargs):
        max_count_per_product = kwargs.pop("max_count_per_product", 99)

        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = "sr-only"
        self.helper.field_class = "col-md-12"
        self.helper.form_tag = False

        count_field = self.fields["count"]
        count_field.validators.append(validators.MaxValueValidator(max_count_per_product))
        count_field.widget.attrs["max"] = count_field.max_value = max_count_per_product  # type: ignore

    @classmethod
    def get_for_order(cls, request, order, admin=False, code=""):
        return [
            cls.get_for_order_and_product(request, order, product, admin=admin)
            for product in Product.get_products_for_event(order.event, code=code, admin=admin)
        ]

    @classmethod
    def get_for_order_and_product(cls, request, order, product, admin=False):
        if order.pk:
            order_product, unused = OrderProduct.objects.get_or_create(order=order, product=product)
        else:
            order_product = OrderProduct(order=order, product=product)

        readonly = admin and (order.is_paid and product.electronic_ticket)

        max_count_per_product = order.event.tickets_event_meta.max_count_per_product
        if not admin:
            max_count_per_product = min(product.amount_available, max_count_per_product)
            max_count_per_product = max(max_count_per_product, 0)

        return initialize_form(
            OrderProductForm,
            request,
            instance=order_product,
            prefix="p%d" % product.pk,
            readonly=readonly,
            max_count_per_product=max_count_per_product,
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
        ]

        terms_and_conditions_url = get_message_in_language(meta.terms_and_conditions_url)
        if terms_and_conditions_url:
            layout_fields.append(
                "accept_terms_and_conditions",
            )
            self.fields["accept_terms_and_conditions"].label = _(
                "I accept the <a href='{}' target='_blank' rel='noreferrer noopener'>terms and conditions</a> (required)."
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
        )

    class Meta:
        model = Order
        fields = (
            "cancellation_time",
            "confirm_time",
            "ip_address",
            "payment_date",
            "reference_number",
            # 'start_time',
        )
