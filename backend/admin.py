import datetime
from django.contrib import admin
from backend.models import Category, Room, Programme


class ProgrammeAdmin(admin.ModelAdmin):
    fieldsets = [
            ('Basic information', {'fields': ['title','description','category']}),
            ('Time and location', {'fields': ['room','start_time','end_time']}),
            ('Display', {'fields': ['hilight','public']}),
    ]

    list_display = ('title','category','room','start_time','length')
    list_filter = ('room','start_time','category')
    
    def length(self, obj):
        return (obj.end_time - obj.start_time)
    length.short_description = 'Length'

admin.site.register(Category)
admin.site.register(Room)
admin.site.register(Programme, ProgrammeAdmin)
