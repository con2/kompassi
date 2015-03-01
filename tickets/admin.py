# encoding: utf-8

from django.contrib import admin

from .models import (
  Batch,
  Customer,
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
      'event',
      'name',
      'internal_description',
      'formatted_price',
      'sell_limit',
      'amount_available',
      'available',
      'requires_shipping',
    )

    list_filter = ('event',)


class LimitGroupAdmin(admin.ModelAdmin):
  model = Product
  list_display = (
    'event',
    'description',
    'amount_available',
    'limit',
  )

  list_filter = ('event',)


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
admin.site.register(LimitGroup, LimitGroupAdmin)

for cls in (Batch, Customer):
    admin.site.register(cls)
