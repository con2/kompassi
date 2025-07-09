from django.contrib import admin

from .models.badge import Badge
from .models.badges_event_meta import BadgesEventMeta
from .models.batch import Batch
from .models.survey_to_badge import SurveyToBadgeMapping


class InlineBadgesEventMetaAdmin(admin.StackedInline):
    model = BadgesEventMeta
    raw_id_fields = ("admin_group", "onboarding_access_group")


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    model = Badge
    list_display = ("event_name", "admin_get_full_name", "personnel_class_name", "batch")
    list_filter = ("personnel_class__event",)
    search_fields = ("person__surname", "person__first_name", "person__nick", "person__email")
    raw_id_fields = ("person", "batch", "personnel_class")


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    model = Batch
    list_display = ("event", "admin_get_number", "personnel_class", "admin_get_num_badges")
    list_display_links = ("event", "admin_get_number")
    list_filter = ("event",)


@admin.register(SurveyToBadgeMapping)
class SurveyToBadgeMappingAdmin(admin.ModelAdmin):
    model = SurveyToBadgeMapping
    list_display = ("survey", "personnel_class", "job_title", "required_dimensions")
    list_filter = ("survey__event",)
    raw_id_fields = ("survey", "personnel_class")
