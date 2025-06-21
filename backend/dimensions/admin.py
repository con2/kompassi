from django.contrib import admin

from .models.dimension import Dimension
from .models.dimension_value import DimensionValue
from .models.scope import Scope
from .models.universe import Universe


class DimensionValueInline(admin.TabularInline):
    model = DimensionValue
    extra = 0


@admin.register(Dimension)
class DimensionAdmin(admin.ModelAdmin):
    model = Dimension
    inlines = [DimensionValueInline]
    list_display = ("admin_get_title", "slug", "admin_get_universe", "admin_get_scope")
    list_filter = ("universe",)
    list_display_links = ("admin_get_title", "slug")


@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    model = Scope
    list_display = ("slug", "event", "organization")


@admin.register(Universe)
class UniverseAdmin(admin.ModelAdmin):
    model = Universe
    list_display = ("slug", "scope", "app")
    list_filter = ("scope", "app")
