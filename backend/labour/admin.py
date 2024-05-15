from django.contrib import admin

from .models import (
    AlternativeSignupForm,
    InfoLink,
    Job,
    JobCategory,
    LabourEventMeta,
    PersonnelClass,
    PersonQualification,
    Qualification,
    Shift,
    Signup,
    Survey,
    WorkPeriod,
)


@admin.register(Signup)
class SignupAdmin(admin.ModelAdmin):
    model = Signup
    list_display = ("event", "full_name", "formatted_state")
    list_filter = ("event",)
    ordering = ("event", "person__surname", "person__surname")
    search_fields = ("person__surname", "person__first_name", "person__nick", "person__email")


class InlineLabourEventMetaAdmin(admin.StackedInline):
    model = LabourEventMeta
    raw_id_fields = ("admin_group",)
    exclude = ("signup_extra_content_type",)


class InlinePersonQualificationAdmin(admin.TabularInline):
    model = PersonQualification
    extra = 0


@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    model = Qualification
    inlines = (InlinePersonQualificationAdmin,)
    fields = ("name", "slug", "description")
    list_display = ("name", "slug")
    readonly_fields = ("slug",)


@admin.action(description="Laita valitut tehtävät julkiseen hakuun")
def make_selected_job_categories_public(modeladmin, request, queryset):
    queryset.update(public=True)


@admin.action(description="Ota valitut tehtävät pois julkisesta hausta")
def make_selected_job_categories_nonpublic(modeladmin, request, queryset):
    queryset.update(public=False)


@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ("event", "name", "public")
    list_filter = ("event", "public")
    ordering = ("event", "name")
    actions = [make_selected_job_categories_public, make_selected_job_categories_nonpublic]


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("admin_get_event", "job_category", "title")
    list_filter = ("job_category__event",)
    ordering = ("job_category__event", "title")


@admin.register(PersonnelClass)
class PersonnelClassAdmin(admin.ModelAdmin):
    list_display = ("event", "name")
    list_filter = ("event",)
    ordering = ("event", "name")


@admin.register(AlternativeSignupForm)
class AlternativeSignupFormAdmin(admin.ModelAdmin):
    list_display = ("event", "slug", "title")
    list_filter = ("event",)
    ordering = ("event", "slug")


@admin.register(InfoLink)
class InfoLinkAdmin(admin.ModelAdmin):
    list_display = ("event", "title", "url")
    list_filter = ("event",)


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ("admin_get_event", "admin_get_job_category", "job", "start_time", "hours", "admin_get_person")
    list_filter = ("job__job_category__event",)
    raw_id_fields = ("job", "signup")


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ("event", "title", "admin_is_active")
    list_filter = ("event",)


admin.site.register(WorkPeriod)
