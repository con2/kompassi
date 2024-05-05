from django.conf import settings
from django.contrib import admin

from . import models

admin.site.register(models.Project)
admin.site.register(models.FileVersion)


class FileVersionInline(admin.TabularInline):
    model = models.FileVersion
    ordering = ("version",)


@admin.register(models.ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    inlines = (FileVersionInline,)


@admin.register(models.RenderResult)
class RenderResultAdmin(admin.ModelAdmin):
    list_display = ("id", "project", "row_count", "started")

    def has_add_permission(self, request, obj=None):
        return settings.DEBUG

    def has_change_permission(self, request, obj=None):
        return settings.DEBUG

    def has_delete_permission(self, request, obj=None):
        return settings.DEBUG
