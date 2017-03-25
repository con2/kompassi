# encoding: utf-8



from django.contrib import admin

from .models import Enrollment, EnrollmentEventMeta


class InlineEnrollmentEventMetaAdmin(admin.StackedInline):
    model = EnrollmentEventMeta


class EnrollmentAdmin(admin.ModelAdmin):
    model = Enrollment
    list_display = ('event', 'person')
    list_filter = ('event',)


admin.site.register(Enrollment, EnrollmentAdmin)
