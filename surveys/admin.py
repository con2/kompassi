# encoding: utf-8



from django.contrib import admin

from .models import (
    EventSurvey,
    EventSurveyResult,
    GlobalSurvey,
    GlobalSurveyResult,
)


class EventSurveyAdmin(admin.ModelAdmin):
    model = EventSurvey
    list_display = ('event', 'title', 'is_active')
    list_filter = ('event', 'is_active')


class GlobalSurveyAdmin(admin.ModelAdmin):
    model = GlobalSurvey
    list_display = ('title', 'is_active')
    list_filter = ('is_active',)


class EventSurveyResultAdmin(admin.ModelAdmin):
    model = EventSurveyResult
    list_display = ('created_at', 'admin_get_event', 'survey', 'author')
    list_filter = ('survey__event', 'survey')

    readonly_fields = ('admin_get_event', 'survey', 'created_at', 'author', 'author_ip_address', 'model')

    def has_add_permission(self, *args, **kwargs):
        return False


class GlobalSurveyResultAdmin(admin.ModelAdmin):
    model = GlobalSurveyResult
    list_display = ('created_at', 'survey', 'author')
    list_filter = ('survey',)

    readonly_fields = ('survey', 'created_at', 'author', 'author_ip_address', 'model')

    def has_add_permission(self, *args, **kwargs):
        return False


admin.site.register(EventSurvey, EventSurveyAdmin)
admin.site.register(EventSurveyResult, EventSurveyResultAdmin)
admin.site.register(GlobalSurvey, GlobalSurveyAdmin)
admin.site.register(GlobalSurveyResult, GlobalSurveyResultAdmin)
