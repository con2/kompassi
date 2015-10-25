from django.contrib import admin

from .models import Privilege, GroupPrivilege, GrantedPrivilege, SlackAccess


class PrivilegeAdmin(admin.ModelAdmin):
    model = Privilege
    list_display = ('slug', 'title')
    readonly_fields = ('slug',)


class GrantedPrivilegeAdmin(admin.ModelAdmin):
    model = GrantedPrivilege
    list_display = ('privilege', 'person', 'state')
    list_filter = ('privilege', 'state')
    search_fields = ('person__surname', 'person__first_name', 'person__nick', 'person__email')
    raw_id_fields = ('person',)


class GroupPrivilegeAdmin(admin.ModelAdmin):
    model = GroupPrivilege
    list_display = ('privilege', 'group')
    list_filter = ('privilege',)
    search_fields = ('group__name',)


class SlackAccessAdmin(admin.ModelAdmin):
    model = SlackAccess
    list_display = ('privilege', 'team_name')
    search_fields = ('privilege__slug', 'privilege__title', 'team_name')


admin.site.register(Privilege, PrivilegeAdmin)
admin.site.register(GroupPrivilege, GroupPrivilegeAdmin)
admin.site.register(GrantedPrivilege, GrantedPrivilegeAdmin)
admin.site.register(SlackAccess, SlackAccessAdmin)
