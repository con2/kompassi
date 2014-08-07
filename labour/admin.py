# encoding: utf-8

from django.contrib import admin

from .models import (
    AlternativeSignupForm,
    InfoLink,
    JobCategory,
    LabourEventMeta,
    PersonQualification,
    Qualification,
    Signup,
    WorkPeriod,
)


class SignupAdmin(admin.ModelAdmin):
    model = Signup
    list_display = ('event', 'full_name', 'formatted_state')
    list_filter = ('event',)
    ordering = ('event', 'person__surname', 'person__surname')
    search_fields = ('person__surname', 'person__first_name', 'person__nick', 'person__email')

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
    list_display = ('event', 'name', 'public')
    list_filter = ('event', 'public')
    ordering = ('event', 'name')


class AlternativeSignupFormAdmin(admin.ModelAdmin):
    list_display = ('event', 'slug', 'title')
    list_filter = ('event',)
    ordering = ('event', 'slug')


class InfoLinkAdmin(admin.ModelAdmin):
    list_display = ('event', 'title', 'url')
    list_filter = ('event',)


admin.site.register(Signup, SignupAdmin)
admin.site.register(WorkPeriod)
admin.site.register(JobCategory, JobCategoryAdmin)
admin.site.register(Qualification, QualificationAdmin)
admin.site.register(AlternativeSignupForm, AlternativeSignupFormAdmin)
admin.site.register(InfoLink, InfoLinkAdmin)