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
  AccommodationInformation,
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

class AccommodationInformationAdmin(admin.ModelAdmin):
    model = AccommodationInformation
    list_display = (
      'event',
      'product_name',
      'formatted_order_number',
      'last_name',
      'first_name',
      'phone_number',
      'email',
    )

    list_filter = ('order_product__product__event',)
    ordering = ('order_product__product__event', 'order_product__product', 'last_name', 'first_name')
    search_fields = ('last_name', 'first_name', 'phone_number', 'email', 'order_product__order__id')

admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(LimitGroup, LimitGroupAdmin)
admin.site.register(AccommodationInformation, AccommodationInformationAdmin)

for cls in (Batch, Customer):
    admin.site.register(cls)
