from django.contrib import admin

from .models import FeedbackMessage


class FeedbackMessageAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'admin_get_abridged_feedback', 'author', 'context')
    readonly_fields = ('created_at', 'feedback', 'author', 'author_ip_address', 'context')

    def has_add_permission(self, *args, **kwargs):
        return False


admin.site.register(FeedbackMessage, FeedbackMessageAdmin)
