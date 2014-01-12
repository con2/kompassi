# encoding: utf-8

from django.contrib import admin

from .models import JobCategory, LabourEventMeta, PersonQualification, Qualification, Signup

class InlineLabourEventMetaAdmin(admin.StackedInline):
    model = LabourEventMeta
    fields = ('registration_opens', 'registration_closes')


class InlinePersonQualificationAdmin(admin.TabularInline):
    model = PersonQualification
    extra = 0


class QualificationAdmin(admin.ModelAdmin):
    model = Qualification
    inlines = (InlinePersonQualificationAdmin,)
    fields = ('name', 'slug', 'description')
    list_display = ('name', 'slug')
    readonly_fields = ('slug',)


class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'event')
    list_filter = ('event',)
    ordering = ('event', 'name')


admin.site.register(Signup)
admin.site.register(JobCategory, JobCategoryAdmin)
admin.site.register(Qualification, QualificationAdmin)
