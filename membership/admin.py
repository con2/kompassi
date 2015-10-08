from django.contrib import admin

from .models import MembershipOrganizationMeta, Membership


class InlineMembershipOrganizationMetaAdmin(admin.StackedInline):
    model = MembershipOrganizationMeta
