# encoding: utf-8

from django import forms

from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Fieldset, Submit

from core.utils import horizontal_form_helper, indented_without_label, initialize_form

from tickets.models import Order, OrderProduct, Customer, Product

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


class NullForm(forms.Form):
    pass


class OrderProductForm(forms.ModelForm):
    count = forms.IntegerField(label=u"Määrä", min_value=0, max_value=99)

    def __init__(self, *args, **kwargs):
        super(OrderProductForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'sr-only'
        self.helper.field_class = 'col-md-12'
        self.helper.form_tag = False

    @classmethod
    def get_for_order(cls, request, order, admin=False):
        product_criteria = dict(event=order.event)

        if not admin:
            product_criteria.update(available=True)

        return [
            cls.get_for_order_and_product(request, order, product, admin=admin)
            for product in Product.objects.filter(**product_criteria)
        ]

    @classmethod
    def get_for_order_and_product(cls, request, order, product, admin=False):
        order_product, unused = OrderProduct.objects.get_or_create(order=order, product=product)
            
        return initialize_form(OrderProductForm, request,
            instance=order_product,
            prefix="o%d" % order_product.pk,

            # XXX disallow changing amounts of electronic tickets for now
            readonly=(order.batch is not None and product.requires_shipping) or (admin and product.electronic_ticket),
        )

    class Meta:
        exclude = ("order", "product")
        model = OrderProduct


class CustomerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'first_name',
            'last_name',
            'address',
            'zip_code',
            'city',
            'phone_number',
            'email',
            indented_without_label('allow_marketing_email'),
        )

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

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.layout = Layout(
            'id',
            'first_name',
            'last_name',
            'email',
            indented_without_label(Submit('submit', u'Hae tilauksia', css_class='btn-primary')),
        )


class AdminOrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AdminOrderForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'reference_number',
            # 'start_time',
            'confirm_time',
            'payment_date',
            'cancellation_time',
            'ip_address',
            'batch',
        )

    class Meta:
        model = Order
        fields = (
            'batch',
            'cancellation_time',
            'confirm_time',
            'ip_address',
            'payment_date',
            'reference_number',
            # 'start_time',
        )