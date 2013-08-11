import datetime

from django.contrib import admin

from .models import View

class ViewAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(View, ViewAdmin)
