from django.template import Library

from ..optimized_server.utils.formatting import format_money, format_order_number, format_vat_rate

register = Library()
register.filter(format_money)
register.filter(format_order_number)
register.filter(format_vat_rate)
