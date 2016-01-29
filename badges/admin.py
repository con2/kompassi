from django.contrib import admin

from .models import BadgesEventMeta, Badge


class InlineBadgesEventMetaAdmin(admin.StackedInline):
    model = BadgesEventMeta


class BadgeAdmin(admin.ModelAdmin):
    model = Badge
    list_display = ('event_name', 'person_full_name', 'personnel_class_name', 'batch')
    list_filter = ('personnel_class__event',)
    search_fields = ('person__surname', 'person__first_name', 'person__nick', 'person__email')
    raw_id_fields = ('person', 'batch', 'personnel_class')


admin.site.register(Badge, BadgeAdmin)
