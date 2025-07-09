from django.contrib import admin

from .models.involvement import Involvement
from .models.involvement_to_badge import InvolvementToBadgeMapping
from .models.involvement_to_group import InvolvementToGroupMapping
from .models.registry import Registry


@admin.register(Involvement)
class InvolvementAdmin(admin.ModelAdmin):
    list_display = (
        "event",
        "person",
        "description",
        "is_active",
    )
    list_display_links = ("event", "person")
    list_filter = ("universe__scope__event", "is_active")
    search_fields = ("person__surname", "person__first_name")
    ordering = ("universe", "person__surname", "person__first_name")

    raw_id_fields = ("universe", "person", "registry", "program", "response")
    fields = (
        "universe",
        "person",
        "registry",
        "program",
        "response",
        "cached_dimensions",
        "is_active",
    )
    readonly_fields = fields


@admin.register(Registry)
class RegistryAdmin(admin.ModelAdmin):
    list_display = (
        "scope",
        "slug",
        "title_en",
        "title_fi",
    )
    list_display_links = ("scope", "slug")
    list_filter = ("scope__event",)


@admin.register(InvolvementToBadgeMapping)
class InvolvementToBadgeMappingAdmin(admin.ModelAdmin):
    list_display = (
        "universe",
        "personnel_class",
        "job_title",
        "priority",
    )
    list_display_links = ("universe", "personnel_class")
    list_filter = ("universe__scope__event",)
    search_fields = ("universe__scope__event__name", "personnel_class__name", "job_title")
    ordering = ("universe", "priority")

    raw_id_fields = ("universe", "personnel_class")
    fields = (
        "universe",
        "required_dimensions",
        "personnel_class",
        "job_title",
        "priority",
        "annotations",
    )
    readonly_fields = fields


@admin.register(InvolvementToGroupMapping)
class InvolvementToGroupMappingAdmin(admin.ModelAdmin):
    list_display = (
        "universe",
        "group",
        "formatted_required_dimensions",
    )
    list_display_links = ("universe", "group")
    list_filter = ("universe__scope__event",)
    search_fields = ("universe__scope__event__name", "group__name")
    ordering = ("universe",)

    raw_id_fields = ("universe", "group")
    fields = (
        "universe",
        "required_dimensions",
        "group",
    )
    readonly_fields = fields
