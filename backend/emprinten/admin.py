from django.conf import settings
from django.contrib import admin
from django.urls import reverse

from . import models


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    # noinspection PyMethodOverriding
    def view_on_site(self, obj: models.Project) -> str | None:  # pyright: ignore reportIncompatibleMethodOverride
        if obj.event is None:
            return None
        return reverse("emprinten_index", kwargs={"event": obj.event.slug, "slug": obj.slug})


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
