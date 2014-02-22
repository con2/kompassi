# encoding: utf-8

from django.contrib import admin

from .models import (
  Batch,
  Customer,
  Customer,
  Order,
  OrderProduct,
  Product,
)


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = (
      'name',
      'internal_description',
      'formatted_price',
      'sell_limit',
      'amount_available',
      'available',
      'requires_shipping',
    )


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


admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)

for cls in (Batch, Customer):
    admin.site.register(cls)
