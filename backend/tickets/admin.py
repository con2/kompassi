from django.contrib import admin

from .models import (
    Customer,
    LimitGroup,
    Order,
    OrderProduct,
    Product,
    TicketsEventMeta,
)


class InlineTicketsEventMetaAdmin(admin.StackedInline):
    model = TicketsEventMeta
    raw_id_fields = ("admin_group", "pos_access_group")


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


admin.site.register(Customer)
