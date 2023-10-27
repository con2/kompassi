from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import (
    AccommodationInformation,
    Customer,
    LimitGroup,
    Order,
    OrderProduct,
    Product,
    TicketsEventMeta,
)


class InlineTicketsEventMetaAdmin(admin.StackedInline):
    model = TicketsEventMeta


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = (
        "event",
        "name",
        "internal_description",
        "formatted_price",
        "sell_limit",
        "amount_available",
        "available",
    )

    list_filter = ("event",)


class LimitGroupAdmin(admin.ModelAdmin):
    model = Product
    list_display = (
        "event",
        "description",
        "amount_available",
        "limit",
    )

    list_filter = ("event",)


class CustomerInline(admin.StackedInline):
    model = Customer


class OrderProductInline(admin.TabularInline):
    model = OrderProduct


class OrderAdmin(admin.ModelAdmin):
    model = Order
    inlines = [
        OrderProductInline,
        #        CustomerInline
    ]


class AccommodationInformationAdmin(admin.ModelAdmin):
    model = AccommodationInformation
    list_display = (
        "event",
        "product_name",
        "formatted_order_number",
        "last_name",
        "first_name",
        "phone_number",
        "email",
    )

    list_filter = ("order_product__product__event",)
    ordering = ("order_product__product__event", "order_product__product", "last_name", "first_name")
    search_fields = ("last_name", "first_name", "phone_number", "email", "order_product__order__id")
    fields = ("last_name", "first_name", "phone_number", "email")


admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(LimitGroup, LimitGroupAdmin)
admin.site.register(AccommodationInformation, AccommodationInformationAdmin)
admin.site.register(Customer)
