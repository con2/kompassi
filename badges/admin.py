from django.contrib import admin

from .models import BadgesEventMeta, Badge


class InlineBadgesEventMetaAdmin(admin.StackedInline):
    model = BadgesEventMeta


class BadgeAdmin(admin.ModelAdmin):
    model = Badge
    list_display = ('event_name', 'person_full_name', 'batch')
    list_filter = ('personnel_class__event')


admin.site.register(Badge, BadgeAdmin)
