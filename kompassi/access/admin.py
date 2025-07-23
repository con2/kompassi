from django.contrib import admin

from kompassi.access.models.cbac_entry import CBACEntry

from .models import (
    AccessOrganizationMeta,
    EmailAlias,
    EmailAliasDomain,
    EmailAliasType,
    GrantedPrivilege,
    GroupEmailAliasGrant,
    GroupPrivilege,
    InternalEmailAlias,
    Privilege,
    SlackAccess,
    SMTPPassword,
    SMTPServer,
)


class InlineAccessOrganizationMetaAdmin(admin.StackedInline):
    model = AccessOrganizationMeta


@admin.register(Privilege)
class PrivilegeAdmin(admin.ModelAdmin):
    list_display = ("slug", "title")
    readonly_fields = ("slug",)


@admin.register(GrantedPrivilege)
class GrantedPrivilegeAdmin(admin.ModelAdmin):
    list_display = ("privilege", "person", "state")
    list_filter = ("privilege", "state")
    search_fields = ("person__surname", "person__first_name", "person__nick", "person__email")
    raw_id_fields = ("person",)


@admin.register(GroupPrivilege)
class GroupPrivilegeAdmin(admin.ModelAdmin):
    list_display = ("privilege", "group")
    list_filter = ("privilege",)
    search_fields = ("group__name",)


@admin.register(SlackAccess)
class SlackAccessAdmin(admin.ModelAdmin):
    list_display = ("privilege", "team_name")
    search_fields = ("privilege__slug", "privilege__title", "team_name")


@admin.register(EmailAliasDomain)
class EmailAliasDomainAdmin(admin.ModelAdmin):
    list_display = ("organization", "domain_name")
    list_filter = ("organization",)
    search_fields = ("organization__name", "domain_name")


@admin.register(EmailAliasType)
class EmailAliasTypeAdmin(admin.ModelAdmin):
    list_display = ("admin_get_organization", "domain", "metavar")
    list_filter = ("domain__organization", "domain")
    search_fields = ("domain__organization__name", "domain__domain_name", "metavar")


@admin.register(EmailAlias)
class EmailAliasAdmin(admin.ModelAdmin):
    list_display = ("admin_get_organization", "email_address", "person")
    list_filter = ("domain__organization", "domain", "type")
    search_fields = (
        "domain__organization__name",
        "email_address",
        "person__surname",
        "person__first_name",
        "person__nick",
    )
    readonly_fields = ("email_address", "domain")
    raw_id_fields = ("person", "group_grant")


@admin.register(InternalEmailAlias)
class InternalEmailAliasAdmin(admin.ModelAdmin):
    list_display = ("admin_get_organization", "email_address", "target_emails")
    list_filter = ("domain__organization", "domain")
    search_fields = ("domain__organization__name", "email_address", "target_emails")
    readonly_fields = ("email_address",)


@admin.register(GroupEmailAliasGrant)
class GroupEmailAliasGrantAdmin(admin.ModelAdmin):
    list_display = ("admin_get_organization", "type", "group")
    list_filter = ("type__domain__organization", "type__domain__domain_name", "type__variant_slug", "group__name")
    raw_id_fields = ("group",)


@admin.register(SMTPServer)
class SMTPServerAdmin(admin.ModelAdmin):
    list_display = ("hostname",)


@admin.register(SMTPPassword)
class SMTPPasswordAdmin(admin.ModelAdmin):
    list_display = ("smtp_server", "person")
    list_filter = ("smtp_server",)
    raw_id_fields = ("person",)


@admin.register(CBACEntry)
class CBACEntryAdmin(admin.ModelAdmin):
    search_fields = ("user__first_name", "user__last_name", "user__username", "user__email")
    list_display = ("user", "claims", "valid_from", "valid_until")
    raw_id_fields = ("user",)
    readonly_fields = ("created_by", "created_at")

    def save_model(self, request, obj, form, change):
        if not obj.pk and not obj.created_by:
            obj.created_by = request.user

        obj.save()
