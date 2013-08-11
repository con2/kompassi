import datetime

from django.contrib import admin

from .models import Category, Room, Person, Role, Tag, Programme, View


class ProgrammeRoleInline(admin.TabularInline):
    model = Programme.organizers.through
    verbose_name = 'organizer'
    verbose_name_plural = 'organizers'


class PersonAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Basic information', {'fields': [('first_name', 'surname'), 'nick']}),
        ('Contact information', {'fields': ['email', 'phone']}),
        ('Display', {'fields': ['anonymous']}),
        ('Notes', {'fields': ['notes']}),
    ]

    list_display = ('full_name', 'email', 'phone', 'anonymous')


class ProgrammeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Basic information', {'fields': ['title', 'description', 'category', 'tags']}),
        ('Time and location', {'fields': ['room', ('start_time', 'length')]}),
        ('Display', {'fields': ['hilight', 'public']}),
        ('Notes', {'fields': ['notes']}),
    ]

    inlines = [
        ProgrammeRoleInline,
    ]

    list_display = ('title', 'category', 'room', 'start_time', 'length', 'end_time')
    list_filter = ('room', 'start_time', 'category')


class ViewAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Category)
admin.site.register(Room)
admin.site.register(Person, PersonAdmin)
admin.site.register(Role)
admin.site.register(Tag)
admin.site.register(Programme, ProgrammeAdmin)
admin.site.register(View, ViewAdmin)
