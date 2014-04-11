import datetime

from django.contrib import admin

from .models import (
    Category,
    Programme,
    ProgrammeEventMeta,
    Role,
    Room,
    SpecialStartTime,
    Tag,
    TimeBlock,
    View,
)


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
    list_display = ('name',)

class RoomAdmin(admin.ModelAdmin):
    list_display = ('venue', 'name',)
    list_filter = ('venue',)


admin.site.register(Category)
admin.site.register(Room, RoomAdmin)
admin.site.register(Role)
admin.site.register(Tag)
admin.site.register(Programme, ProgrammeAdmin)
admin.site.register(View, ViewAdmin)
admin.site.register(TimeBlock)
admin.site.register(SpecialStartTime)
