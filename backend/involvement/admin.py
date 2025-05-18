from django.contrib import admin

from .models.involvement import Involvement
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
