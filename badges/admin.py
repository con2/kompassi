from django.contrib import admin

from .models import BadgesEventMeta


class InlineBadgesEventMetaAdmin(admin.StackedInline):
    model = BadgesEventMeta
