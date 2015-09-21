from django.contrib import admin

from .models import Connection, ConfirmationCode


class ConnectionAdmin(admin.ModelAdmin):
    model = Connection
    raw_id_fields = ('user',)


class ConfirmationCodeAdmin(admin.ModelAdmin):
    model = ConfirmationCode
    raw_id_fields = ('person',)


admin.site.register(Connection, ConnectionAdmin)
admin.site.register(ConfirmationCode, ConfirmationCodeAdmin)
