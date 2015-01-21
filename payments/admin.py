from django.contrib import admin

from .models import PaymentsEventMeta

class InlinePaymentsEventMetaAdmin(admin.StackedInline):
    model = PaymentsEventMeta
