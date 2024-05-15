from django.contrib import admin

from .models import IntraEventMeta, Team, TeamMember


class InlineIntraEventMetaAdmin(admin.StackedInline):
    model = IntraEventMeta
    raw_id_fields = ("admin_group", "organizer_group")


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    model = Team
    list_display = ("event", "name")
    list_filter = ("event",)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    model = Team
    list_display = ("admin_get_event", "team", "person")
    list_filter = ("team__event",)
