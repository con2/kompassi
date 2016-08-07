from django.contrib import admin

from .models import IntraEventMeta, Team, TeamMember


class InlineIntraEventMetaAdmin(admin.StackedInline):
    model = IntraEventMeta


class TeamAdmin(admin.ModelAdmin):
    model = Team
    list_display = ('event', 'name')
    list_filter = ('event',)


class TeamMemberAdmin(admin.ModelAdmin):
    model = Team
    list_display = ('admin_get_event', 'team', 'person')
    list_filter = ('team__event',)


admin.site.register(Team, TeamAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
