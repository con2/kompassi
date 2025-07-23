from django.contrib import admin

from .models import ExternalEvent, Listing


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("hostname", "title")


@admin.register(ExternalEvent)
class ExternalEventAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "start_time", "end_time")
    ordering = ("start_time",)
