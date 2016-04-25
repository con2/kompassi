import datetime

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import (
    Category,
    FreeformOrganizer,
    Programme,
    ProgrammeEventMeta,
    Role,
    Room,
    SpecialStartTime,
    Tag,
    TimeBlock,
    View,
)
from .proxies.freeform_organizer.admin import FreeformOrganizerAdminProxy
from .proxies.invitation.admin import InvitationAdminProxy


def deactivate_selected_items(modeladmin, request, queryset):
    queryset.update(active=False)
deactivate_selected_items.short_description = _('Deactivate selected items')


def activate_selected_items(modeladmin, request, queryset):
    queryset.update(active=False)
activate_selected_items.short_description = _('Activate selected items')


class InlineProgrammeEventMetaAdmin(admin.StackedInline):
    model = ProgrammeEventMeta


class ProgrammeRoleInline(admin.TabularInline):
    model = Programme.organizers.through
    verbose_name = 'organizer'
    verbose_name_plural = 'organizers'


class ProgrammeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Basic information', {'fields': ['title', 'description', 'category', 'tags']}),
        ('Time and location', {'fields': ['room', ('start_time', 'length')]}),
        ('Notes', {'fields': ['notes']}),
    ]

    inlines = [
        ProgrammeRoleInline,
    ]

    list_display = ('title', 'category', 'room', 'start_time', 'length', 'end_time')
    list_filter = ('room', 'start_time', 'category')


class ViewAdmin(admin.ModelAdmin):
    list_display = ('event', 'name', 'public')
    list_filter = ('event',)


class RoomAdmin(admin.ModelAdmin):
    list_display = ('venue', 'name', 'active')
    list_filter = ('venue', 'active')
    actions = (activate_selected_items, deactivate_selected_items)


class RoleAdmin(admin.ModelAdmin):
    list_display = ('admin_get_event', 'title', 'personnel_class')
    list_filter = ('personnel_class__event',)
    raw_id_fields = ('personnel_class',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('event', 'title', 'public')
    list_filter = ('event',)


class SpecialStartTimeAdmin(admin.ModelAdmin):
    list_display = ('event', 'start_time')
    list_filter = ('event',)


class TimeBlockAdmin(admin.ModelAdmin):
    list_display = ('event', 'start_time', 'end_time')
    list_filter = ('event',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('event', 'title')
    list_filter = ('event',)


class InvitationAdmin(admin.ModelAdmin):
    list_display = ('admin_get_event', 'admin_get_title', 'email', 'state', 'created_by')
    list_filter = ('programme__category__event', 'state')
    ordering = ('programme__category__event', 'programme__title', 'email')
    raw_id_fields = ('programme',)


class FreeformOrganizerAdmin(admin.ModelAdmin):
    list_display = ('admin_get_event', 'admin_get_title', 'text')
    list_filter = ('programme__category__event',)
    raw_id_fields = ('programme',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Programme, ProgrammeAdmin)
admin.site.register(View, ViewAdmin)
admin.site.register(TimeBlock, TimeBlockAdmin)
admin.site.register(SpecialStartTime, SpecialStartTimeAdmin)
admin.site.register(InvitationAdminProxy, InvitationAdmin)
admin.site.register(FreeformOrganizerAdminProxy, FreeformOrganizerAdmin)