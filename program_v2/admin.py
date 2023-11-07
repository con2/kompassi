from django.contrib import admin

from .models import Dimension, DimensionValue, OfferForm


class DimensionValueInline(admin.TabularInline):
    model = DimensionValue
    extra = 0


class DimensionAdmin(admin.ModelAdmin):
    model = Dimension
    inlines = [DimensionValueInline]
    list_display = ("event", "slug", "title")
    list_filter = ("event",)


class OfferFormAdmin(admin.ModelAdmin):
    model = OfferForm
    list_display = ("event", "slug", "short_description")
    list_filter = ("event",)


admin.site.register(Dimension, DimensionAdmin)
admin.site.register(OfferForm, OfferFormAdmin)
