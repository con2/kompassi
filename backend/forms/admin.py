from django.contrib import admin

from .models import Form, Response, Survey


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    model = Form
    list_display = ("event", "slug", "title")
    list_filter = ("event",)
    search_fields = ("slug", "title")


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    model = Response
    list_display = ("created_at", "form", "created_by")
    list_filter = ("form__event", "form")
    readonly_fields = ("form", "form_data", "created_by", "ip_address", "created_at", "updated_at")
    fields = readonly_fields

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_change_permission(self, *args, **kwargs):
        return False


class SurveyFormInline(admin.TabularInline):
    model = Survey.languages.through
    extra = 1


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    model = Survey
    list_display = ("event", "slug", "admin_is_active")
    list_filter = ("event",)
    fields = (
        "event",
        "slug",
        "login_required",
        "anonymity",
        "max_responses_per_user",
        "active_from",
        "active_until",
    )
    inlines = (SurveyFormInline,)
