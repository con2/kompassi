# encoding: utf-8

from django.contrib import admin

from .models import (
    AlternativeSignupForm,
    InfoLink,
    JobCategory,
    Job,
    LabourEventMeta,
    PersonnelClass,
    PersonQualification,
    Qualification,
    Shift,
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


def make_selected_job_categories_public(modeladmin, request, queryset):
    queryset.update(public=True)
make_selected_job_categories_public.short_description = u'Laita valitut tehtävät julkiseen hakuun'


def make_selected_job_categories_nonpublic(modeladmin, request, queryset):
    queryset.update(public=False)
make_selected_job_categories_nonpublic.short_description = u'Ota valitut tehtävät pois julkisesta hausta'


class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ('event', 'name', 'public')
    list_filter = ('event', 'public')
    ordering = ('event', 'name')
    actions = [make_selected_job_categories_public, make_selected_job_categories_nonpublic]


class JobAdmin(admin.ModelAdmin):
    list_display = ('admin_get_event', 'job_category', 'title')
    list_filter = ('job_category__event',)
    ordering = ('job_category__event', 'title')


class PersonnelClassAdmin(admin.ModelAdmin):
    list_display = ('event', 'name')
    list_filter = ('event',)
    ordering = ('event', 'name')


class AlternativeSignupFormAdmin(admin.ModelAdmin):
    list_display = ('event', 'slug', 'title')
    list_filter = ('event',)
    ordering = ('event', 'slug')


class InfoLinkAdmin(admin.ModelAdmin):
    list_display = ('event', 'title', 'url')
    list_filter = ('event',)


class ShiftAdmin(admin.ModelAdmin):
    list_display = ('admin_get_event', 'admin_get_job_category', 'job', 'start_time', 'hours', 'admin_get_person')
    list_filter = ('job__job_category__event',)
    raw_id_fields = ('job', 'signup')


admin.site.register(AlternativeSignupForm, AlternativeSignupFormAdmin)
admin.site.register(InfoLink, InfoLinkAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(JobCategory, JobCategoryAdmin)
admin.site.register(PersonnelClass, PersonnelClassAdmin)
admin.site.register(Qualification, QualificationAdmin)
admin.site.register(Shift, ShiftAdmin)
admin.site.register(Signup, SignupAdmin)
admin.site.register(WorkPeriod)
