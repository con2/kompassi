from django.contrib import admin

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


@admin.register(Product)
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


@admin.register(LimitGroup)
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


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    inlines = [
        OrderProductInline,
        #        CustomerInline
    ]


@admin.register(AccommodationInformation)
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


admin.site.register(Customer)
