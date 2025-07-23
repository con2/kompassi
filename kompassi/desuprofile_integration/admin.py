from django.contrib import admin

from .models import ConfirmationCode, Connection


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    model = Connection
    list_display = ("user", "desuprofile_username")
    raw_id_fields = ("user",)
    search_fields = ("user__username", "user__first_name", "user__last_name", "user__email", "desuprofile_username")


@admin.register(ConfirmationCode)
class ConfirmationCodeAdmin(admin.ModelAdmin):
    model = ConfirmationCode
    list_display = ("person", "desuprofile_username")
    raw_id_fields = ("person",)
