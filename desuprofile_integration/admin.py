from django.contrib import admin

from .models import Connection, ConfirmationCode

admin.site.register(Connection)
admin.site.register(ConfirmationCode)
