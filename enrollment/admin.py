from django.contrib import admin

from .models import Enrollment, EnrollmentEventMeta

admin.site.register(Enrollment)

class InlineEnrollmentEventMetaAdmin(admin.StackedInline):
    model = EnrollmentEventMeta
