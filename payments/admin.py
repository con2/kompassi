from django.contrib import admin

from .models import PaymentsOrganizationMeta, CheckoutPayment


class InlinePaymentsOrganizationMetaAdmin(admin.StackedInline):
    model = PaymentsOrganizationMeta


class CheckoutPaymentAdmin(admin.ModelAdmin):
    def has_delete_permission(self, *args, **kwargs):
        return False

    def has_add_permission(self, *args, **kwargs):
        return False

    readonly_fields = (
        "event",
        "created_at",
        "updated_at",
        "stamp",
        "reference",
        "admin_get_formatted_amount",
        "items",
        "customer",
        "checkout_reference",
        "checkout_transaction_id",
        "provider",
        "status",
    )

    fieldsets = (
        (
            "General",
            dict(
                fields=(
                    "organization",
                    "event",
                    "created_at",
                    "updated_at",
                )
            ),
        ),
        (
            "Create Payment Request",
            dict(
                fields=(
                    "stamp",
                    "reference",
                    "admin_get_formatted_amount",
                    "items",
                    "customer",
                )
            ),
        ),
        (
            "Create Payment Response",
            dict(
                fields=(
                    "checkout_reference",
                    "checkout_transaction_id",
                )
            ),
        ),
        (
            "Redirect/Callback",
            dict(
                fields=(
                    "provider",
                    "status",
                )
            ),
        ),
    )

    list_display_links = ("stamp",)
    list_display = (
        "organization",
        "event",
        "stamp",
        "reference",
        "checkout_transaction_id",
        "checkout_reference",
        "admin_get_customer_email",
        "admin_get_formatted_amount",
        "status",
        "created_at",
    )
    list_filter = ("event", "status")
    search_fields = ("stamp", "reference", "checkout_reference", "checkout_transaction_id")


admin.site.register(CheckoutPayment, CheckoutPaymentAdmin)
