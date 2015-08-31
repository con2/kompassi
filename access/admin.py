from django.contrib import admin

from .models import Privilege, GroupPrivilege, GrantedPrivilege


class PrivilegeAdmin(admin.ModelAdmin):
    model = Privilege
    list_display = ('slug', 'title')
    readonly_fields = ('slug',)


class GrantedPrivilegeAdmin(admin.ModelAdmin):
    model = GrantedPrivilege
    list_display = ('privilege', 'person', 'state')
    list_filter = ('privilege', 'state')
    search_fields = ('person__surname', 'person__first_name', 'person__nick', 'person__email')


class GroupPrivilegeAdmin(admin.ModelAdmin):
    model = GroupPrivilege
    list_display = ('privilege', 'group')
    list_filter = ('privilege',)
    search_fields = ('group__name',)



admin.site.register(Privilege, PrivilegeAdmin)
admin.site.register(GroupPrivilege, GroupPrivilegeAdmin)
admin.site.register(GrantedPrivilege, GrantedPrivilegeAdmin)
