from django.contrib import admin

from .models import ExternalEvent, Listing


class ListingAdmin(admin.ModelAdmin):
    list_display = ("hostname", "title")


class ExternalEventAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "start_time", "end_time")
    ordering = ("start_time",)


admin.site.register(Listing, ListingAdmin)
admin.site.register(ExternalEvent, ExternalEventAdmin)
