from django.contrib import admin

from .models import (
    DirectoryAccessGroup,
    DirectoryOrganizationMeta,
)


class InlineDirectoryOrganizationMetaAdmin(admin.StackedInline):
    model = DirectoryOrganizationMeta


class DirectoryAccessGroupAdmin(admin.ModelAdmin):
    model = DirectoryAccessGroup
    list_display = ("organization", "group", "active_from", "active_until")
    list_filter = ("organization",)


admin.site.register(DirectoryAccessGroup, DirectoryAccessGroupAdmin)
