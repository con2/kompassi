"""
NOTE: Generally V2 apps should not rely on taka-admin to do basic administrative tasks.
This should be thought of an escape hatch and most admin functions provided in etuadmin.
"""

from django import forms
from django.contrib import admin

from .models.meta import ProgramV2EventMeta
from .models.program import Program
from .models.schedule import ScheduleItem


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


class ProgramV2EventMetaForm(forms.ModelForm):
    class Meta:
        model = ProgramV2EventMeta
        fields = (
            "is_accepting_feedback",
            "contact_email",
            "guide_v2_embedded_url",
        )


class InlineProgramV2EventMetaAdmin(admin.StackedInline):
    model = ProgramV2EventMeta
    form = ProgramV2EventMetaForm
