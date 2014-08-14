from django.contrib import admin

from models import SMSMessage, SMSRecipientGroup

class SMSRecipientGroupAdmin(admin.ModelAdmin):
    list_display = ('app_label', 'event', 'verbose_name')
    list_filter = ('app_label', 'event')


admin.site.register(SMSMessage)
admin.site.register(SMSRecipientGroup, SMSRecipientGroupAdmin)