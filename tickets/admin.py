# encoding: utf-8
# vim: shiftwidth=4 expandtab

from ticket_sales.models import *
from django.contrib import admin

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

for cls in (School, Batch, Customer):
    admin.site.register(cls)
