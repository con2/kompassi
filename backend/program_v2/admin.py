from django.contrib import admin

from .models import Program, ScheduleItem


class ScheduleItemInline(admin.TabularInline):
    model = ScheduleItem
    extra = 0
    readonly_fields = ("cached_end_time",)


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    model = Program
    list_display = ("title_fi", "title_en", "slug", "event")
    list_filter = ("event",)
    exclude = ("favorited_by",)
    autocomplete_fields = ("event",)
    inlines = [ScheduleItemInline]
    readonly_fields = (
        "created_by",
        "cached_dimensions",
        "cached_earliest_start_time",
        "cached_latest_end_time",
        "cached_location",
        "cached_color",
    )
