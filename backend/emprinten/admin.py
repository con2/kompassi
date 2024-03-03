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
