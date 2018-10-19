# encoding: utf-8

from django.contrib import admin

from .models import Entry, Subscription


ENTRY_READ_ONLY_FIELDS = (
    'created_at',
    'created_by',
    'ip_address',
    'entry_type',
    'message',
    'context',
    'organization',
    'event',
    'person',
)


class EntryAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'entry_type', 'message')
    list_filter = ('entry_type', 'organization',)
    raw_id_fields = ('created_by',)
    fields = ENTRY_READ_ONLY_FIELDS
    readonly_fields = ENTRY_READ_ONLY_FIELDS

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('entry_type', 'user', 'active')
    raw_id_fields = ('user', 'job_category_filter')


admin.site.register(Entry, EntryAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
