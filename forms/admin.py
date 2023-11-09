from django.contrib import admin

from .models import EventForm, GlobalForm, EventFormResponse, GlobalFormResponse


class GlobalFormAdmin(admin.ModelAdmin):
    model = GlobalForm
    list_display = ("slug", "title")
    search_fields = ("slug", "title")


class EventFormAdmin(admin.ModelAdmin):
    model = EventForm
    list_display = ("event", "slug", "title")
    list_filter = ("event",)
    search_fields = ("slug", "title")


class GlobalFormResponseAdmin(admin.ModelAdmin):
    model = GlobalFormResponse
    list_display = ("created_at", "form", "created_by")
    list_filter = ("form",)
    readonly_fields = ("form", "form_data", "created_by", "created_at", "updated_at")

    def has_add_permission(self, *args, **kwargs):
        return False


class EventFormResponseAdmin(admin.ModelAdmin):
    model = EventFormResponse
    list_display = ("created_at", "form", "created_by")
    list_filter = ("form__event", "form")
    readonly_fields = ("form", "form_data", "created_by", "created_at", "updated_at")

    def has_add_permission(self, *args, **kwargs):
        return False


admin.site.register(EventForm, EventFormAdmin)
admin.site.register(GlobalForm, GlobalFormAdmin)
admin.site.register(EventFormResponse, EventFormResponseAdmin)
admin.site.register(GlobalFormResponse, GlobalFormResponseAdmin)
