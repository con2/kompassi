from django.contrib import admin

from .models import Form, FormResponse


class FormAdmin(admin.ModelAdmin):
    model = Form
    list_display = ('title', 'is_active', 'is_standalone')
    list_filter = ('is_active', 'is_standalone')
    search_fields = ('slug', 'title')


class FormResponseAdmin(admin.ModelAdmin):
    model = FormResponse
    list_display = ('created_at', 'form', 'created_by')
    list_filter = ('form',)
    readonly_fields = ('form', 'values', 'created_by', 'created_at', 'updated_at')

    def has_add_permission(self, *args, **kwargs):
        return False


admin.site.register(Form, FormAdmin)
admin.site.register(FormResponse, FormResponseAdmin)
