# encoding: utf-8

from django.contrib import admin

from .models import (
    AlternativeSignupForm,
    JobCategory,
    LabourEventMeta,
    PersonQualification,
    Qualification,
    Signup,
    WorkPeriod,
)

class InlineLabourEventMetaAdmin(admin.StackedInline):
    model = LabourEventMeta


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


class AlternativeSignupFormAdmin(admin.ModelAdmin):
    list_display = ('event', 'slug', 'name')
    list_filter = ('event',)
    ordering = ('event', 'slug')


admin.site.register(Signup)
admin.site.register(WorkPeriod)
admin.site.register(JobCategory, JobCategoryAdmin)
admin.site.register(Qualification, QualificationAdmin)
admin.site.register(AlternativeSignupForm, AlternativeSignupFormAdmin)