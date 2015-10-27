from django.contrib import admin

from .models import (
    EmailAliasDomain,
    EmailAliasType,
    GroupEmailAliasGrant,
    EmailAlias,
    GrantedPrivilege,
    GroupPrivilege,
    Privilege,
    SlackAccess,
)


class PrivilegeAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title')
    readonly_fields = ('slug',)


class GrantedPrivilegeAdmin(admin.ModelAdmin):
    list_display = ('privilege', 'person', 'state')
    list_filter = ('privilege', 'state')
    search_fields = ('person__surname', 'person__first_name', 'person__nick', 'person__email')
    raw_id_fields = ('person',)


class GroupPrivilegeAdmin(admin.ModelAdmin):
    list_display = ('privilege', 'group')
    list_filter = ('privilege',)
    search_fields = ('group__name',)


class SlackAccessAdmin(admin.ModelAdmin):
    list_display = ('privilege', 'team_name')
    search_fields = ('privilege__slug', 'privilege__title', 'team_name')


class EmailAliasDomainAdmin(admin.ModelAdmin):
    list_display = ('organization', 'domain_name')
    list_filter = ('organization',)
    search_fields = ('organization__name', 'domain_name')


class EmailAliasTypeAdmin(admin.ModelAdmin):
    list_display = ('admin_get_organization', 'domain', 'metavar')
    list_filter = ('domain__organization', 'domain')
    search_fields = ('domain__organization__name', 'domain__domain_name', 'metavar')


class EmailAliasAdmin(admin.ModelAdmin):
    list_display = ('admin_get_organization', 'email_address')
    list_filter = ('domain__organization', 'domain', 'type')
    search_fields = ('domain__organization__name', 'email_address')
    readonly_fields = ('email_address', 'domain')
    raw_id_fields = ('person',)


admin.site.register(Privilege, PrivilegeAdmin)
admin.site.register(GroupPrivilege, GroupPrivilegeAdmin)
admin.site.register(GrantedPrivilege, GrantedPrivilegeAdmin)
admin.site.register(SlackAccess, SlackAccessAdmin)
admin.site.register(EmailAliasDomain, EmailAliasDomainAdmin)
admin.site.register(EmailAliasType, EmailAliasTypeAdmin)
admin.site.register(EmailAlias, EmailAliasAdmin)