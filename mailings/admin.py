from django.contrib import admin

from models import RecipientGroup, Message


class RecipientGroupAdmin(admin.ModelAdmin):
    list_display = ('app_label', 'event', 'verbose_name')
    list_filter = ('app_label', 'event')


admin.site.register(Message)
admin.site.register(RecipientGroup, RecipientGroupAdmin)
