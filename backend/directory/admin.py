from django.contrib import admin

from .models import (
    DirectoryAccessGroup,
    DirectoryOrganizationMeta,
)


class InlineDirectoryOrganizationMetaAdmin(admin.StackedInline):
    model = DirectoryOrganizationMeta


@admin.register(DirectoryAccessGroup)
class DirectoryAccessGroupAdmin(admin.ModelAdmin):
    model = DirectoryAccessGroup
    list_display = ("organization", "group", "active_from", "active_until")
    list_filter = ("organization",)
