from django.contrib import admin

from .models.dimension import Dimension, DimensionValue, ResponseDimensionValue
from .models.form import Form
from .models.response import Response
from .models.survey import Survey


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    model = Form
    list_display = ("event", "slug", "title")
    list_filter = ("event",)
    search_fields = ("slug", "title")


class ResponseDimensionValueInline(admin.TabularInline):
    model = ResponseDimensionValue
    extra = 1


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    model = Response
    list_display = ("created_at", "form", "created_by")
    list_filter = ("form__event", "form")
    readonly_fields = ("form", "form_data", "created_by", "ip_address", "created_at", "updated_at")
    fields = readonly_fields
    inlines = (ResponseDimensionValueInline,)

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
        "key_fields",
    )
    inlines = (SurveyFormInline,)


class DimensionValueInline(admin.TabularInline):
    model = DimensionValue
    extra = 1


@admin.register(Dimension)
class DimensionAdmin(admin.ModelAdmin):
    model = Dimension
    list_display = ("admin_get_event", "survey", "slug")
    list_filter = (
        "survey__event",
        "survey",
    )
    search_fields = ("slug", "title")
    fields = ("survey", "slug", "title", "order", "is_key_dimension")
    readonly_fields = ("survey",)
    inlines = (DimensionValueInline,)
