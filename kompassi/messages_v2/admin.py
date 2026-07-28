from django.contrib import admin

from .models.message import Message
from .models.message_recipient import MessageRecipient
from .models.message_reply_to import MessageReplyTo


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "universe",
        "subject",
        "state",
        "sent_at",
        "expired_at",
    )
    list_display_links = ("universe", "subject")
    list_filter = ("universe__scope__event",)
    search_fields = ("subject",)
    ordering = ("-id",)

    raw_id_fields = ("universe", "reply_to", "created_by")
    fields = (
        "universe",
        "app",
        "subject",
        "body",
        "dispatch",
        "reply_to",
        "recipient_filters",
        "sent_at",
        "expired_at",
        "created_by",
    )
    readonly_fields = fields


@admin.register(MessageReplyTo)
class MessageReplyToAdmin(admin.ModelAdmin):
    list_display = ("universe", "name", "email")
    list_display_links = ("universe", "name")
    list_filter = ("universe__scope__event",)
    search_fields = ("name", "email")

    raw_id_fields = ("universe",)
    fields = ("universe", "app", "name", "email")
    readonly_fields = fields


@admin.register(MessageRecipient)
class MessageRecipientAdmin(admin.ModelAdmin):
    list_display = ("message", "person", "email", "sent_at")
    list_display_links = ("message", "person")
    list_filter = ("message__universe__scope__event",)
    search_fields = ("person__surname", "person__first_name", "email")
    ordering = ("-sent_at",)

    raw_id_fields = ("message", "person", "involvement", "body")
    fields = (
        "message",
        "person",
        "involvement",
        "email",
        "subject",
        "body",
        "sent_at",
        "cached_dimensions",
    )
    readonly_fields = fields
