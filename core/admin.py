from django.contrib import admin

from .models import Person


class PersonAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Basic information', {'fields': [('first_name', 'surname'), 'nick']}),
        ('Contact information', {'fields': ['email', 'phone']}),
        ('Display', {'fields': ['anonymous']}),
        ('Notes', {'fields': ['notes']}),
    ]

    list_display = ('full_name', 'email', 'phone', 'anonymous')


admin.site.register(Person, PersonAdmin)
