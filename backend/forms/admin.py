from django.contrib import admin

from .models.form import Form
from .models.response import Response
from .models.response_dimension_value import ResponseDimensionValue
from .models.survey import Survey
from .models.survey_default_dimension_value import SurveyDefaultDimensionValue


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    model = Form
    list_display = ("event", "survey", "language", "title")
    list_filter = ("event",)
    search_fields = ("survey__slug", "title")


class ResponseDimensionValueInline(admin.TabularInline):
    model = ResponseDimensionValue
    extra = 1
    raw_id_fields = ("value",)


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    model = Response
    list_display = ("created_at", "form", "sequence_number", "created_by")
    list_filter = ("form__event", "form")
    readonly_fields = (
        "form",
        "form_data",
        "created_by",
        "ip_address",
        "created_at",
        "updated_at",
        "sequence_number",
    )
    fields = readonly_fields
    inlines = (ResponseDimensionValueInline,)

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_change_permission(self, *args, **kwargs):
        return False


class SurveyDefaultDimensionValueInline(admin.TabularInline):
    model = SurveyDefaultDimensionValue
    extra = 1
    raw_id_fields = ("value",)


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    model = Survey
    inlines = (SurveyDefaultDimensionValueInline,)
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
        "key_fields",
    )
