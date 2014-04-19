from django.contrib import admin

from .models import ExtraDomain, ViewArg, ViewKwarg


class InlineViewArgAdmin(admin.TabularInline):
    model = ViewArg

class InlineViewKwargAdmin(admin.TabularInline):
    model = ViewKwarg


class ExtraDomainAdmin(admin.ModelAdmin):
    model = ExtraDomain
    inlines = (InlineViewArgAdmin, InlineViewKwargAdmin)


admin.site.register(ExtraDomain, ExtraDomainAdmin)