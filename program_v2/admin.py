from django.contrib import admin

from .models import Dimension, DimensionValue


class DimensionValueInline(admin.TabularInline):
    model = DimensionValue
    extra = 0


class DimensionAdmin(admin.ModelAdmin):
    model = Dimension
    inlines = [DimensionValueInline]
    list_display = ("event", "slug", "title")
    list_filter = ("event",)


admin.site.register(Dimension, DimensionAdmin)
