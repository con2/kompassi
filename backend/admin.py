import datetime
from django.contrib import admin
from backend.models import Category, Room, Person, Programme

class PersonAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Basic information', {'fields': [('first_name','surname'),'nick']}),
        ('Contact information', {'fields': ['email','phone']}),
        ('Display', {'fields': ['anonymous']}),
    ]

    list_display = ('full_name','nick','email','phone')

class ProgrammeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Basic information', {'fields': ['title','hosts','description','category']}),
        ('Time and location', {'fields': ['room',('start_time','end_time')]}),
        ('Display', {'fields': ['hilight','public']}),
    ]

    filter_horizontal = ('hosts',)

    list_display = ('title','category','room','start_time','length')
    list_filter = ('room','start_time','category')
    
    def length(self, obj):
        return (obj.end_time - obj.start_time)
    length.short_description = 'Length'

admin.site.register(Category)
admin.site.register(Room)
admin.site.register(Person, PersonAdmin)
admin.site.register(Programme, ProgrammeAdmin)
