from django.contrib import admin

from .models import (
    Membership,
    MembershipFeePayment,
    MembershipOrganizationMeta,
    Term,
)


class InlineMembershipOrganizationMetaAdmin(admin.StackedInline):
    model = MembershipOrganizationMeta


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ("organization", "person")
    list_filter = ("organization",)
    search_fields = (
        "person__surname",
        "person__first_name",
        "person__official_first_names",
        "person__nick",
        "person__email",
    )
    raw_id_fields = ("person",)
    ordering = ("organization", "person__surname", "person__official_first_names")


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ("organization", "title", "start_date", "end_date")
    list_filter = ("organization",)
    ordering = ("organization", "start_date")


@admin.register(MembershipFeePayment)
class MembershipFeePaymentAdmin(admin.ModelAdmin):
    list_display = (
        "admin_get_organization",
        "term",
        "admin_get_official_name",
        "admin_get_formatted_amount",
        "admin_is_paid",
        "payment_date",
    )
    list_filter = ("term__organization",)
    ordering = ("term__organization", "member__person__surname", "member__person__official_first_names")
