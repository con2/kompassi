from django.contrib import admin

from .models import Connection, ConfirmationCode


class ConnectionAdmin(admin.ModelAdmin):
    model = Connection
    list_display = ("user", "desuprofile_username")
    raw_id_fields = ("user",)
    search_fields = ("user__username", "user__first_name", "user__last_name", "user__email", "desuprofile_username")


class ConfirmationCodeAdmin(admin.ModelAdmin):
    model = ConfirmationCode
    list_display = ("person", "desuprofile_username")
    raw_id_fields = ("person",)


admin.site.register(Connection, ConnectionAdmin)
admin.site.register(ConfirmationCode, ConfirmationCodeAdmin)
