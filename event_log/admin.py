# encoding: utf-8

from django.contrib import admin

from .models import Entry, Subscription


class EntryAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'entry_type', 'created_by')
    raw_id_fields = ('created_by',)
    fields = ('created_at', 'entry_type', 'message', 'created_by')
    readonly_fields = ('created_at', 'entry_type', 'message', 'created_by')

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('entry_type', 'user', 'active')
    raw_id_fields = ('user',)


admin.site.register(Entry, EntryAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
