from django.contrib import admin

from .models import Dimension, DimensionValue, OfferForm, Program, ScheduleItem


class DimensionValueInline(admin.TabularInline):
    model = DimensionValue
    extra = 0


@admin.register(Dimension)
class DimensionAdmin(admin.ModelAdmin):
    model = Dimension
    inlines = [DimensionValueInline]
    list_display = ("event", "slug", "title")
    list_filter = ("event",)


@admin.register(OfferForm)
class OfferFormAdmin(admin.ModelAdmin):
    model = OfferForm
    list_display = ("event", "slug", "short_description")
    list_filter = ("event",)


class ScheduleItemInline(admin.TabularInline):
    model = ScheduleItem
    extra = 0
    readonly_fields = ("cached_end_time",)


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    model = Program
    list_display = ("title", "slug", "event")
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
