
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import (
  AccommodationInformation,
  Batch,
  Customer,
  Customer,
  LimitGroup,
  Order,
  OrderProduct,
  Product,
  ShirtOrder,
  ShirtSize,
  ShirtType,
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
    fields = ('last_name', 'first_name', 'phone_number', 'email')


class ShirtTypeAdmin(admin.ModelAdmin):
    list_display = ('event', 'name')
    list_filter = ('event',)


def shirt_size_get_event(shirt_size):
    return shirt_size.type.event if shirt_size.type else None
shirt_size_get_event.short_description = _('Event')
shirt_size_get_event.admin_order_field = 'type__event'


class ShirtSizeAdmin(admin.ModelAdmin):
    list_display = (shirt_size_get_event, 'type', 'name')
    list_filter = ('type__event',)


def shirt_order_get_event(shirt_order):
    return shirt_size_get_event(shirt_order.size) if shirt_order.size else None
shirt_order_get_event.short_description = _('Event')
shirt_order_get_event.admin_order_field = 'size__type__event'


def shirt_order_get_type(shirt_order):
    return shirt_order.size.type if shirt_order.size else None
shirt_order_get_type.short_description = _('Type')
shirt_order_get_type.admin_order_field = 'size__type'


class ShirtOrderAdmin(admin.ModelAdmin):
    list_display = (shirt_order_get_event, 'order', shirt_order_get_type, 'size', 'count')
    list_filter = ('order__event',)
    raw_id_fields = ('order',)


admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(LimitGroup, LimitGroupAdmin)
admin.site.register(AccommodationInformation, AccommodationInformationAdmin)
admin.site.register(ShirtType, ShirtTypeAdmin)
admin.site.register(ShirtSize, ShirtSizeAdmin)
admin.site.register(ShirtOrder, ShirtOrderAdmin)

for cls in (Batch, Customer):
    admin.site.register(cls)
