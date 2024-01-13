from django.contrib import admin

from .models import Badge, BadgesEventMeta, Batch


class InlineBadgesEventMetaAdmin(admin.StackedInline):
    model = BadgesEventMeta


class BadgeAdmin(admin.ModelAdmin):
    model = Badge
    list_display = ("event_name", "admin_get_full_name", "personnel_class_name", "batch")
    list_filter = ("personnel_class__event",)
    search_fields = ("person__surname", "person__first_name", "person__nick", "person__email")
    raw_id_fields = ("person", "batch", "personnel_class")


class BatchAdmin(admin.ModelAdmin):
    model = Batch
    list_display = ("event", "admin_get_number", "personnel_class", "admin_get_num_badges")
    list_display_links = ("event", "admin_get_number")
    list_filter = ("event",)


admin.site.register(Badge, BadgeAdmin)
admin.site.register(Batch, BatchAdmin)
