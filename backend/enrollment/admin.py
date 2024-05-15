from django.contrib import admin

from .models import Enrollment, EnrollmentEventMeta


class InlineEnrollmentEventMetaAdmin(admin.StackedInline):
    model = EnrollmentEventMeta
    raw_id_fields = ("admin_group",)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    model = Enrollment
    list_display = ("event", "person")
    list_filter = ("event",)
