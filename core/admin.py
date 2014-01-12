# encoding: utf-8

from django.contrib import admin
from django.conf import settings

from .models import Event, Person, Venue


class PersonAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Basic information', {'fields': [('first_name', 'surname'), 'nick']}),
        ('Contact information', {'fields': ['email', 'phone']}),
        ('Display', {'fields': ['anonymous']}),
        ('Notes', {'fields': ['notes']}),
    ]

    list_display = ('full_name', 'email', 'phone', 'anonymous')


if 'labour' in settings.INSTALLED_APPS:
    from labour.admin import InlineLabourEventMetaAdmin
    LABOUR_EVENTADMIN_INLINES = (InlineLabourEventMetaAdmin,)
else:
    LABOUR_EVENTADMIN_INLINES = ()


class EventAdmin(admin.ModelAdmin):
    inlines = LABOUR_EVENTADMIN_INLINES

    fieldsets = (
        ('Tapahtuman nimi', dict(fields=(
            'name',
            'name_genitive',
            'name_illative',
            'name_inessive',
            'slug'
        ))),

        ('Tapahtuman perustiedot', dict(fields=(
            'venue',
            'start_time',
            'end_time',
        ))),

        ('Järjestäjän tiedot', dict(fields=(
            'homepage_url',
            'organization_name',
            'organization_url',
        ))),
    )

    def get_readonly_fields(self, request, obj=None):
        # slug may be edited when creating but not when modifying existing event
        # (breaks urls and kills puppies)
        if obj:
            return self.readonly_fields + ('slug',)

        return self.readonly_fields


admin.site.register(Event, EventAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Venue)
